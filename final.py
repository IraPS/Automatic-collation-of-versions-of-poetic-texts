 # -*- coding: utf-8 -*-

from __future__ import division
import codecs
import os
import re

# задаём расположение файлов для сравнения
SOURCE_PATH='./poem' # название папки, в которой лежат варианты, которые нужно сравнить с каноническим
CANON='./afrodita_kanon.txt' # название файла, в котором лежит канонический текст

beg_g = '<font color="#008000">' # начало выделения зеленым цветом в html
beg_r = '<font color="#E80000">' # начало выделения красным цветом в html
end = '</font>' # конец выделения цветом в html

# Вычисление расстояния Левенштейна между двумя текстами (где Лев. для самого себя = -6)
def levenshtein_damerau(word1, word2):
    table = [[j for j in range(len(word1) + 1)]] +\
            [[i + 1] + [None] * len(word1)
             for i in range(len(word2))]
    for i in range(len(word2)):
        for j in range(len(word1)):
            if word1[j] == word2[i]:
                replacement = table[i][j]
            else:
                replacement = table[i][j] + 1
            insertion = table[i][j + 1] + 1
            removal = table[i + 1][j] + 1
            table[i + 1][j + 1] = min(replacement,
                                      insertion, removal)
            if i and j and word1[j] == word2[i - 1] and word1[j - 1] == word2[i]:
                table[i+1][j+1] = min(replacement-1, insertion, removal)
    return table[len(word2)][len(word1)]

# Вычисление расстояния Левенштейна между двумя текстами (где Лев. для самого себя = 0)
def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

# Принимает имена файлов t. Возвращает список дескрипторов открытых файлов.
def OpenFiles(t):
  textOpen1 = codecs.open(t[0], 'r', 'utf-8')
  textOpen2 = codecs.open(t[1], 'r', 'utf-8')
  textWrite1 = codecs.open(t[2], 'w', 'utf-8')
  return [textOpen1, textOpen2, textWrite1]

# Закрывает открытые файлы
def CloseFiles(t):
  for i in t:
    i.close()

