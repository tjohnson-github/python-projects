#!/usr/bin/env python3

import os
import socket
import struct
import multiprocessing
import logging
import array
import subprocess
import shlex
import json
import urllib.request
import pprint
import pyodbc
import hashlib 
import uuid
import requests

from datetime import datetime
from natsort import natsorted
from googlesearch import search


import glob
import csv
import openpyxl # from https://pythonhosted.org/openpyxl/ or PyPI (e.g. via pip)




api_key = "fl36xkrepxj1ontpnikzitb3iwvv4d"
url = "https://api.barcodelookup.com/v2/products?barcode={upc}&key=" + api_key

data = {'products': [{'actor': '',
               'artist': '',
               'asin': '',
               'audience_rating': '',
               'author': '',
               'barcode_formats': 'UPC 073561000994, EAN 0073561000994',
               'barcode_number': '073561000994',
               'barcode_type': 'UPC',
               'brand': 'Miracle Gro',
               'category': 'Home & Garden > Plants > Seeds',
               'color': '',
               'description': 'America s favorite plant food  Great for all '
                              'types of plants vegetables trees shrubs and '
                              'houseplants  Works instantly for quick '
                              'beautiful results  Feeds through leaves and '
                              'roots  Use in either mg garden feeder or a '
                              'watering can  Guaranteed not to burn when used '
                              'as directed  24-8-16  Dimensions: 2.5 x 2.5 x '
                              '4.25.',
               'director': '',
               'features': [],
               'format': '',
               'genre': '',
               'height': '',
               'images': ['https://images.barcodelookup.com/1153/11536987-1.jpg'],
               'ingredients': '',
               'label': '',
               'length': '',
               'manufacturer': 'THE SCOTT',
               'model': '',
               'mpn': '995665',
               'nutrition_facts': '',
               'package_quantity': '',
               'product_name': 'The Scott Mg 8-ounce All Purpose Plant Food',
               'publisher': '',
               'release_date': '',
               'reviews': [],
               'size': '',
               'stores': [{'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'http://www.hardwareandtools.com/dp/UDFB-2640',
                           'store_name': 'Hardware And Tools Corp',
                           'store_price': '3.39'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'http://www.truevalue.com/catalog/product.jsp?productId=19703&parentCategoryId=0&categoryId=2184&subCategoryId=1443&type=product',
                           'store_name': 'True Value Hardware',
                           'store_price': '2.99'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'https://www.rakuten.com/shop/life-and-home/product/40264840/?scid=af_feed',
                           'store_name': 'Rakuten.com',
                           'store_price': '9.65'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'https://www.hayneedle.com/product/miraclegro8ozallpurposeplantfoodfertilizer.cfm?source=channel_intelligence_shopzilla_hayneedle&szredirectid=SZ_REDIRECT_ID&mid',
                           'store_name': 'Hayneedle',
                           'store_price': '9.49'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'https://www.overstock.com/7438370/product.html?TRACK=affcjfeed&CID=207442&fp=F',
                           'store_name': 'Overstock.com',
                           'store_price': '10.85'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'http://jet.com/product/detail/9a5019feb72f4ef985a6d97545111d0d',
                           'store_name': 'Jet.com',
                           'store_price': '14.31'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'https://www.neweggbusiness.com/Product/Product.aspx?Item=9SIV19P8AC2222&nm_mc=afc-cjb2b&cm_mmc=afc-cjb2b-_-OG+-+Fertilizers+++Treatments-_-Scott+Publishing+Company-_-9SIV19P8AC2222',
                           'store_name': 'Newegg Business',
                           'store_price': '18.21'},
                          {'currency_code': 'USD',
                           'currency_symbol': '$',
                           'product_url': 'https://www.newegg.com/Product/Product.aspx?Item=9SIA62V84F7439&nm_mc=AFC-C8Junction-MKPL&cm_mmc=AFC-C8Junction-MKPL-_-OG+-+Fertilizers+++Treatments-_-Scott+Publishing+Company-_-9SIA62V84F7439',
                           'store_name': 'Newegg.com',
                           'store_price': '18.21'}],
               'studio': '',
               'title': '',
               'weight': '',
               'width': ''}]}




counter_id=0

logger = logging.getLogger(__name__)

