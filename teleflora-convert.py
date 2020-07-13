import util
import sys
import pandas as pd







def AddProduct(row, product, rowList):
   newRow = {}
   newRow['handleId'] = product
   newRow['fieldType'] = 'Product'
   newRow['name'] = row['name']
   newRow['description'] = row['description']
   newRow['productImageUrl'] = Url.format(productId=row['handleId'], productName=row['name'].replace(" ", ""))
   newRow['collection'] = 'Teleflora Collection; Teleflora {0} {1}'.format(row['collection'], row['Category'])
   newRow['sku'] = ''
   newRow['ribbon']=''
   newRow['price'] = "{:.2f}".format(float(row['price']) + 10) 
   newRow['surcharge'] = ''
   newRow['visible'] = 'TRUE'
   newRow['discountMode'] = 'PERCENT'
   newRow['discountValue'] = '0'
   newRow['inventory'] = 'InStock'
   newRow['weight'] = '5'
   newRow['productOptionName1'] = 'Select Size'
   newRow['productOptionType1'] = 'DROP_DOWN'
   newRow['productOptionDescription1'] = 'Deluxe;Premium;Standard'
   rowList.append(newRow)
   return rowList



def AddVariant(row, product, option, rowList):
   newRow = {}
   newRow['handleId'] = product
   newRow['fieldType'] = 'Variant'
   newRow['name'] = ''
   newRow['description'] = ''
   newRow['productImageUrl'] = Url.format(productId=row['handleId'], productName=row['name'].replace(" ", ""))
   newRow['collection'] = ''
   newRow['sku'] = 'Teleflora-{0}'.format(row['handleId'])
   newRow['ribbon']=''
   newRow['price'] = ''
   if ('Standard' in option):
      newRow['surcharge'] = '0'
   elif ('Deluxe' in option):
      newRow['surcharge'] = '10'
   elif ('Premium' in option):
      newRow['surcharge'] = '20'
   
   newRow['visible'] = 'TRUE'
   newRow['discountMode'] = ''
   newRow['discountValue'] = ''
   newRow['inventory'] = 'InStock'
   newRow['weight'] = '5'
   newRow['productOptionName1'] = ''
   newRow['productOptionType1'] = ''
   newRow['productOptionDescription1'] = option
   rowList.append(newRow)
   return rowList









productA=""
Url = """https://img.teleflora.com/images/o_0/l_flowers:{productId},pg_6/w_368,h_460,cs_no_cmyk,c_pad/f_jpg,q_auto:eco,e_sharpen:200/flowers/{productId}/{productName}"""

df = pd.read_csv('teleflora_2019_sep_products_new.csv', usecols=lambda x: x in ['handleId', 'name', 'VariantType', 'collection', 'description', 'price', 'Category'])

outDF = pd.DataFrame(columns=['handleId','fieldType','name','description','productImageUrl','collection','sku','ribbon','price','surcharge','visible','discountMode','discountValue','inventory','weight','productOptionName1','productOptionType1','productOptionDescription1'])

rowList=[]

for index, row in df.iterrows():

   rowList.clear()
   variant = row['VariantType']

   if ('Standard' in variant):     
      productA = row['handleId']
      rowList = AddProduct(row, productA, rowList)
      rowList = AddVariant(row, productA, 'Standard', rowList)
   elif ('Deluxe' in variant):  
      rowList  = AddVariant(row, productA, 'Deluxe', rowList)
   elif ('Premium' in variant):
      rowList  = AddVariant(row, productA, 'Premium', rowList)
   else:  
       print("******  ERROR VARIANT WRONG    ***************")


   outDF = outDF.append(rowList, ignore_index=True)
       
export_csv = outDF.to_csv (r'telefloraProducts-out.csv', index = None, header=True)


