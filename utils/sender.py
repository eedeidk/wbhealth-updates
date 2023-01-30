from pyrogram import Client
import os, io
from requests import get

## the telegram app
class tgsend:
	'''Send via tg to the channel'''
	def __init__(self, dataframe, df_type) -> None:
		'''Create Pyrogram app'''
		self.app = Client("kriti_bot", 
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
			caption += f' #Notice **@WBHealthU**'
		elif self.dftype == 'go':
			# 'Title', 'Category', 'Branch'
			caption = x['Title']
			caption += f''' [Source]({x['Link']}) '''
			caption += f" #{x['Category']}"
			caption += f" #{x['Branch']}"
			caption += f' #GO **@WBHealthU**'
		elif self.dftype == 'career':
			# Not ready yet
			caption += f' #Recruitment **@WBHealthU**'
		return caption, x['Link'], x['Title']
		
	def pdf_downloader(self, link):
		'''Downloads the PDF'''
		fileobj = get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'}).content
		# Create BytesIO object
		fobj = io.BytesIO(fileobj)
		return fobj

	async def main(self):
		'''Main message sender'''
		await self.app.start()
		for i in self.df.index:
			caption, link, fname = self.create_caption(self.df.iloc[i])
			#download the pdf
			fobj = self.pdf_downloader(link)
			#send the pdf + add thumb
			await self.app.send_document(chat_id=os.environ.get('TG_CHANNEL_ID') ,document=fobj,
			file_name='@WBHealthU - '+fname+'.pdf', caption=caption, parse_mode='MARKDOWN')
			print(i, '/', self.df.shape[0])
		await self.app.stop()