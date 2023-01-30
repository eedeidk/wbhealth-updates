import os
urls = ['https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/career']
url1 = ['https://www.wbhealth.gov.in/pages/notice']

from utils import parser
df_main = parser.Parser(url1).main()

##extra parse
df_processed = parser.OptionalParser(0, df_main).main()
# print(df_processed)