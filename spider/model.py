#encoding:utf8
import sqlite3
import os

base_path = os.getcwd()
dbfile =  base_path + r'\spider.db'
tabledesc = ("storyN", "chatper varchar(128), storyname varchar(128)")

class spiderModel(object):

	def __init__(self, dbfile, tabledesc):
		self.tablename = tabledesc[0]
		self.tablefield = tabledesc[1]
		self.dbfile = dbfile

	@staticmethod
	def instansce(dbfile,tabledesc):
		global m_instance
		try:
			m_instance
		except:
			m_instance = spiderModel(dbfile,tabledesc)
		return m_instance

	def createDB(self):
		createlist = ["create table if not exists ", self.tablename, "(id integer primary key autoincrement, ", self.tablefield, ")"]
		createsql = "".join(createlist)
		self.conn = sqlite3.connect(self.dbfile)
		self.conn.isolation_level = None  #?
		print(createsql)
		self.conn.execute(createsql)

	def connectDB(self):
		if hasattr(self,"conn") and self.conn != None:
			self.conn.close()

		self.conn = sqlite3.connect(self.dbfile)


	def execDB(self, execsql):
		self.conn.execute(execsql)
		self.conn.commit()
		return

	def getResult(self, selectsql):
		self.cur = self.conn.cursor()
		self.cur.execute(selectsql)
		self.res = self.cur.fetchall()
		return self.res

	def getChapterName(self):
		if self.res == None:
			return

		for line in self.res:
			for col in line:
				return col

	def getCount(self):
		return len(self.res)

	def closeDB(self):
		if hasattr(self,"cur"):
			self.cur.close()
		if hasattr(self,"conn"):
			self.conn.close()

if __name__ == "__main__":
	dbfile =  base_path + r'\spider.db'
	tabledesc = ("storyN", "chatper varchar(128), storyname varchar(128)")
	# insertsql = "insert into storyN(chatper, storyname) values ('卷3', '大明春色')"
	# selectsql = "select * from storyN order by id desc "

	dbd = spiderModel.instansce(dbfile, tabledesc)
	dbd.createDB()
	# dbd.execDB(insertsql)
	# res = dbd.getResult(selectsql)
	# rows = dbd.getCount()
	dbd.closeDB()


