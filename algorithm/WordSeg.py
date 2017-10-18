#encoding:utf8

import jieba
import pickle
jieba.load_userdict(r'..\statics\user_dict.txt')
# 输出dict，key为类别标签，默认为-1
def wordseg(data, filename=None):
	"""输入一个字典，该字典的每一个key是一个文档
	输出一个字典，该字典的key是类别，每个类别下有很多文档"""
	if data == {}:
		print('未获取数据')
		return
	if filename == None:
		filename = "../segresult/data_all_1011.pkl"

	stw_list = [line.strip() for line in open(r'..\statics\stopwords.txt', 'r', encoding="utf8").readlines()]

	# 每个文档的词，一篇文档，一个字符串
	outresult = {}
	outlist = []

	outrefer = {}
	outcontent = []
	for cont in data:
		label = -1
		if "label" in data[cont]:
			label = data[cont]['label']
			if label in outresult.keys():
				outlist = outresult[label]
				outcontent = outrefer[label]
			else:
				outresult[label] = []
				outlist = []
				outrefer[label] = []
				outcontent = []

		else:
			if label in outresult.keys():
				outlist = outresult[label]
				outcontent = outrefer[label]
			else:
				outresult[label] = []
				outlist = []
				outrefer[label] = []
				outcontent = []

		if "content" not in data[cont]:
			continue
		seg_list = jieba.cut(data[cont]["content"])
		outstr = ""
		# 去除停用词
		for word in seg_list:
			# print word
			# print type(word),type(stw_list[0])
			# raw_input()
			if word.encode('utf8') not in stw_list and word.strip() != '':
				if len(word) >= 2:  # 去掉长度小于1的词
					if word != '\t':
						outstr += word
						outstr += " "

		if outstr != "":
			outlist.append(outstr)
			outresult[label] = outlist
			#原始参考的数据
			outcontent.append(data[cont]["content"])
			outrefer[label] = outcontent
		# print data[cont]["content"]
		# print outstr
		# raw_input()

	# print outresult.keys()
	# print outresult[1]
	# print len(outresult[1])
	output_file = open(filename, 'wb')
	pickle.dump(outresult, output_file)
	output_file.close()
	return outresult
	#参考
	# output_file = open("../segresult/data_trans_cankao.pkl", 'wb')
	# pickle.dump(outrefer, output_file)
	# output_file.close()
