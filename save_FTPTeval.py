import sympy as sym
import itertools
import sys
import numpy as np
sys.path.append(".")
from listofPTterms import ListofPTterms

Ii = sym.symbols('Ii')
Ij = sym.symbols('Ij')
Ik = sym.symbols('Ik')
Il = sym.symbols('Il')
wi = sym.symbols('wi')
wj = sym.symbols('wj')
wk = sym.symbols('wk')
wl = sym.symbols('wl')
fi = sym.symbols('fi')
fj = sym.symbols('fj')
fk = sym.symbols('fk')
fl = sym.symbols('fl')
Qi = sym.symbols('Qi')
Qj = sym.symbols('Qj')
Qk = sym.symbols('Qk')
Ql = sym.symbols('Ql')
D0 = sym.symbols('D0')
D1 = sym.symbols('D1')
D2 = sym.symbols('D2')
D3 = sym.symbols('D3')
D4 = sym.symbols('D4')
D1n = sym.symbols('D1n')
D2n = sym.symbols('D2n')
D3n = sym.symbols('D3n')
D4n = sym.symbols('D4n')

class ThermalAvg:
    def __init__(self):
        #operator combinations 
        self.fc3rd_origin,self.fc4th_origin = self.fcoperator()
        #difference combinations
        self.diff3rd_origin,self.diff4th_orgin = self.diffgen()
        #list of each symbols
        self.operatorlst = [Qi,Qj,Qk,Ql]
        self.freqlst = [wi,wj,wk,wl]
        self.qtnumberlst = [Ii,Ij,Ik,Il]
        self.BEfactorlst = [fi,fj,fk,fl]
        #D1 is : <..Ii..|V|..Ji..> Ji-Ii = 1 with denomenator of (-wi)
        self.diffsymlst = [D0,D1,D2,D3,D4,D4n,D3n,D2n,D1n]
        #two rules for substituding
        self.thermAverules = self.thermAvgeval()#return a list of dict
        self.BornHuangrules = self.BHruleeval()#return a list of dict
        #start with one mode excited wave function
        self.onemodewvfn()


    def onemodewvfn(self):
        #the one mode exicted wave function thermal average means two things:
        #1, the operator group should have non-zero first element. 
        #following this rule we need to calculate the pairing scheme afterwards cause we leave out the equavalent terms here.
        #2, the difference group should have non-zero first element and zero rest elements.
        #need to specify the unnecessary index here.
        unnecesry = [1,2]
        fc3rd1mode = []
        diff3rd1mode = []
        #do 3rd first
        for i in range(len(self.fc3rd_origin)):
            if (self.fc3rd_origin[i][0] != 0):
                fc3rd1mode.append(self.fc3rd_origin[i])
        for i in range(len(self.diff3rd_origin)):
            if (self.diff3rd_origin[i][0]!=0 and self.diff3rd_origin[i][1]==0 and self.diff3rd_origin[i][2]==0):
                diff3rd1mode.append(self.diff3rd_origin[i])
        #do it
        numorder = 3
        lstofPTterms = []
        for i in range(len(diff3rd1mode)):
            for j in range(len(fc3rd1mode)):
                valueofeachmode = 1
                for modeidx in range(numorder):
                    tempvalue = self.Dx_Qm(diff3rd1mode[i],fc3rd1mode[j],modeidx)
                    tempvalue2 = self.BornHuangrules[tempvalue] #instead of using sym.subs I use dictionary replacement directly because it is faster and no other case will be left out
                    valueofeachmode *= tempvalue2
                    if (tempvalue2 == 0 ):
                        valueofeachmode = 0
                        break
                if (valueofeachmode != 0):
                    #for each new expression for diff and operator, fill in the same one if find one, otherwise add a new one.
                    if (len(lstofPTterms)!=0):
                        judge = 0
                        for lstidx in range(len(lstofPTterms)):
                            if (np.array_equal(np.array(lstofPTterms[lstidx].diff ),np.array(diff3rd1mode[i]))):
                                    lstofPTterms[lstidx].mergesamediff(ListofPTterms(diff3rd1mode[i],fc3rd1mode[j],valueofeachmode))
                                    judge += 1
                        if (not judge):
                            lstofPTterms.append(ListofPTterms(diff3rd1mode[i],fc3rd1mode[j],valueofeachmode))
                    else:
                        lstofPTterms.append(ListofPTterms(diff3rd1mode[i],fc3rd1mode[j],valueofeachmode))
        #  merge those with same diff in the same class, and iterate between them and obtain <Phi|V|Phi>**2
        for each in lstofPTterms:
            each.iterate_samediff()
        # merge again those with reverse sign in the diff in the same class, this is the last step for merging
        lstofPTterms_revers = []
        for i in range(len(lstofPTterms)):
            if (len(lstofPTterms_revers) ==0):
                lstofPTterms_revers.append(lstofPTterms[i])
            else:
                judge = 0
                for j in range(len(lstofPTterms_revers)):
                    if(np.array_equal(np.array(lstofPTterms[i].diff),-1*np.array(lstofPTterms_revers[j].diff))):
                        judge +=1
                        lstofPTterms_revers[j].mergereversediff(lstofPTterms[i])
                if (judge ==0):
                    lstofPTterms_revers.append(lstofPTterms[i])
                #checking 
                if (judge >1):
                    sys.exit("There shouldn't be more than one reverse merge for the same term")
        #4, substitute Im with fm.
        for i in range(len(lstofPTterms_revers)):
            lstofPTterms_revers[i].subsIm_fm(self.thermAverules)
        #5, for each class with same diff, we need to filter out those terms equivalent algebraicly,like Qijj Qijj and  Qikk Qikk, the rule to do that is switching the unnecessary index like for one mode wave fn, k and l is the unnecessary one.
        for i in range(len(lstofPTterms_revers)):
            lstofPTterms_revers[i].filteroutovrlap(unnecesry)

        for each in lstofPTterms_revers:
            each.printout(3)

        #5, do pairing scheme calculation for each term in each classes.
        #6, output each term with same diff(same class) in the latex style.

    #helper function to evaluate the Dx_Qm expression by substituting 
    def Dx_Qm(self,diff,fc,modeidx):
        eachDxQm = self.diffsymlst[diff[modeidx]]*self.operatorlst[modeidx]**fc[modeidx]
        return eachDxQm

    #rules for substituting Im with fm
    def thermAvghelper(self,Qm,Im,fm):
        tempdict = {Im**4:24*fm**4+36*fm**3+14*fm**2+fm,Im**3:fm*(6*fm**2+6*fm+1),Im**2:fm*(fm+2),Im:fm}
        return tempdict
    
    def thermAvgeval(self):
        #Im -> fm
        lstofthermalAvg ={} 
        for i in range(len(self.operatorlst)):
            lstofthermalAvg.update(self.thermAvghelper(self.operatorlst[i],self.qtnumberlst[i],self.BEfactorlst[i]))
        return lstofthermalAvg

    #rules for substituting Dx_Qm with Im and wm
    def BHrulehelper(self,Qm,Im,wm):
        tempdict = {D0*Qm:0,D0*Qm**2:(Im+sym.Rational(1,2))/wm,D0*Qm**3:0,D0*Qm**4:(6*Im*(Im+1)+3)/wm/wm*sym.Rational(1,4),
                    D1*Qm:sym.sqrt((Im+1)/wm*sym.Rational(1,2)),D1*Qm**2:0,D1*Qm**3:3*((Im+1)/wm*sym.Rational(1,2))**sym.Rational(3,2),D1*Qm**4:0,
                    D2*Qm:0,D2*Qm**2:sym.sqrt((Im+2)*(Im+1))/wm*sym.Rational(1,2),D2*Qm**3:0,D2*Qm**4:(Im+sym.Rational(3,2))*sym.sqrt((Im+2)*(Im+1))/wm/wm,
                    D3*Qm:0,D3*Qm**2:0,D3*Qm**3:sym.sqrt((Im+3)*(Im+2)*(Im+1))*(sym.Rational(1,2)/wm)**sym.Rational(3,2),D3*Qm**4:0,
                    D4*Qm:0,D4*Qm**2:0,D4*Qm**3:0,D4*Qm**4:sym.sqrt((Im+4)*(Im+3)*(Im+2)*(Im+1))/wm/wm*sym.Rational(1,4),
                    D1n*Qm:sym.sqrt(Im/wm*sym.Rational(1,2)),D1n*Qm**2:0,D1n*Qm**3:3*(Im/wm*sym.Rational(1,2))**sym.Rational(3,2),D1n*Qm**4:0,
                    D2n*Qm:0,D2n*Qm**2:sym.sqrt(Im*(Im-1))/wm*sym.Rational(1,2),D2n*Qm**3:0,D2n*Qm**4:(Im-sym.Rational(1,2))*sym.sqrt(Im*(Im-1))/wm/wm,
                    D3n*Qm:0,D3n*Qm**2:0,D3n*Qm**3:sym.sqrt(Im*(Im-1)*(Im-2))*(sym.Rational(1,2)/wm)**sym.Rational(3,2),D3n*Qm**4:0,
                    D4n*Qm:0,D4n*Qm**2:0,D4n*Qm**3:0,D4n*Qm**4:sym.sqrt(Im*(Im-1)*(Im-2)*(Im-3))/wm/wm*sym.Rational(1,4)}
        return tempdict

    def BHruleeval(self):
        #Dx*Qm**y - > Im
        dictofBHdict ={} 
        for i in range(len(self.operatorlst)):
            dictofBHdict.update(self.BHrulehelper(self.operatorlst[i],self.qtnumberlst[i],self.freqlst[i]))
        dictofBHdict.update({D0:1,D1:0,D2:0,D3:0,D4:0,D1n:0,D2n:0,D3n:0,D4n:0})
        return dictofBHdict


    def diffgen(self):
        difflst = [0,1,2,3,4,-4,-3,-2,-1]
        iterdiff3rd = list(itertools.product(difflst,repeat=3))
        iterdiff4th = list(itertools.product(difflst,repeat=4))
        return iterdiff3rd,iterdiff4th

    def fcoperator(self):
        #|1 0 2> for QiQk**2 the number is the multiplicity of each mode
        lst3rd = [0,1,2,3]
        iter3rdtemp = list(itertools.product(lst3rd,repeat=3))
        iter3rd = []
        #filter out those with sum = 3
        for i in range(len(iter3rdtemp)):
            if (sum(list(iter3rdtemp[i])) == 3):
                iter3rd.append(iter3rdtemp[i])
        #same with 4th:
        lst4th = [0,1,2,3,4]
        iter4thtemp = list(itertools.product(lst4th,repeat=4))
        iter4th = []
        #filter out those with sum = 3
        for i in range(len(iter4thtemp)):
            if (sum(list(iter4thtemp[i])) == 4):
                iter4th.append(iter4thtemp[i])
        return iter3rd,iter4th



test = ThermalAvg()
