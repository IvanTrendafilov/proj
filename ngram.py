import random
from StringIO import StringIO
class Trigram:
    """Compute similarity scores between trigrams
        >>> reference_en = Trigram('string to use')
        >>> unknown = Trigram('file://pointing/to/unknown/text')
    """
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
            # \n's are spurious in a prose context
            for letter in line.strip() + ' ':
                d = self.lut.setdefault(pair, {})
                d[letter] = d.get(letter, 0) + 1
                pair = pair[1] + letter
        f.close()
        self.measure()


    def measure(self):
        """calculates the scalar length of the trigram vector and
        stores it in self.length."""
        total = 0
        for y in self.lut.values():
            total += sum([ x * x for x in y.values() ])
        self.length = total ** 0.5

    def similarity(self, other):
        """returns a number between 0 and 1 indicating similarity.
        1 means an identical ratio of trigrams;
        0 means no trigrams in common.
        """
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
        """indicates difference between trigram sets; 1 is entirely
        different, 0 is entirely the same."""
        return 1 - self.similarity(other)


