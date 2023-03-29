from pyrogram import Client
import os, io, time
from requests import get

## the telegram app
class tgsend:
	'''Send via tg to the channel'''
	def __init__(self, dataframe, df_type) -> None:
		'''Create Pyrogram app'''
		self.app = Client("WBHUAPP", 
			api_id=os.environ.get('TG_API_ID'), 
			api_hash=os.environ.get('TG_API_HASH'),
			bot_token = os.environ.get('TG_BOT_TOKEN'))
		self.tg_channel_id = os.environ.get('TG_CHANNEL_ID')
		self.df = dataframe
		self.dftype = df_type
	
	def create_caption(self, dfiloc):
		'''Creates caption from single df iloc'''
		x=dfiloc
		if self.dftype == 'notice':
			caption = x['Description']
			caption += f''' [Source]({x['Link']}) '''
			caption += f' **#Notice @WBHealthU**'
			title = x['Title']
		elif self.dftype == 'go':
			# 'Title', 'Category', 'Branch'
			caption = x['Title']
			caption += f''' [Source]({x['Link']}) '''
			caption += f" #{x['Category'].replace(' ', '_')}"
			caption += f" #{x['Branch'].replace(' ', '_')}"
			caption += f' **#GO @WBHealthU**'
			title = x['Title']
		elif self.dftype == 'employment':
			# Subject	Details	Date	End Date Link
			caption = x['Details']
			caption += f''' [Source]({x['Link']}) '''
			caption += f''' upto {x['End Date']} '''
			caption += f' **#Recruitment @WBHealthU**'
			title = x['Subject']
		return caption, x['Link'], title
	
	def getfile(self, url):
		self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'}
		try:
			r = get(url=url, stream=True, headers=self.header)
			self.fblob = io.BytesIO(r.content)
		except Exception as e:
			print(f'Exception Raised {e}')
			retry_count = 0
			max_retries = 2  # number of retries
			while retry_count < max_retries:
				try:
					r = get(url=url, stream=True, headers=self.header)
					self.fblob = io.BytesIO(r.content)
				except Exception as e:
					print("Exception on Retry: {0}".format(e))
					retry_count = retry_count + 1
					time.sleep(3)
			raise ValueError('No idea')
		

	def main(self):
		'''Main message sender'''
		with self.app:
			for i in self.df.index:
				# print('caption create')
				caption, link, fname = self.create_caption(self.df.iloc[i])
				#download the pdf
				try:
					self.getfile(link)
					#send the pdf + add thumb
					self.app.send_document(chat_id=int(self.tg_channel_id), document=self.fblob, thumb='thumb.jpg',
					file_name='@WBHealthU - '+fname+'.pdf', caption=caption)

					print(i+1, '/', self.df.shape[0])
					time.sleep(2)
				except ValueError as e:
					print(f'{e} about: {link}')