import sqlite3
import pandas as pd
import datetime
import os

class DAO:
    def __init__(self, profile_id:str, firefox_profile_dir_path:str=None, backup_dir_path:str=None) -> None:
        profile_path = f"C:/Users/{os.environ['username']}/AppData/Roaming/Mozilla/Firefox/Profiles/{profile_id}/"
        self.firefox_profile_dir_path = profile_path if firefox_profile_dir_path is None else firefox_profile_dir_path
        self.backup_dir_path = profile_path + "bm_editor_backup" if backup_dir_path is None else backup_dir_path
        # Initialise le DAO avec le chemin d'accès à la base de données de Firefox
        self.database_path_places = self.firefox_profile_dir_path + "places.sqlite"
        self.database_path_favicons = self.firefox_profile_dir_path + "favicons.sqlite"
        # Connecte à la base de données SQLite
        self.conn_places = sqlite3.connect(self.database_path_places)
        self.conn_favicons = sqlite3.connect(self.database_path_favicons)
        self.backup_already_maked:bool = False

    def __remove_old_backup__(self) -> None:
        bklist = os.listdir(self.backup_dir_path)
        while len(bklist) > 100:
            os.remove(bklist[0])
            bklist = os.listdir(self.backup_dir_path)

    def __make_backup__(self) -> None:
        if not self.backup_already_maked:
            if not os.path.exists(self.backup_dir_path):
                os.mkdir(self.backup_dir_path)
            filetsid = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = self.backup_dir_path + f"/places_backup_{filetsid}.sqlite"
            with open(self.database_path_places, "rb") as backup_content:
                with open(filename, "wb") as new_backup:
                    new_backup.write(backup_content.read())
                    self.backup_already_maked = True
            self.__remove_old_backup__()

    def get_bookmarks(self):
        # Requête SQL pour extraire les marque-pages depuis la table moz_bookmarks de Firefox
        # utilise une requête récursive pour construire l'arborescence de dossiers et leurs chemins
        # retourne les marque-pages avec leur parent, titre et fk (foreign key)
        query = '''
            WITH RECURSIVE folders (id, parent, title, path) AS (
                SELECT id, parent, title, title as path FROM moz_bookmarks WHERE type = 2
                UNION ALL
                SELECT f.id, f.parent, f.title, f2.path || '/' || f.title 
                FROM moz_bookmarks AS f
                JOIN folders AS f2 ON f.parent = f2.id
            )
            SELECT id, parent, title, fk FROM moz_bookmarks WHERE type = 1
        '''
        return pd.read_sql_query(query, self.conn_places)

    def get_places(self):
        # Requête SQL pour extraire les URLs depuis la table moz_places de Firefox
        query = "SELECT id, url, preview_image_url FROM moz_places"
        return pd.read_sql_query(query, self.conn_places)

    def get_folders(self):
        # Requête SQL pour extraire les dossiers depuis la table moz_bookmarks de Firefox
        # utilise une requête récursive pour construire l'arborescence de dossiers et leurs chemins
        # retourne les dossiers avec leur ID et leur chemin
        query = '''
            WITH RECURSIVE folders (id, parent, title, path) AS (
                SELECT id, parent, title, title as path FROM moz_bookmarks WHERE type = 2
                UNION ALL
                SELECT f.id, f.parent, f.title, f2.path || '/' || f.title 
                FROM moz_bookmarks AS f
                JOIN folders AS f2 ON f.parent = f2.id
            )
            SELECT id, path FROM folders
        '''
        return pd.read_sql_query(query, self.conn_places)
    
    def get_icons(self):
        query = '''
            SELECT mpwi.page_url AS "url", mi.data AS "icon" FROM moz_icons mi 
            INNER JOIN moz_icons_to_pages mitp ON mitp.icon_id = mi.id 
            INNER JOIN moz_pages_w_icons mpwi ON mpwi.id = mitp.page_id
        '''
        return pd.read_sql_query(query, self.conn_favicons)

    def get_bookmarks_with_places_and_folders(self) -> list:
        # Obtenir les marque-pages, les URL et les dossiers
        bookmarks = self.get_bookmarks()
        places = self.get_places()
        folders = self.get_folders()
        favicons = self.get_icons()
        # Jointure pour lier les marque-pages aux URL
        bookmarks = bookmarks.merge(places, how='left', left_on='fk', right_on='id')
        # Jointure pour lier les marque-pages à leur dossier parent
        bookmarks = bookmarks.merge(folders, how='left', left_on='parent', right_on='id')

        bookmarks = bookmarks.merge(favicons, how='left', left_on='url', right_on='url')
        # Créer une liste de tuples pour les marque-pages avec leur ID, titre, URL et chemin
        bookmarks = [(row.id, row.title, row.url, row.path, row.icon) for row in bookmarks.itertuples()]
        # Fermer la connexion à la base de données SQLite
        self.conn_places.close()
        return bookmarks

    def to_list(self) -> list:
        # Obtenir les marque-pages avec les URL et les dossiers
        bookmarks = self.get_bookmarks_with_places_and_folders()
        # Créer un dictionnaire pour stocker les marque-pages avec leur ID, titre, URL et chemin
        x = {}
        for id, name, url, dirpath, icon in bookmarks:
            # Stocker chaque marque-page dans le dictionnaire avec une clé unique basée sur l'ID, le titre et l'URL
            x[f"{id}{name}{url}"] = (id, name, url, dirpath, icon)
        # Retourner une liste de tous les marque-pages, triée par ordre alphabétique du titre
        return [x[i] for i in x.keys()]
    
    def to_dict(self) -> dict:
        result = {}
        for id, name, url, dirpath, icon in self.to_list():
            # Obtenir les éléments de chemin dans une liste
            path_elements = dirpath.split("/")
            # Créer une référence au dictionnaire résultant pour chaque élément de chemin
            nested_dict = result
            for element in path_elements:
                # Si l'élément n'existe pas encore dans le dictionnaire, créer un dictionnaire vide
                if element not in nested_dict:
                    nested_dict[element] = {}
                # Réaffecter la référence imbriquée au dictionnaire nouvellement créé
                nested_dict = nested_dict[element]
            # Ajouter les données de l'URL à la liste des fichiers dans le dictionnaire imbriqué final
            if "__files_list__" not in nested_dict.keys():
                nested_dict["__files_list__"] = []
            nested_dict["__files_list__"].append((id, name, url, dirpath, icon))
        # Renvoyer le dictionnaire résultant
        if list(result.keys())[0] == "":
            return result[""]
        else:
            return result

    def update_bookmark_title(self, bookmark_id: int, new_title: str):
        self.__make_backup__()
        # Met à jour le titre d'un marque-page avec un nouvel intitulé
        query = "UPDATE moz_bookmarks SET title = ? WHERE id = ?"
        self.conn_places.execute(query, (new_title, bookmark_id))
        self.conn_places.commit()

    def update_titles(self, contains:str, replace_by:str=""):
        # Requête pour récupérer tous les marque-pages contenant " - YouTube" dans leur titre
        bookmarks = self.get_bookmarks()
        youtube_bookmarks = bookmarks[bookmarks['title'].str.contains(contains, na=False)]

        # Mise à jour de chaque titre
        for _, row in youtube_bookmarks.iterrows():
            new_title = row['title'].replace(contains, replace_by)
            self.update_bookmark_title(row['id'], new_title)
