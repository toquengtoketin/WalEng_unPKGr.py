#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#: Title	: walleng_unpkgr
#: Date		: Wednesday, 31 January 2018
#: Author	: "bpato" & "toki"
#: Version	:
#: Description	:
#-----------------------------------------------------------------------

import sys
from os import path, makedirs

def get_bin2data_Int(data, byteorder, sig):
	return int.from_bytes(data, byteorder, signed=sig)

def get_bin2data_Str(data):
	s = ("{}").format(data.decode('utf8'))
	try:
		s = s.rstrip("\x00")
		s = s.rstrip(" ")
	except:
		pass
	return s

def read_file(pathfile):
	info = {}
	files = []
	with open(pathfile, 'rb') as f:
		info["ROOT"] = get_bin2data_Str(f.read(get_bin2data_Int(f.read(4),"little",False)))
		info["NUMFILES"] = get_bin2data_Int(f.read(4),"little",False)
		info["FILES"] = []
		files = info["FILES"]
		for i in range(info["NUMFILES"]):
			files.append([])
			files[i].append(get_bin2data_Str(f.read(get_bin2data_Int(f.read(4),"little",False))))
			files[i].append(get_bin2data_Int(f.read(4), "little", False))
			files[i].append((get_bin2data_Int(f.read(4), "little", False)))
		info['OFFSET'] = f.tell()
	return info

def make_tree(info):

	ROOT = info["ROOT"]

	if not path.exists(ROOT):
		makedirs(ROOT)
		for f in info["FILES"]:
			if path.dirname(f[0]):
				d = "{}/{}".format(ROOT,path.dirname(f[0]))
				if not path.exists(d):
					makedirs(d)
			else:
				continue

def extract_files(info, pathfile):
	ROOT = info["ROOT"]
	files = info["FILES"]
	for f in files:
		archive = "{}/{}".format(ROOT,f[0])
		if not path.isfile(archive):
			offset = info['OFFSET'] + f[1]
			length = f[2]
			with open(pathfile, 'rb') as f:
				f.seek(offset)
				binData = f.read(length)
			with open(archive, 'wb') as f:
				f.write(binData)

def main(pathfile):
	if not path.isfile(pathfile):
		sys.exit()
	
	info = read_file(pathfile)
	make_tree(info)
	extract_files(info, pathfile)
	
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("number of wrong arguments")
        sys.exit()

    main(sys.argv[1])
