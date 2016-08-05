print 'if'
age = 23
bool = 1
if (age < 20):
    print 'kid'
elif (age < 25):
    print 'teenage'
else:
    print 'aludt'
if (bool):
    print '1 is True'

brith = input ('when are you bron:')
print brith

height = 1.8
weight = 78.1
BMI = weight / (height*100) / (height*100)
print (BMI)
if (BMI < 18.5):
    print ('Too ligth')
elif (BMI < 25):
    print ('normal')
elif (BMI < 28):
    print ('fat')
elif (BMI >= 32):
    print ('obesity')
