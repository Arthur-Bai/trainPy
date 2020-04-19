import linecache

file = '/Users/arthur/Desktop/lines.txt'
count = len(open(file, 'r').readlines())
for k in range(2,count):
    finalvalue = ''
    value =  linecache.getline(file,k)
    forma = linecache.getline(file,1)
    lis = forma.split(' ')

    k=0
    for i in lis:
        j = len(i)
        newvalue = value[k:k+j].strip()+''

        if newvalue == '-':
            newvalue = ''
        if newvalue.isnumeric() and newvalue.startswith('00') == False :
            pass
        elif  newvalue == '' or newvalue.startswith('-'):
            pass
        else:
            newvalue = '"' + newvalue + '"'
        newvalue = newvalue+','
        # print(newvalue)
        k=k+j+1
        # print(j,k)
        finalvalue += newvalue
    print(finalvalue)
        
    