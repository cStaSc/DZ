# import название_библиотеки as псевдоним названия библиотеки
import numpy as np
import matplotlib.pyplot as plt
import math
import xml.etree.ElementTree as et

def func(x):
   return(a*(y-b*x**2+c*x-r)**2+s*(1-t)*np.cos(x)+s)

x_min = -0
x_max = 13
a = 1
b = 5.1/(4*(np.pi)**2)
c = 5/np.pi
r = 6
s = 10
t = 1/(8*np.pi)
y = 2.275

y_points = []
x_points = []
for x in np.arange(x_min, x_max, 0.005):
    f = func(x)
    y_points.append(f)
    x_points.append(x)


plt.grid()
#fontsize размер шрифта
plt.xlabel('x', fontsize=14)
#labelpad сдвиг от оси влево, rotation поворот по кругу
plt.ylabel('y',rotation=0, fontsize=14, labelpad=10) 

plt.plot(x_points, y_points)
plt.show()

#Сохранение XML.
data = et.Element('data')
for i in range(len(y_points)):
    item_row = et.SubElement(data, 'row')
    item_x = et.SubElement(item_row, 'x')
    item_y = et.SubElement(item_row, 'y')
    item_x.text = str(x_points[i])
    item_y.text = str(y_points[i])

ffile = et.ElementTree(data)
et.indent(ffile, space="\t", level=0)
ffile.write("results_1.xml", encoding="utf-8", xml_declaration=True)

