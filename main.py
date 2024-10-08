import sys

from qgis.core import QgsApplication
from qgis.PyQt.QtCore import Qt
from ui_manager import DlgGmao


def main_app():
	""" Create main application """

	app = QgsApplication([], True)
	app.initQgis()

	try:
		# load UI
		dlg_gmao = DlgGmao()
		flags = Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
		dlg_gmao.setWindowFlags(dlg_gmao.windowFlags() | flags)
		dlg_gmao.show()
	except Exception as e:
		print(f"{e}")
	finally:
		exitcode = app.exec()
		QgsApplication.exitQgis()
		sys.exit(exitcode)


if __name__ == "__main__":
	main_app()
