import os, glob
def cleanHeaders(text):
	msg_lines = text.splitlines()
	headers = []
	for line in msg_lines:
		foundAlpha = False
		for i in range(0, len(line)):
			char = line[i]
			if char.isalpha() and not foundAlpha:
				foundAlpha = True
				if char.isupper():
					count = 0
					while True:
						count += 1
						try:
							if line[i + count].isalpha() or line[i + count] == '-':
								pass
							elif line[i + count] == ':':
								if line[i + count + 1] == " ":
									headers.append(line)
									break
									# this is def.
							else:
								break
						except:
							break
	return headers

def buildHeaderDB():
	path = '/home/fusion/dev/proj/data/test/' 
	valid = []
	invalid = []
	dictionary = open('headers.txt','a')
	for filename in glob.glob( os.path.join(path, '*.txt') ):
		print "current file is: " + filename
		text = open(filename, 'r').read()
		headers = cleanHeaders(text)
		for candidate in headers:
			if candidate not in valid and candidate not in invalid:
				asking = True
				while asking:
					resp = raw_input('Is this a header?')
					if resp.lower() == 'y':
						asking = False
						valid.append(candidate)
						dictionary.write(candidate)
						dictionary.flush()
						os.fsync()
					elif resp.lower() == 'n':
						asking = False
						invalid.append(candidate)
					elif resp.lower() == 'q':
						asking = False
						print "Quitting & saving"
		print "DONEEEE!!!!"
		return 