#encoding:utf8
import socket,string,struct,sys
import json
import urllib.request
import sys
import time
# ip地址查询
# 纯真数据库

class IPInfo(object):
	'''QQWry.Dat数据库查询功能集合
	'''

	def __init__(self, dbname):
		''' 初始化类，读取数据库内容为一个字符串，
		通过开始8字节确定数据库的索引信息'''

		self.dbname = dbname
		f = open(dbname, 'rb')
		self.img = f.read()
		f.close()

		# QQWry.Dat文件的开始8字节是索引信息,前4字节是开始索引的偏移值，
		# 后4字节是结束索引的偏移值。
		(self.firstIndex, self.lastIndex) = struct.unpack('II', self.img[:8])
		# 每条索引长7字节，这里得到索引总个数
		self.indexCount = (self.lastIndex - self.firstIndex) / 7 + 1

	def getString(self, offset=0):
		''' 读取字符串信息，包括"国家"信息和"地区"信息

		QQWry.Dat的记录区每条信息都是一个以'\0'结尾的字符串'''

		o2 = self.img.find('\0', offset)
		# return self.img[offset:o2]
		# 有可能只有国家信息没有地区信息，
		gb2312_str = self.img[offset:o2]
		try:
			utf8_str = str(gb2312_str, 'gb2312').encode('utf-8')
		except:
			return '未知'
		return utf8_str

	def getLong3(self, offset=0):
		'''QQWry.Dat中的偏移记录都是3字节，本函数取得3字节的偏移量的常规表示
		QQWry.Dat使用“字符串“存储这些值'''
		offset = int(offset)
		s = self.img[offset: offset + 3]
		# s += b'\0'
		# unpack用一个'I'作为format，后面的字符串必须是4字节
		return struct.unpack('I', s)[0]

	def getAreaAddr(self, offset=0):
		''' 通过给出偏移值，取得区域信息字符串，'''

		byte = ord(self.img[offset])
		if byte == 1 or byte == 2:
			# 第一个字节为1或者2时，取得2-4字节作为一个偏移量调用自己
			p = self.getLong3(offset + 1)
			return self.getAreaAddr(p)
		else:
			return self.getString(offset)

	def getAddr(self, offset, ip=0):
		img = self.img
		o = offset
		byte = ord(img[o])

		if byte == 1:
			# 重定向模式1
			# [IP][0x01][国家和地区信息的绝对偏移地址]
			# 使用接下来的3字节作为偏移量调用字节取得信息
			return self.getAddr(self.getLong3(o + 1))

		if byte == 2:
			# 重定向模式2
			# [IP][0x02][国家信息的绝对偏移][地区信息字符串]
			# 使用国家信息偏移量调用自己取得字符串信息
			cArea = self.getAreaAddr(self.getLong3(o + 1))
			o += 4
			# 跳过前4字节取字符串作为地区信息
			aArea = self.getAreaAddr(o)
			return cArea, aArea

		if byte != 1 and byte != 2:
			# 最简单的IP记录形式，[IP][国家信息][地区信息]
			# 重定向模式1有种情况就是偏移量指向包含国家和地区信息两个字符串
			# 即偏移量指向的第一个字节不是1或2,就使用这里的分支
			# 简单地说：取连续取两个字符串！

			cArea = self.getString(o)
			# o += len(cArea) + 1
			# 我们已经修改cArea为utf-8字符编码了，len取得的长度会有变，
			# 用下面方法得到offset
			o = self.img.find('\0', o) + 1
			aArea = self.getString(o)
			return cArea, aArea

	def find(self, ip, l, r):
		''' 使用二分法查找网络字节编码的IP地址的索引记录'''
		if r - l <= 1:
			return l

		m = (l + r) / 2
		o = int(self.firstIndex + m * 7)
		print(type(o),o)
		new_ip = struct.unpack('I', self.img[o: o + 4])[0]
		if ip  <= new_ip:
			return self.find(ip, l, m)
		else:
			return self.find(ip, m, r)

	def getIPAddr(self, ip):
		''' 调用其他函数，取得信息！'''
		# 使用网络字节编码IP地址
		ip = struct.unpack('!I', socket.inet_aton(ip))[0]
		# 使用 self.find 函数查找ip的索引偏移
		i = self.find(ip, 0, self.indexCount - 1)
		# 得到索引记录
		o = self.firstIndex + i * 7
		# 索引记录格式是： 前4字节IP信息+3字节指向IP记录信息的偏移量
		# 这里就是使用后3字节作为偏移量得到其常规表示（QQWry.Dat用字符串表示值）
		o2 = self.getLong3(o + 4)
		# IP记录偏移值+4可以丢弃前4字节的IP地址信息。
		(c, a) = self.getAddr(o2 + 4)
		return c, a

	def output(self, first, last):
		for i in range(first, last):
			o = self.firstIndex + i * 7
			ip = socket.inet_ntoa(struct.pack('!I', struct.unpack('I', self.img[o:o + 4])[0]))
			offset = self.getLong3(o + 4)
			(c, a) = self.getAddr(offset + 4)
			print("%s %d %s/%s" % (ip, offset, c, a))


"通过淘宝接口获取ip信息"
def getIPbytb(ip):
	time.sleep(0.5)
	url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
	data = {}
	try:
		data['jsondata'] = json.loads(str(urllib.request.urlopen(url).read(),encoding="utf8"))
	except Exception as e:
		print(e)
		data['jsondata'] = {}
		data['jsondata']['code'] = 1
	# {u'code': 0, u'data': {u'ip': u'119.124.101.221', u'city':
	# 其中code的值的含义为，0：成功，1：失败。{u'code': 1, u'data': u'invaild ip.'}
	# print(jsondata)
	if data['jsondata']['code'] == 1:
		data['jsondata']['data'] = {'region': '', 'city': '', 'isp': ''}
	print(1,data['jsondata']['data']['region'], data['jsondata']['data']['city'], data['jsondata']['data']['isp'])
	return (data['jsondata']['data']['region'], data['jsondata']['data']['city'], data['jsondata']['data']['isp'])
def main():
    # IPL = IPLocator("../statics/qqwry.dat")
    # ip = "218.107.55.252"
    # address = IPL.getIpAddr(IPL.str2ip(ip))
    # range = IPL.getIpRange(IPL.str2ip(ip))
    # print((address[1]))
    # print("此IP %s 属于 %s\n所在网段: %s" % (ip, address, range))
    i = IPInfo('../statics/qqwry.dat')
    (c, a) = i.getIPAddr("218.107.55.252")
    print('%s %s/%s' % ("218.107.55.252", c, a))

if __name__ == "__main__":
    print('\xb4\xbf\xd5\xe6\xcd\xf8\xc2\xe7')
    #getIPbytb("218.107.55.252")
    main()
