from pyrogram import Client
import os, io, tempfile, time
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
		
	def pdf_downloader(self, link):
		'''Downloads the PDF'''
		r = get(link, stream=True,
			headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'})
		with tempfile.NamedTemporaryFile(delete=False) as f:
			f.write(r.content)
			f.seek(0)
			return f.name
		# with open('tempxyz.file', 'wb') as f:
		# 	for chunk in r.iter_content(chunk_size=8192): 
		# 		# If you have chunk encoded response uncomment if
		# 		# and set chunk_size parameter to None.
		# 		#if chunk: 
		# 		f.write(chunk)

	def main(self):
		'''Main message sender'''
		with self.app:
			for i in self.df.index:
				# print('caption create')
				caption, link, fname = self.create_caption(self.df.iloc[i])
				# print(caption)
				#download the pdf
				fpath = self.pdf_downloader(link)
				# print('Downloaded')
				#send the pdf + add thumb
				self.app.send_document(chat_id=int(self.tg_channel_id), document=fpath, thumb='thumb.jpg',
				file_name='@WBHealthU - '+fname+'.pdf', caption=caption)
				# await self.app.send_message(chat_id=int(cid), text=caption)
				os.remove(fpath)
				print(i+1, '/', self.df.shape[0])
				time.sleep(2)