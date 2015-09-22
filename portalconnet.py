import urllib,urllib2
import json
import random,hashlib
import time

#Change your id and password here.
username = '12125xxxx'
password = '**********'

url = 'http://p.nju.edu.cn/portal_io/'
url_logout = url+'logout'
url_login = url+'login'

def GetChallenge():
	url_getchallenge = url+'getchallenge'
	challenge_data = urllib2.urlopen(url_getchallenge).read()
	challenge = json.loads(challenge_data)['challenge']
	return challenge

def ChapPassword(password,challenge):
	id = random.randint(0,255)
	#print 'id='+str(id)
	strs = ''
	strs += unichr(id)
	strs += password
	i = 0
	length = len(challenge)
	while i < length:
		hex_tmp = challenge[i:i+2]
		dec_tmp = int(hex_tmp,16)
		strs += unichr(dec_tmp)
		i += 2
	hash = hashlib.md5(strs.encode('ISO-8859-1')).hexdigest()
	#print hash
	result = ''
	if id<16:
		result = '0'+hex(id)[2:]+hash
	else:
		result = ''+hex(id)[2:]+hash
	return result
	

challenge = GetChallenge()
chappassword = ChapPassword(password,challenge)
data = {}
data['username'] = username
data['password'] = chappassword
data['challenge'] = challenge

post_data = urllib.urlencode(data)

req_logout = urllib2.urlopen(url_logout)
time.sleep(2)
req_login = urllib2.urlopen(url_login, post_data)
