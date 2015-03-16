def LCS(x, y):
  m = len(x)
  n = len(y)
  length = 0 # длина текущей общей подпоследовательности
  maxlength = 0 # длина наибольшей общей последовательности
  currentsub = ''
  maxsub = ''
  for i in range(m):  # цикл по x[i]
    currentsub = ''
    length = 0
    savei = ii = i # i - начало проверяемой последовательности, ii положение текущего сравнения в x, savei - последнее совпадение в x
    savej = j = 0 # j - положение текущего сравнения в y, savej - последнее совпадение в y
    while True: 
      while j < n and ii < m: 
        if x[ii] == y[j]:   
          length += 1
          currentsub += x[ii]
          savej = j  
          savei = ii
          ii += 1    
        j += 1      
      ii += 1 # проверены все y для x[ii] - переходим к ii+1
      j = savej+1 # j сбрасывается в первую возможную позицию (первую после последнего совпадения в y)
      if ii == m or j == n:
        break # все x[ii] закончились -- каждый из них проверен для каждого j > savej 
    if length > maxlength: 
      maxlength = length
      maxsub = currentsub
    #print i, j, currentsub, length, maxsub, maxlength #, savei, savej
  return maxlength, maxsub

x = '0120304'
y = '91234'

'''
x = '0120304'
y = '91234'

x = '0670120304'
y = '969791234'

x = '670120304'
y = '969791234'

x = '0670120304'
y = '69791234'
'''

print LCS(x, y)


