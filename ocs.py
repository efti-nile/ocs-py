import numpy as np

class Ocs:  
    def __init__(self):
        self.L_MAX = 1000
        self.N_MAX = 100
        self.L_STEP = self.L_MAX // self.N_MAX
        self.L_BEG_STEP = self.L_STEP * 1
        self.BUF_SIZE = 5;
        self.t = -(2 * self.BUF_SIZE)
        self.p, self.pa, self.pm = 0, 0, 0
        self.v, self.va, self.vm = 0, 0, 0
        self.zt = 400;
        self.ct = 1200; # 1200 == 6 seconds
        self.ab = np.array([[0, 0, 0] for i in range(self.BUF_SIZE)])
        self.mb = np.array([[0, 0, 0] for i in range(self.BUF_SIZE)])
        self.mz = np.array([0,0,0])
        self.az = np.array([0,0,0])
        self.ctab = [];
        self.mt = 50
        self.mtp = 0.1
        self.pt = 10000
        self.ptp = 0.1
        self.door = None
        self.wci = False
        self.ci = False
        self.maxp = None
        self.slope = None
        
    def mp(self, m):
        p = None
        min = np.linalg.norm(self.ctab[0][1] - self.ctab[-1][1])
        for item in self.ctab:
            if min > np.linalg.norm(m - item[1]):
                min = np.linalg.norm(m - item[1])
                p = item[0]
        if min > self.mt:
            return None
        else:
            return p
         
    def smp(self):
        if self.maxp == None:
            max = 0
            for item in self.ctab:
                if max < abs(item[0]):
                    max = abs(item[0])
            self.maxp = max
        return self.maxp
            
    def pb(self, n):
        s = ''
        n = int(round(n * 50));
        if n < 0:
            n = 0
        if n > 50:
            n = 50
        for i in range(n - 1):
            s += ' '
        s += '#'
        for i in range(50 - n):
            s += ' '
        print(s)
        
        
            
    def lnd(self, data):
        for item in data:
            mm = 0
            self.t += 1;
            
            # convert new data in NumPy array
            m = np.array(item[0])
            a = np.array(item[1])
            
            # first execute running mean filter for both magnetometer and accelerometer
            self.ab = np.delete(self.ab, 0, 0)
            self.ab = np.append(self.ab, [a], 0)
            a = sum(self.ab) / self.BUF_SIZE
            
            self.mb = np.delete(self.mb, 0, 0)
            self.mb = np.append(self.mb, [m], 0)
            m = sum(self.mb) / self.BUF_SIZE
            
            if self.t == 0:
                print("zer. in progress")
            
            if 0 <= self.t < self.zt:
                self.mz += m
                self.az += a
                    
            if self.t == self.zt:
                self.mz /= self.zt
                self.az /= self.zt
                self.mo = self.mz
                print("magn. zero:", self.mz)
                print("acc. zero:", self.az)
                print("magn. cal. in progress...")
                      
            '''self.va = self.va + (a[2] - self.az[2])*0.1
            self.pa = self.pa + self.va*0.1
            
            if self.t % 10 == 0:
                print(self.pa)
            
            if self.t % 800 == 0:
                self.pa, self.va = 0, 0
                print('zero')'''
            
            if self.zt <= self.t < self.ct and not self.ci:
                self.va = self.va + (a[2] - self.az[2])
                self.pa = self.pa + self.va
                if np.linalg.norm(self.mo - m) > self.L_STEP:
                    self.ctab.append((self.pa, m))
                    self.mo = m
                if np.linalg.norm(self.mz - m) > self.L_BEG_STEP and not self.wci:
                    self.wci = True
                if np.linalg.norm(self.mz - m) < self.L_BEG_STEP * 0.8 and self.wci:
                    self.ci = True
                    print('interrupted')
                    
            if self.t == self.ct:
                self.va, self.pa = 0, 0
                self.pt = self.ptp * (max([item[0] for item in self.ctab]) - min([item[0] for item in self.ctab]))
                print("magn. cal. OK")
                self.ctab = self.ctab[0:len(self.ctab)//2]
                for item in self.ctab:
                    print(item)
            
            if self.t > self.ct:
                self.va = self.v + a[2]
                self.pa = self.p + self.va
                if self.mp(m) != None:
                    self.pm = self.mp(m)
                    k = 1 - np.linalg.norm(self.mb[0] - self.mb[-1]) / sum([np.linalg.norm(self.mb[i] - self.mb[i+1]) for i in range(self.BUF_SIZE - 1)])
                else:
                    k = 0
                op = self.p
                self.p = k*self.pm + (1 - k)*self.pa
                self.v = self.p - op
                self.door = (self.p > self.pt)
                if self.t % 50 == 0:
                    #print(k, self.v)
                    self.pb(abs(self.p)/self.smp())