# Возвращает общую последовательность подряд идущих символов - для случаев, когда слова совпадают не полностью
def common_s(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

# Сравнивает строку со строкой. Возвращает (не)окрашеную строку если строки соответствуют полностью или частично, иначе ''.
# Без '\n' !
def compare(l1, l2):
    same = '' # строка с совпадениями
    diff = '' # строка с несовпадениями с первой строке
    new1 = ''
    #r = re.compile(ur'[.,:;!?,-`—",—]', flags=re.UNICODE)
    #l1 = r.sub('',l1)
    #l2 = r.sub('',l2)
    l1 = l1.strip()
    l2 = l2.strip()
    match = False # совпадение строки
    if len(l1)==0:
        return ' ' # Если первая строка пуста, вернем пустую строку
    if len(l2)==0:
        return ''
    print l1, '-', l2 # Если первая не пуста, а вторая не пуста - вернем ''
    if l1 == l2:
        print 'YES - ', l1
        return l1 # Если строки совпали - то полное завершение функции, возврат строки черного цвета

    l1 = l1.split()
    l2 = l2.split()
    for i in l1: # цикл по словам в 1й строке
        match_ij = False # Совпадение слов i, j
        for j in l2:
            if i == j:
                print 'SAME I=', i
                same += i + '\n'
                match_ij = True
            else:
                if len(common_s(i,j)) >= 4:
                    newi = i.split(common_s(i,j))
                    newii = u'<r>' + newi[0] + u'</r>' + u'<g>' + common_s(i,j) + u'</g>' + u'<r>' + newi[1] + u'</r>'
                    same += newii + '\n'
                    l1 = ' '.join(l1)
                    l1 = re.sub(i, newii, l1)
                    l1 = l1.split()
                    print "L1 IS", l1
                    match=match_ij=True
        if not match_ij:
            diff += i + '\n'

    # условие про минимум одинаковых слов в строках (60%)
    if len(same.split())!=0:
        if (len(same.split())/len(l1)) >= 0.6:
            match=True
        else:
            diff += same
            same = ''
            match=False
    else:
        match = False



    # При частичном совпадении: Окрашивает частичное совпадение слова в первой строке зеленым, несовпадающую - красным.
    '''
    if match:
        # ввести счетчик для восстановления пунктуации
        for e in l1:
            if e in same:
                new1 += e + ' '
            else:
                for h in same.split():
                    #print len(common_s(e, h))
                    if len(common_s(e, h)) >= 4:
                        print 'green common'
                        new1 += e + beg_g + '(' + common_s(e, h) + ')' + end + ' '
                    else:
                        e = beg_r + e + end
                        new1 += e + ' '

        l1=new1
        return l1
    else: 
        return ''

    '''

    if match:
        for e in l1:
            if e in same:
                new1 += e + ' '
            else:
                e = beg_r + e + end
                new1 += e + ' '

        new1 = re.sub(u'<r>', beg_r, new1)
        new1 = re.sub(u'<g>', beg_g, new1)
        new1 = re.sub(u'</r>', end, new1)
        new1 = re.sub(u'</g>', end, new1)
        #print "NEW1 IS", new1
        l1 = new1
        return l1
    else:
        return ''

# t- список дескрипторов 3 файлов. Сравнивает t[0] с t[1]. Но не наоборот. Формирует t[2].
def analysis(t,CompareFunction):
  header='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'
  header += '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  header += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
  header += '<title></title></head>\n<body>'
  footer = str('</body>\n</html>')
  text1 = t[0].read()
  text1 = unicode(text1)
  text2 = t[1].read()
  text2 = unicode(text2)
  a1 = text1.split('\n')
  a2 = text2.split('\n')
  t[2].write(header)
  for i1 in a1:
    found=False
    for i2 in a2:
      match=CompareFunction(i1, i2) # Возвращает окрашеную строку, если найдено, или '', если не найдено соответствие.
      # print '***', match
      if len(match)>0:
        # print 'if match'
        i1=match
        #print i1
        found=True
        t[2].write(i1 + '<br>\n')  # Есть частичное сопадение - часть строки красным. match не нул.длины
        break
    if not found:   # Нет ни одного совпадения i1 ни с одной i2, в том числе частичного - красным i1 целиком.
        t[2].write(beg_r + i1 + end + '<br>\n')
  t[2].write(u'Расстояние Левенштейна для текстов: ' + str(levenshteinDistance(text1, text2)) + u'<br>\n')
  t[2].write(footer)

# Анализировать 3 файла
def proceed(FileList,CompareFunction):
  DescriptorList=OpenFiles(FileList)
  analysis(DescriptorList,CompareFunction) # Сравнивает t[0] с t[1]. Формирует t[2].
  CloseFiles(DescriptorList)

# f - список 4 имен. Сравнивает t[0] с t[1], затем t[1] с t[0]. Формирует 2 Html: t[2], t[3].
def double_analysis(f):
  proceed([f[0],f[1],f[2]],compare) # Сравнивает t[0] с t[1]. Формирует t[2].
  proceed([f[1],f[0],f[3]],compare) # Сравнивает t[1] с t[0]. Формирует t[3].


# 2 вариант использования- анализировать все файлы из папки source, лежащей в той же папке, что программа.
'''
lst = os.listdir(SOURCE_PATH)
if '.DS_Store' in lst:          # фикс скрытого файла изменения папки в MacOS
    lst.remove('.DS_Store')
print 'Process path: ',SOURCE_PATH, ', source files: ', lst
for i in range(0,len(lst)-1):
  for j in range(i+1,len(lst)):
    double_analysis( [SOURCE_PATH+'/'+lst[i], SOURCE_PATH+'/'+lst[j], (lst[i].split('.'))[0]+'_'+(lst[j].split('.'))[0]+'.html', (lst[j].split('.'))[0]+'_'+(lst[i].split('.'))[0]+'.html'] )
'''


# Сравнение канонического CANON с вариантами из SOURCE_PATH . Требует наличия и файла, и папки (где указано).
lst = os.listdir(SOURCE_PATH)
if '.DS_Store' in lst:          # фикс скрытого файла изменения папки в MacOS
    lst.remove('.DS_Store')
print 'Канонический вариант', CANON, 'сравнивается с вариантами: в папке',SOURCE_PATH, ' файлы: ', lst
for i in range(0,len(lst)):
    proceed([SOURCE_PATH+'/'+lst[i], CANON, (lst[i].split('.'))[0]+'.html'], compare)
