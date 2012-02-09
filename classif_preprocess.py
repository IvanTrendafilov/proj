## Prepare data for the classifier
import os
import glob
from clean_email import removeHeaders

def removeAllHeaders():
	dirs = ['atm_card', 'employment', 'next_of_kin', 'banking', 'fake_cheques', 'orphans', 'business', 'government', 'refugees', 'church_and_charity', 'loans', 'romance', 'commodities', 'lottery', 'western_union_and_moneygram', 'compensation', 'military', 'widow', 'delivery_company', 'misc', 'dying_people', 'mystery_shopper']
	for d in dirs:
		path = '/home/fusion/dev/419/' + d + '/'
		for filename in glob.glob(os.path.join(path, '*.txt')):
			f = open(filename, 'r')
			content = removeHeaders(f.read())
			f.close()
			f = open(filename, 'w')
			f.write(content)
			f.close()

def splitData():
		dirs = ['atm_card', 'employment', 'next_of_kin', 'banking', 'fake_cheques', 'orphans', 'business', 'government', 'refugees', 'church_and_charity', 'loans', 'romance', 'commodities', 'lottery', 'western_union_and_moneygram', 'compensation', 'military', 'widow', 'delivery_company', 'misc', 'dying_people', 'mystery_shopper']
		allTrainFiles = []
		allTestFiles = []
		for d in dirs:
			path = '/home/fusion/dev/419_train/' + d + '/'
			full_count =  len([name for name in os.listdir(path)])
			curr_count = 0 
			trainFilenames = []
			for filename in glob.glob(os.path.join(path, '*.txt')):
				curr_count += 1
				if curr_count <= 0.8 * float(full_count):
					trainFilenames.append(filename.split('/')[-1])
					allTrainFiles.append(filename.split('/')[-1])
				else:
					os.remove(filename)
			path = '/home/fusion/dev/419_test/' + d + '/'
			for filename in glob.glob(os.path.join(path, '*.txt')):
				if filename.split('/')[-1] in trainFilenames:
					os.remove(filename)
				else:
					allTestFiles.append(filename.split('/')[-1])
		return (allTrainFiles, allTestFiles)

def buildPropertyFile():
			dirs = ['atm_card', 'employment', 'next_of_kin', 'banking', 'fake_cheques', 'orphans', 'business', 'government', 'refugees', 'church_and_charity', 'loans', 'romance', 'commodities', 'lottery', 'western_union_and_moneygram', 'compensation', 'military', 'widow', 'delivery_company', 'misc', 'dying_people', 'mystery_shopper']
			total = ""
			for d in dirs:
				path = '/home/fusion/dev/419_train/' + d + '/'
				for filename in glob.glob(os.path.join(path, '*.txt')):
					content = open(filename).readlines()
					output = ""
					for line in content:
						output += line.strip() + ' '
					for l in output:
						if l.isalpha():
							total += d + '\t' + output + os.linesep
							break
			f = open('train.prop', 'w')
			f.write(total)
			total = ""
			for d in dirs:
				path = '/home/fusion/dev/419_test/' + d + '/'
				for filename in glob.glob(os.path.join(path, '*.txt')):
					content = open(filename).readlines()
					output = ""	
					for line in content:
						output += line.strip() + ' '
					for l in output:
						if l.isalpha():
							total += d + '\t' + output + os.linesep
							break
			f = open('test.prop', 'w')
			f.write(total)
			