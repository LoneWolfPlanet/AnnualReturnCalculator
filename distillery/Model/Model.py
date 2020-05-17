
class Distillery():
    def __init__(self):
        self.key = ''
        self.listBarrelType = []

    def add(self,element):
        found = False
        for barrel in self.listBarrelType:
            if barrel.key == element['@barrelTypeCode']:
                found = True
                barrel.add(element)
                break
        if not found:
            barrel = BarrelType()
            barrel.key = element['@barrelTypeCode']
            barrel.add(element)
            self.listBarrelType.append(barrel)

class BarrelType():

    def __init__(self):
        self.key = ''
        self.listOfPitch = []
        self.average = 0.0000000

    def add(self,element):
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

    def set(self, element):
        self.category = element['@categoryName']
        self.bondYear = int(element['@bondYear'])
        if(element['@bondQuarter'].lower() == 'q1'):
            self.bondQuarter = 0.00
        elif (element['@bondQuarter'].lower() == 'q2'):
            self.bondQuarter = 0.25
        elif (element['@bondQuarter'].lower() == 'q3'):
            self.bondQuarter = 0.50
        elif (element['@bondQuarter'].lower() == 'q4'):
            self.bondQuarter = 0.75
        else:
            raise
        self.integerAge = self.bondYear + self.bondQuarter
        self.securityId = element['@securityId']
        self.considerationCurrency = element['@considerationCurrency']
        if (element['@soldOut'].lower() == 'true'):
            self.soldOut = True

        #Pase buyPrices tags
        try:
            if element['buyPrices']:
                if element['buyPrices']['price']:
                    for field in element['buyPrices']['price']:
                        price = Price()
                        price.set(field)
                        self.buyPriceList.append(price)
                        if(field['@actionIndicator'].lower() == 'b'):
                            if float(field['@limit']) < self.lowestBuyPrice :
                                self.lowestBuyPrice = float(field['@limit'])
        except Exception as e:
            print(str(e))

        #Parse sellPrices tags
        try:
            if element['sellPrices']:
                if element['sellPrices']['price']:
                    for field in element['sellPrices']['price']:
                        price = Price()
                        price.set(field)
                        self.salePriceList.append(price)
                        if (field['@actionIndicator'].lower() == 's'):
                            if float(field['@limit']) > self.highestSalePrice:
                                self.highestSalePrice = float(field['@limit'])
        except Exception as e:
            print(str(e))

class  Price():

     def __init__(self):
         self.actionIndicator = ''
         self.quantity = 0
         self.limit  =  0.0000

     def set(self, field):
            self.actionIndicator  = field['@actionIndicator']
            self.quantity = int(field['@quantity'])
            self.limit = float(field['@limit'])


class Result():

        def __init__(self):
            self.distillery = ''
            self.barrelTypeCode  = ''
            self.date = ''
            self.average = 0.0000

