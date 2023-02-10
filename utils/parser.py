from bs4 import BeautifulSoup as bs
import requests, time, os
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
	
	def compare_dfs(self):
		'''Compares previous dataframe with newer for unique
		and later entries. checks 'Date' column'''
		# Read New DF
		newdf = self.df
		# Rename column only if career page:
		if self.urltype=='employment':
			newdf.rename(columns={'Start Date': 'Date'}, inplace=True)

		newdf['Date']=pd.to_datetime(newdf['Date'], format='%d/%m/%Y')
		newdf.sort_values(by='Date')
		print('New Dataframe',newdf, sep='\n')
		## Test RUN logic JUst in Case df.query('istoday) changed
		## Stores upto the specified date
		# newdf = newdf.loc[(newdf.Date <= np.datetime64(date(2023,2,9)))]
		# Read Previous Dataframe
		if os.path.exists(f'logs/logged-{self.urltype}.json'):
			# read the df: df2 is old
			df2 = pd.read_json(f'logs/logged-{self.urltype}.json')
			df2.sort_values(by='Date')
			# get last date
			# minimum date might help for the career page
			latest_date = df2.Date.min()
			## Compare them
			dfC = newdf[(newdf['Date']>=latest_date) &
			(~newdf['Link'].isin(df2['Link']))]
			# dfC = df1[~newdf['Link'].isin(df1['Link'])]
			# dfC = newdf.loc[(~newdf.Link.isin(df2.Link)) & (newdf.Date >= latest_date)]
			dfC=dfC.reset_index(drop=True)
			print('difference',dfC)
			## then save the newer df if not empty
			if not dfC.dropna().empty:
				dfC.to_json(f'logs/logged-{self.urltype}.json')
			# not done
			return dfC

		else:
			newdf.to_json(f'logs/logged-{self.urltype}.json')
			newdf=newdf.reset_index(drop=True)
			return newdf

	
	def main(self):
		com_df=self.compare_dfs()
		return com_df