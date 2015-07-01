import os
import sys
import llfuse
import errno


class Operations(llfuse.Operations):
	def __init__(self):
		super(Operations, self).__init__()

if __name__ == "__main__":
	mountpoint = sys.argv[1]
	operations = Operations()
	llfuse.init(operations, mountpoint, [])
	llfuse.main()
	llfuse.close()
