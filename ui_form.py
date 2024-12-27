# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHeaderView,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 50, 801, 551))
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.search_input_name = QLineEdit(self.tab)
        self.search_input_name.setObjectName(u"search_input_name")
        self.search_input_name.setGeometry(QRect(10, 10, 771, 24))
        self.search_button_goto = QPushButton(self.tab)
        self.search_button_goto.setObjectName(u"search_button_goto")
        self.search_button_goto.setGeometry(QRect(700, 480, 80, 24))
        self.search_res_tree = QTreeWidget(self.tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.search_res_tree.setHeaderItem(__qtreewidgetitem)
        self.search_res_tree.setObjectName(u"search_res_tree")
        self.search_res_tree.setEnabled(True)
        self.search_res_tree.setGeometry(QRect(10, 80, 771, 381))
        self.search_res_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.search_res_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.search_is_specific_url = QCheckBox(self.tab)
        self.search_is_specific_url.setObjectName(u"search_is_specific_url")
        self.search_is_specific_url.setGeometry(QRect(10, 40, 91, 22))
        self.search_input_url = QLineEdit(self.tab)
        self.search_input_url.setObjectName(u"search_input_url")
        self.search_input_url.setGeometry(QRect(110, 40, 671, 24))
        self.tabWidget.addTab(self.tab, "")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.replace_input_search = QLineEdit(self.widget)
        self.replace_input_search.setObjectName(u"replace_input_search")
        self.replace_input_search.setGeometry(QRect(10, 10, 351, 24))
        self.replace_input_replace = QLineEdit(self.widget)
        self.replace_input_replace.setObjectName(u"replace_input_replace")
        self.replace_input_replace.setGeometry(QRect(430, 10, 351, 24))
        self.replace_input_url = QLineEdit(self.widget)
        self.replace_input_url.setObjectName(u"replace_input_url")
        self.replace_input_url.setGeometry(QRect(230, 40, 551, 24))
        self.replace_match_url = QCheckBox(self.widget)
        self.replace_match_url.setObjectName(u"replace_match_url")
        self.replace_match_url.setGeometry(QRect(10, 40, 221, 22))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(375, 8, 41, 21))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 70, 351, 391))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 349, 389))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QScrollArea(self.widget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(430, 70, 351, 391))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 349, 389))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.replace_button_commit = QPushButton(self.widget)
        self.replace_button_commit.setObjectName(u"replace_button_commit")
        self.replace_button_commit.setGeometry(QRect(700, 480, 80, 24))
        self.replace_button_reset = QPushButton(self.widget)
        self.replace_button_reset.setObjectName(u"replace_button_reset")
        self.replace_button_reset.setGeometry(QRect(610, 480, 80, 24))
        self.replace_is_live_preview = QCheckBox(self.widget)
        self.replace_is_live_preview.setObjectName(u"replace_is_live_preview")
        self.replace_is_live_preview.setGeometry(QRect(10, 480, 91, 22))
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.view_tree = QTreeWidget(self.tab_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.view_tree.setHeaderItem(__qtreewidgetitem1)
        self.view_tree.setObjectName(u"view_tree")
        self.view_tree.setGeometry(QRect(10, 10, 771, 501))
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.search_input_name.setPlaceholderText(QCoreApplication.translate("Widget", u"Search Name (regex)", None))
        self.search_button_goto.setText(QCoreApplication.translate("Widget", u"Go to", None))
        self.search_is_specific_url.setText(QCoreApplication.translate("Widget", u"Specific URL:", None))
        self.search_input_url.setPlaceholderText(QCoreApplication.translate("Widget", u"Search URL (regex)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Widget", u"Search", None))
        self.replace_input_search.setPlaceholderText(QCoreApplication.translate("Widget", u"Search", None))
        self.replace_input_replace.setPlaceholderText(QCoreApplication.translate("Widget", u"Replace", None))
        self.replace_input_url.setPlaceholderText(QCoreApplication.translate("Widget", u"regex", None))
        self.replace_match_url.setText(QCoreApplication.translate("Widget", u"If the URL matches the following rule:", None))
        self.label.setText(QCoreApplication.translate("Widget", u"-->", None))
        self.replace_button_commit.setText(QCoreApplication.translate("Widget", u"Commit", None))
        self.replace_button_reset.setText(QCoreApplication.translate("Widget", u"Reset", None))
        self.replace_is_live_preview.setText(QCoreApplication.translate("Widget", u"Live preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QCoreApplication.translate("Widget", u"Replace", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Widget", u"View", None))
    # retranslateUi

