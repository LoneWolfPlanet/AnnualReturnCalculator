from lxml import etree
from Model.Model import *
class  XMLReader():

    def __init__(self):
        self.listOfDistillery = []


    def parse(self ,data):
        try:
            tree = etree.fromstring(data)
            self.walkElement(tree)
        except Exception as e:
            raise Exception('Error in parsing response')

    def walkElement(self,element):
        if len(element) > 0:
            for ele in element.getchildren():
                if ele.tag == 'pitches':
                    for pitch in ele.getchildren():
                        self.setListOfPitch(pitch)
                    return
                else:
                    self.walkElement(ele)
        else:
            return

    def setListOfPitch(self, element):
        found  = False
        if element.attrib['considerationCurrency'] == 'GBP':
            for distillery in self.listOfDistillery:
                if distillery.key == element.attrib['distillery']:
                    distillery.add(element)
                    found = True
                    break
            if not found:
                distillery = Distillery()
                distillery.key = element.attrib['distillery']
                distillery.add(element)
                self.listOfDistillery.append(distillery)

