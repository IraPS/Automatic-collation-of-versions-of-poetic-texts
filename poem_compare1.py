 # -*- coding: utf-8 -*-

import codecs
import os
import re # для compare()

SOURCE_PATH='./poem'

# Печать таблицы для levenshtein_damerau
def pretty_print(table):
    for row in table:
        print u'\t'.join(str(i) for i in row)

# Вычисление расстояния Левенштейна между двумя текстами.
def levenshtein_damerau(word1, word2):
    table = [[j for j in range(len(word1) + 1)]] +\
            [[i + 1] + [None] * len(word1)
             for i in range(len(word2))]
    # print u'Initial table:'
    # pretty_print(table)
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
    # pretty_print(table)
    return table[len(word2)][len(word1)]

# Возвращает список имен 4 файлов для открытия, в случае если этот интерфейс нужен программе (default - dir list).
def AskFiles():
  fname1 = input('First file to compare: ')
  fname2 = input('Second file to compare: ')
  res1 = input('First resultfile name: ')
  res2 = input('Second resultfile name: ')
  return [fname1, fname2, res1, res2]

# Принимает имена файлов t. Возвращает список дескрипторов открытых файлов.
def OpenFiles(t):
  textOpen1 = open(t[0], 'r')  # textOpen1 = codecs.open(t[0], 'r', 'utf-8')
  textOpen2 = open(t[1], 'r')  # textOpen2 = codecs.open(t[1], 'r', 'utf-8')
  textWrite1 = open(t[2], 'w') # textWrite1 = codecs.open(t[2], 'w', 'utf-8')
  return [textOpen1, textOpen2, textWrite1]

def CloseFiles(t):
  for i in t:
    i.close()

# 1 метод сравнения: True если есть текстуальное сопадение строк.
def isLineEqual(l1, l2):
  return (l1 == l2)

# 2 метод сравнения: True если строки непусты и полностью соответсвуют.
def isLineStrictMatch(l1, l2):
  l1=l1.strip()
  l2=l2.strip()
  match = (len(l1)>0 and len(l2)>0 and (l1 == l2))
  return match

# 3 метод сравнения: True если строки непусты и полностью соответсвуют, или совпадают в 2 и более словах.
def isLineMatch(l1, l2):
  l1=l1.lower().strip()
  l2=l2.lower().strip()
  match = (len(l1)>0 and len(l2)>0 and (l1 == l2))
  match = True if match else SoftMatch(l1, l2)   # Проверять соотвествие слов только если нет точного совпадения
  return match

# 4 метод сравнения: Проверка совпадают ли отдельные слова (2 и более). True , False.
def SoftMatch(l1, l2):
    match=False
    a1=l1.lower().split()
    a2=l2.lower().split()
    cnt=0
    for i in a1:
        for j in a2:
            if i==j:
                cnt+=1
    if cnt>=2:
        match=True
    # print cnt
    return match

# 5 метод сравнения - оптимален для поэтических текстов. Возвращает окрашеную строку.

# возвращает общую последовательность подряд идущих символов - для случаев, когда слова разные
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

