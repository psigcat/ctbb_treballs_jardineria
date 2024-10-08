# -*- coding: utf-8 -*-
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog


def get_ui_class(ui_file_name):
    """ Get UI Python class from @ui_file_name """

    # Folder that contains UI files
    ui_folder_path = os.path.join(os.path.dirname(__file__), 'ui')
    ui_file_path = os.path.abspath(os.path.join(ui_folder_path, ui_file_name))
    if not os.path.exists(ui_file_path):
        print(f"File not found: {ui_file_path}")
        return None

    return uic.loadUiType(ui_file_path)[0]


FORM_CLASS = get_ui_class('dlg_gmao.ui')
class DlgGmao(QDialog, FORM_CLASS):
    def __init__(self):
        super().__init__()
        self.ui = FORM_CLASS()
        self.ui.setupUi(self)