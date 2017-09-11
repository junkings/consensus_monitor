#encoding: utf8
import jieba
import pickle
from algorithm import TF_IDF_algo as tf
import copy
import random


def minheap(heap, value, label, str):
	# 最小堆排序算法
	# heap 是一个字典
	if heap == None:
		return heap

	if heap[0]["value"] == -1 or heap[0]["value"] < value:
		heap[0]["value"] = value
		heap[0]["label"] = label
		heap[0]["str"] = str
	else:
		return heap

	t = 0
	m = 1
	n = 2
	val_tmp = -1
	lab_tmp = -1
	str_tmp = ""
	while((m < len(heap.keys())) and (n < len(heap.keys())) and (value > min(heap[m]["value"], heap[n]["value"]))):
		if (heap[m]["value"]< heap[n]["value"]):
			val_tmp = heap[m]["value"]
			lab_tmp = heap[m]["label"]
			str_tmp = heap[m]["str"]
			heap[m]["value"] = value
			heap[m]["label"] = label
			heap[m]["str"] = str
			heap[t]["value"] = val_tmp
			heap[t]["label"] = lab_tmp
			heap[t]["str"] = str_tmp
			t = m
			n = (m+1)*2
			m = n-1
		else:
			val_tmp = heap[n]["value"]
			lab_tmp = heap[n]["label"]
			str_tmp = heap[n]["str"]
			heap[n]["value"] = value
			heap[n]["label"] = label
			heap[n]["str"] = str
			heap[t]["value"] = val_tmp
			heap[t]["label"] = lab_tmp
			heap[t]["str"] = str_tmp
			t = n
			n = (n+1)*2
			m = n-1

	if m < len(heap):
		if value > heap[m]:
			val_tmp = heap[m]["value"]
			lab_tmp = heap[m]["label"]
			str_tmp = heap[m]["str"]
			heap[m]["value"] = value
			heap[m]["label"] = label
			heap[m]["str"] = str
			heap[t]["value"] = val_tmp
			heap[t]["label"] = lab_tmp
			heap[t]["str"] = str_tmp

	return heap

def calsimilar(test, trans, data_test, data_trans, data_name, k):
	"""
	# 计算相似度
	# Test 是测试集，字典
	# trans 是训练节， 字典
	# data1 测试集， 列表
	# data_trans, 列表
	"""
	# result
	result_data_test = {}
	num = 0
	allnum = 0



	# print heap
	# raw_input()
	# 每个测试集
	for file_test in test:
		allnum += 1
		max_similar = -1
		# 每个样本集
		heap = {}
		for cont in range(k):
			heap[cont] = {}
			heap[cont]["value"] = -1.0
			heap[cont]["label"] = -1
			heap[cont]["str"] =""
		for file_trans in trans:


			# 计算相似度
			r_tmp = tf.calcosine(test[file_test], trans[file_trans])
			# for key in trans[file_trans].keys():
			# 	if key == "Label":
			# 		continue
			# 	tmp = 0 if key not in test[file_test].keys() else test[file_test][key]['TFIDF']
			# 	# 分子
			# 	result = result + trans[file_trans][key]['TFIDF'] * tmp
			#
			# 	# 分母计算-训练样本
			# 	result1 = result1 + pow(trans[file_trans][key]['TFIDF'], 2)
			#
			# for key in test[file_test]:
			# 	if key == "Label":
			# 		continue
			# 	# 分母计算-测试样本
			# 	result2 = result2 + pow(test[file_test][key]['TFIDF'], 2)
			#
			# if result != 0:
			# 	r_tmp = result / (pow(result1, 0.5)*pow(result2, 0.5))
			# else:
			# 	r_tmp = 0
			# print r_tmp, trans[file_trans]["Label"]
			heap = minheap(heap, r_tmp, trans[file_trans]["Label"], data_trans[file_trans])

			# 最近邻算法
			# if max_similar < r_tmp:
			# 	max_similar = r_tmp
			# 	max_doc = file_trans

		dict_label = {}
		for cont in heap:
			if heap[cont]["label"] not in dict_label.keys():
				dict_label[heap[cont]["label"]] = 1
			else:
				dict_label[heap[cont]["label"]] += 1

		libnum = -1
		trans_label = -1
		for cont in dict_label:
			if dict_label[cont] > libnum:
				libnum = dict_label[cont]
				trans_label = cont

		if trans_label != test[file_test]["Label"]:
			# print test[file_test]
			# print data_test[file_test]
			num += 1
			# print num
			# raw_input()


		# 最近邻算法
		# if max_similar > 0.00001:
		# 	# print test[file_test]
		# 	# print trans[fff]
		# 	# print data_test[file_test]
		# 	# print data_trans[fff]
		# 	# print '------------'
		# 	# print '测试集',test[file_test]['Label']
		# 	# print '训练集',trans[fff]['Label']
		# 	if trans[max_doc]['Label'] != test[file_test]['Label']:
		# 		num += 1
		# 		# raw_input()
		# else:
		# 	num += 1
	print(num,allnum)
	accuracy = float(allnum - num) / float(allnum)
	print('准确率', accuracy)


