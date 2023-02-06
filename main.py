url_dict ={
	# 'notice': 'https://www.wbhealth.gov.in/pages/notice',
	# 'go':'https://www.wbhealth.gov.in/pages/gov_order',
	'employment' : 'https://www.wbhealth.gov.in/pages/career'
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
		print(df_processed.shape[0], 'updates on #',k)
		sender.tgsend(df_processed, df_type=k).main()
	else:
		print('No updates today on #',k)
