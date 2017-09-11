# encoding:utf8


def gendict(data):
	"""
	输入是一个列表
	建立总词典,每个特征词的位置
	建立特征词
	data是一个列表
	"""
	if data == None:
		return
	# 建立总词典
	sumdic = {}

	# 记录每个词的特征位置
	pos = 0
	for str in data:
		flag = True
		eachw = 0
		# if type(str) != "str":
		# 	continue
		for key in str.split(" "):
			if key == "":
				continue
			eachw += 1

			# 记录每个特征词的位置和数量
			# 位置：POS 数量：num
			if key not in sumdic.keys():
				sumdic[key] = {}
				sumdic[key]['num'] = 1
				sumdic[key]['pos'] = pos
				pos = pos+1
			else:
				sumdic[key]['num'] += 1
	i = 0
	# 获取每个特征词的数量排序
	# L = sorted(Sumdic.iteritems(), key=lambda x: x[1]['num'], reverse=True)
	# print L
	# raw_input()
	# for i in L:
	# 	print i[0], i[1]['num']
	# 	raw_input()

	return sumdic


def cal_TFIDF(data, Sumdic):
	"""
	# 计算TF-IDF 特征
	data 列表
	Sumdic 字典
	"""
	# 总文本数
	Sumfile = 0
	# 每个文本
	Sumeach = {}
	# 每个文本的词总数
	Sumeachw = {}

	#
	datadic = {}
	for label in data:
		for str in data[label]:
			Sumeach[Sumfile] = {}
			eachw = 0
			if str == "":
				continue

			for key in str.split(" "):
				if key == "" or key not in Sumdic.keys():
					continue

				tmp_dic = {}
				eachw += 1

				if key not in Sumeach[Sumfile].keys():
					Sumeach[Sumfile][key] = 1
				else:
					Sumeach[Sumfile][key] += 1

				if key not in tmp_dic.keys():
					tmp_dic[key] = 1
					if key not in datadic.keys():
						datadic[key] = {}
						datadic[key]['num'] = 1
					else:
						datadic[key]['num'] += 1

			if eachw > 0:
				Sumeachw[Sumfile] = {}
				Sumeachw[Sumfile]['WordNum'] = eachw
				Sumeachw[Sumfile]['Label'] = label
				Sumfile += 1

	# 计算词频
	import math
	# print("cal_TFIDF", Sumfile)
	SumTFIDF = {}
	for doc in Sumeach:
		SumTFIDF[doc] = {}
		SumTFIDF[doc]['Label'] = Sumeachw[doc]['Label']
		for key in Sumeach[doc].keys():
			SumTFIDF[doc][key] = {}
			# TF 文章中出现的某个词的次数 / 该文档中词的总数
			SumTFIDF[doc][key]['TF'] = (Sumeach[doc][key]/float(Sumeachw[doc]['WordNum']))
			# IDF 语料库的文档总数 / 包含改词的文档书+1
			SumTFIDF[doc][key]['IDF'] = math.log((float(Sumfile)/(datadic[key]['num']+1)))
			SumTFIDF[doc][key]['TFIDF'] = SumTFIDF[doc][key]['TF']*SumTFIDF[doc][key]['IDF']
			# Sumdic[key]['pos'] 总词典中词的位置，这里没有用到文档中词的总数量
			SumTFIDF[doc][key]['pos'] = Sumdic[key]['pos']

	return SumTFIDF


def calcosine(test, trans):
	"""计算相似度 test是一个dict，key是每个提取的关键字"""
	"""trans是一个dict，key是每个提取的关键字，test和trans 都是一个文档"""
	"""计算test和doc的相似度"""
	result = 0
	result1 = 0
	result2 = 0
	for key in trans.keys():
		if key == "Label":
			continue
		tmp = 0 if key not in test.keys() else test[key]['TFIDF']
		tfidf_k = trans[key]['TFIDF']
		# 分子
		result += tfidf_k * tmp

		# 分母计算-训练样本
		result1 += pow(tfidf_k, 2)

	for key in test:
		if key == "Label":
			continue
		# 分母计算-测试样本
		result2 += pow(test[key]['TFIDF'], 2)

	if result != 0:
		r_tmp = result / (pow(result1, 0.5) * pow(result2, 0.5))
	else:
		r_tmp = 0

	return r_tmp



if __name__ == "__main__":
	heap = [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
	value = [0.45, 0.89, 0.12,0.45, 0.02, 0.56, 0.46, 0.34, 0.03, 1.20]

	for val in value:
		pass
		# heap = minheap(heap, val)

	print(heap)
