import codecs

def AskFile():
  fname1 = input('First file to compare: ')
  fname2 = input('Second file to compare: ')
  res1 = input('First resultfile name: ')
  res2 = input('Second resultfile name: ')
  return fname1, fname2, res1, res2

def OpenFile(t):
  textOpen1 = codecs.open(t[0], 'r', 'utf-8')
  textOpen2 = codecs.open(t[1], 'r', 'utf-8')
  textWrite1 = codecs.open(t[2], 'w', 'utf-8')
  textWrite2 = codecs.open(t[3], 'w', 'utf-8')
  return textOpen1, textOpen2, textWrite1, textWrite2

def analysis(t):
  header = str('<html>\n<body>')
  footer = str('</body>\n</html>')
  #text1 = t[0].read()
  #text2 = t[1].read()
  a1 = t[0].read().split('\n')
  a2 = t[1].read().split('\n')
  b1 = set(line.strip() for line in a1)
  b2 = set(line.strip() for line in a2)
  t[2].write(header)
  for line in b1 & b2:
    if line:
        print line
        #print i
        t[2].write('<font color="#008000">' + line + '</font>'+'<br>\n')
    else:
        t[2].write(line + '<br>\n')
  t[2].write(footer)

    
  # t[2].write(text1)
  #t[3].write(text2)
  
#analysis(OpenFile(AskFile()))
analysis( OpenFile(('t1.txt', 't2.txt', 'r1.html', 'r2.html')) )
