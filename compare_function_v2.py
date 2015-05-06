 # -*- coding: utf-8 -*-

import re

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
    same = '' # строка с совпадениями
    diff1 = '' # строка с несовпадениями с первой строке
    r = re.compile(r'[.,:;!?]')
    l1 = r.sub('',l1)
    l2 = r.sub('',l2)
    # print l1
    # print l2
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
                    cnt += 1  # количество совпавших слов в строках (всего)
                    if len(l1) < 4 or len(l2) < 4:
                        if cnt >= 1:
                            same += i + '\n'
                            match=match_ij=True
                            break
                    elif cnt >= 2:
                            same += i + '\n'
                            match=match_ij=True
                            break
                else:
                    # совпавшие части слов (если это >= 3 символов) записываются в same. or и не.
                    if len(common_s(i, j)) >= 3 or len(common_s(i, j))==len(i) or len(common_s(i, j))==len(j):
                        same += common_s(i, j) + '\n'
                        match=match_ij=True
                        break
            if not match_ij:
                # нужно, чтобы несовпавшие части слова записывались в diff1 и diff2, но записываются слова целиком
                diff1 += i + '\n'
    print 'same: \n', same
    print 'diff1: \n', diff1
    return match

#l1 = u'Пять могучих коней мне дарил Люцифер'
#l2 = u'Пять коней подарил мне мой друг Люцифер'
#l1 = 'cat dog me cow...'
#l2 = 'cat house  precow'

# ПЕРВЫЙ ВАРИАНТ ДЛЯ ТЕСТА - тут все ок -- строки равны
l1 = u'выстрелил не целясь цветком, и смеясь'
l2 = u'Выстрелил, не целясь, цветком и, смеясь,'

# ВТОРОЙ ВАРИАНТ ДЛЯ ТЕСТА - тут "выстрелил" не записывается (возможно, что-то не так с условием про 2 слова одинаковых в строке), /
# от "смеясь" записывается "ясь"
l1 = u'выстрелил а не целясь цветком, и смеясь'
l2 = u'Выстрелил, не целясь, цветком и, смеясь,'

print compare(l1, l2)
#print common_s(u'не', u'не')

#'<font color="#008000">' + i1 + '</font>'+'<br>\n'


w2 = 'cow'
w1 = 'precow'




