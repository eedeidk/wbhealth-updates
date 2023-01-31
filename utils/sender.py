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
		

	def main(self):
		'''Main message sender'''
		with self.app:
			for i in self.df.index:
				# print('caption create')
				caption, link, fname = self.create_caption(self.df.iloc[i])
				#download the pdf
				r = get(link, stream=True,
				headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'})
				fblob = io.BytesIO(r.content)
				#send the pdf + add thumb
				self.app.send_document(chat_id=int(self.tg_channel_id), document=fblob, thumb='thumb.jpg',
				file_name='@WBHealthU - '+fname+'.pdf', caption=caption)

				print(i+1, '/', self.df.shape[0])
				time.sleep(2)