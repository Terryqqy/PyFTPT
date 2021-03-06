import sympy as sym
import itertools
import sys
import numpy as np
sys.path.append(".")
from listofPTterms import ListofPTterms
import csv
from collections import OrderedDict

Ii = sym.symbols('Ii')
Ij = sym.symbols('Ij')
Ik = sym.symbols('Ik')
Il = sym.symbols('Il')
wi = sym.symbols('wi',positive=True,real=True)
wj = sym.symbols('wj',positive=True,real=True)
wk = sym.symbols('wk',positive=True,real=True)
wl = sym.symbols('wl',positive=True,real=True)
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
        self.diff3rd_origin,self.diff4th_origin = self.diffgen()
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
        #self.onemodewvfn()
        #self.twomodewvfn()
        #self.threemodewvfn()
        #self.fourmodewvfn()
        self.individualtest()

        #this is the test running for draft
        #temp = self.BornHuangrules[D1*Qi**1]
        #tempa = self.BornHuangrules[D1*Qi**3]
        #print(sym.expand(temp*tempa))
        ##temp1 = sym.together(sym.expand(temp**2).subs(self.thermAverules))
        #temp1 = sym.together(sym.expand(temp*tempa).subs(self.thermAverules))
        #(num,den) = sym.fraction(temp1)
        #temp2 = sym.latex(sym.expand(num)/den)
        #temp2 = temp2.replace('fi','f_i')
        
        #temp2 = temp2.replace('wi','\omega_i')
        #print(temp2)
    def individualtest(self):
        testni = sym.expand(self.BornHuangrules[D2n*Qi**2]*self.BornHuangrules[D2n*Qi**4])
        testnj = sym.expand(self.BornHuangrules[D2n*Qi**4])
        #XXX for the squared term like (2n+1)**2 you need to expand first then sub
        #middle = sym.together(sym.expand(testni**2))
        #print(sym.together(sym.expand(testni**2)))
        #print(testt.subs(self.thermAverules))
        #print(sym.together(self.subs(testni*testnj)))
        #print(sym.together(self.subs(testni**2)))
        print(sym.together(self.subs(testni)))
        #testfi = sym.expand(sym.together(testni.subs(self.thermAverules)))
        #print(testfi)

    def subs(self,symipt):
        ret = sym.expand(sym.together(symipt.subs(self.thermAverules[0])))
        ret = sym.expand(sym.together(ret.subs(self.thermAverules[1])))
        ret = sym.expand(sym.together(ret.subs(self.thermAverules[2])))
        ret = sym.expand(sym.together(ret.subs(self.thermAverules[3])))
        return ret


    def fourmodewvfn(self):
        #the four mode exicted wave function :
        #one, the operator with non-zero 1st 2nd 3rd 4th terms because it is orthogonal
        #two, the difference have non-zero 1st 2nd 3rd 4th terms and zero rest
        unnecesry = []
        fc4th4mode = []
        diff4th4mode = []
        #1, get the diff and fc list under each condition, do 4th
        for i in range(len(self.fc4th_origin)):
            if (self.fc4th_origin[i][0] != 0 and self.fc4th_origin[i][1] !=0 and self.fc4th_origin[i][2] !=0 and self.fc4th_origin[i][3] !=0):
                fc4th4mode.append(self.fc4th_origin[i])
        for i in range(len(self.diff4th_origin)):
            if (self.diff4th_origin[i][0]!=0 and self.diff4th_origin[i][1]!=0 and self.diff4th_origin[i][2] !=0 and self.diff4th_origin[i][3]!=0):
                diff4th4mode.append(self.diff4th_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_4th =self.step2_8(unnecesry,diff4th4mode,fc4th4mode)
        self.write_csv('fourmode_latex.csv',lstofPTterms_4th,lstofPTterms_4th)
        #self.write_csv_mathform('four_math.csv',lstofPTterms_4th,lstofPTterms_4th)

    def threemodewvfn(self):
        #the three mode exicted wave function :
        #one, the operator with non-zero 1st 2nd 3rd terms because it is orthogonal
        #two, the difference have non-zero 1st 2nd 3rd terms and zero rest
        unnecesry = []
        fc3rd3mode = []
        diff3rd3mode = []
        #1, get the diff and fc list under each condition, do 3rd first
        for i in range(len(self.fc3rd_origin)):
            if (self.fc3rd_origin[i][0] != 0 and self.fc3rd_origin[i][1] !=0 and self.fc3rd_origin[i][2] !=0):
                fc3rd3mode.append(self.fc3rd_origin[i])
        for i in range(len(self.diff3rd_origin)):
            if (self.diff3rd_origin[i][0]!=0 and self.diff3rd_origin[i][1]!=0 and self.diff3rd_origin[i][2] !=0):
                diff3rd3mode.append(self.diff3rd_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_3rd =self.step2_8(unnecesry,diff3rd3mode,fc3rd3mode)
        unnecesry = [3]
        fc4th3mode = []
        diff4th3mode = []
        #1, get the diff and fc list under each condition, do 4th
        for i in range(len(self.fc4th_origin)):
            if (self.fc4th_origin[i][0] != 0 and self.fc4th_origin[i][1] !=0 and self.fc4th_origin[i][2] !=0):
                fc4th3mode.append(self.fc4th_origin[i])
        for i in range(len(self.diff4th_origin)):
            if (self.diff4th_origin[i][0]!=0 and self.diff4th_origin[i][1]!=0 and self.diff4th_origin[i][2] !=0 and self.diff4th_origin[i][3] == 0):
                diff4th3mode.append(self.diff4th_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_4th =self.step2_8(unnecesry,diff4th3mode,fc4th3mode)
        self.write_csv('threemode_latex.csv',lstofPTterms_3rd,lstofPTterms_4th)
        #self.write_csv_mathform('three_math.csv',lstofPTterms_3rd,lstofPTterms_4th)

    def twomodewvfn(self):
        #the two mode exicted wave function :
        #one, the operator with non-zero 1st 2nd terms because it is orthogonal
        #two, the difference have non-zero 1st 2nd terms and zero rest 
        unnecesry = [2]
        fc3rd2mode = []
        diff3rd2mode = []
        #1, get the diff and fc list under each condition, do 3rd first
        for i in range(len(self.fc3rd_origin)):
            if (self.fc3rd_origin[i][0] != 0 and self.fc3rd_origin[i][1] !=0):
                fc3rd2mode.append(self.fc3rd_origin[i])
        for i in range(len(self.diff3rd_origin)):
            if (self.diff3rd_origin[i][0]!=0 and self.diff3rd_origin[i][1]!=0 and self.diff3rd_origin[i][2]==0):
                diff3rd2mode.append(self.diff3rd_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_3rd = self.step2_8(unnecesry,diff3rd2mode,fc3rd2mode)
        #4th
        unnecesry = [0,1,2,3]
        fc4th2mode = []
        diff4th2mode = []
        #1, get the diff and fc list under each condition, do 4th 
        for i in range(len(self.fc4th_origin)):
            if (self.fc4th_origin[i][0] != 0 and self.fc4th_origin[i][1] !=0):
                fc4th2mode.append(self.fc4th_origin[i])
        for i in range(len(self.diff4th_origin)):
            if (self.diff4th_origin[i][0]!=0 and self.diff4th_origin[i][1]!=0 and self.diff4th_origin[i][2]==0 and self.diff4th_origin[i][3]==0):
                diff4th2mode.append(self.diff4th_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_4th = self.step2_8(unnecesry,diff4th2mode,fc4th2mode)
        self.write_csv('twomode_latex.csv',lstofPTterms_3rd,lstofPTterms_4th)
        #self.write_csv_mathform('two_math.csv',lstofPTterms_3rd,lstofPTterms_4th)

    def onemodewvfn(self):
        #the one mode exicted wave function thermal average means two things:
        #One, the operator group should have non-zero first element. 
        #following this rule we need to calculate the pairing scheme afterwards cause we leave out the equavalent terms here.
        #Two, the difference group should have non-zero first element and zero rest elements.
        #need to specify the unnecessary index here.
        unnecesry = [1,2]
        fc3rd1mode = []
        diff3rd1mode = []
        #1, get the diff and fc list under each condition, do 3rd first
        for i in range(len(self.fc3rd_origin)):
            if (self.fc3rd_origin[i][0] != 0):
                fc3rd1mode.append(self.fc3rd_origin[i])
        for i in range(len(self.diff3rd_origin)):
            if (self.diff3rd_origin[i][0]!=0 and self.diff3rd_origin[i][1]==0 and self.diff3rd_origin[i][2]==0):
                diff3rd1mode.append(self.diff3rd_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_3rd = self.step2_8(unnecesry,diff3rd1mode,fc3rd1mode)
        #4th order
        unnecesry = [1,2,3]
        fc4th1mode = []
        diff4th1mode = []
        for i in range(len(self.fc4th_origin)):
            if (self.fc4th_origin[i][0] != 0):
                fc4th1mode.append(self.fc4th_origin[i])
        for i in range(len(self.diff4th_origin)):
            if (self.diff4th_origin[i][0]!=0 and self.diff4th_origin[i][1]==0 and self.diff4th_origin[i][2]==0 and self.diff4th_origin[i][3]==0) :
                diff4th1mode.append(self.diff4th_origin[i])
        #generalized function for the step 2-8
        lstofPTterms_4th = self.step2_8(unnecesry,diff4th1mode,fc4th1mode)
        self.write_csv('onemode_latex.csv',lstofPTterms_3rd,lstofPTterms_4th)
        #self.write_csv_mathform('one_math_updateprefactor.csv',lstofPTterms_3rd,lstofPTterms_4th)


    def step2_8(self,unnecesry,diffiptlst,fciptlst):
        #2, evaluate each term by Born huang rules and do first merge for terms with same diff
        lstofPTterms = self.evalBH_firstmerge(diffiptlst,fciptlst)
        #3,  merge those with same diff in the same class, and iterate between them and obtain <Phi|V|Phi>**2
        for each in lstofPTterms:
            each.iterate_samediff()
        #4, merge again those with reverse sign in the diff in the same class, this is the last step for merging
        lstofPTterms_revers = self.reversMerge(lstofPTterms)
        #5, substitute Im with fm.
        for i in range(len(lstofPTterms_revers)):
            lstofPTterms_revers[i].subsIm_fm(self.thermAverules)
        #6, for each class with same diff, we need to filter out those terms equivalent algebraicly,like Qijj Qijj and  Qikk Qikk, the rule to do that is switching the unnecessary index like for one mode wave fn, k and l is the unnecessary one. 
        #XXX Need to update to between classes (different diff), we need to check if we switch the index, the expressions will be the same, then kill one.
        for i in range(len(lstofPTterms_revers)):
            lstofPTterms_revers[i].filteroutovrlap(unnecesry)
        #XXX 7, do pre-factor calculation(pairing scheme) calculation for each term in each classes. Didn't have that in this code, since I prefer to mannully to verify each one.
        for i in range(len(lstofPTterms_revers)):
            lstofPTterms_revers[i].prefactor()
        #XXX we write the latex form in this printout at "3"
        for each in lstofPTterms_revers:
            each.printout(3)
        return lstofPTterms_revers

        #8, output each term with same diff(same class) in the latex style.

    def reversMerge(self,lstofPTterms):
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
        return lstofPTterms_revers

    def evalBH_firstmerge(self,diffipt,fcipt):
        lstofPTterms = []
        numorder= len(diffipt[0])
        #here we evaluate all the combinations by Born-huang rules.
        for i in range(len(diffipt)):
            for j in range(len(fcipt)):
                valueofeachmode = 1
                for modeidx in range(numorder):
                    tempvalue = self.Dx_Qm(diffipt[i],fcipt[j],modeidx)
                    tempvalue2 = self.BornHuangrules[tempvalue] #instead of using sym.subs I use dictionary replacement directly because it is faster and no other case will be left out
                    valueofeachmode *= tempvalue2
                    if (tempvalue2 == 0 ):
                        valueofeachmode = 0
                        break
                #First merge:for each new expression for diff and operator, fill in the same one if find one, otherwise add a new one.
                if (valueofeachmode != 0):
                    if (len(lstofPTterms)!=0):
                        judge = 0
                        for lstidx in range(len(lstofPTterms)):
                            if (np.array_equal(np.array(lstofPTterms[lstidx].diff ),np.array(diffipt[i]))):
                                    lstofPTterms[lstidx].mergesamediff(ListofPTterms(diffipt[i],fcipt[j],valueofeachmode))
                                    judge += 1
                        if (not judge):
                            lstofPTterms.append(ListofPTterms(diffipt[i],fcipt[j],valueofeachmode))
                    else:
                        lstofPTterms.append(ListofPTterms(diffipt[i],fcipt[j],valueofeachmode))
        return lstofPTterms

    #helper function to evaluate the Dx_Qm expression by substituting 
    def Dx_Qm(self,diff,fc,modeidx):
        eachDxQm = self.diffsymlst[diff[modeidx]]*self.operatorlst[modeidx]**fc[modeidx]
        return eachDxQm

    #rules for substituting Im with fm
    def thermAvghelper(self,lst,Im,fm):
        nopt =4 #order of operator Qi**4 Qi**3 Qi**2 Qi**1
        lst[0][Im**4]= 24*fm**4+36*fm**3+14*fm**2+fm
        lst[1][Im**3] = 6*fm**3+6*fm**2+fm
        lst[2][Im**2] = 2*fm**2 + fm
        lst[3][Im] = fm
        #tempdict = {Im**4:24*fm**4+36*fm**3+14*fm**2+fm,Im**3:fm*(6*fm**2+6*fm+1),Im**2:fm*(2*fm+1),Im:fm}
    
    def thermAvgeval(self):
        #Im -> fm
        lst = [{},{},{},{}]
        for i in range(len(self.operatorlst)):
            self.thermAvghelper(lst,self.qtnumberlst[i],self.BEfactorlst[i])
        return lst

    #rules for substituting Dx_Qm with Im and wm
    #XXX warning: this is reverse version of paper's table: D1 = D1n in paper
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
        #pick those with sum = 3
        for i in range(len(iter3rdtemp)):
            if (sum(list(iter3rdtemp[i])) == 3):
                iter3rd.append(iter3rdtemp[i])
        #same with 4th:
        lst4th = [0,1,2,3,4]
        iter4thtemp = list(itertools.product(lst4th,repeat=4))
        iter4th = []
        #pick those with sum = 4
        for i in range(len(iter4thtemp)):
            if (sum(list(iter4thtemp[i])) == 4):
                iter4th.append(iter4thtemp[i])
        return iter3rd,iter4th

    def write_csv(self,namefile,lstofPTterms_3rd,lstofPTterms_4th):
        with open(namefile,'w') as csvfile:
            wrtr = csv.writer(csvfile,delimiter=' ')
            outputlist = []
            judge = 0
            indx = ['i','j','k','l']
            for i in range(len(lstofPTterms_3rd)):
                #deal with the latex form and add extra symbol for table
                eachPT = lstofPTterms_3rd[i]
                for j in range(len(eachPT.explst_fm_filter)):
                    temp = sym.latex(sym.together(eachPT.explst_fm_filter[j]))
                    fctemp = eachPT.fclst_filter[j]
                    firstpart = r'\tilde{F}_{'+indx[0]*fctemp[0]+indx[1]*fctemp[1]+indx[2]*fctemp[2]+r'}'
                    secondpart =r'\tilde{F}_{'+indx[0]*fctemp[3]+indx[1]*fctemp[4]+indx[2]*fctemp[5]+r'}'
                    if (firstpart == secondpart):
                        temp = firstpart+r'^2'+temp
                    else:
                        temp = firstpart+secondpart+temp
                    if (judge == 0):
                        temp = '$'+temp+r'$ &Eq&' 
                    elif (judge == 1):
                        temp = '$'+temp+r'$ &Eq \\' 
                    temp = temp.replace('fi','f_i')
                    temp = temp.replace('fj','f_j')
                    temp = temp.replace('fk','f_k')
                    temp = temp.replace('fl','f_l')
                    temp = temp.replace('w','\omega_')
                    judge +=1
                    judge = judge%2
                    outputlist.append(temp)
            wrtr.writerow(outputlist)
            outputlist = []
            judge = 0
            indx = ['i','j','k','l']
            for i in range(len(lstofPTterms_4th)):
                #deal with the latex form and add extra symbol for table
                eachPT = lstofPTterms_4th[i]
                for j in range(len(eachPT.explst_fm_filter)):
                    temp = sym.latex(sym.together(eachPT.explst_fm_filter[j]))
                    fctemp = eachPT.fclst_filter[j]
                    firstpart =r'\tilde{F}_{'+indx[0]*fctemp[0]+indx[1]*fctemp[1]+indx[2]*fctemp[2]+indx[3]*fctemp[3] +r'}'
                    secondpart =r'\tilde{F}_{'+ indx[0]*fctemp[4]+indx[1]*fctemp[5]+indx[2]*fctemp[6]+indx[3]*fctemp[7]+r'}'
                    if (firstpart == secondpart):
                        temp = firstpart+r'^2'+temp
                    else:
                        temp = firstpart+secondpart+temp
                    if (judge == 0):
                        temp = '$'+temp+r'$ &Eq&' 
                    elif (judge == 1):
                        temp = '$'+temp+r'$ &Eq \\' 
                    temp = temp.replace('fi','f_i')
                    temp = temp.replace('fj','f_j')
                    temp = temp.replace('fk','f_k')
                    temp = temp.replace('fl','f_l')
                    temp = temp.replace('w','\omega_')
                    judge +=1
                    judge = judge%2
                    outputlist.append(temp)
            wrtr.writerow(outputlist)

    #this is to numerically verify the algebraic expressions
    def write_csv_mathform(self,namefile,lstofPTterms_3rd,lstofPTterms_4th):
        with open(namefile,'w') as csvfile:
            wrtr = csv.writer(csvfile,delimiter=' ')
            outputlist = []
            judge = 0
            indx = ['i','j','k','l']
            for i in range(len(lstofPTterms_3rd)):
                #deal with the latex form and add extra symbol for table
                eachPT = lstofPTterms_3rd[i]
                for j in range(len(eachPT.explst_fm_filter)):
                    temp = str(sym.together(eachPT.explst_fm_filter[j]))
                    fctemp = eachPT.fclst_filter[j]
                    firstpart = r'FCQ3['+indx[0]*fctemp[0]+indx[1]*fctemp[1]+indx[2]*fctemp[2]+r']'
                    secondpart =r'FCQ3['+indx[0]*fctemp[3]+indx[1]*fctemp[4]+indx[2]*fctemp[5]+r']'
                    if (firstpart == secondpart):
                        temp = firstpart+r'**2'+'*'+temp
                    else:
                        temp = firstpart+'*'+secondpart+'*'+temp
                    outputlist.append(temp)
            wrtr.writerow(outputlist)
            outputlist = []
            judge = 0
            indx = ['i','j','k','l']
            for i in range(len(lstofPTterms_4th)):
                #deal with the latex form and add extra symbol for table
                eachPT = lstofPTterms_4th[i]
                for j in range(len(eachPT.explst_fm_filter)):
                    temp = str(sym.together(eachPT.explst_fm_filter[j]))
                    fctemp = eachPT.fclst_filter[j]
                    firstpart =r'FCQ4['+indx[0]*fctemp[0]+indx[1]*fctemp[1]+indx[2]*fctemp[2]+indx[3]*fctemp[3] +r']'
                    secondpart =r'FCQ4['+ indx[0]*fctemp[4]+indx[1]*fctemp[5]+indx[2]*fctemp[6]+indx[3]*fctemp[7]+r']'
                    if (firstpart == secondpart):
                        temp = firstpart+r'**2'+'*'+temp
                    else:
                        temp = firstpart+'*'+secondpart+'*'+temp
                    outputlist.append(temp)
            wrtr.writerow(outputlist)

        



test = ThermalAvg()
