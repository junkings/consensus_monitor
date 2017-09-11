#encoding:utf8
from pymongo import MongoClient

class dbmanage(object):
	def __init__(self,ip,port):
		# if ip == '' or type(ip) != 'str':

		self.ip = ip + ':' +port
		pass

	def getcursor_mongo(self,list_date,db_name):
		if list_date == None:
			return
		client = MongoClient(self.ip)
		# db = client.g37_forum
		db = client.g37_forum
		# cursor = db.feedback.find({"time": {'$gte': '2017-2-27'}})#'$gte': '2016-12-14','$lt': '2016-15' #'$regex': '2016-12-23'
		cursor = db[db_name].find({"date": {'$in': list_date}})#"2017-3-20","2017-3-21","2017-3-22","2017-3-23","2017-3-24","2017-3-25",_copy_0330 ["2017-3-31","2017-4-1","2017-4-2","2017-4-3","2017-4-4","2017-4-5",]
		# cursor = db.feedback.find({"time": {'$gte': '2017-1-10'}})#'$gte': '2016-12-14','$lt': '2016-15' #'$regex': '2016-12-23'
		# print len(list(cursor))
		return cursor