# Сравнивает строку со строкой. Возвращает окрашеную строку если строки соответствуют полностью или частично, иначе ''.
def compare(l1, l2):
    beg_g = '<font color="#008000">'
    beg_r = '<font color="#E80000">'
    end = '</font>'

    same = '' # строка с совпадениями
    diff1 = '' # строка с несовпадениями с первой строке
    new1 = ''
    new2 = ''
    r = re.compile(r'[.,:;!?]')
    l1 = r.sub('',l1)
    l2 = r.sub('',l2)
    # print l1
    # print l2
    l1 = l1.strip().lower()
    l2 = l2.strip().lower()
    match = False # совпадение строки
    if len(l1)==0:
        return ' ' # Если первая строка пуста - вернем пустую строку
    if len(l2)==0:
        return ''
    print l1, '-', l2 # Если первая не пуста, а вторая не пуста - вернем ''
    if (l1 == l2):
        print 'YES - ', l1
        return (beg_g + l1 + end + '\n')  # Если строки совпали - то полное завершение функции, возврат GREEN строки.

    l1 = l1.split()
    l2 = l2.split()
    cnt=0
    for i in l1:    # цикл по словам в 1й строке
        match_ij = False # Совпадение слов i, j
        for j in l2:
            if i == j:
                print 'SAME I=', i
                same += i + '\n'
                match_ij = True
            else:
                # совпавшие части слов (если это >= 3 символов) записываются в same. or и не.
                if len(common_s(i, j)) >= 3: #or len(common_s(i, j))==len(i) or len(common_s(i, j))==len(j): --
                # если это оставить, то "выстрелил" и "и" будут совпадать -- т.к. len("и") = 1
                    # print 'i=', i, ';', 'j=', j # видно, что с чем сравнивается
                    print 'COMMON S=', common_s(i, j), len(common_s(i, j)), type(common_s(i, j))
                    same += common_s(i, j) + '\n'
                    match=match_ij=True
                    #break , если break оставить, то "смеясь" не записывается
        if not match_ij:
            diff1 += i + '\n'

    # условие про минимум одинаковых слов в строках
    if len(l1) < 4 or len(l2) < 4:
        print 'SAME LEN', len(same.split())
        if len(same.split()) >= 1:
            match=True
        else:
            match=False
    if len(l1)>=4 or len(l2)>=4:
        print 'SAME LEN', len(same.split())
        if len(same.split()) >= 2:
            match=True
        else:
            diff1 += same
            same = ''
            match=False

    # При частичном совпадении: Окрашивает частичное совпадение слова в первой строке зеленым, несовпадающую - красным.
    print match  # Проблема выше: кто-то ошибочно выставляет match.
    if match:
        for e in l1:
            if e in same:
                #print 'e in same'
                e = beg_g + e + end
                new1 += e + ' '
                #print 'done'
                #print new1
            else:
                e = beg_r + e + end
                new1 += e + ' '


        for m in l2:
            if m in same:
                #print 'm in same'
                m = beg_g + m + end
                new2 += m + ' '
                #print 'done'
                #print new2
            else:
                m = beg_r + m + end
                new2 += m + ' '
        l1=new1
        l2=new2
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
  text2 = t[1].read()
  a1 = text1.split('\n')
  a2 = text2.split('\n')
  t[2].write(header)
  for i1 in a1:
    found=False
    for i2 in a2:
      match=CompareFunction(i1, i2) # Возвращает окрашеную строку, если найдено, или '', если не найдено соответствие.
      print '***', match
      if len(match)>0:
        # print 'if match'
        i1=match
        #print i1
        found=True
        break
    t[2].write(i1 + '<br>\n')
  t[2].write('Расстояние Левенштейна для текстов: ' + str(levenshtein_damerau(text1, text2)) + '<br>\n')
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

# 1 вариант - спрашивать пользователя
#analysis(OpenFile(AskFiles)))
# 2 вариант использования- анализировать все файлы из папки source, лежащей в той же папке, что программа.
lst = os.listdir(SOURCE_PATH)
if '.DS_Store' in lst:          # фикс скрытого файла изменения папки в MacOS
    lst.remove('.DS_Store')
print 'Process path: ',SOURCE_PATH, ', source files: ', lst
for i in range(0,len(lst)-1):
  for j in range(i+1,len(lst)):
    double_analysis( [SOURCE_PATH+'/'+lst[i], SOURCE_PATH+'/'+lst[j], (lst[i].split('.'))[0]+'_'+(lst[j].split('.'))[0]+'.html', (lst[j].split('.'))[0]+'_'+(lst[i].split('.'))[0]+'.html'] )
# 3 вариант использования - для тестирования кода
#double_analysis( ['t1.txt', 't2.txt', 'r1.html', 'r2.html'] )
#double_analysis( ['source/t1.txt', 'source/t2.txt', 'r1.html', 'r2.html'] )

