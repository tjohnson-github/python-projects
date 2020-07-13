import util
import sys
import pandas as pd
import math

categories = { 'Plant Food & Fertilizer': 119683,
               'Pest & Disease Control': 50365,
               'Tools & Hardware': 3186,
               'Lawn Care': 181051,
               'Pots & Containers': 2034
               }

df = pd.read_csv('master-garden-center-products.csv', usecols=lambda x: x in ['name', 'description', 'productImageUrl', 'collection', 'sku', 'price'],
                                                           converters={'sku': lambda x: str(x)} )


for index, row in df.iterrows():  

   print("SKU: {0}".format(row['sku']))
   df.loc[index,'*Action(SiteID=US|Country=US|Currency=USD|Version=941)'] = 'Add'

   category = '181051' 
   for key, value in categories.items():
      if key in row['collection']:
         category = value
         break          

   df.loc[index,'*Category'] = category
   df.loc[index,'*Title'] = row['name']
   df.loc[index,'Subtitle'] = ''
   df.loc[index,'*Description'] = row['description']
   df.loc[index,'*ConditionID'] = '1000'
   df.loc[index,'PicURL'] = row['productImageUrl']
   df.loc[index,'*Quantity'] = '5'
   df.loc[index,'*Format'] = 'FixedPrice'
   df.loc[index,'*StartPrice'] = row['price']
   df.loc[index,'BuyItNowPrice'] = ''
   df.loc[index,'*Duration'] = 'GTC'
   df.loc[index,'ImmediatePayRequired'] = ''
   df.loc[index,'*Location'] = 'MD, USA'
   df.loc[index,'GalleryType'] = ''
   df.loc[index,'PayPalAccepted'] = '1'
   df.loc[index,'PayPalEmailAddress'] = 'admin@johnsonsflorists.com'
   df.loc[index,'PaymentInstructions'] = ''
   df.loc[index,'StoreCategory'] = ''
   df.loc[index,'ShippingDiscountProfileID'] = ''
   df.loc[index,'DomesticRateTable'] = ''
   df.loc[index,'ShippingType'] = 'Calculated'
   df.loc[index,'ShippingService-1:Option'] = 'UPSGround'
   df.loc[index,'ShippingService-1:Cost'] = ''
   df.loc[index,'ShippingService-1:Priority'] = ''
   df.loc[index,'ShippingService-1:ShippingSurcharge'] = ''
   df.loc[index,'ShippingService-2:Option'] = ''
   df.loc[index,'ShippingService-2:Cost'] = ''
   df.loc[index,'ShippingService-2:Priority'] = ''
   df.loc[index,'ShippingService-2:ShippingSurcharge'] = ''
   df.loc[index,'DispatchTimeMax'] = '2'
   df.loc[index,'CustomLabel'] = str(row['sku'])
   df.loc[index,'ReturnsAcceptedOption'] = 'ReturnsAccepted'
   df.loc[index,'RefundOption'] = 'MoneyBack'
   df.loc[index,'ReturnsWithinOption'] = 'Days_30'
   df.loc[index,'ShippingCostPaidByOption'] = 'Buyer'
   df.loc[index,'AdditionalDetails'] = ''
   df.loc[index,'ShippingProfileName'] = ''
   df.loc[index,'ReturnProfileName'] = ''

   name = row['name'].upper()
   description = row['description'].upper()
   name_lb_pos_space = name.find(' LB')
   name_lb_pos = name.find('LB')

   desc_lb_pos_space = description.find(' LB')
   desc_lb_pos = description.find('LB')

   if name_lb_pos_space >= 0:
      weight_pos = name.rfind(' ', 0, name_lb_pos_space) + 1
      weight = name[weight_pos:name_lb_pos_space]
   elif name_lb_pos >= 0:
      weight_pos = name.rfind(' ', 0, name_lb_pos) + 1
      weight = name[weight_pos:name_lb_pos]
   elif desc_lb_pos_space >= 0:
      weight_pos = description.rfind(' ', 0, desc_lb_pos_space) + 1
      check_weight_size = desc_lb_pos_space - weight_pos 
      weight = description[weight_pos:desc_lb_pos_space]

      html_end_pos = weight.rfind('>',0,len(weight))
      if html_end_pos >= 0:
         weight = description[html_end_pos:len(weight)]


   elif desc_lb_pos >= 0:
      weight_pos = description.rfind(' ', 0, desc_lb_pos) + 1
      weight = description[weight_pos:desc_lb_pos]

      html_end_pos = weight.rfind('>',0,len(weight))
      if html_end_pos >= 0:
         weight = description[html_end_pos:len(weight)]

   else:
      weight = '5'

   try:
      weight = math.ceil(float(weight))  
   except Exception as ex:
      weight = 5


   print('weight {0}'.format(weight))

   df.loc[index,'WeightMajor'] = weight
   df.loc[index,'WeightMinor'] = '0'
   df.loc[index,'WeightUnit'] = 'lb'
   df.loc[index,'OriginatingPostalCode'] = '20895'

export_csv = df.to_csv (r'Ebay-Out-Products.csv', index = None, header=True, columns=[ '*Action(SiteID=US|Country=US|Currency=USD|Version=941)',
                                                                                    '*Category',
                                                                                    '*Title',
                                                                                    'Subtitle',
                                                                                    '*Description',
                                                                                    '*ConditionID',
                                                                                    'PicURL',
                                                                                    '*Quantity',
                                                                                    '*Format',
                                                                                    '*StartPrice',
                                                                                    'BuyItNowPrice',
                                                                                    '*Duration',
                                                                                    'ImmediatePayRequired',
                                                                                    '*Location',
                                                                                    'GalleryType',
                                                                                    'PayPalAccepted',
                                                                                    'PayPalEmailAddress',
                                                                                    'PaymentInstructions',
                                                                                    'StoreCategory',
                                                                                    'ShippingDiscountProfileID',
                                                                                    'DomesticRateTable',
                                                                                    'ShippingType',
                                                                                    'ShippingService-1:Option',
                                                                                    'ShippingService-1:Cost',
                                                                                    'ShippingService-1:Priority',
                                                                                    'ShippingService-1:ShippingSurcharge',
                                                                                    'ShippingService-2:Option',
                                                                                    'ShippingService-2:Cost',
                                                                                    'ShippingService-2:Priority',
                                                                                    'ShippingService-2:ShippingSurcharge',
                                                                                    'DispatchTimeMax',
                                                                                    'CustomLabel',
                                                                                    'ReturnsAcceptedOption',
                                                                                    'RefundOption',
                                                                                    'ReturnsWithinOption',
                                                                                    'ShippingCostPaidByOption',
                                                                                    'AdditionalDetails',
                                                                                    'ShippingProfileName',
                                                                                    'ReturnProfileName',
                                                                                    'PaymentProfileName',
                                                                                    'WeightMajor',
                                                                                    'WeightMinor',
                                                                                    'WeightUnit',
                                                                                    'OriginatingPostalCode'])
