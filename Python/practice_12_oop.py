class Student (object):

    def __init__ (self, name, score):
        self.name = name
        self.score = score

    def print_score (self):
        print ('%s %s'% (self.name, self.score))

    def his_pic (self):
        print ('''
                ___      _      ___    _____
               |___|    /_\    |___|     |
               |___|   /   \   |   \     |

              ''')

bart = Student('Bart Simpson', 59)
print(bart.name)
print(bart.score)
bart.print_score()
bart.his_pic()

