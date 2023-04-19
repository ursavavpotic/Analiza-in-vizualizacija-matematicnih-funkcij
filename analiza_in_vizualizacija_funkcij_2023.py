from turtle import *
import math
from sympy import *
import re

polovicna_sirina = 7
polovicna_visina = 7
obseg_x = polovicna_sirina*100

#KOORDINATNI SISTEM:
def koordinatni_sistem(zelva, razdalja):
  polozaj = zelva.position()
  zelva.pendown()

  j = 0
  for i in range(0, razdalja):
    zelva.forward(1)
    zelva.dot(size=4)
    j += 1
    zelva.write(j)

  zelva.setposition(polozaj)

  j = 0
  for i in range(0, razdalja):
    zelva.backward(1)
    zelva.dot(size=4)
    j -= 1
    zelva.write(j)

  zelva.setposition(polozaj)


#FUNKCIJA:
def izrisF(z, zelva, obseg):
  for x in obseg:
    x = x / 100
    try:
      y = eval(z)
      zelva.goto(x, y)
      zelva.pendown() 
    except:
      zelva.penup()


#DELJENJE POLINOMOV: (+ razstavljanje v in iz seznama)
def razstavi_polinom(p):
    razstavljen_p= []
    nov_razstavljen_p= []
    prelom = "+", "-"
    vzorec = '|'.join('(?={})'.format(re.escape(pr)) for pr in prelom) 
    razstavljen_p = re.split(vzorec, p)
    if razstavljen_p[0] == '': 
        razstavljen_p.pop(0)

    if '**' in razstavljen_p[0] :
        prvi_element = razstavljen_p[0][::-1]
        vmes= prvi_element.split('**')
        prvi_eksponent =int(vmes[0])
    else:
        prvi_eksponent = 1

    eksponenti = []
    if len(razstavljen_p) != int(prvi_eksponent + 1):
        i = 0

        while i < len(razstavljen_p):
            a = razstavljen_p[i][::-1]

            if 'x' in a:
                if "**" in a:
                    vmesElement= a.split('**')
                    eksponent = int(vmesElement[0])
                    eksponenti.append(eksponent)
                else:
                    eksponent= 1
                    eksponenti.append(eksponent)
            else:
                eksponent = 0
                eksponenti.append(eksponent)
            
            razlika = (prvi_eksponent -i) - eksponent

            if i != 0:
                if razlika != 0:
                    nov_razstavljen_p.extend(['0' for j in range(razlika)]) 
                    nov_razstavljen_p.append(razstavljen_p[i])
                    for j in range (razlika):
                        razstavljen_p.insert(i, '0')
                    i += razlika

                else:
                    nov_razstavljen_p.append(razstavljen_p[i])
            else:
                nov_razstavljen_p.append(razstavljen_p[0])
            i += 1 
        zadnji_eksponent = eksponenti[-1]
        if zadnji_eksponent != 0:
            nov_razstavljen_p.extend(['0' for j in range(zadnji_eksponent)])
    else:
        nov_razstavljen_p = razstavljen_p

    #odstrani x-e:        
    for element in nov_razstavljen_p:
        if '*x' in nov_razstavljen_p[nov_razstavljen_p.index(element)]:
            nov_razstavljen_p[nov_razstavljen_p.index(element)] = element.split('*x')[0]
        elif 'x' in nov_razstavljen_p[nov_razstavljen_p.index(element)]:
            if '-' in nov_razstavljen_p[nov_razstavljen_p.index(element)]:
                nov_razstavljen_p[nov_razstavljen_p.index(element)] = '-1'
            else:
                nov_razstavljen_p[nov_razstavljen_p.index(element)] = '1'

    nov_razstavljen_p = [eval(element) for element in nov_razstavljen_p] 
    return nov_razstavljen_p

def sestavi_polinom(p):
    polinom = ""
    for i in range(len(p)):
        if p[i] == 0:
            polinom = polinom
        else:
            if i > 0 and p[i] > 0:
                polinom = polinom + " + "
            polinom = polinom + str(p[i])
            if len(p)-i-1 != 0:
                if len(p)-i-2 == 0:
                    polinom = polinom + "*x"
                else:
                    polinom = polinom + "*x**" + str(len(p)-i-1)
    return polinom

def deljenje(p1, p2, k):
    if len(p1) < len(p2):
        return k
    else:
        k.append(p1[0]/p2[0])
        vmes = []
        for i in range (len(p2)):
            vmes.append(k[-1]*p2[i])
        for i in range(len(vmes)):
            p1[i] = p1[i] - vmes[i]
        if int(p1[0]) == 0:
            p1.pop(0)
        deljenje(p1, p2, k)
    return k


#BISEKCIJA:
def bisekcija(z, a, b, niclerezultat, tol=1e-6, max_ponovitev=100):
    if f(a, z) * f(b, z) > 0:
        return None

    c = (a + b) / 2
    ponovitve = 0

    while abs(f(c, z)) > tol and ponovitve < max_ponovitev:
        if f(c, z) * f(a, z) < 0:
            b = c
        else:
            a = c
        c = (a + b) / 2
        ponovitve += 1

    if abs(f(c, z)) <= tol:
        nicla = round(c, 2)
        niclerezultat.append(nicla)
    else:
        pass

