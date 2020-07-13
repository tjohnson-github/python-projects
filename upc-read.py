import util
import sys


print("product id: " + sys.argv[1])

tmpfile = 'temp.csv'
category = sys.argv[3]
barcodeFile = sys.argv[1]
outfile = sys.argv[2]

util.removeDuplicates('products-header.csv', barcodeFile, tmpfile)

util.LookupUPCProducts(category, tmpfile, sys.argv[2])




