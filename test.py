
aList = [1, 2]
bList = [1, 2]
cList = [2, 1]

print('lists:')

if aList == bList:
    print('aList and bList are equal')
else:
    print('aList and bList are not equal')

if aList == cList:
    print('aList and cList are equal')
else:
    print('aList and cList are not equal')

aSet = {1, 2}
bSet = {1, 2}
cSet = {2, 1}
dSet = {1 , 1, 2}

print('sets:')

if aSet == bSet:
    print('aSet and bSet are equal')
else:
    print('aSet and bSet are not equal')

if aSet == cSet:
    print('aSet and cSet are equal')
else:
    print('aSet and cSet are not equal')

if aSet == dSet:
    print('aSet and dSet are equal')
else:
    print('aSet and dSet are not equal')


necessary_files = [
    'verse_1.txt',
    'verse_2.txt'
]

song = ''
for file_name in necessary_files:
    try:
        input_file = open(self.file_name, 'r')
        song += input_file.readline()
        input_file.close()
    except:
        song += 'something went wrong'
output_file = open(self.output_file, 'w')
output_file.write(song)
output_file.close()