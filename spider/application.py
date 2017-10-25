#encoding:utf8

import threading
import time
import requests
from bs4 import BeautifulSoup
from spider.model import spiderModel, dbfile, tabledesc
# from mailinter import Mail

class spider(object):
	def __init__(self, product=None):
		self.res = ""
		self.model = spiderModel.instansce(dbfile, tabledesc)
		self.baseurl = r"***"
		if product == None:
			self.product = {"***":"***"}
		else:
			self.product = product
		#
		self.cont = 0
		self.Flag = True
		self.get_freshtime()
		# self.Mail = Mail()

	@staticmethod
	def instance(product=None):
		global m_instance
		try:
			m_instance
		except:
			m_instance = spider(product)
		return m_instance

	def get_freshtime(self):
		if not hasattr(self, "productfresh"):
			self.productfresh = dict()
		for productname in self.product.keys():
			self.selectsql = "select date from Product where productname = '%s' order by date desc limit 1" % productname

			self.model.connectDB()
			self.model.getResult(self.selectsql)

			self.productfresh[productname] = self.model.getFreshtime()
			self.model.closeDB()
			print("the Newest chapter name", self.productfresh[productname], productname)

	def insert_data(self, ip, content, date, productname):
		self.insertsql = "insert into Product(ip, content, date, productname) values ('%s', '%s', '%s', '%s')" \
		                 %(ip, content, date, productname)
		self.model.connectDB()
		self.model.execDB(self.insertsql)
		self.model.closeDB()


	def dataget(self):
		for productName in self.product:
			self.url = self.product[productName]  # 阴阳师
			while True:
				if self.Flag and self.cont <99:
					self.cont += 1
					# 处理网络异常情况
					try:
						ir = requests.get(self.url)
					except Exception as e:
						print(e)
						return
					if ir.status_code == 200:
						self.res = ir.text
						self.dealxpath(productName)
				else:
					break
			self.Flag = True
			self.cont = 0
			self.get_freshtime()
		# print(self.res)



	def dealxpath(self, productName):
		if self.res == "":
			return
		soup = BeautifulSoup(self.res, "html5lib")
		page = soup.find(attrs={"class": "pg"})
		for pg in page:
			if pg.text == "下一页":
				self.url = self.baseurl + pg.get("href")
				print(self.url)
		# input()

		content_class = soup.find(attrs={'id':"postlist"})
		for s in content_class:
			try:
				if "id" in s.attrs and s.attrs["id"] not in ["post_49710777", "postlistreply"]:
					content = s.find("tr")
					ip = (content.find(attrs={"href":"javascript:;"})).find("em").text

					date = (content.find(attrs={"class":"authi"})).find("em").text
					date = (date.replace("发表于", "")).strip()

					data = (content.find(attrs={"class":"t_f"}).text).strip()
					print(date, self.productfresh[productName] < date)
					# input()
					if self.productfresh[productName] == None or self.productfresh[productName] < date:
						self.insert_data(ip, data, date, productName)
					else:
						self.Flag = False
						return
			except Exception as e:
				pass


def run():
	print("time:%s" % time.time())
	spider.instance(product).dataget()
	global timer
	timer = threading.Timer(360, run)
	timer.start()
	pass

product = {"***": "***"}

if __name__ == "__main__":
	spider.instance(product).dataget()
	timer = threading.Timer(360, run)
	timer.start()
	# spider.instance()
