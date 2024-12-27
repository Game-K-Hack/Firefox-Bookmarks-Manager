import sys
from dao import DAO
from ui_form import Ui_Widget  # Fichier généré
from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem, QTreeWidget, QMenu, QAbstractItemView, QMessageBox
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Qt, QByteArray, QBuffer
from formater import convert_to_new_format, sort_by_dir_type, search_bookmarks
from urllib.parse import urlparse
import webbrowser

class CustomTreeWidget(QTreeWidget):
    """QTreeWidget personnalisé pour détecter les drops."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def dropEvent(self, event):
        super().dropEvent(event)  # Appelle la gestion par défaut du glisser-déposer
        if hasattr(self, 'on_item_dropped'):
            self.on_item_dropped()  # Signale que des éléments ont été déplacés

def byte_to_qicon(data:bytes) -> QIcon:
    if data != data:
        return QIcon("./images/none_icon.svg")
    else:
        byte_array = QByteArray(data)
        buffer = QBuffer()
        buffer.setData(byte_array)
        buffer.open(QBuffer.ReadOnly)

        pixmap = QPixmap()
        pixmap.loadFromData(buffer.data())

        return QIcon(pixmap)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.bookmarks_data = None

        # Remplacer treeWidget existant par CustomTreeWidget
        self.tree_widget = CustomTreeWidget(self.ui.tab_2)
        self.tree_widget.setGeometry(self.ui.view_tree.geometry())
        self.tree_widget.setObjectName(self.ui.view_tree.objectName())
        self.ui.view_tree.deleteLater()  # Supprimer l'ancien widget
        self.ui.view_tree = self.tree_widget

        # Configuration du view_tree pour le glisser-déposer
        self.ui.view_tree.setHeaderLabels(["Name", "URL"])
        self.ui.view_tree.setColumnWidth(0, 550)
        self.ui.view_tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.ui.view_tree.setDefaultDropAction(Qt.MoveAction)

        self.ui.search_res_tree.setHeaderLabels(["Name", "URL"])
        self.ui.search_res_tree.setColumnWidth(0, 550)

        # Connecter l'événement personnalisé
        self.ui.view_tree.on_item_dropped = self.update_data
        self.ui.search_button_goto.clicked.connect(self.on_goto)
        self.ui.search_input_name.textChanged.connect(self.on_search)
        self.ui.search_input_url.textChanged.connect(self.on_search)
        self.ui.search_is_specific_url.checkStateChanged.connect(self.on_search)

        # Liste sous-jacente pour le nouveau format
        self.data = []

    def set_bookmarks(self, data, set_elements:bool=True) -> None:
        self.bookmarks_data = data
        if set_elements:
            self.load_data(self.bookmarks_data, element=self.ui.search_res_tree)
            self.load_data(self.bookmarks_data, element=self.ui.view_tree)

    def load_data(self, data, element:QTreeWidget):
        """Charge les données au nouveau format dans le QTreeWidget."""
        self.data = data
        element.clear()

        def add_items(items, parent=None):
            for item in items:
                if item["type"] == "dir":
                    # Créer un élément parent pour le répertoire
                    tree_item = QTreeWidgetItem(parent or element, [item["name"], ""])
                    tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
                    # Ajouter récursivement les URLs du répertoire
                    if "urls" in item:
                        add_items(item["urls"], tree_item)
                else:  # type == "url"
                    # Créer un élément pour l'URL
                    domain = urlparse(item["url"]).netloc
                    url_item = QTreeWidgetItem(parent or element, [item["name"], domain])
                    url_item.setData(1, 1, item["url"])
                    icon = byte_to_qicon(item["icon"])
                    url_item.setIcon(0, icon)
                    url_item.setFlags(url_item.flags() | Qt.ItemIsEditable | Qt.ItemIsDragEnabled)

        add_items(data)

    def update_data(self):
        """Met à jour la structure de données en fonction du QTreeWidget."""
        def process_item(item):
            """Convertit un QTreeWidgetItem en dictionnaire au nouveau format."""
            result = {
                "name": item.text(0),
                "type": "dir" if item.childCount() > 0 else "url"
            }
            
            if result["type"] == "dir":
                result["urls"] = []
                for i in range(item.childCount()):
                    child_result = process_item(item.child(i))
                    result["urls"].append(child_result)
            else:
                result["url"] = item.text(1)
                
            return result

        self.data = []
        root = self.ui.treeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            item_data = process_item(root.child(i))
            self.data.append(item_data)
            
        print("Données mises à jour :", self.data)

    def add_tree_item(self, parent_item=None):
        """Ajoute un nouvel élément à l'arbre."""
        if parent_item is None:
            # Ajout d'un nouveau dossier à la racine
            new_item = QTreeWidgetItem(self.ui.treeWidget, ["New Directory", ""])
            new_item.setFlags(new_item.flags() | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
        else:
            # Ajout d'une nouvelle URL dans un dossier
            new_item = QTreeWidgetItem(parent_item, ["New URL", "https://"])
            new_item.setFlags(new_item.flags() | Qt.ItemIsEditable | Qt.ItemIsDragEnabled)
        
        parent_item.setExpanded(True) if parent_item else None

    def remove_tree_item(self, item):
        """Supprime un élément de l'arbre."""
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            root = self.ui.treeWidget.invisibleRootItem()
            root.removeChild(item)
        self.update_data()

    def show_context_menu(self, position):
        """Affiche un menu contextuel pour gérer les éléments."""
        item = self.ui.treeWidget.itemAt(position)
        menu = QMenu()

        if item:
            # Pour les dossiers, permettre l'ajout d'URLs
            if item.childCount() > 0 or item.text(1) == "":
                add_action = QAction("Add URL", self)
                add_action.triggered.connect(lambda: self.add_tree_item(item))
                menu.addAction(add_action)

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.remove_tree_item(item))
            menu.addAction(delete_action)
        else:
            # Ajout d'un nouveau dossier à la racine
            add_root_action = QAction("Add Directory", self)
            add_root_action.triggered.connect(lambda: self.add_tree_item())
            menu.addAction(add_root_action)

        menu.exec(self.ui.treeWidget.mapToGlobal(position))

    def on_commit(self):
        search = self.ui.lineEdit_2.text()
        replace = self.ui.lineEdit_3.text()
        regex = self.ui.lineEdit_4.text()
        use_regex = self.ui.checkBox.isChecked()
        print(search, replace, regex, use_regex)

    def on_reset(self):
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.checkBox.setChecked(False)

    def on_live_preview(self, state):
        is_live = state == 2

    def on_search(self):
        search_text = self.ui.search_input_name.text()
        search_url = self.ui.search_input_url.text()
        is_specific_url = self.ui.search_is_specific_url.isChecked()

        if search_text != "" or (is_specific_url and search_url != ""):
            try:
                # Effectuer la recherche
                filtered_data = search_bookmarks(
                    self.bookmarks_data,
                    name_pattern=search_text,
                    url_pattern=search_url,
                    is_specific_url=is_specific_url
                )
                
                # Mettre à jour l'interface avec les résultats
                self.load_data(filtered_data, self.ui.search_res_tree)

                self.ui.search_res_tree.expandAll()
                
            except Exception as e:
                # Gérer les erreurs (par exemple, regex invalide)
                QMessageBox.warning(self, "Erreur de recherche", 
                                f"Erreur lors de la recherche: {str(e)}")
        else:
            self.ui.search_res_tree.collapseAll()

    def on_goto(self):
        for i in self.ui.search_res_tree.selectedItems():
            webbrowser.open(i.data(1, 1), new=0, autoraise=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    bookmarks = DAO(profile_id="kpnd9nxd.default-release")
    data_bookmarks = bookmarks.to_dict()
    data_bookmarks = convert_to_new_format(data_bookmarks)
    data_bookmarks = sort_by_dir_type(data_bookmarks)
    window.set_bookmarks(data_bookmarks)

    window.show()
    sys.exit(app.exec())