sprinrg_collection_order = {'Spring Collection': '1', 
                    'Anniversary  Collection': '2', 
                    'Birthday Collection': '3', 
                    'Rose Collection': '4', 
                    'Love & Romance Collection': '5', 
                    'Get Well Collection': '6', 
                    'Thank You Collection': '7',
                    'Sympathy Collection': '8',
                    'Orchid Collection': '9',
                    'Blooming House Plant Collection': '10',
                    'House Plant Collection': '11',
                    'Annuals Collection': '12',
                    'Odds and Ends': '13',
                    'Gift Cards': '14'
                    }

garden_center_collection_order = {
                    'House Plant Collection': '1',
                    'Annual Patio Containers': '2', 
                    'Annual Hanging Baskets': '3', 
                    'Birthday Collection': '4', 
                    'Lawn Care': '5', 
                    'Plant Food & Fertilizers': '6', 
                    'Mulch and Soils': '7', 
                    'Bulk Mulch and Soil': '8',
                    'Blooming House Plant Collection': '9',
                    'Gift Cards': '10'
                    }


deptMargin = {  "1": 65.20,
            "1N": 65.20,
            "2": 59.00,
            "3": 59.00,
            "4": 64.20,
            "5": 64.70,
            "6": 64.20,
            "7": 64.70,
            "10": 69.50,
            "11": 69.50,
            "12": 69.50,
            "14": 60.32,
            "15": 66.00,
            "16": 69.27,
            "17": 66.00,
            "20": 66.00,
            "21": 66.00,
            "23": 64.20,
            "24": 56.20,
            "25": 59.50,
            "26": 56.20,
            "27": 56.20,
            "29": 64.00,
            "31": 61.00,
            "32": 64.20,
            "33": 64.00,
            "34": 64.49,
            "35": 62.50,
            "36": 63.00,
            "37": 63.00,
            "39": 64.00,
            "40": 64.00,
            "45": 63.00,
            "46": 61.00,
            "47": 62.20,
            "49": 66.00
            }


departments = { "1": "Flower",
            "2": "Ribbon, Bow" ,
            "3": "Design" ,
            "4": "Holiday" ,
            "5": "Dried" ,
            "6": "Candle" ,
            "7": "Balloon" ,
            "10": "Houseplant, indoor plant" ,
            "12": "potted Bulb" ,
            "14": "Pottery, clay pot, ceramic pot, clay, ceramic" ,
            "15": "outdoor plant, plant" ,
            "16": "Perennial, tree" ,
            "17": "Vegetable" ,
            "20": "Woodies" ,
            "21": "holiday Tree" ,
            "23": "Bulb, Tuber" ,
            "24": "Seed" ,
            "25": "Garden, Supplies, pot, planter" ,
            "26": "Bagged Goods, mulch, soil, sand, stone" ,
            "27": "Pond" ,
            "29": "Patio" ,
            "30": "Contribution" ,
            "31": "Concrete" ,
            "33": "Fashion" ,
            "34": "Propane" ,
            "35": "nature" ,
            "36": "Gift" ,
            "37": "Seasonal Gift" ,
            "40": "Jewelry" ,
            "45": "Ornament" ,
            "46": "Christmas Green, green, Wreath" ,
            "47": "Christmas Tree" ,
            "49": "Pumpkin" 
            } 



