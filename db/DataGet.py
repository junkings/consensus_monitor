#encoding:utf8

# from algorithm.datetostr import *
from algorithm.ipconvert import IPLocator
import algorithm.WordSeg as ws
from db import dbmanage, config
import pickle
import algorithm.TF_IDF_algo as tf

# from setting import *
# from database.dbmanage import *


def DataGet(lb, listdate,mfilename=None, dformat=None,level=None,date_flag=None ):
	"""dformat  :	 "%Y-%m-%d %H:%M"
	# level	:	  year month day hour minute second
	# date_flag:	  true: hour : year-month-day-hour
	#				false: hour   :  hour
	# lb:	0 : text  1: mongo
	# 数据获取，变换成一个dict数组要换格式"""
	# 输出一个字典，每个key是一个文档，content是玩家评论
	dictAlldata = {}
	# ip数据库
	# ipdb = IPLocator('..\statics\qqwry.Dat')
	path = "../input/result.txt"
	# filename = ""
	cursor = {}

	if lb == 1:
		client = dbmanage.dbmanage(config.ip,config.port)
		cursor['cursor'] = client.getcursor_mongo(listdate,config.dbname)
	elif lb == 0:
		cursor['cursor'] = open(path, encoding='utf-8')

	# f = open("../output/result_shantui.txt", "a")
	# dict的键，从1到N
	cont = 1
	# 判断最后一个是否
	flag = True
	if "cursor" not in cursor :
		return

	for _document in cursor['cursor']:
		flag = True
		try:
			dictAlldata[cont] = {}
			if lb == 1:
				document = _document
				doctmp = document['desc'].encode('utf8')
				doctmp = doctmp.replace('}}', '')
				feedback = doctmp.split('{{')
			elif lb == 0:
				document = {}
				doctmp = _document.split('\t')
				if doctmp[0] == "时间":
					continue

				document['time'] = doctmp[0]
				doc_index = -1
				for index, con in enumerate(doctmp):
					if con == "回帖":
						doc_index = index
						break

				if doc_index == -1:
					continue

				document['ip'] = doctmp[index + 4]

				doctmp[index + 1] = doctmp[index + 1].replace('}}', '')
				feedback = doctmp[index + 1].split('{{')
			'''
			document = {}

			doctmp = _document.split('\t')
			if doctmp[0] == "时间":
				continue

			document['time'] = doctmp[0]
			doc_index = -1
			for index,con in enumerate(doctmp):
				if con == "回帖":
					doc_index = index
					break

			if doc_index == -1:
				continue

			document['ip'] = doctmp[index+4]

			doctmp[index+1] = doctmp[index+1].replace('}}', '')
			# 玩家留言
			feedback = doctmp[index+1].split('{{')
			'''
			# 默认值
			content = ['','','','','未知']
			#print(feedback)
			try:
				if len(feedback) > 1:
					for content_tmp in feedback:
						if "usr_id" in content_tmp:
							content[1] = content_tmp.split(':')[1]
						elif "usr_server" in content_tmp:
							content[2] = content_tmp.split(':')[1]
						elif "usr_model" in content_tmp:
							content[4] = content_tmp.split(':')[1]
						elif "usr_nickname" in content_tmp:
							content[3] = content_tmp.split(':')[1]
				else:
					continue
			except Exception as e:
				print("feedback", e)

			content[0] = feedback[0]

			if "闪退" not in content[0]:
				continue
			# 处理数据，server_name
			# if tmp_content[2] in server_map.keys():
			# 	tmp_content[2] = server_map[tmp_content[2]]
			#
			# 手机型号解码
			# if tmp_content[4] in iphone_map.keys():
			# 	tmp_content[4] = iphone_map[tmp_content[4]]
			# elif tmp_content[4] in android_map.keys():
			# 	tmp_content[4] = android_map[tmp_content[4]]

			# iptmp = (document['ip'].split(':')[0].encode('utf8')).replace('x', '0')
			#ipinfo = ipdb.getIpAddr(ipdb.str2ip(iptmp)).split()

			# print(ipinfo[0])
			# input()
			# raw_input()
			dictAlldata[cont]['time'] = document['time']#datetostr(document['time'].encode('utf8'),"%Y-%m-%d %H:%M",'day',True)
			# dictAlldata[cont]['time_sort'] = datetostr(document['time'].encode('utf8'),dformat,level,date_flag)

			#dictAlldata[cont]['ip'] = document['ip']
			dictAlldata[cont]['content'] = content[0]
			dictAlldata[cont]['usr_id'] = content[1]
			dictAlldata[cont]['usr_server'] = content[2]
			dictAlldata[cont]['usr_name'] = content[3]
			dictAlldata[cont]['usr_equip'] = content[4]
			#dictAlldata[cont]['ip_area'] = ipinfo[0]
			#dictAlldata[cont]['ip_isp'] = (ipinfo[1] == 'CZ88.NET' and 'unknow' or ipinfo[1])


			# print dictAlldata[cont]
			# print dictAlldata[cont]['content']
			# raw_input()
			# tmp_str = ""
			# for x in dictAlldata[cont]:
			# 	# print(x)
			# 	# input()
			# 	tmp_str += x + ":" + dictAlldata[cont][x] + "\t"
			# # print(tmp_str)
			# # input()
			# f.write(tmp_str+"\n")
			cont += 1
		except Exception as e:
			flag = False
			print(333333333, e)
			# raw_input()

	if flag == False:
		# 如果最后一个是空的，则删除
		del dictAlldata[cont]

	cursor['cursor'].close()
	# f.close()
	return dictAlldata


