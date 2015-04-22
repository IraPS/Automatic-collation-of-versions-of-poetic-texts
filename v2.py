import codecs
import os

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
  l1=l1.strip()
  l2=l2.strip()
  match = (len(l1)>0 and len(l2)>0 and (l1 == l2))
  #match = True if True else SoftMatch(l1, l2)   # Проверять соотвествие слов только если нет точного совпадения
  if match == True:
      True
  '''else:
      SoftMatch(l1, l2)'''
  return match

# Проверка совпадают ли отдельные слова (2 и более). True , False.
def SoftMatch(l1, l2):
    match=False
    h1=l1.split()
    h2=l2.split()
    cnt=0
    for i in h1:
        for j in h2:
            if i==j:
                cnt+=1
    if cnt>=2:
        match=True
    print cnt
    return match

# t- список дескрипторов 3 файлов. Сравнивает t[0] с t[1]. Но не наоборот. Формирует t[2].
def analysis(t,CompareFunction1, CompareFunction2):
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
      if CompareFunction1(i1, i2):
        #print i
        t[2].write('<font color="#008000">' + i1 + '</font>'+'<br>\n')
        found=True
        break
      # "если строки разные"
      '''else:
          for k1 in i1:
              found=False
              for k2 in i2:
                  if CompareFunction2(i1, i2):
                     t[2].write('<font color="#008000">' + k1 + '</font>'+'<br>\n')
                     found=True
                     break'''

    if not found:
        t[2].write(i1 + '<br>\n')
  t[2].write('Расстояние Левенштейна для текстов: ' + str(levenshtein_damerau(text1, text2)) + '<br>\n')
  t[2].write(footer)


def proceed(FileList,CompareFunction1, CompareFucntion2):
  DescriptorList=OpenFiles(FileList)
  analysis(DescriptorList,CompareFunction1, CompareFucntion2) # Сравнивает t[0] с t[1]. Формирует t[2].
  CloseFiles(DescriptorList)

# f - список 4 имен. Сравнивает t[0] с t[1], затем t[1] с t[0]. Формирует 2 Html: t[2], t[3].
def double_analysis(f):
  proceed([f[0],f[1],f[2]],isLineMatch, SoftMatch) # Сравнивает t[0] с t[1]. Формирует t[2].
  proceed([f[1],f[0],f[3]],isLineMatch, SoftMatch) # Сравнивает t[1] с t[0]. Формирует t[3].

#analysis(OpenFile(AskFiles)))
'''lst = os.listdir('source')
for i in range(0,len(lst)-1):
  for j in range(i+1,len(lst)):
    double_analysis( [lst[i], lst[j], lst[i]+lst[j]+'.html', lst[j]+lst[i]+'.html'] )'''
#double_analysis( ['t1.txt', 't2.txt', 'r1.html', 'r2.html'] )
double_analysis( ['source/t1.txt', 'source/t2.txt', 'r1.html', 'r2.html'] )