def readProducts(productsFile, categoryFile, product_categoryFile, optionsFile, outfile):
        try:
            skipFirstLine = True  

            cList = list()

            indict = dict()
            products = dict()
            categories = dict()
            product_category =dict()
            options = dict()
            header=''

           

            print("read category File file")
            with open(categoryFile) as f:
                for line in f:        
                    line = line.strip('\n')    
                    fields = line.split(',')
                    categories[fields[0]] = fields

            print("read products file")
            skip_first_one=True
            with open(productsFile) as f:
                for line in f:   

                    if skip_first_one:
                        header = line
                        skip_first_one=False
                        continue


                    line = line.replace('"','')
                    fields = line.split(',')

                    products[fields[0]] = fields


            print("read products file")
            with open(optionsFile) as f:
                for line in f:   

                    fields = line.split(',')

                    options[fields[0]] = fields


            print("read product_category file")
            with open(product_categoryFile) as f:
                for line in f:
                   
                
                    line = line.strip('\n')
                    line = line.replace('"','')
                    fields = line.split(',')

                    print("Fields: {0} {1}".format(len(fields) ,', '.join(map(str, fields))))
                    if len(fields) > 1:
                        product_id = fields[0]
                        if product_id.isdigit():
                            #  add categories
                            if product_id in products.keys(): 
                                collection=""
                                categoryList = fields[1:]
                                print("Product: {0} Cat List {1}".format(product_id, categoryList))
                                for cat in categoryList:
                                    if cat in categories:
                                        collection +=  "{0};".format(categories[cat][1])
                                        print("collection: {0}".format(collection))
                                    else:
                                        print("Category Not found {0}".format(product_id))        

                                print("\n ***** Products: {0}  ******\n".format(products[product_id]))
                                if 'GIFT CARD' in products[product_id][2]:
                                    collection = 'Florist Shop;Gift Cards'
                                else:
                                    collection = 'Florist Shop;' + collection

                                

                                products[product_id][5] = collection

                                # add collection information for additional filter field 

                                # this didn't work
                                #products[product_id][3] =  products[product_id][3] + ".  Part of These Collections (" + collection + ")"

                            else:
                                print("Product Not found {0}".format(product_id))

                            # commented out because product options don't work now the way we want
                            # will uncomment this later
                            #  add options
                            #if product_id in options.keys():
                            #    print("\n ***** options: {0}  ******\n".format(options[product_id]))
                            # options field
                            #products[product_id][17] = options[product_id][2]                                

                        else:
                            print("Category not a digit")
                    else:
                        print("No categories")

            print("write johnsons products out with categories file")

            skip_first_one=True
            with open(outfile, 'w') as f:


                f.write(header)

                # sort products first
                products = dict(natsorted(products.items(), key=lambda p: p[1][8]))
                print("products sorted")
                print(products)

                for key in products:

                    
                    fields = products[key]


                    # this is description field and need to clean it
                    #if ('<p>' not in fields[3]):
                    fields[3] = fields[3].replace('<p>','')

                    #if ('</p>' not in fields[3]):
                    fields[3] = fields[3].replace('</p>','')

                    # replace any spaces in url with '%20' 
                    fields[4] = fields[4].replace(' ', '') 

                    # if no picture, make invisible for now, but need to fix this later

                    if ('jpg' not in fields[4]):
                        fields[10] = 'FALSE'
                        fields[4] = ''

                    outStr = ','.join(map(str, fields)) 
                    f.write(outStr)

                    # commented  for now, not doing options
                    # check if options, doing here because same key and can't add duplicate keys in dictionary
                    # if fields[0] in  options.keys():
                    #     optionsList = options[fields[0]][2].split(';') 
                    #     priceList = options[fields[0]][3].split(';') 

                    #     print("\n ***** options: {0}  ******\n ".format( options[fields[0]]))
                    #     print("\n ***** optionsList: {0}  ******\n ".format( optionsList))

                    #     i=0
                    #     for option in optionsList:

                    #         variant = ['']*20
                    #         variant[0] = fields[0]
                    #         variant[1] = 'Variant'
                    #         variant[9] = priceList[i]
                    #         variant[10] = 'TRUE'
                    #         variant[13] = 'InStock'
                    #         variant[17] = option

                    #         outStr = ','.join(map(str, variant)) + '\n'
                    #         f.write(outStr)

                    #         i=i+1





            
        except Exception as ex:
            print("Error: {0}".format(ex))
        
        return


def lookupCPProduct(upc):

    conn = pyodbc.connect('Driver={SQL Server};Server="192.168.4.7";Database="dbo.JFGC";Trusted_Connection=yes;')


def writeOutProducts(products, header, outfile):

    skip_first_one=True
    with open(outfile, 'w') as f:


        f.write(header)

        # sort products first
        #products = dict(natsorted(products.items(), key=lambda p: p[1][8]))
        print("products sorted")
        print(products)

        for key in products:

            
            fields = products[key]


            # this is description field and need to clean it
            #if ('<p>' not in fields[3]):
            fields[3] = fields[3].replace('<p>','')

            #if ('</p>' not in fields[3]):
            fields[3] = fields[3].replace('</p>','')

            # replace any spaces in url with '%20' 
            fields[4] = fields[4].replace(' ', '') 

            # if no picture, make invisible for now, but need to fix this later

            if ('jpg' not in fields[4]):
                fields[10] = 'FALSE'
                fields[4] = ''

            outStr = ','.join(map(str, fields)) 
            f.write(outStr + '\n')


