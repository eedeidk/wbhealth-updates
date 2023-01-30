import os
urls = ['https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/career']
url1 = ['https://www.wbhealth.gov.in/pages/notice']

from utils import parser
df_main = parser.Parser(url1).main()