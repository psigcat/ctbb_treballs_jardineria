import os
import configparser

from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class ctbb_database:

	def __init__(self, plugin_dir):

		self.plugin_dir = plugin_dir
		self.param = {}
		self.db = None
		self.obert = False
		self.bd_open = False
		self.last_error = None
		self.last_msg = None
		self.num_fields = None
		self.num_records = None


	def read_config(self):
		""" read params from metadata.txt """
		
		self.param = {
			"database": self.get_metadata_parameter("app", "database"),
			"service": self.get_metadata_parameter("app", "service"),
			"schema": self.get_metadata_parameter("app", "schema"),
			"table": self.get_metadata_parameter("app", "table")
		}
		print(self.param)


	def get_metadata_parameter(self, section="general", parameter="version", file="metadata.txt"):
		""" Get parameter value from Metadata """

		# Check if metadata file exists
		metadata_file = os.path.join(self.plugin_dir, file)
		if not os.path.exists(metadata_file):
			show_warning(f"No s'ha trobat l'arxiu de metadades: {metadata_file}")
			return None

		value = None
		try:
			metadata = configparser.ConfigParser()
			metadata.read(metadata_file)
			value = metadata.get(section, parameter)
		except Exception as e:
			show_warning(e)
		finally:
			return value


	def open_database(self):
		""" Open database on server """

		if self.bd_open:
			return self.db

		if self.param["service"] == "":
			self.last_error = "No s'ha definit service"
			return None

		self.db = QSqlDatabase.addDatabase("QPSQL", self.param['database'])
		self.db.setConnectOptions(f"service={self.param['service']}")
		self.db.open()
		if self.db.isOpen() == 0:
			self.last_error = f"No s'ha pogut obrir la Base de Dades del servidor\n\n{self.db.lastError().text()}"
			return None

		self.bd_open = True
		print("connected to database")
		return self.db


	def close_database(self):
		"""Close database on server """

		if not self.bd_open:
			return True
		self.db.close()
		self.bd_open = False
		return True


	def reset_info(self):
		""" Reset query information values """

		self.last_error = None
		self.last_msg = None
		self.num_fields = None
		self.num_records = None


	def exec_sql(self, sql):
		""" Execute SQL (Insert or Update) """

		self.reset_info()
		query = QSqlQuery(self.db)
		status = query.exec(sql)
		if not status:
			self.last_error = query.lastError().text()
		return status


	def get_rows(self, sql):
		""" Execute SQL (Select) and return rows """

		print("execute", sql)

		self.reset_info()
		query = QSqlQuery(self.db)
		status = query.exec(sql)
		if not status:
			self.last_error = query.lastError().text()
			return None
		# Get number of records
		self.num_records = query.size()
		if self.num_records == 0:
			self.last_msg = "No s'ha trobat cap registre amb els filtres seleccionats"
			return None

		# Get number of fields
		record = query.record()
		self.num_fields = record.count()
		if self.num_fields == 0:
			self.last_msg = "No s'han especificat camps a retornar"
			return None

		rows = []
		while query.next():
			row = []
			for i in range(self.num_fields):
				row.append(query.value(i))
			rows.append(row)

		return rows
