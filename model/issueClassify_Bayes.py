# encoding=utf8
# P(A|B) = P(B|A) P(A) / P(B)
import pickle
import random
import algorithm.TF_IDF_algo as tf
import copy
import math

def getcount(Sumdic, listdata, label, dataword):
	# 获取每个类别中每个词的数目和酶类文档的总次数
	if listdata == None:
		return

	if "word" not in dataword:
		dataword["word"] = {}
		dataword["num"] = {}

	data_word = dataword["word"]
	num = 0
	if label not in dataword["num"]:
		dataword["num"][label] = num

	for doc in listdata:
		for key in doc.split(" "):
			if key not in Sumdic.keys():
				continue

			num += 1

			if key in data_word.keys():
				if label in data_word[key]:
					data_word[key][label] += 1
				else:
					data_word[key][label] = 1
			else:
				data_word[key] = {}
				data_word[key][label] = 1
	# 记录总词数
	dataword["num"][label] = num

	return dataword


def bayes(dataInput):
	if dataInput == None:
		return

	data_trans = dataInput["train"]
	data_test = dataInput["test"]
	lb = data_trans.keys()

	listtrans = []
	for label in data_trans:
		listtrans.extend(data_trans[label])

	listtest = []
	for label in data_test:
		listtest.extend(data_test[label])

	# 建立特征集
	data_tmp = copy.deepcopy(listtrans)
	# data_tmp.extend(copy.deepcopy(listtest))
	sumdic = tf.gendict(data_tmp)

	# 提取每个类别中的特征词数目
	dataword = {}
	for label in data_trans:
		dataword = getcount(sumdic, data_trans[label], label, dataword)

	# print len(dataword["word"]), len(sumdic.keys())
	# raw_input()
	# 计算概率
	if "word" not in dataword:
		print("word not in dataword")
		return

	# # 计算每个特征的概率
	p_word = {}

	for key in dataword["word"]:
		p_word[key] = {}
		tmp_cont = 0
		for label in dataword["word"][key]:
			tmp_cont += dataword["word"][key][label]
		for label in lb:
			if label in dataword["word"][key]:
				p_word[key][label] = float(dataword["word"][key][label] + 1) / float(tmp_cont + len(lb))
			else:
				p_word[key][label] = float(1) / float(tmp_cont + len(lb))

	p_label = {}
	sum_doc = 0
	for label in data_trans:
		p_label[label] = len(data_trans[label])
		sum_doc += p_label[label]

	for label in p_label:
		p_label[label] = float(p_label[label]) / float(sum_doc)

	print(p_label)
	input()
	# # 计算每个文档的概率
	# result = 0
	result  = [0 for label in data_trans]
	cont = 0
	num = 0
	allnum = 0
	for label in data_test:
		for doc in data_test[label]:
			allnum += 1
			tmp = {}
			for label2 in lb:
				tmp[label2] = 0
			# tmp1 = 0.0
			# tmp2 = 0.0
			for key in doc.split(" "):
				if key not in sumdic.keys():
					continue

				for label2 in lb:
					if label2 in p_word[key].keys():
						tmp[label2] += math.log(p_word[key][label2], math.e)
					# if label2 in p_word[key].keys():
					# 	tmp[label] += math.log(p_word[key][0], math.e)
					# 	# print "tmp1", tmp1,  math.log(p_word[key][0], math.e)
					# if 1 in p_word[key].keys():
					# 	tmp2 += math.log(p_word[key][1], math.e)
					# 	# print "tmp2", tmp2, math.log(p_word[key][0], math.e)
					# 	# tmp += math.log()


				# raw_input()
			# print "---------------"

			for label2 in lb:
				tmp[label2] += math.log(p_label[label2], math.e)

			rlabel = max(tmp.items(), key=lambda x: x[1])[0]

			if rlabel != label:
				num += 1
			# tmp1 += math.log(p_label[0], math.e)
			# tmp2 += math.log(p_label[1], math.e)
			#
			# print "tmp1", tmp1
			# print "tmp2", tmp2
			#
			# if (tmp1<tmp2):
			# 	print label, 1
			#
			# 	raw_input()

	print(allnum, num)
	print("准确率", float(allnum-num) / float(allnum))



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

if __name__ == "__main__":
	data_ = sample()
	bayes(data_)