def knn(dataInput):
	"""knn算法"""
	if dataInput == None:
		return

	data_trans = dataInput['train']
	data_test = dataInput['test']

	listtrans = []
	for label in data_trans:
		listtrans.extend(data_trans[label])

	listtest = []
	for label in data_test:
		listtest.extend(data_test[label])

	# 建立全部字典
	data_tmp = copy.deepcopy(listtrans)
	# data_tmp.extend(copy.deepcopy(listtest))
	sumdic = tf.gendict(data_tmp)
	# print len(sumdic.keys())
	# raw_input()

	# 计算相似度
	# print listtrans
	# raw_input()
	tfidftrans = tf.cal_TFIDF(data_trans, sumdic)
	tfidftest = tf.cal_TFIDF(data_test, sumdic)

	# 计算余弦定理
	calsimilar(tfidftest, tfidftrans, listtest, listtrans, '1', 9)


def sample():
	# 训练集合
	pkl_file = open('../segresult/data_trans.pkl', 'rb')
	data = pickle.load(pkl_file)

	## refer
	# pkl_file_rf = open('../segresult/data_trans_cankao.pkl', 'rb')
	# data_refer = pickle.load(pkl_file_rf)

	# print data
	# raw_input()
	# 划分训练集和测试集
	data_trans = {}
	data_test = {}
	data_return = {}
	for label in data:
		# print data[label]
		strtmp = data[label]
		# print strtmp
		# print len(strtmp)
		# print random.shuffle(strtmp)
		# raw_input()
		strtmp = data[label]
		strlen = len(strtmp)
		strtmp = random.sample(strtmp, strlen)
		data_trans[label] = strtmp[:int(strlen/5)]
		data_test[label] = strtmp[int(strlen/5):]

	data_return['train'] = data_trans
	data_return['test'] = data_test

	return data_return


def test():
	"""测试例子"""
	# 获取数据
	pkl_file = open('..\segresult\data.pkl', 'rb')

	data_test = pickle.load(pkl_file)

	pkl_file_shantui = open('..\segresult\data_shantui.pkl', 'rb')
	data_shantui = pickle.load(pkl_file_shantui)

	pkl_file_loginerror = open('..\segresult\data_loginerror.pkl', 'rb')
	data_loginerror = pickle.load(pkl_file_loginerror)


	# 深拷贝
	dicdata = copy.deepcopy(data_test)
	dicdata.extend(copy.deepcopy(data_shantui))
	dicdata.extend(copy.deepcopy(data_loginerror))

	# 生成总词典
	Sumdic = tf.gendict(dicdata)

	# 生成测试集
	data1_TFIDF = tf.cal_TFIDF(data_test, Sumdic)
	# 生成训练集
	transdata = copy.deepcopy(data_shantui)
	transdata.extend(copy.deepcopy(data_loginerror))
	data_trans_TFIDF = tf.cal_TFIDF(transdata, Sumdic)
	# data_shantui_TFIDF = tf.calTFIDF(data_shantui, Sumdic)
	# data_loginerror_TFIDF = tf.calTFIDF(data_loginerror, Sumdic)


	calsimilar(data1_TFIDF, data_trans_TFIDF, data_test, transdata, 'shantuierror')

if __name__ == "__main__":
	data = sample()
	knn(data)
	# data_trans = data['train']
	# data_test = data['test']

	# test minheap
	# heap = {}
	# for cont in xrange(3):
	# 	heap[cont] = {}
	# 	heap[cont]["value"] = -1.0
	# 	heap[cont]["label"] = -1
	# 	heap[cont]["str"] = ""
	#
	# value = [0.45, 0.89, 0.12, 0.45, 0.02, 0.56, 0.46, 0.34, 0.03, 1.20]
	# label = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	# str = ["1", "2", "3", "4", "5", "11", "12", "13", "14", "15"]
	# for index, val in enumerate(value):
	# 	# print val
	# 	heap = minheap(heap, val, label[index], str[index])
	#
	# print heap
