from bs4 import BeautifulSoup as bs
import requests, time, re
import pandas as pd
import numpy as np
from datetime import date

class Parser:
	''''Parser object and functions'''
	def __init__(self, main_url):
		'''Creates session with a user-agent'''
		self.sess = requests.Session()
		UA = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'}
		self.sess.headers.update(UA)
		self.url = main_url

	def get_page(self, url):
		'''Fetches the url page using session'''
		self.response = self.sess.get(url)
		i=0
		if self.response.status_code == 200:
			return self.response
		else:
			i=i+1
			time.sleep(4)
			if not i>3:
				return self.get_page(self, url)
			else:
				return None

	def page_souper(self):
		'''Soups the page response to get the table'''		
		self.soup = bs(self.response.text, 'lxml')
		tab_cont = self.soup.find('div', class_='middle_content')
		table_first = tab_cont.find('table')
		# first table is for searching
		table_main = table_first.find_next('table')
		self.table = table_main
		# with open('test.html', 'w') as html:
		# 	html.write(str(table_main))

	def table_parse(self):
		'''Parses the table for latest insertions'''
		# print(self.table)
		df = pd.read_html(str(self.table), header=0, flavor=["lxml", "bs4"])[0]
		# df drop none values
		df1 = df.dropna(axis=0, how='all')
		df1 = df1.dropna(axis=1, how='all')
		# drop 
		df1 = df1.reset_index(drop=True)

		#do some url append:
		links = []
		rows = self.table.find_all("tr")
		print(len(rows))
		for row in rows:
			innr_row = row.find("td")
			link_c = innr_row.find('a')
			if not link_c ==None:
				link = link_c.get('href')
				# print(link)
				links.append(link)
			else:
				pass
		

		#check
		df1['Link'] = links
		# print(df1.columns)
		# print(df1.iloc[2].values)

		# save to a dfobject
		self.df = df1
		

	def main(self):
		'''Serialize them return dataframe'''
		# self.url=each
		resp = self.get_page(self.url)
		if not resp==None:
			self.page_souper()
			self.table_parse()
			return self.df

class OptionalParser:
	'''Parser according to URL'''
	def __init__(self, urltype, df) -> None:
		self.urltype = urltype
		self.df = df
	
	def date_present(self):
		df = self.df
		df['Date']=pd.to_datetime(df['Date'], format='%d/%m/%Y')
		df['is_today'] = df['Date'] == np.datetime64(date.today())
		# print(df.columns)
		self.newdf = df.query('is_today == True')
	
	def main(self):
		self.date_present()
		return self.newdf