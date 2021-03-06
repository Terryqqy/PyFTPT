import sympy as sym
#the verification for diagrams in FT-XVH2
wi = sym.symbols('wi',positive=True,real=True)
wj = sym.symbols('wj',positive=True,real=True)
wk = sym.symbols('wk',positive=True,real=True)
wl = sym.symbols('wl',positive=True,real=True)
fi = sym.symbols('fi')
fj = sym.symbols('fj')
fk = sym.symbols('fk')
fl = sym.symbols('fl')
def pp(ipt):
    #print(sym.expand(sym.simplify(ipt),numer =True))
    print(sym.expand(sym.simplify(ipt),numer =True))
    #print(sym.expand(ipt))
    #print(sym.nsimplify(ipt))
    #print(ipt)

C1 =  - sym.Rational(1,6)*(fi*fj+fj*fk+fi*fk+fi+fj+fk+1)/(wi+wj+wk)
C2 =  sym.Rational(1,6)*(fi*fj+fj*fk-fi*fk+fj)/(wj-wi-wk)
C3 =  sym.Rational(1,6)*(fi*fj-fk*fj-fi*fk-fk)/(wj+wi-wk)
C4 =  sym.Rational(1,6)*(fk*fj-fi*fj-fi*fk-fi)/(wj-wi+wk)
diagram2C = C1+C2+C3+C4
Dia2A = -sym.Rational(1,4)*(2*fj+1)*(2*fk+1)/wi
subC1 = C1.subs({fk:fj,wk:wj})
subC2 = C2.subs({fk:fj,wk:wj})
subC3 = C3.subs({fk:fj,wk:wj})
subC4 = C4.subs({fk:fj,wk:wj})
sub2 = Dia2A.subs({fk:fj,wk:wj})
#-----------
#__________________1.03 
S03 = -(8*fj**2 + 8*fj + 1)/(4*wi) #S03
Diag = (3*C2+3*C3+Dia2A).subs({fk:fj,wk:wj}) #3 is from i=j j=k k=i
#pp(S03)
#pp(Diag)
#_________________2.01 2.02
D01 = -(fi + fj**2 + 2*fj*(fi + 1) + 1)/(2*(wi + 2*wj)) #D01
D02 = (2*fi*fj + fi - fj**2)/(2*(wi - 2*wj)) #D02 
Diag = (C1).subs({fk:fj,wk:wj})
#pp(D01)
#pp(Diag)# diagram of i =j j=k k = i so times3
#___________1.04 1.05
Diag1 = C1.subs({fj:fi,wj:wi,fk:fi,wk:wi})
Diag2 = C2.subs({fj:fi,wj:wi,fk:fi,wk:wi})
Diag3 = C3.subs({fj:fi,wj:wi,fk:fi,wk:wi})
Diag4 = C4.subs({fj:fi,wj:wi,fk:fi,wk:wi})
Diag5 = Dia2A.subs({fj:fi,wj:wi,fk:fi,wk:wi})
#pp(Diag1)
#pp(Diag2+Diag3+Diag4+Diag5)



#sub1 = diagram2C.subs({fk:fi,wk:wi,fj:fi,wj:wi})