def removeDuplicates(headerFile, UPCFile, outfile):
        try:
            skipFirstLine = True  

            product = list()

            indict = dict()
            products = dict()
            UPCProducts = dict()
            product_category =dict()
            options = dict()
            header=''
            title=''
            description=''
            collection=''
            productImageUrl=''
            weight=''
            error = ''
            productId=''
            category=''

           
            print("read products file")
            skip_first_one=True
            with open(headerFile) as f:
                for line in f:   

                    if skip_first_one:
                        header = line
                        skip_first_one=False
                        continue



            print("read product_category file")
            with open(UPCFile) as f:
                for line in f:
                   

                    try:

                        upc = line[0:20]
                        name = line[20:53]
                        price = line[53:59]

                        #print('Upc: "{upc}" Name: "{name}" Price: "{price}"'.format(upc=upc, name=name, price=price))

                        upc = upc.strip(' ')
                        name = name.strip(' ')
                        price = price.strip(' ')   

                        #print('Upc: "{upc}" Name: "{name}" Price: "{price}"'.format(upc=upc, name=name, price=price))

                      
                        if upc == '':
                            continue

                        # having upc be field[0] will remove any duplicates     
                        fields = [upc,'Product',name, title, description, productImageUrl, category, upc,'',price,'','TRUE', 'Percent', '0', 'InStock',weight]
                  
                        # only unique field[0] will remain because it just over writes if exist 
                        products[fields[0]] = fields

                    except Exception as ex:
                        print("Error: " + upc + " " + name)
                        print("Error: " + ex)
                        continue


            writeOutProducts(products, header, outfile)
            
        except Exception as ex:
            print("Error: " + ex)
        
        return



def LookupUPCProducts(category, productsFile, outfile):

    name=''

    products = dict()

    print("read products file")
    skip_first_one=True
    with open(productsFile) as f:
        for line in f:   

            if skip_first_one:
                header = line
                skip_first_one=False
                continue


            line = line.replace('"','')
            fields = line.split(',')

            products[fields[0]] = fields


    skip_first_one=True
    with open(outfile, 'w') as f:


        f.write(header)

        # sort products first
        #products = dict(natsorted(products.items(), key=lambda p: p[1][8]))
        print("products sorted")
        print(products)

        for key in products:

            
            fields = products[key]

            name = fields[2]
            upc = fields[7]

            try:
                #title, description, collection, productImageUrl, weight, error =  upcLookup(upc)
                title, description, collection, productImageUrl, weight, manufacturer, manufacturer_number, newprice, department, error = upcLookup(upc)
            except Exception as ex:
                print("Error: " + upc + " " + name)
                print("Error: " + ex)
                continue

            if error == 'error':
                print("Could not find: " + upc + " " + name)
                continue

            if description == '':
                description = title

            if name == '':
                name = title

            if weight == '':
                weight = '5'

           

            #  [product_id,'Product',name, title, description, productImageUrl, 'Garden Center;', upc,'',price,'','TRUE', 'Percent', '0', 'InStock',weight]
            #  we add title to see if better then name for a name of the product
            fields[0] = uuid.uuid1()
            fields[2] = name
            fields[3] = title
            fields[4] = description
            fields[5] = productImageUrl
            fields[6] = category
            fields[15] = weight

            print("Record: {0}".format(fields))

            outStr = ','.join(map(str, fields)) 
            f.write(outStr + '\n')


def inventoryCP(productsFile, outfile):

    name=''

    products = dict()

    print("read products file")
    skip_first_one=True
    with open(productsFile) as f:
        for line in f:   

            if skip_first_one:
                header = line
                skip_first_one=False
                continue


            line = line.replace('"','')
            fields = [x.strip() for x in line.split(',')]

            products[fields[0]] = fields


    skip_first_one=True
    with open(outfile, 'w') as f:


        f.write(header)

        # sort products first
        #products = dict(natsorted(products.items(), key=lambda p: p[1][8]))
     
        for key in products:

            
            fields = products[key]

            print("Fields: {0}".format(fields))


            upc = fields[0]
            manufacturer_number = fields[1]
            description = fields[2]
            cost = fields[3]
            price = fields[4]
            tax_category = fields[5]
            category = fields[6]
            account_code = fields[7]
            vender_number = fields[8]
            price_code = fields[9]
            manufacturer = fields[10]
            pc = fields[11]



            try:
                name, description, collection, productImageUrl, weight, manufacturer, manufacturer_number, newprice, department, error =  upcLookup(upc)
            except Exception as ex:
                print("Error: " + upc + " " + name)
                print("Error: " + ex)
                continue

            if error == 'error':
                print("Could not find: " + upc + " " + name)
                continue


            
            description = name
            if price == "" or float(price) <= 0: 
                price = newprice
            elif '.' not in price:
                price = "{0}.99".format(price)



            cost = float(price) - ((float(deptMargin[department]) / 100) * float(price))
          
          

            fields[1] = manufacturer_number
            fields[2] = description
            fields[3] = cost
            fields[4] = price
            fields[6] = "{:03d}".format(int(department))
            fields[7] = "{:03d}".format(int(department))
            fields[9] = getPriceCode(department)
            fields[10] = manufacturer
            fields[11] = manufacturer_number
 

            print("Record: {0}".format(fields))

            outStr = ','.join(map(str, fields)) 
            f.write(outStr + '\n')


