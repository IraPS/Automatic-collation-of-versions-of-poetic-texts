 # -*- coding: utf-8 -*-
__author__ = 'IrinaPavlova'

#l1 = 'Пять могучих коней мне дарил Люцифер'
#l2 = 'Пять коней подарил мне мой друг Люцифер'

l1 = 'cat dog'
l2 = 'dog'

def compare(l1, l2):
    indexes1 = []
    indexes2 = []
    #l1 = l1.strip()
    #l2 = l2.strip()
    match = False
    if len(l1)>0 and len(l2)>0 and (l1 == l2):
        for i in xrange(0, len(l1)):
            indexes1.append(i)
        for j in xrange(0, len(l2)):
            indexes2.append(j)
        match = True
    if not match:
        l1 = l1.split()
        l2 = l2.split()
        cnt=0
        for i in xrange(len(l1)):
            for j in xrange(len(l2)):
                if l1[i]==l2[j]:
                    cnt+=1
                    indexes1.append(i)
                    indexes2.append(j)
        if len(l1) < 4 and len(l2) < 4:
            if cnt >= 1:
                match=True
        else:
            if cnt >= 2:
                match = True


    print l1, indexes1
    print l2, indexes2
    return match


print compare(l1, l2)
