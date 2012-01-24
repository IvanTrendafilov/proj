import os
import glob
from clean_email import *


def cleanCorpus():
	dirs = ['atm_card', 'employment', 'next_of_kin', 'banking', 'fake_cheques', 'orphans', 'business', 'government', 'refugees', 'church_and_charity', 'loans', 'romance', 'commodities', 'lottery', 'western_union_and_moneygram', 'compensation', 'military', 'widow', 'delivery_company', 'misc', 'dying_people', 'mystery_shopper']
	orig_path = '/tmp/corpus_dirty/'
	clean_path = '/tmp/corpus_clean/'
	count = 0
	for d in dirs:
		full_orig_path = orig_path + d + '/'
		for filename in glob.glob(os.path.join(full_orig_path, '*.txt')):
			count += 1
			print "Count: ", count
			rtext = open(filename, 'r').read()
			result = extractInfo(rtext)
			if result:
				try:
					os.makedirs(clean_path + d + '/')
				except OSError:
					pass
				f_clean = open(clean_path + d + '/' + str(filename).split('/')[-1], 'w')
				f_clean.write(result)
				f_clean.fush()
				os.fsync(f_clean)
				f_clean.close()









def buildFileDir():
	orig_path = os.environ['HOME'] + '/dev/proj/data/test/'
	path1 = os.environ['HOME'] + '/dev/proj/data/no-headers/'
	path2 = os.environ['HOME'] + '/dev/proj/data/with-headers/'
	count = 0
	for filename in glob.glob(os.path.join(orig_path, '*.txt')):
		count += 1
		print "Count:", count
		rtext = open(filename, 'r').read()
		result = prepareFileContent(rtext)
		if result:
			w_no_headers = open(path1 + str(filename).split('/')[-1], 'w')
			w_with_headers = open(path2 + str(filename).split('/')[-1], 'w')
			text_no_headers, text_with_headers = result[0], result[1]
			w_no_headers.write(text_no_headers)
			w_with_headers.write(text_with_headers)
			w_no_headers.flush()
			w_with_headers.flush()
			os.fsync(w_no_headers)
			os.fsync(w_with_headers)
			w_no_headers.close()
			w_with_headers.close()
	print "Done."
	return







	path = os.environ['HOME'] + '/dev/proj/data/test/'
	valid = []
	invalid = []
	try:
		dict_read = open(os.environ['HOME'] + '/dev/proj/data/headers.txt', 'r')
		for line in dict_read:
			if line not in valid:
				valid.append(line)
	except IOError:
		pass
	dictionary = open(os.environ['HOME'] + '/dev/proj/data/headers.txt', 'a')
	count = 0
	for filename in glob.glob(os.path.join(path, '*.txt')):
		count += 1
		print "count:", count
		print "current file is:", filename
		text = open(filename, 'r').read()
		headers = cleanHeader_heuristic(text)
		for candidate in headers:
			cand = candidate.split(':')[0] + ':'
			if cand not in valid and cand not in invalid:
				asking = True
				while asking:
					print cand
					resp = raw_input('Is this a header?')
					if resp.lower() == 'y':
						asking = False
						valid.append(cand)
						dictionary.write(cand + os.linesep)
						dictionary.flush()
						os.fsync(dictionary)
					elif resp.lower() == 'n':
						asking = False
						invalid.append(cand)
					elif resp.lower() == 'q':
						asking = False
						print "Quitting & saving"
	print "Done."
	return
