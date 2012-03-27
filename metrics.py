from __future__ import division
from main import init
import os
a, b = init()
count, sum, sum2, bounce = 0,0,0,0
for i in b:
	if len(b[i]['Messages']) > 2:
		sum2 += len(b[i]['Messages'])
		count += 1
	if b[i]['State'] == 'CLOSED':
		bounce += 1
	sum += len(b[i]['Messages'])

print "Avg. thread length, inclusive of all", sum / len(b)
print "Avg. thread length for exist. emails:", sum / (len(b) - bounce)
print "Avg. thread length for ans. msg:", sum2 / count
print "Max thread length:", max([len(b[x]['Messages']) for x in b])
print "Bounce rate:", (bounce - 1) / len(b) # -1 for the test message
print "Participation rate:", count / (len(b) - bounce)
print "Sample size:", len(b)
print "All classes:", len(filter(lambda x: 'CRAWLER' in x, os.listdir('incoming/')))
