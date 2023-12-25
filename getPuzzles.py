import requests
from bs4 import BeautifulSoup
import sys
import pickle

def getPuzzle(difficulty):
	html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
	soup = BeautifulSoup(html_doc,features="lxml")

	ids = ['f00','f01','f02','f03','f04','f05','f06','f07','f08',
	'f10','f11','f12','f13','f14','f15','f16','f17','f18',
	'f20','f21','f22','f23','f24','f25','f26','f27','f28',
	'f30','f31','f32','f33','f34','f35','f36','f37','f38',
	'f40','f41','f42','f43','f44','f45','f46','f47','f48',
	'f50','f51','f52','f53','f54','f55','f56','f57','f58',
	'f60','f61','f62','f63','f64','f65','f66','f67','f68',
	'f70','f71','f72','f73','f74','f75','f76','f77','f78',
	'f80','f81','f82','f83','f84','f85','f86','f87','f88']

	data = []
	for cid in ids:
		data.append(soup.find('input',id=cid))

	board = [[0 for x in range(9)] for x in range(9)]
	for index, cell in enumerate(data):
		try:
			board[int(ids[index][2])][int(ids[index][1])] =  int(cell['value'])
			#board[index//9][index%9] = int(cell['value'])
		except:
			pass
	#print(soup.prettify())
	return board


def saveBoard(board,difficulty,num):
	pickle.dump(board, open('puzzles\\{}-{}.pz'.format(difficulty,num),'wb'))

def loadBoard(difficulty,num):
	return pickle.load(open('puzzles\\{}-{}.pz'.format(difficulty,1),'rb'))


board = getPuzzle(1)
for difficulty in range(1,5):
	for num in range(100):
		saveBoard(board, difficulty,num)


