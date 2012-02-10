# Simple Python wrapper for Stanford Classifier
import os
import hashlib

class Pycla(object):
	def __init__(self):
		self.cmd = 'java -jar ../stanford-classifier/stanford-classifier.jar -loadClassifier 419classifier.ser.gz -testFile '

	def classify(self, text_list, classifname='classif.tmp'):  #  takes in a str or list of email text, with no headers.
		if type(text_list) is str:
			text_list = [text_list]
		output, allHashes = "", []
		for text in text_list:
			p_text = " ".join(text.splitlines())
			p_hash = hashlib.sha224(text).hexdigest()
			allHashes.append(p_hash)
			output += p_hash + '\t' + p_text + os.linesep
		f = open(classifname, 'w')
		f.write(output)
		f.flush()
		os.fsync(f)
		f.close()
		self.currentcmd = self.cmd + classifname
		output = os.popen(self.currentcmd, 'r')
		out = {}
		for line in output:
			try:
				if line.split('\t')[0] in allHashes:
					hashval, classval, prob = line.strip().split('\t')
					out[hashval] = (classval, prob)
			except:
				pass
		output.close()
		return out