def f(x, z):
  try:
    return eval(z)
  except ZeroDivisionError:
    x1 = symbols('x')
    return limit(z, x1, x)


#INTEGRIRANJE:
def integralF(p):
  integriraniEksponenti = []
  for i in range(len(p), -1, -1):
      integriraniEksponenti.append(i)
  p.append(0)
  integriran_polinom = []
  for i in range(-1, len(p)):
      try:
          integriran_polinom.append(p[i]/integriraniEksponenti[i])
      except ZeroDivisionError:
          integriran_polinom.append(0)
  if integriran_polinom[0] == 0:
      integriran_polinom.pop(0)
  return integriran_polinom

def doloceni_integral(p, a, b):
  x = a
  y1 = eval(p)
  x = b
  y2 = eval(p)
  doloceniIntegral = round (y2 - y1, 2)
  return doloceniIntegral


#GUMBI:
def narisi_gumb(gumb, gumb_x, gumb_y, dolzinaG, tekst):
    gumb.pencolor('white')
    gumb.fillcolor('cornflower blue')
    gumb.penup()
    gumb.begin_fill()
    gumb.goto(gumb_x, gumb_y)
    gumb.goto(gumb_x + dolzinaG, gumb_y)
    gumb.goto(gumb_x + dolzinaG, gumb_y + sirinaG)
    gumb.goto(gumb_x, gumb_y + sirinaG)
    gumb.goto(gumb_x, gumb_y)
    gumb.end_fill()
    gumb.goto(gumb_x + 1/5, gumb_y + 1/7)
    gumb.write(tekst, font = ('Arial', 10, 'italic'))

#klik na gumbe:
stanjeAsimptote = ['predKlikom']
def asimptota(z, stanje, gumb, a, b, tekst):
  if ')/(' in z:
    y = z
    polinom1, polinom2 = y.split(')/(')
    polinom1 = polinom1.replace('(', '')
    polinom2 = polinom2.replace(')','')
    polinom1_razstavljen = razstavi_polinom(polinom1)
    polinom2_razstavljen = razstavi_polinom(polinom2)

    if len(polinom1_razstavljen) < len(polinom2_razstavljen):
      rezultat = 'y = 0'
    else:
      zdeljeno = deljenje(polinom1_razstavljen, polinom2_razstavljen, k = [])
      rezultat = 'y = ' + str(sestavi_polinom(zdeljeno))
  else:
    x = symbols('x')
    y = eval(z)
    limitavPlusN =limit(z, x, oo)
    limitavMinusN = limit(z, x, -oo)
    if limitavPlusN == -limitavMinusN :
      rezultat = 'ni asimptote'
    if limitavPlusN == limitavMinusN:
      if limitavPlusN == oo:
        rezultat = 'ni asimptote'
      else:
        rezultat = 'y = ' + str(limitavPlusN)
    if limitavPlusN != -limitavMinusN and limitavPlusN != limitavMinusN and (limitavPlusN == oo or limitavPlusN == -oo):
      rezultat = 'y = ' + str(limitavMinusN)
    if limitavPlusN != -limitavMinusN and limitavPlusN != limitavMinusN and (limitavMinusN == -oo or limitavMinusN == oo):
      rezultat = 'y = ' + str(limitavPlusN)
  klik(stanje, gumb, a, b, tekst, rezultat)


stanjePolov = ['predKlikom']
def poli(z,stanje, gumb, a, b, tekst, obseg):
  pred_rezultat = []
  for x in obseg:
    x = x / 100
    try:
      y = eval(z)
    except ValueError:
      pass
    except ZeroDivisionError:
      pred_rezultat.append(x)

  if pred_rezultat == []:
    rezultat = 'ni polov'
  else:
    rezultat = 'x = ' + str(pred_rezultat)
  klik(stanje, gumb, a, b, tekst, rezultat)


stanjeNicle = ['predKlikom']

def nicle(z, stanje, gumb, a, b, tekst, obseg):
  niclerezultat = []
  vrednostiF = []
  for x in obseg:
    vrednostiF.append(x)

  for i in range(len(vrednostiF)-1):
    x1 = vrednostiF[i]
    x2 = vrednostiF[i+1]
    bisekcija(z, x1, x2, niclerezultat)
  if len(niclerezultat) == 0:
    rezultat = 'ni ničel'
  else:
    rezultat = 'x ∈ ' + str(niclerezultat)
  klik(stanje, gumb, a, b, tekst, rezultat)


stanjeZacVr = ['predKlikom']
def zacetnaVrednost(z, stanje, gumb, a, b, tekst):
  try:
    x = 0
    rezultat = 'y = ' +str(eval(z))
  except ZeroDivisionError:
    rezultat = 'ni začetne vrednosti'
  klik(stanje, gumb, a, b, tekst, rezultat)


stanjeIntegral = ['predKlikom']
def integral(z, stanje, gumb, a, b, tekst, zacetek, konec):
  polinom = razstavi_polinom(z)
  integriran_p1 = sestavi_polinom(integralF(polinom))
  rezultat = doloceni_integral(integriran_p1, zacetek, konec)
  klik(stanje, gumb, a, b, tekst, rezultat)


stanjeNedoloceniInt = ['predKlikom']
def nedoloceniIntegral(z, stanje, gumb, a, b, tekst):
  polinom = razstavi_polinom(z)
  rezultat = sestavi_polinom(integralF(polinom))
  klik(stanje, gumb, a, b, tekst, rezultat)


def klik(stanje, gumb, a, b, tekst, rezultat):
  if stanje == ['predKlikom']:
    gumb.clear()
    gumb.pencolor('black')
    gumb.write(rezultat, font=('Arial', 10, 'bold'))
    stanje[0] = 'poKliku'
  else:
    gumb.clear()
    narisi_gumb(gumb, 4, a, b, tekst)
    stanje[0] = 'predKlikom'


def KlikNaGumb(x, y):
  if 4 <= x <= 4 + 3/2:
    if 6 <= y <= 6 + sirinaG:
      asimptota(z, stanjeAsimptote, asimptotaGumb, 6, 3/2, 'asimptota(y):')
  if 4 <= x <= 4 + 5/4:
    if 16/3 <= y <= 16/3 + sirinaG:
      poli(z, stanjePolov, polGumb, 16/3, 5/4, 'poli(x):', obseg1)
  if 4 <= x <= 4 + 5/4:
    if 14/3 <= y <= 14/3 + sirinaG:
      nicle(z,  stanjeNicle, nicleGumb, 14/3, 5/4, 'ničle:', obseg1)
  if 4 <= x <= 4 + 9/5:
    if 12/3 <= y <= 12/3 + sirinaG:
      zacetnaVrednost(z, stanjeZacVr, zacetVredGumb, 12/3, 9/5, 'začetna vrednost:')
  if 4 <= x <= 4 + 8/4:
    if 10/3 <= y <= 10/3 + sirinaG:
      nedoloceniIntegral(z, stanjeNedoloceniInt, nedoloceniIntGumb, 10/3, 8/4, 'nedoločeni integral:')
  if 4 <= x <= 4 + 7/4:
    if 8/3 <= y <= 8/3 + sirinaG:
      integral(z, stanjeIntegral, integralGumb, 8/3, 7/4, 'določeni integral:', -polovicna_sirina, polovicna_sirina)


#IZVAJANJE:

zaslon = Screen()
zaslon.title('Matematične funkcije')
zaslon.setworldcoordinates(-polovicna_sirina, -polovicna_visina, polovicna_sirina, polovicna_visina)
zaslon.tracer(4)

z = zaslon.textinput("vpiši funkcijo:", "y= ")

zelvica = Turtle(visible=False)
zelvica.speed(0)
zelvica.penup()
zelvica.pencolor('black')

funkcija = Turtle(visible=True)
funkcija.hideturtle()
funkcija.penup()
funkcija.pencolor('navy')
funkcija.goto(-5, 5)
funkcija.write("y = " + z, align='center', font = ('Arial', 13, 'italic'))

koordinatni_sistem(zelvica, polovicna_sirina)
zelvica.home()
zelvica.setheading(90)
koordinatni_sistem(zelvica, polovicna_visina)
zelvica.penup()

zelvica.pencolor('navy')
zelvica.goto(27/4, 1/5)
zelvica.write('x', font = ('Arial', 12, 'italic'))
zelvica.goto(1/5, 27/4)
zelvica.write('y', font = ('Arial', 12, 'italic'))

obseg1 = range(-obseg_x, obseg_x)
zelvica.width(2)
izrisF(z, zelvica, obseg1)
print(z)


#GUMBI:
sirinaG = 1/2

if 'math' in z or 'abs' in z:
  pass
else:
  funkcija.goto(5, 20/3)
  funkcija.write("Na intervalu x ∈ (-7, 7):", align='center', font = ('Arial', 13, 'italic'))

  asimptotaGumb = Turtle()
  asimptotaGumb.hideturtle()
  narisi_gumb(asimptotaGumb, 4, 6, 3/2, 'asimptota(y):')

  polGumb = Turtle()
  polGumb.hideturtle()
  narisi_gumb(polGumb, 4, 16/3, 5/4, 'poli(x):')

  nicleGumb = Turtle()
  nicleGumb.hideturtle()
  narisi_gumb(nicleGumb, 4, 14/3, 5/4, 'ničle:')

  zacetVredGumb = Turtle()
  zacetVredGumb.hideturtle()
  narisi_gumb(zacetVredGumb, 4, 12/3, 9/5, 'začetna vrednost:')

  if ')/(' not in z and '**x' not in z and '/' not in z:

    nedoloceniIntGumb = Turtle()
    nedoloceniIntGumb.hideturtle()
    narisi_gumb(nedoloceniIntGumb, 4, 10/3, 8/4 , 'nedoločeni integral:')

    integralGumb = Turtle()
    integralGumb.hideturtle()
    narisi_gumb(integralGumb, 4, 8/3, 7/4 , 'določeni integral:')


#klik:
zaslon.onclick(KlikNaGumb)

zaslon.mainloop()