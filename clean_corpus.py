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
				i = 0
				for elem in result:
					i += 1
					try:
						os.makedirs(clean_path + d + '/')
					except OSError:
						pass
					if len(result) > 1:
						f_clean = open(clean_path + d + '/' + str(filename).split('/')[-1].split('.')[0] + str(i) + '.txt', 'w')
					else:
						f_clean = open(clean_path + d + '/' + str(filename).split('/')[-1], 'w')
					f_clean.write(result)
					f_clean.fush()
					os.fsync(f_clean)
					f_clean.close()