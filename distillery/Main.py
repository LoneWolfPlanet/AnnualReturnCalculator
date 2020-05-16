import os
from  Controller.Parser  import *

def main():
    req = XMLParse()
    req.getData()

if __name__ == '__main__':
    main()