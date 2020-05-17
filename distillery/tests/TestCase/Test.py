
class TestData():

     def __init__(self):
         self.text = None


     def getData(self,name):

         file = open(name,'r')
         self.text = file.read()
         file.close()
