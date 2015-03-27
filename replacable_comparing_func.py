import codecs

# Возвращает список имен 4 файлов для открытия. 
def AskFiles():
  fname1 = input('First file to compare: ')
  fname2 = input('Second file to compare: ')
  res1 = input('First resultfile name: ')
  res2 = input('Second resultfile name: ')
  return [fname1, fname2, res1, res2]

# Принимает имена файлов t. Возвращает список дескрипторов открытых файлов. 
def OpenFiles(t):
  textOpen1 = codecs.open(t[0], 'r', 'utf-8')
  textOpen2 = codecs.open(t[1], 'r', 'utf-8')
  textWrite1 = codecs.open(t[2], 'w', 'utf-8')
  return [textOpen1, textOpen2, textWrite1]

def CloseFiles(t):
  for i in t:
    i.close()

# 1 метод сравнения: True если есть текстуальное сопадение строк.
def isLineEqual(l1, l2):
  return (l1 == l2)

# 2 метод сравнения: True если строки непусты и полностью соответсвуют.
def isLineMatch(l1, l2):
  l1=l1.strip()
  l2=l2.strip()
  match = (len(l1)>0 and len(l2)>0 and (l1 == l2))
  return match

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
      if CompareFunction(i1, i2):
        #print i
        t[2].write('<font color="#008000">' + i1 + '</font>'+'<br>\n')
        found=True
        break
    if not found:
        t[2].write(i1 + '<br>\n')
  t[2].write(footer)

# Анализировать 3 файла
def proceed(FileList,CompareFunction):
  DescriptorList=OpenFiles(FileList)
  analysis(DescriptorList,CompareFunction) # Сравнивает t[0] с t[1]. Формирует t[2].
  CloseFiles(DescriptorList)

# f - список 4 имен. Сравнивает t[0] с t[1], затем t[1] с t[0]. Формирует 2 Html: t[2], t[3].
def double_analysis(f):
  proceed([f[0],f[1],f[2]],isLineMatch) # Сравнивает t[0] с t[1]. Формирует t[2].
  proceed([f[1],f[0],f[3]],isLineMatch) # Сравнивает t[1] с t[0]. Формирует t[3].

#analysis(OpenFile(AskFiles)))
double_analysis( ['t1.txt', 't2.txt', 'r1.html', 'r2.html'] )