def getPriceCode(data):
    if int(data) < 15:
        return "A"
    if int(data) > 15 and int(data) < 30:
        return "B"
    return "C"

def getCategory(data):
    global departments

    try:
        for key in departments:
            department = departments[key]
            department_list = department.split(',')
            for keyphrase in department_list:
                if keyphrase.lower() in data.lower():
                    return key
    except Exception as ex:
        print("Error: " + key + " " + departments[key])
        pass

    # return default garden supplies
    return "25"


def upcLookup(upc):
    global url
   
    name=''
    description=''
    collection=''
    productImageUrl=''
    weight=''
    error=''
    manufacturer=''
    manufacturer_number=''
    department=''
    price=''
   
    try: 
        localUrl = url.format(upc=upc)


        with urllib.request.urlopen(localUrl) as localUrl:
            data = json.loads(localUrl.read().decode())

        barcode = data["products"][0]["barcode_number"]
        print ("Barcode Number: ", barcode, "\n")

        name = data["products"][0]["product_name"]
        name = name.replace(',', ' ')
        print ("Product Name: ", name, "\n")

        description = data["products"][0]["description"]
        print ("Product description: ", description, "\n")
        description = description.replace(',', '.')
       

        categories = data["products"][0]["category"].split('>')
        collection = categories[len(categories)-1]
        print ("Product Category: ", collection, "\n")

        images = data["products"][0]["images"]
        if len(images) > 0:
            productImageUrl = images[0]

        print ("Product ImageUrl: ", productImageUrl, "\n")

        weight = data["products"][0]["weight"]
        print ("Product weight: ", weight, "\n")

        manufacturer = data["products"][0]["manufacturer"]
        print ("Product manufacturer: ", manufacturer, "\n")
        manufacturer = manufacturer.replace(',', '')

        manufacturer_number = data["products"][0]["mpn"]
        print ("Product manufacturer number: ", manufacturer_number, "\n")
       

        stores = data["products"][0]["stores"]
        if len(stores) > 0:
            price = stores[0]["store_price"]
            print ("Product price: ", price, "\n")
        else:
            price = 0


        categories = data["products"][0]["category"]
        department = getCategory(categories)
        print ("Product department: ", department, "\n")    


    #print ("Entire Response:")
    #pprint.pprint(data)
    except:
        print("Error: " + upc)
        error='error'
        pass

    return name, description, collection, productImageUrl, weight, manufacturer, manufacturer_number, price, department, error



def readConfig(infile, infile2, outfile):
        try:
            cList = list()

            indict = dict()
            outdict = dict()

            print("read johnsons file")
            with open(infile2) as f:
                for line in f:            
                    fields = line.split(',')
                    outdict[fields[0]] = fields

            print("read vendor file")
            with open(infile) as f:
                for line in f:
                   
                    line = line.strip('\n')
                    fields = line.split(',')

                    print("Fields: {0} {1}".format(len(fields) ,', '.join(map(str, fields))))
                    if len(fields) > 0:
                        if fields[0].isdigit():
                            if fields[0] in outdict: 
                                outdict[fields[0]][3] = fields[1] 
                            else:
                                print("Not found {0}".format(fields[0]))

            print("write johnsons/vendor file")
            with open(outfile, 'w') as f:
                for key in outdict:
                    fields = outdict[key]
                    outStr = ','.join(map(str, fields)) 
                    f.write(outStr)


            
        except Exception as ex:
            print("Error: {0}".format(ex))
        
        return

