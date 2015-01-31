import collections
from hex2int import *

class Parser:
    def __init__(self):
        self.b = collections.deque(maxlen = 14)
        
    def lnd(self, nd):
        result = []
        for i in nd:
            self.b.append(i)
            if len(self.b) < 14:
                continue
            if sum([self.b[i] for i in range(12)]) % 65536 == self.b[13]*256 + self.b[12]:
                l = list(self.b);
                result.append(
                    (
                        (hex2int_2c(l[0:2]),   hex2int_2c(l[2:4]),   hex2int_2c(l[4:6])),
                        (hex2int_2c(l[6:8]),  hex2int_2c(l[8:10]), hex2int_2c(l[10:12]))
                    )
                )
        return result
