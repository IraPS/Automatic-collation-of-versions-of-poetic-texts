 # -*- coding: utf-8 -*-

import re

global l1
global l2

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

# Сравнивает строку со строкой, возвращает результат (True/False).
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
    print l1
    print l2
    l1 = l1.strip().lower()
    l2 = l2.strip().lower()
    match = False # совпадение строки

    if len(l1)>0 and len(l2)>0 and (l1 == l2):
        same += l1 + '\n'
        match = True

    if not match:
        l1 = l1.split()
        l2 = l2.split()
        cnt=0
        for i in l1:    # цикл по словам в 1й строке
            match_ij = False # Совпадение слов i, j
            for j in l2:
                if i == j:
                    same += i + '\n'
                    match_ij = True
                else:
                    # совпавшие части слов (если это >= 3 символов) записываются в same. or и не.
                    if len(common_s(i, j)) >= 3: #or len(common_s(i, j))==len(i) or len(common_s(i, j))==len(j): --
                    # если это оставить, то "выстрелил" и "и" будут совпадать -- т.к. len("и") = 1
                        print 'i=', i, ';', 'j=', j # видно, что с чем сравнивается
                        same += common_s(i, j) + '\n'
                        match=match_ij=True
                        #break , если break оставить, то "смеясь" не записывается
            if not match_ij:
                diff1 += i + '\n'

    # условие про минимум одинаковых слов в строках
    if len(l1) < 4 or len(l2) < 4:
        if len(same.split()) >= 1:
            match=True
    else:
        if len(same.split()) >= 2:
            match=True
        else:
            diff1 += same
            same = ''
            match = False

    for e in l1:
        if e in same:
            #print 'e in same'
            e = beg_g + e + end
            new1 += e
            #print 'done'
            #print new1
        else:
            e = beg_r + e + end
            new1 += e


    for m in l2:
        if m in same:
            #print 'm in same'
            m = beg_g + m + end
            new2 += m
            #print 'done'
            #print new2
        else:
            m = beg_g + m + end
            new2 += m

    l1 = new1
    l2 = new2

    print 'same:', same
    print 'diff1: \n', diff1
    print l1
    print l2

    return match


s1 = u'выстрелил а не целясь цветком, и смеясь '
s2 = u'Выстрелил, не целясь, цветком и, смеясь,'


print compare(s1, s2)
#print common_s(u'не', u'не')

#'<font color="#008000">' + i1 + '</font>'+'<br>\n'

#l1 = u'Пять могучих коней мне дарил Люцифер'
#l2 = u'Пять коней подарил мне мой друг Люцифер'
#l1 = 'cat dog me cow...'
#l2 = 'cat house  precow'

