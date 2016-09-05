#!/usr/bin/python
"""
Wrapper of auth protocols
"""
import webbrowser
import json
import urllib
import appdirs
import os, os.path
import ConfigParser
import sys
import requests
import re
import datetime, time
from calendar import month_abbr

REDIRECTION_TYPE = 0
APP_NAME = "nikolayfs"

def nowTime(dateStr):
	"""
	Extract time from Epoch from date string
	"""
	mat = re.match(r"^..., (\d+) (\w+) (\d+) (\d+):(\d+):(\d+) ...$",\
		dateStr)
	return time.mktime(\
		datetime.datetime(\
			int(mat.group(3)),\
			list(month_abbr).index(mat.group(2)),\
			int(mat.group(1)),\
			int(mat.group(4)),\
			int(mat.group(5)),\
			int(mat.group(6))\
		).timetuple()\
		)

class Auth(object):
	"""
	Sufficienty collection of auth info
	"""
	confs = appdirs.user_data_dir(appname=APP_NAME)
	def __init__(self, creds, first=False):
		if not first and os.path.exists(self.confs):
			self.getData()
		else:
			credsFile = open(creds)
			credDict = json.load(credsFile)[u"installed"]
			credsFile.close()
			self.cid = credDict[u"client_id"]
			auri = credDict[u"auth_uri"]
			self.token_uri = credDict[u"token_uri"]
			self.secret = credDict[u"client_secret"]
			ruri = credDict[u"redirect_uris"]
			scopes = [u"https://www.googleapis.com/auth/drive", u"profile"]
			reqUri = auri + u"?" +\
				 urllib.urlencode(\
					{\
						u"scope" : u" ".join(scopes),\
						u"redirect_uri" : ruri[REDIRECTION_TYPE],\
						u"response_type" : u"code",\
						u"client_id" : self.cid\
					}\
				)
			webbrowser.open(reqUri)
			if not REDIRECTION_TYPE:
				sys.stdout.write(u"Type your auth code: ")
				code = unicode(sys.stdin.readline())
			else:
				#TODO: my little server
				pass
			response = requests.post(self.token_uri, data={\
					u"code" : code,\
					u"client_id" : self.cid,\
					u"client_secret" : self.secret,\
					u"redirect_uri" : ruri[REDIRECTION_TYPE],\
					u"grant_type" : u"authorization_code"\
				}\
				)
			ans = json.loads(response.text)
			self.expires = nowTime(response.headers[u"date"]) + ans[u"expires_in"]
			self.token = ans[u"access_token"]
			self.tokentype = ans[u"token_type"]
			self.rtoken = ans[u"refresh_token"]
			self.saveData()

	def check(self):
		"""
		check if access token is vaild and refresh it, if nessesary
		"""
		if time.mktime(time.gmtime()) + 5 < self.expires:
			return
		else:
			self.refresh()

	def refresh(self):
		"""
		refresh access token
		"""
		response = requests.post(self.token_uri, data={\
				u"client_id" : self.cid,\
				u"client_secret" : self.secret,\
				u"refresh_token" : self.rtoken,\
				u"grant_type" : u"refresh_token"\
			}\
			)
		ans = json.loads(response.text)
		self.expires = nowTime(response.headers[u"date"]) + ans[u"expires_in"]
		self.token = ans[u"access_token"]
		self.tokentype = ans[u"token_type"]
		self.saveData()

	def getData(self):
		"""
		get auth data from previous runs
		"""
		conf = open(self.confs)
		configer = ConfigParser.SafeConfigParser()
		configer.readfp(conf)
		for opt in configer.options(u"Main"):
			self.__setattr__(opt, configer.get(u"Main", opt))
		self.expires = float(self.expires)
		conf.close()

	def saveData(self):
		"""
		save data for next runs
		"""
		conf = open(self.confs, "w")
		configer = ConfigParser.SafeConfigParser()
		configer.add_section(u"Main")
		for key in self.__dict__.keys():
			configer.set(u"Main", key, unicode(self.__dict__[key]))
		configer.write(conf)
		conf.close()


if __name__ == "__main__":
	client = Auth(u"native.json", first = False)
	client.refresh()
