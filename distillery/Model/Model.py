
class Distillery():
    def __init__(self):
        self.key = ''
        self.listBarrelType = []

    def add(self,element):
        found = False
        for barrel in self.listBarrelType:
            if barrel.key == element.attrib['barrelTypeCode']:
                found = True
                barrel.add(element)
                break
        if not found:
            barrel = BarrelType()
            barrel.key = element.attrib['barrelTypeCode']
            barrel.add(element)
            self.listBarrelType.append(barrel)

class BarrelType():

    def __init__(self):
        self.key = ''
        self.listOfPitch = []
        self.average = 0.0000000

    def add(self,element):
        '''exclude = False
        for el in element.getchildren():
            if el.tag == 'sellPrices' or el.tag == 'buyPrices':
                if len(el.getchildren()) == 0:
                    exclude = True
                    break

        if not exclude: '''
        pitch = Pitch()
        pitch.set(element)
        self.listOfPitch.append(pitch)


class Pitch():

    def __init__(self):
        self.category = ''
        self.bondYear = 0
        self.bondQuarter = 0.00
        self.securityId = ''
        self.considerationCurrency  = ''
        self.soldOut = False
        self.integerAge = 0.00
        self.buyPriceList = []
        self.salePriceList = []
        self.lowestBuyPrice = 1000000000.00000
        self.highestSalePrice = 0.00000
        self.exclude = False

    def set(self, element):
        self.category = element.attrib['categoryName']
        self.bondYear = int(element.attrib['bondYear'])
        if(element.attrib['bondQuarter'].lower() == 'q1'):
            self.bondQuarter = 0.00
        elif (element.attrib['bondQuarter'].lower() == 'q2'):
            self.bondQuarter = 0.25
        elif (element.attrib['bondQuarter'].lower() == 'q3'):
            self.bondQuarter = 0.50
        elif (element.attrib['bondQuarter'].lower() == 'q4'):
            self.bondQuarter = 0.75
        else:
            raise
        self.integerAge = self.bondYear + self.bondQuarter
        self.securityId =  element.attrib['securityId']
        self.considerationCurrency = element.attrib['considerationCurrency']
        if ( element.attrib['soldOut'].lower() == 'true'):
            self.soldOut = True
        self.walkPricesTag(element)

    def  walkPricesTag(self, element):
         for child in element.getchildren():
             if child.tag == 'sellPrices':
                 for ele in child.getchildren():
                     price = Price()
                     price.set(ele)
                     self.salePriceList.append(price)
                     self.setPrice(ele, 'sellPrices')
             elif child.tag == 'buyPrices':
                 for ele in child.getchildren():
                    price = Price()
                    price.set(ele)
                    self.buyPriceList.append(price)
                    self.setPrice(ele, 'buyPrices')

    def setPrice(self, element, key):
        if key == 'sellPrices':
            if (element.attrib['actionIndicator'].lower() == 's'):
                if float(element.attrib['limit']) > self.highestSalePrice:
                    self.highestSalePrice = float(element.attrib['limit'])
        elif key == 'buyPrices':
            if (element.attrib['actionIndicator'].lower() == 'b'):
                if float(element.attrib['limit']) < self.lowestBuyPrice:
                    self.lowestBuyPrice = float(element.attrib['limit'])

class  Price():
     def __init__(self):
         self.actionIndicator = ''
         self.quantity = 0
         self.limit  =  0.0000

     def set(self, element):
            self.actionIndicator  = element.attrib['actionIndicator']
            self.quantity = int(element.attrib['quantity'])
            self.limit = float(element.attrib['limit'])


class Result():

        def __init__(self):
            self.distillery = ''
            self.barrelTypeCode  = ''
            self.date = ''
            self.average = 0.0000

