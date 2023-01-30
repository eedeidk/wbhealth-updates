from bs4 import BeautifulSoup as bs
import requests, time

urls = ['https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/notice', 'https://www.wbhealth.gov.in/pages/career']

def create_session():
	'''Creaets session with a user-agent'''
	sess = requests.Session()
	UA = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:106.0) Gecko/20100101 Firefox/106.0'}
	sess.headers.update(UA)
	return sess

def get_page(url, sess):
	'''Fetches the url page using session'''
	response = sess.get(url)
	i=0
	if response.status_code == 200:
		return response
	else:
		i=i+1
		time.sleep(4)
		if not i>3:
			return get_page(url, sess)
		else:
			return None
		