D1 = -(fi*fk*(fj+fl+1)+fi*(fl+1)*(fj+1)-fk*fj*fl)/(-wi+wj+wk+wl)/24
D2 = -(fi*fl*(fk+fj+1)-fj*fk*(fi+fl+1))/(-wi+wj+wk-wl)/24
D3 = -(fl*fk*(fj+fi+1)+fl*(fi+1)*(fj+1)-fi*fj*fk)/(wi+wj+wk-wl)/24
D4 = -((fk+1)*(fi+1)*(fl+1)*(fj+1)-fi*fj*fk*fl)/(wi+wj+wk+wl)/24
D5 = -(fk*fl*(fj+fi+1)-fi*fj*(fl+fk+1))/(wi+wj-wk-wl)/24
D6 = -(fk*fj*(fi+fl+1)+fj*(fi+1)*(fl+1)-fi*fk*fl)/(wi-wj+wk+wl)/24
D7 = -(fi*fk*(fj+fl+1)-fj*fl*(fi+fk+1))/(-wi+wj-wk+wl)/24
D8 = -(fk*(fi+1)*(fj+1)*(fl+1)-fi*fj*fl*(fk+1))/(wi+wj-wk+wl)/24
diagram2B = -sym.Rational(1,8)*(2*fk+1)*(2*fl+1)*(wi*(2*fj+1)-wj*(2*fi+1))/(wi**2-wj**2)
diagram2B_1 = -sym.Rational(1,8)*(2*fk+1)*(2*fl+1)*(fi+sym.Rational(1,2))/wi
#________________degenerate______2B
#diag2B_dg = sym.Rational(1,8)*(2*fk+1)*(2*fl+1)*fi*(fi+1)
##pp(diag2B_dg)
#PT208 = (2*fi*fk+2*fi*fl+fi-2*fj*fk-2*fj*fl-fj+4*fk*fl*(fi-fj))/8#2.08
#PT204 = (2*fi*fj+2*fi*fl+fi-2*fj**2+4*fj*fl*(fi-fj)-2*fj*fl-fj)/8
#PT206 = (2*fi**2+4*fi*fj*(fi-fj)+fi-2*fj**2-fj)/8
#PT210 = (fi-fj+8*fl*(fi*fl+fi-fj*fl-fj))/48
#PT214 = (fi**2+2*fi*fj*(fi-fj)-fj**2)/48
#PT216 = (fi+6*fj*(fi*fj+fi-fj**2-fj)-fj)/16
##PT1 = PT208+PT204+PT206+PT210+PT214+PT216
##PT1 = PT1.subs({fj:fi})
#PT208 = PT208.subs({fj:fi})
#pp(PT208)
 
#_______________1.09 1.10
#PT1 = -(4*fi**3+6*fi**2+4*fi+1)/96/wi
#PT2 = -(32*fi**3+48*fi**2+22*fi+3)/48/wi
#sub1 = diagram2D.subs({fk:fi,wk:wi,fj:fi,wj:wi,fl:fi,wl:wi})
Diag4 = D4.subs({fk:fi,wk:wi,fj:fi,wj:wi,fl:fi,wl:wi})
Diagt = (D1+D3+D6+D8).subs({fk:fi,wk:wi,fj:fi,wj:wi,fl:fi,wl:wi})
sub2 = diagram2B_1.subs({fk:fi,fl:fi})
#pp(PT1+PT2)
#pp(Diagt+sub2)
#pp(Diag4)
#______________1.04  ___
#PT1 = -(16*fi*fj**2+16*fi*fj+2*fi+8*fj**2+8*fj+1)/16/wi
#D1 and D2 is 2wj 
diagram2D = (D6+D8)
sub1 = diagram2D.subs({fl:fi,wl:wi,fk:fj,wk:wj})
#pp(sub1)
sub2 = diagram2B_1.subs({fk:fj,fl:fj})
#pp(sub2)
#pp(6*sub1+sub2)
#________________________2.07 2.08 Bingo
#PT1 = -(2*fi*fk+2*fi*fl+fi+2*fj*fk+2*fj*fl+fj+4*fk*fl*(fi+fj+1)+2*fk+2*fl+1)/8/(wi+wj)
#PT2 = (2*fi*fk+2*fi*fl+fi-2*fj*fk-2*fj*fl-fj+4*fk*fl*(fi-fj))/8/(wi-wj)
#pp(sym.expand(sym.simplify(PT1+PT2),numer =True))
#test = -(2*fk+1)*(2*fl+1)*(wi*(2*fj+1)-wj*(2*fi+1))/8/(wi**2-wj**2)
#pp(sym.expand(test))
#_______________________2.03 2.04
PT1 = -(2*fi*fj+2*fi*fl+fi+2*fj**2+4*fj*fl*(fi+fj)+6*fj*fl+3*fj+2*fl+1)/8/(wi+wj)
PT2 = (2*fi*fj+2*fi*fl+fi-2*fj**2+4*fj*fl*(fi-fj)-2*fj*fl-fj)/8/(wi-wj)
diag2B = -(2*fk+1)*(2*fl+1)*(wi*(2*fj+1)-wj*(2*fi+1))/8/(wi**2-wj**2)
diag2B = diag2B.subs({fk:fj})
#pp(PT1+PT2)
#pp(diag2B)
#________________________2.05 2.06
PT1 = (2*fi**2*fj+fi**2+2*fi*fj**2+4*fi*fj+2*fi+fj**2+2*fj+1)/4/(wi+wj)
PT2 = (fi**2+2*fi*fj*(fi-fj)-fj**2)/4/(wi-wj)
diag2B = diag2B.subs({fl:fj,fk:fi})
#pp(PT1+PT2)
#pp(diag2B)
#____________1.06 1.07
#diag2B = -(2*fk+1)*(2*fl+1)*(fi+sym.Rational(1,2))/wi/8
#PT = - (8*fi*fk*fl+4*fi*fk+4*fi*fl+2*fi+4*fk*fl+2*fk+2*fl+1)/wi/16
#pp(sym.expand(diag2B))
#pp(sym.expand(PT))

