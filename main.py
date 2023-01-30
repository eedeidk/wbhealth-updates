import os, asyncio
urls = ['https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/career']

url_dict ={
	'notice': 'https://www.wbhealth.gov.in/pages/notice',
	'go':'https://www.wbhealth.gov.in/pages/gov_order'
	}

from utils import parser, sender

# iteration
for k in url_dict.keys():
	url = url_dict[k]
	df_main = parser.Parser(url).main()
	##extra parse
	df_processed = parser.OptionalParser(k, df_main).main()
	# print(df_processed)
	if not df_processed.empty:
		print(df_processed.shape[0])
		TgSend = sender.tgsend(df_processed, df_type=k)
		asyncio.run(TgSend.main())
	else:
		print(k, 'No updates today')
