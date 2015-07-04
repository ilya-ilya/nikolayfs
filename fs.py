"""
Main module that use fuse to provide filesystem
"""
import os
import sys
import llfuse
import errno
import auth
import requests
import json

FILES = "https://www.googleapis.com/drive/v2/files/"


def timeRFC3339(dateStr):
	"""
	Extract time from Epoch from date string
	"""
	mat = re.match(r"^(\d+)-(\d+)-$",\
		dateStr)
	return time.mktime(\
		datetime.datetime(\
			int(mat.group(1)),\
			int(mat.group(2)),\
			int(mat.group(3)),\
			int(mat.group(4)),\
			int(mat.group(5)),\
			int(mat.group(6))\
		).timetuple()\
		)


def id2inode(sid):
	"""
	convert google id to inode number
	"""
	if sid == u"root":
		return 1
	else:
		inode = 0
		for e in sid:
			inode *= 128
			inode += ord(e)
		return inode

def inode2id(inode):
	"""
	convert inode number to google id
	"""
	if inode == 1:
		return u"root"
	else:
		sid = ""
		while inode > 0:
			sid += chr(inode % 128)
			inode /= 128
		return sid[::-1]


class Operations(llfuse.Operations):
	"""
	Redirector (Broker) of system calls to google
	"""
	def __init__(self, first = False):
		super(Operations, self).__init__()
		self.auth = auth.Auth(u"native.json", first)

	def getattr(self, inode):
		self.auth.check()
		sid = inode2id(inode)
		response = requests.get(FILES + sid, headers = {\
				u"Authorization" : "%s %s" % (self.auth.tokentype, self.auth.token)\
			})
		print response.text
		meta = json.loads(response.text)
		entry = llfuse.EntryAttributes()
		entry.st_ino = inode
		entry.generation = 0
		#TODO:modes
		entry.st_mode = 0440
		if meta[u"editable"]:
			entry.st_mode += 0200
		entry.st_nlink = 1
		entry.st_uid = os.getuid()
		entry.st_gid = os.getgid()
		entry.st_rdev = 0
		entry.st_size = meta.get(u"fileSize", 0)
		entry.st_blksize = 512
		entry.st_blocks = 1
		#entry.st_atime = timeRFC3339(meta.get(u"lastViewedByMeDate"))
		entry.st_atime = 0
		entry.st_ctime = 0
		entry.st_mtime = 0
		entry.attr_timeout = 300
		entry.entry_timeout = 300
		return entry


if __name__ == "__main__":
	mountpoint = sys.argv[1]
	first = False
	if len(sys.argv) > 2:
		first = True
	operations = Operations(first = first)
	llfuse.init(operations, mountpoint, [])
	llfuse.main()
	llfuse.close()
