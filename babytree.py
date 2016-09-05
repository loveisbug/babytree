# -*- coding: utf-8 -*-
import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import codecs
import os, sys
import time

host = 'http://www.babytree.com'
base_path = 'babytree'

def mkchdir(path):
	if not os.path.exists(path):
		os.mkdir(path)
	os.chdir(path)

def fetch_youerqi():
	urlrequest = urllib2.Request('http://www.babytree.com/learn/youerqi')
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")

def fetch_learn():
	urlrequest = urllib2.Request(host + '/learn/specialtopics')
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	mkchdir(base_path)
	blks = parser.findAll('div', 'knowListAllBlk')
	bingo = 0
	failed = 0
	for blk in blks:
		mkchdir(blk.findNext('h5').text.strip())
		tops = blk.findAll('dl', 'knowListAllByCat')
		for top in tops:
			mkchdir(top.findNext('dt').text.strip())
			alist = top.findAll('a')
			for article in alist:
				fout = codecs.open(article.text.strip() + '.txt', 'w', 'utf-8')
				# print blk.findNext('h5').text.strip() + '/' + top.findNext('dt').text.strip() + '/' + article.text.strip() + '.txt'
				articleurl = host + article['href']
				urlrequest = urllib2.Request(articleurl)
				html_src = urllib2.urlopen(urlrequest).read()
				parser = BeautifulSoup(html_src, "html.parser", from_encoding="gb18030")
				contents = parser.findAll('span', {'style' : 'font-size:14px;'}) #'color:#696969;'
				# print len(contents)
				if len(contents) > 0:
					bingo += 1
				else:
					failed += 1
				contstr = ''
				for content in contents:
					contstr += content.text.strip() + '\n'
				try:
					fout.write(contstr)
				except UnicodeDecodeError:
					print 'UnicodeDecodeError: ' + article.text.strip() + '.txt'
				fout.close()
			os.chdir('..')
		os.chdir('..')
	os.chdir('..')
	print 'scanned ' + str(bingo + failed) + ' articles, ', str(bingo) + ' fetched, ', str(failed) + ' failed.'
	
def fetch_weekly():
	pass

def test():
	urlrequest = urllib2.Request('http://www.babytree.com/learn/specialtopic/shengnanshengnv')
	html_src = urllib2.urlopen(urlrequest).read()
	print len(html_src)
	parser = BeautifulSoup(html_src, "html.parser", from_encoding="gb2312")
	cons = parser.findAll('span', {'style' : 'color:#696969;'})
	constr = ''
	print len(cons)
	for con in cons:
		constr += con.text.strip() + '\n'
	fout = codecs.open('test.txt', 'w', 'utf-8')
	fout.write(constr)
	fout.close()

def main(argv):
	t0 = time.clock()
	fetch_learn()
	# test()
	t = time.clock() - t0
	print 'time elapsed: ', t
	# if len(argv) > 1:
	# 	return 0
	# else:
	# 	return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv))