import os.path
import requests as r
import re
import scipy.special as sci
import numpy as np
import matplotlib.pyplot as plt
import math

def J(order, countt):
    jlist = (sci.spherical_jn(order, k[countt] * D / 2))
    return jlist

def HANK(order, countt):
    ylist = (sci.spherical_yn(order, k[countt] * D / 2))
    hlist = (complex(J(order, countt), ylist))
    return hlist

def A(order, countt):
    alist = (J(order, countt) / HANK(order, countt))
    return alist


def B(order, countt):
    blist = (((k[countt] * (D / 2) * J(order - 1, countt) - order * J(order, countt)) / (k[countt] * (D / 2) * HANK(order - 1, countt) - order * HANK(order, countt))))
    return blist


if(os.path.exists('download') == False):
    os.mkdir('download')
if(os.path.exists('results') == False):
    os.mkdir('results')

#Ссылка на вариант 
url = 'https://jenyay.net/uploads/Student/Modelling/task_02.xml'

#Смотрим правильно ли открыли файл
file = r.get(url)
if file.ok is False:
    print('Smth went wrong')
    quit()

#Записывает в файл значения которые по ссылке
with open('download/DZ_2Parametrs.txt', 'wb') as f:
    f.write(file.content)
with open('download/DZ_2Parametrs.txt', 'r') as f:
    data = f.readlines()

#needvar номер варианта 
needvar = data[19]
print(needvar)

#pattern регулярное выражение которое смотрит шаблон чтобы достать значения
pattern = r'(?<!\d)\d+[.]\d+|\d+|-\d+(?!\d)'
var = re.findall(pattern, str(needvar))
print(var)

#Получуенные параметры
D = float(var[1])*10**float(var[2])
fmin = float(var[3])*10**float(var[4])
fmax = float(var[5])*10**float(var[6])
c = 3*10**8
print(D)
print(fmin)
print(fmax)

count = 200
step = 25

#Массив частот частот, k-волновое число
flist = np.linspace(fmin, fmax, count)
k = []
for i in range(count):
    k.append(2 * math.pi * flist[i] / c)

#Расчет ЭПР
j = 1
suum = [0]*count
while j <= step:
    for i in range(count):
        suum[i] += ((-1)**j * (j+0.5) * (B(j, i) - A(j, i)))
    j += 1

epr = []
lam = []
for i in range(count):
    epr.append((c ** 2 / (math.pi * flist[i] ** 2)) * (abs(suum[i]) ** 2))
    lam.append(c/flist[i])

#Запись в необходимом формате
flist = flist.tolist()
with open('results/results_2.json', 'w') as f:
    f.write(f"{{\n    \"freq\": {flist},\n    \"lambda\": {lam},\n    \"rcs\": {epr}\n}}")

plt.grid()
plt.xlabel('f, ГГц', fontsize=14)
plt.ylabel('RCS',rotation=0, fontsize=14, labelpad=10) 
plt.plot(flist, epr)
plt.show()