def createtransdata(filename=None, label=None, cont=0):
	# 输出一个字典，每个key是一个文档，content是玩家评论，label是类别
	dictAlldata = {}
	if filename == None:
		filename = "../input/loginerror.txt"
	cursor = {}
	if label == None:
		label = 1

	cursor["cursor"] = open(filename,"r",encoding="utf8")
	if cont == 0:
		cont = 0
	for _doc in cursor["cursor"]:
		doctmp = _doc.split("\t")
		if doctmp[0] == "时间":
			continue
		dictAlldata[cont] = {}
		dictAlldata[cont]["content"] = doctmp[1]
		dictAlldata[cont]["label"] = label
		cont += 1

	return dictAlldata

if __name__ == "__main__":
	# 测试数据并分割
	# data = DataGet("%Y-%m-%d %H:%M:%S", 'day', True, 0, 0)
	# listdate = ["2017-8-8"]
	# data = DataGet(0, [""])
	# output_file = open("../output/result_shantui.pkl", 'wb')
	# pickle.dump(data, output_file)
	# output_file.close()
	# output_file = open("../output/result_shantui.pkl", 'rb')
	# data = pickle.load(output_file)
	# output_file.close()

	# 获取资料
	of = open("../segresult/data_all_0908.pkl","rb")
	data = pickle.load(of)
	of.close()
	sumdic = tf.gendict(data[-1])

	outf = open("../output/output_shantui.txt","a")
	sumdics = sorted(sumdic.items(), key=lambda  asd:asd[1]["num"], reverse=True)
	# print(sumdics)
	for strs in sumdics:
		if strs[1]["num"] == 1:
			continue
		if len(strs[0]) <= 1:
			continue
		tmp_str = strs[0] + ": " + str(strs[1]["num"]) + "\n"
		outf.write(tmp_str)
	outf.close()

	# tfidf_dic = tf.cal_TFIDF(data, sumdic)
	# aaa = {"a": 2}
	# print(aaa)
	# aaa.update({"a":1})
	# print(aaa)
	# # 获取训练数据并分割
	# filename = ['../input/loginerror.txt', '../input/shantui.txt']
	# label = [0, 1]
	# data = {}
	# for index, efile in enumerate(filename):
	# 	cont = len(data.keys())
	# 	datatmp = {}
	# 	datatmp = createtransdata(efile, label[index], cont+1)
	# 	print(datatmp)
	# 	data.update(datatmp)
	# 	input()
	#
	# ws.wordseg(data, '../segresult/data_trans.pkl')