#______________________1.04 iijj XXX wtf
diag2B= - sym.Rational(1,8)*(2*fk+1)**2*(fi+sym.Rational(1,2))/wi
diag2D_2 = - sym.Rational(1,24)*(D3+D8)
#diag2D_2 = diag2D_2.subs({fk:fi,fl:fj,wk:wi,wl:wj})
#diag2D = - sym.Rational(1,48)*(2*fj**2+2*fj)*(2*fi+1)/wi
diag = diag2B+diag2D_2
diag = diag.subs({fj:fi,wj:wi,fl:fk,wl:wk})
#pp(diag2B)
#pp(diag2D)
#pp(diag2D_2)
#pp(diag)
#________________________2.13 2.14 iijj Bingo
diag2D_2 = (D7)
diag2D_2 = diag2D_2.subs({fk:fi,fl:fj,wk:wi,wl:wj})
#pp(diag2D_2)

#______________________2.15 2.16 the 16 should be 8 i and j can switch. we times 2 here because k = i l = i and k = j l = j need to be counted 
diag2D_1 = (D3+D6+D8)
diag2D_2 = (D2+D5+D7)
diag2Btest = -(2*fk+1)*(2*fl+1)*(wi*(2*fj+1)-wj*(2*fi+1))/8/(wi**2-wj**2)
diag2D_2 = (2*diag2D_1+2*diag2D_2+diag2Btest).subs({fk:fj,fl:fj,wk:wj,wl:wj})
test1 = -(fi+12*fj**2+6*fj*(fi*fj+fi+fj**2)+7*fj+1)/4/(wi+wj)
test2 = (fi+6*fj*(fi*fj+fi-fj**2-fj)-fj)/4/(wi-wj)
pp(test2+test1)
pp(diag2D_2)
#_____________________2.11 Bingo ijjj
diag2D_2 = (D4)
#diag2D_2 = (D1)
diag2D_2 = (diag2D_2).subs({fk:fj,fl:fj,wk:wj,wl:wj})
#pp(diag2D_2)
#____________________2.02 2.10
PT1 = -(fi+fj+8*fl*(fi*fl+fi+fj*fl+fj+fl+1)+1)/8/(wi+wj)
PT2 = (fi-fj+8*fl*(fi*fl+fi-fj*fl-fj))/8/(wi-wj)
diag2D = (D2+D3+D8+D7)
diag2B = -sym.Rational(1,8)*(2*fk+1)*(2*fl+1)*(wi*(2*fj+1)-wj*(2*fi+1))/(wi**2-wj**2)
diag = (6*diag2D+diag2B).subs({fk:fl,wk:wl})
#diag = (diag2B).subs({fk:fl,wk:wl})
#pp(PT2+PT1)
#pp(diag)

#filter:
#pp(D1.subs({fk:fl,wk:wl}))
#pp(D2.subs({fk:fl,wk:wl}))
#pp(D3.subs({fk:fl,wk:wl}))
#pp(D4.subs({fk:fl,wk:wl}))
#pp(D5.subs({fk:fl,wk:wl}))
#pp(D6.subs({fk:fl,wk:wl}))
#pp(D7.subs({fk:fl,wk:wl}))
#pp(D8.subs({fk:fl,wk:wl}))

#_____________________4.01-4.08
#diag2D = -D2 #bingo
#diag2D = -D5 #bingo I got bug on this shit
#diag2D = -D7 #bingo
#diag2D = -D3 #bingo
#diag2D = -D6 #bingo
#diag2D = -D8 #bingo
#diag2D = -D4 #bingo
#diag2D = -D1 #bingo
#pp(diag2D)
#_________________1.04 



