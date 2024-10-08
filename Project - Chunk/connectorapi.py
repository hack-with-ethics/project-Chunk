import mysql.connector as sql


class database_connector:

	def __init__(self):
		self.host = "127.0.0.1"

		self.user = "root"

		self.passd = "ROOT@SANJAI"
		self.db = "mydb"
	def connect_database(self):
		try:
			connection = sql.connect(host=self.host,passwd=self.passd,user=self.user,database=self.db)
		
			if connection:
				print("* connection Initiated [ $ ]")

				return connection
			else:
				return None

		except:
			return None
		

		

	def console(self,cmd):

		con = self.connect_database()
		

		if con == None:
			return False

		else:
			cursor = con.cursor()
		
			
			cmd = cmd.replace("--","").strip() # Basic injection sec !
				
			
			cursor.execute(cmd)

			lst = []
			for i in cursor.fetchall():
				lst.append(i)
			con.commit()
			cursor.close()
			con.close()
			return lst
					
			
	
				


