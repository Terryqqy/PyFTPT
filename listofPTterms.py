import numpy as np
import sympy as sym
import sys
import itertools
import math
import copy
#Ii-Il can't be set to as positive True and real True because:
#when substitue Im with fm, it will do like Im = sqrt(Im**2)replacement
Ii = sym.symbols('Ii')
Ij = sym.symbols('Ij')
Ik = sym.symbols('Ik')
Il = sym.symbols('Il')
wi = sym.symbols('wi',positive=True,real=True)
wj = sym.symbols('wj',positive=True,real=True)
wk = sym.symbols('wk',positive=True,real=True)
wl = sym.symbols('wl',positive=True,real=True)
wp = sym.symbols('wp',positive=True,real=True)
fi = sym.symbols('fi')
fj = sym.symbols('fj')
fk = sym.symbols('fk')
fl = sym.symbols('fl')
fp = sym.symbols('fp')
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
#data structure class of the algebraic expressions.
class ListofPTterms:
    def __init__(self,diff,fc,expression):
        self.operatorlst = [Qi,Qj,Qk,Ql]
        self.freqlst = [wi,wj,wk,wl]
        self.qtnumberlst = [Ii,Ij,Ik,Il]
        self.BEfactorlst = [fi,fj,fk,fl]
        self.diffsymlst = [D0,D1,D2,D3,D4,D4n,D3n,D2n,D1n]
        #we will have only one diff for each data sturcutre class, even at second step we merge two terms with reverse sign diff, after merging, they all have same diff.
        self.diff = diff
        #operator for each term, at second steps, two terms with reverse sign diff should have same operator list, otherwise, report error
        self.fclst = [fc]
        #expressions for each operator list
        self.explst = [expression]

    #XXX leave the part with pairing scheme first it is kind of messy and tricky. 
    #like iijj is only with iijj ijij ijji three unique set.
    def prefactor(self):
        for i in range(len(self.fclst_filter)):
            if (len(self.fclst_filter[i]) == 6):
                #self.explst_fm_filter[i] *= sym.Rational(1,math.factorial(3)**2)
                #XXX we use sorted fc instead as in our papers and xvscf paper
                self.explst_fm_filter[i] *= self.prefactnum(self.fclst_filter[i])
                #scale the force constants
                self.explst_fm_filter[i] *= 8*sym.sqrt(self.freqlst[0]**self.fclst_filter[i][0]*self.freqlst[1]**self.fclst_filter[i][1]*self.freqlst[2]**self.fclst_filter[i][2]*self.freqlst[0]**self.fclst_filter[i][3]*self.freqlst[1]**self.fclst_filter[i][4]*self.freqlst[2]**self.fclst_filter[i][5])
                self.explst_fm_filter[i] = sym.simplify(self.explst_fm_filter[i])
            elif (len(self.fclst_filter[i]) == 8):
                #self.explst_fm_filter[i] *= sym.Rational(1,math.factorial(4)**2)
                self.explst_fm_filter[i] *= self.prefactnum(self.fclst_filter[i])
                #scale the force constants
                self.explst_fm_filter[i] *= 16*sym.sqrt(self.freqlst[0]**self.fclst_filter[i][0]*self.freqlst[1]**self.fclst_filter[i][1]*self.freqlst[2]**self.fclst_filter[i][2]*self.freqlst[3]**self.fclst_filter[i][3]*self.freqlst[0]**self.fclst_filter[i][4]*self.freqlst[1]**self.fclst_filter[i][5]*self.freqlst[2]**self.fclst_filter[i][6]*self.freqlst[3]**self.fclst_filter[i][7])
                self.explst_fm_filter[i] = sym.simplify(self.explst_fm_filter[i])

    def prefactnum(self,fcipt):
        # we use the product of the number to determine the combination:
        #like [2,1,1,0]for fcipt, product = 2, would multiply forthchart[2]
        prefret = 1
        thirdchart = [0,sym.Rational(1,6),sym.Rational(1,2),sym.Rational(1,6)]
        forthchart = [sym.Rational(1,8),sym.Rational(1,24),sym.Rational(1,4),sym.Rational(1,6),sym.Rational(1,24)]
        if(len(fcipt)==6):
            product = 1
            for i in range(3):
               if(fcipt[i]!=0):
                   product*=fcipt[i]
            prefret *= thirdchart[product]
            product = 1
            for i in range(3,6):
               if(fcipt[i]!=0):
                   product*=fcipt[i]
            prefret *= thirdchart[product]
        if(len(fcipt)==8):
            product = 1
            count=0
            for i in range(4):
               if(fcipt[i]!=0):
                   count+=1
                   product*=fcipt[i]
            if(product==4 and count==2):
                product=0
            prefret *= forthchart[product]
            product = 1
            count=0
            for i in range(4,8):
               if(fcipt[i]!=0):
                   count+=1
                   product*=fcipt[i]
            if(product==4 and count==2):
                product=0
            prefret *= forthchart[product]
        return prefret
            


    def mergesamediff(self,PTterms):
        fclst = PTterms.fclst
        explst = PTterms.explst
        diff = PTterms.diff
        #check diff
        if (self.diff == diff):
            print("same diff merging running")
            self.fclst = self.fclst + fclst
            self.explst = self.explst + explst
        else:
            sys.exit("first merge need two terms with same diff")

    def diffexp(self,iptlst):
        #iptlst is (1,0,-1) -> -wi+wk D1 is -1*wi
        diffexpreturn = 0
        for i in range(len(iptlst)):
            diffexpreturn -= iptlst[i]*self.freqlst[i]
        return diffexpreturn

    def mergereversediff(self,PTterms):
        fclst_sd = PTterms.fclst_samediff
        explst_sd = PTterms.explst_samediff
        self.explst_revers = []
        diff = PTterms.diff
        if (np.array_equal(np.array(self.diff),-1*np.array(diff))):
            print("reverse diff merging running")
            for i in range(len(fclst_sd)):
                if(np.array_equal(np.array(fclst_sd[i]),np.array(self.fclst_samediff[i]))):
                    #Here: we introduce the denomenator
                    self.explst_revers.append(self.explst_samediff[i]/self.diffexp(self.diff)+explst_sd[i]/self.diffexp(diff))
        else:
            sys.exit("second merge need two terms with reverse diff")

    #substitute Im with fm 
    def subsIm_fm(self,thermAverules):
        leng =len(self.explst_revers)
        self.explst_fm = [0]*leng
        #expand first:
        for i in range(leng):
            self.explst_fm[i] = sym.expand(sym.expand(self.explst_revers[i]).subs(thermAverules))



    #iterate through the fc and exp list to obtain <Phi|V|Phi>**2 only for second order now, probably generalize to third order in the future.
    def iterate_samediff(self):
        self.fclst_samediff = []
        self.explst_samediff = []
        for i in range(len(self.fclst)):
            #don't need to recount the former one  so start with i
            for j in range(i,len(self.fclst)):
                self.fclst_samediff.append(self.fclst[i]+self.fclst[j])
                self.explst_samediff.append(sym.simplify(self.explst[i]*self.explst[j]))

    def fclst_Qform(self,lstipt):
        leng = len(lstipt)
        fcprintlst = [0]*leng
        if (leng<=4):
            for j in range(leng):
                #here fclst[i] is (1,0,2) like, so would be QiQk**2
                fcprintlst[j] =self.operatorlst[j]**lstipt[j]
        else:
            #this is specifically for 3rd and 4th (max) order force constants, so I used this trick
            for j in range(leng):
                #here fclst_samediff[i] is (1,0,2,2,0,1) like, so would be QiQk**2 Qi**2 Qk
                fcprintlst[j] =self.operatorlst[int(j%(leng/2))]**lstipt[j]

        return fcprintlst
    #go over the terms, and if the term has the same expression after switch the unnecesry index, then kill it.
    def filteroutovrlap(self,unnecesry):
        if (len(unnecesry)>1): 
            allswitch = list(itertools.combinations(unnecesry,2))
            self.fclst_filter = []
            self.explst_fm_filter = []
            for i in range(len(self.fclst_samediff)):
                if (len(self.explst_fm_filter)== 0):
                    self.explst_fm_filter.append(self.explst_fm[i])
                    self.fclst_filter.append(self.fclst_samediff[i])
                else:
                    judge = 0
                    for j in range(len(self.explst_fm_filter)):
                        #play switching
                        tempexp1 = self.explst_fm_filter[j]#the one already appended
                        tempexp2 = self.explst_fm[i]#the one want to be appended
                        for eachgp in allswitch:
                            #switch each group of indexes.
                            #one term switch eachgp[0] and eachgp[1],only take care of fm and wm
                            temp1 = tempexp1.subs({self.BEfactorlst[eachgp[0]]:fp,self.freqlst[eachgp[0]]:wp})
                            temp2 = temp1.subs({self.BEfactorlst[eachgp[1]]:self.BEfactorlst[eachgp[0]],self.freqlst[eachgp[1]]:self.freqlst[eachgp[0]]})
                            temp3 = temp2.subs({fp:self.BEfactorlst[eachgp[1]],wp:self.freqlst[eachgp[1]]})
                            if(temp3.equals(tempexp2)):
                                break
                                judge = 1
                        if(judge != 0):
                            break
                    if (judge == 0):
                        self.explst_fm_filter.append(self.explst_fm[i])
                        self.fclst_filter.append(self.fclst_samediff[i])
        else:
            self.fclst_filter = copy.deepcopy(self.fclst_samediff) 
            self.explst_fm_filter =copy.deepcopy(self.explst_fm)


    def printout(self,whichstage):
        print("++++++++++++++++++++++++++++++")
        print("The diff is ",self.diff," ",[self.diffsymlst[x] for x in self.diff])
        print("each of corresponding terms")
        if(whichstage==0):
            for i in range(len(self.fclst)):
                fcprintlst = self.fclst_Qform(self.fclst[i])
                print("The fc is ",self.fclst[i]," ",fcprintlst)
                print("The expression is", self.explst[i]) 
                print("---------------")
        #print the term after first merge of same diff. 
        if(whichstage==1):
            for i in range(len(self.fclst_samediff)):
                fcprintlst = self.fclst_Qform(self.fclst_samediff[i])
                print("The fc is", self.fclst_samediff[i], " ",fcprintlst)
                print("The expression is", self.explst_samediff[i]) 
        #print the term after Im fm substitution.
        if (whichstage == 2):
            for i in range(len(self.fclst_samediff)):
                fcprintlst = self.fclst_Qform(self.fclst_samediff[i])
                print("The fc is", self.fclst_samediff[i], " ",fcprintlst)
                print("The revers expression is", self.explst_revers[i]) 
                print("The subs expression is", self.explst_fm[i]) 
        if (whichstage == 3):
            for i in range(len(self.fclst_filter)):
                fcprintlst = self.fclst_Qform(self.fclst_filter[i])
                print("The fc is", self.fclst_filter[i], " ",fcprintlst)
                print("The final expression is", sym.together(self.explst_fm_filter[i]))
                #print("Latex is",sym.latex(self.explst_fm_filter[i]))





    