def ConvertOptions(infile, outfile):
    try:
        cList = list()

        indict = dict()
        outdict = dict()

        print("read johnsons file")
        with open(infile) as f:

            savFields = ''
            for line in f:           
                line = line.strip('\n')    
                line = line.strip('\r')   
                fields = line.split(',')
                if fields[0] in savFields:
                    savFields[2] = savFields[2] + ";" + fields[2]
                    savFields[3] = savFields[3] + ";" + fields[3]
                    outdict[fields[0]] = savFields
                else:
                    savFields = fields

        writecsv(outfile, outdict)        

    except Exception as ex:
        print("Error: {0}".format(ex))
    
    return


def writecsv(outfile, outdict):


    with open(outfile, 'w') as f:
        for key in outdict:
            fields = outdict[key]
            outStr = ','.join(map(str, fields)) + '\n'
            f.write(outStr)


def loadcsv(infile):


    outdict = dict()

    with open(infile) as f:
        for line in f:            
            fields = line.split(',')
            outdict[fields[0]] = fields

    return outdict

def readCSV(infile):
    with open(infile, 'rU') as csvIN:
        outCSV=(line for line in csv.reader(csvIN, dialect='excel'))




def googleSearch(searchText, domain, numresults):
  
    i = 0
    saveResult=""

    for result in search(searchText, tld="com", num=10, stop=numresults, pause=20): 
        
        print(result)

        if (saveResult != getDomain(result)): 
            i+=1

        if (domain in result):
            break
        

        saveResult = getDomain(result)


    return i

def getDomain(result):

    idx1=0
    idx2=0
    try:
        idx1 = result.index("://")
    except Exception as ex:
        print("Error idx1: {0} {1}".format(ex, result))
        pass
    
    try:
        idx2 = result.index(".com")
    except Exception as ex:
        idx=0
        pass
   
    if (idx2 == 0):
        try:
            idx2 = result.index(".net")
        except Exception as ex:
            print("Error idx2: {0} {1}".format(ex, result))
            pass
    try:
        domain = result[idx1+3:idx2+4] 
    except Exception as ex:
        print("Error: {0} {1}".format(ex, result))
        domain=""
        pass

    return domain

def runCmd(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
    except Exception as e:
        logger.error(e)




def PayPal_Trackers(trans_id):

    try:
        api_key = "Bearer A21AAHtiBEKgIfFZddAHXzl2SWoJMhWgG3hvuxNs3fxmY62RziFFst0T0X3mZgP6wis0-Y2lHrLk_BsUv2O21UICwvwYbZ6ng"
    
        transactions = dict(transaction_id=trans_id, status="PROCESSED")
        tList = []

        tList.append(transactions)
        payload = dict(trackers=tList)
        print("payload {0}".format(payload))
        resp = requests.post('https://api.paypal.com/v1/shipping/trackers-batch', json=payload, headers={'Authorization': api_key })

        print("Response: {0}".format(resp.status_code))

        if resp.status_code!=200:
            logger.error("REST API Error {0}".format(resp))
            logger.error(" Json: {0}".format(payload))



    except Exception as e:
        logger.error(e)


def PayPal_Trackers2(trans_id):

    try:
        api_key = "Bearer A21AAHtiBEKgIfFZddAHXzl2SWoJMhWgG3hvuxNs3fxmY62RziFFst0T0X3mZgP6wis0-Y2lHrLk_BsUv2O21UICwvwYbZ6ng"
    
        transactions = dict(transaction_id=trans_id, status="SHIPPED")
        tList = []

        tList.append(transactions)
        payload = dict(trackers=tList)
        print("payload {0}".format(payload))
        resp = requests.post('https://api.paypal.com/v1/shipping/trackers-batch', json=payload, headers={'Authorization': api_key })

        print("Response: {0}".format(resp.status_code))

        if resp.status_code!=200:
            logger.error("REST API Error {0}".format(resp))
            logger.error(" Json: {0}".format(payload))



    except Exception as e:
        logger.error(e)

def ConvertToExcel(csvfile):

    wb = openpyxl.Workbook()
    ws = wb.active
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader, start=1):
            for c, val in enumerate(row, start=1):
                ws.cell(row=r, column=c).value = val

    filename = os.path.splitext(os.path.basename(csvfile))[0]
    wb.save(filename + '.xlsx')