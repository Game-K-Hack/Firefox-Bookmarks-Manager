import re


def convert_to_new_format(data):
    """
    Convertit la structure de données d'origine vers le nouveau format JSON.
    
    Args:
        data (dict): Dictionnaire contenant la structure d'origine
        
    Returns:
        list: Liste de dictionnaires au nouveau format
    """
    result = []
    
    def process_files_list(files_list):
        """Traite la liste des fichiers et retourne une liste d'URLs"""
        urls = []
        for item in files_list:
            # Vérifie si l'item est un tuple de 4 éléments comme dans les données d'origine
            if isinstance(item, tuple) and len(item) == 5:
                urls.append({
                    "name": item[1],
                    "url": item[2],
                    "icon": item[4],
                    "type": "url"
                })
        return urls
    
    def process_directory(directory, path=""):
        """
        Traite récursivement un répertoire et ses sous-répertoires.
        
        Args:
            directory (dict): Dictionnaire représentant un répertoire
            path (str): Chemin actuel dans l'arborescence
        """
        for key, value in directory.items():
            if key == "__files_list__":
                # Traite les URLs directement dans ce répertoire
                urls = process_files_list(value)
                result.extend(urls)
            elif isinstance(value, dict):
                # Crée un nouvel élément de type 'dir'
                dir_item = {
                    "name": key,
                    "type": "dir",
                    "urls": []
                }
                
                # Sauvegarde la longueur actuelle du résultat
                current_len = len(result)
                
                # Traite récursivement le sous-répertoire
                process_directory(value, path + "/" + key)
                
                # Récupère tous les éléments ajoutés pendant le traitement récursif
                new_items = result[current_len:]
                
                # Si des éléments ont été trouvés, les ajoute au répertoire
                if new_items:
                    dir_item["urls"] = new_items
                    # Supprime les éléments qui ont été déplacés dans le répertoire
                    del result[current_len:]
                    result.append(dir_item)
    
    # Commence le traitement avec le répertoire racine
    process_directory(data)
    
    return result

def sort_by_dir_type(data, sort_by_alpha: bool = True):
    """
    Trie récursivement les données en mettant les répertoires en premier,
    puis en triant par ordre alphabétique si demandé.
    
    Args:
        data (list): Liste de dictionnaires au format converti
        sort_by_alpha (bool): Si True, trie aussi par ordre alphabétique
    
    Returns:
        list: Liste triée selon les critères spécifiés
    """
    def sort_key(item):
        """
        Fonction clé pour le tri.
        Retourne un tuple (type_priority, name) pour le tri.
        """
        # Les répertoires (dir) ont priorité 0, les urls ont priorité 1
        type_priority = 0 if item["type"] == "dir" else 1
        
        # Si le tri alphabétique est activé, on utilise le nom en minuscules
        # Sinon, on utilise une chaîne vide pour ignorer le tri alphabétique
        name = item["name"].lower() if sort_by_alpha else ""
        
        return (type_priority, name)
    
    # Copie profonde pour ne pas modifier les données d'origine
    import copy
    sorted_data = copy.deepcopy(data)
    
    # Trie la liste principale
    sorted_data.sort(key=sort_key)
    
    # Trie récursivement les sous-listes dans les répertoires
    for item in sorted_data:
        if item["type"] == "dir" and "urls" in item:
            item["urls"] = sort_by_dir_type(item["urls"], sort_by_alpha)
    
    return sorted_data

def search_bookmarks(data, name_pattern="", url_pattern="", is_specific_url=False):
    """
    Recherche dans les bookmarks selon les critères donnés et préserve la hiérarchie.
    
    Args:
        data (list): Liste des bookmarks au format converti
        name_pattern (str): Pattern regex pour la recherche par nom
        url_pattern (str): Pattern regex pour la recherche par URL
        is_specific_url (bool): Si True, recherche exacte d'URL
        
    Returns:
        list: Liste filtrée des bookmarks correspondant aux critères
    """
    def matches_criteria(item):
        """Vérifie si un item correspond aux critères de recherche"""
        try:
            # Compile les regex si non vides
            name_regex = re.compile(name_pattern, re.IGNORECASE) if name_pattern else None
            url_regex = re.compile(url_pattern, re.IGNORECASE) if url_pattern else None
            
            # Vérifie le nom si un pattern est fourni
            if name_regex and not name_regex.search(item["name"]):
                return False
                
            # Vérifie l'URL pour les items de type "url"
            if is_specific_url and item["type"] == "url" and url_pattern:
                if url_regex and not url_regex.search(item["url"]):
                    return False

            return True
        except re.error:
            # En cas d'erreur dans le pattern regex
            return False
    
    def filter_recursive(items):
        """Filtre récursivement les items en préservant la hiérarchie"""
        result = []
        
        for item in items:
            if item["type"] == "dir":
                # Pour les répertoires, filtrer récursivement leur contenu
                filtered_urls = filter_recursive(item["urls"])
                if filtered_urls or matches_criteria(item):
                    # Copier le répertoire et mettre à jour ses URLs
                    new_dir = item.copy()
                    new_dir["urls"] = filtered_urls
                    result.append(new_dir)
            elif matches_criteria(item):
                # Pour les URLs, ajouter si elles correspondent aux critères
                result.append(item)
        
        return result
    
    def clean_empty_dirs(items):
        """Supprime les répertoires qui ne contiennent pas d'URLs"""
        result = []
        
        for item in items:
            if item["type"] == "dir":
                # Nettoyer récursivement les sous-répertoires
                cleaned_urls = clean_empty_dirs(item["urls"])
                # Ne garder le répertoire que s'il contient des URLs
                if cleaned_urls:
                    new_dir = item.copy()
                    new_dir["urls"] = cleaned_urls
                    result.append(new_dir)
            else:
                result.append(item)
        
        return result
    
    # Filtrer d'abord les données
    filtered_data = filter_recursive(data)
    # Puis nettoyer les répertoires vides
    return clean_empty_dirs(filtered_data)
