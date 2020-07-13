import util
import sys


print("UPC: " + sys.argv[1])

name, description, collection, productImageUrl, weight = util.upcLookup(sys.argv[1])

print ("Product Name: ", name, "\n")  
print ("Product description: ", description, "\n")  
print ("Product Category: ", collection, "\n")  
print ("Product ImageUrl: ", productImageUrl, "\n")
print ("Product weight: ", weight, "\n")


