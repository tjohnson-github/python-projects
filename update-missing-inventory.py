import util
import sys


print("file: " + sys.argv[1])


util.inventoryCP(sys.argv[1], 'master-inv-out.csv')
