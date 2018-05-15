class Student (object):

    def __init__ (self, name, score):
        self.__name = name
        self.__score = score

    def print_score (self):
        print ('%s %s'% (self.__name, self.__score))

    def his_pic (self):
        print ('''
                ___      _      ___    _____
               |___|    /_\    |___|     |
               |___|   /   \   |   \     |

              ''')

    def get_name (self):
        return self.__name

    def get_score (self):
        return self.__score

    def set_score (self, score):
        self.__score = score

bart = Student('Bart Simpson', 59)
bart.__name = 'bart simpson'
bart.set_score('0')
bart.print_score()
bart.his_pic()
