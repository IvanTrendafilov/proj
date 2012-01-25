from StringIO import StringIO
class Trigram:
    # Compute similarity scores between trigrams
    length = 0

    def __init__(self, fn=None):
        self.lut = {}
        if fn is not None:
            self.parseFile(fn)

    def parseFile(self, fn):
        pair = '  '
	if 'file://' in fn:
	    f = open(fn[len('file://'):])
	else:
	    f = StringIO(fn)
        for z, line in enumerate(f):
            if not z % 1000:
                print "line %s" % z
            for letter in line.strip() + ' ':
                d = self.lut.setdefault(pair, {})
                d[letter] = d.get(letter, 0) + 1
                pair = pair[1] + letter
        f.close()
        self.measure()


    def measure(self):
        # calc the scalar length of the trigram vector and score it
        total = 0
        for y in self.lut.values():
            total += sum([ x * x for x in y.values()])
        self.length = total ** 0.5

    def similarity(self, other):
        # return similarity. 1- full, 0- nothing in common.

        if not isinstance(other, Trigram):
            raise TypeError("can't compare Trigram with non-Trigram")
        lut1 = self.lut
        lut2 = other.lut
        total = 0
        for k in lut1.keys():
            if k in lut2:
                a = lut1[k]
                b = lut2[k]
                for x in a:
                    if x in b:
                        total += a[x] * b[x]

        return float(total) / (self.length * other.length)

    def __sub__(self, other):
        return 1 - self.similarity(other)


