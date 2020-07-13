import util
import sys
import pandas as pd


comment=""

cBirthday=0
cAnniversary=0
cChristmas=0
cNewyears=0
cHolidays=0
cHanukkah=0
cValentines=0
cEaster=0
cMothersday=0
cFathersday=0
cThanks=0
cThinkingofyou=0
cDeath=0
cRecovery=0
cCongrats=0
cThanksgiving=0
cUnknown=0


df1 = pd.read_csv('.\weborders-old\Orders.csv', usecols=lambda x: x in ['Order ID', 'First Name', 'Last Name', 'Email', 'Comment', 'Date Added', 'Tag'])
df2 = pd.read_csv('.\weborders-old\Order Products.csv', usecols=lambda x: x in ['Order ID', 'Product ID', 'Name', 'Model'])

df = pd.merge(df1, df2, on=['Order ID', 'Order ID'])



for index, row in df.iterrows():
  

   try:
      comment = str(row['Comment']).replace('\n', ' ')
      df.loc[index,'Comment'] = comment
   except Exception as e:
      pass
   
   comment = comment.lower()

   tag=''


  tag = checkComment(comment,"")


   if 'Birthday' in tag:
      cBirthday += 1
   if 'Anniversary' in tag:
      cAnniversary += 1
   if 'Christmas' in tag:
      cChristmas += 1
   if 'Newyears' in tag:
      cNewyears += 1
   if 'Holiday' in tag:
      cHolidays += 1
   if 'Hanukkah' in tag:
      cHanukkah += 1
   if 'Valentine' in tag:
      cValentines += 1
   if 'Easter' in tag:
      cEaster += 1
   if 'Mothers' in tag:
      cMothersday += 1
   if 'Fathers' in tag:
      cFathersday += 1
   if 'Thanks' in tag:
      cThanks += 1
   if 'Thinkingofyou' in tag:
      cThinkingofyou += 1
   if 'death' in tag:
      cDeath += 1
   if 'recovery' in tag:
      cRecovery += 1
   if 'Congratulations' in tag:
      cCongrats += 1
   if 'Thanksgiving' in tag:
      cThanksgiving += 1
   if 'unknown' in tag:
      cUnknown += 1





   df.loc[index,'Tag'] = tag

   print(index)
   print(row)

print(df['Comment'])

export_csv = df.to_csv (r'CustomerTags.csv', index = None, header=True)



print("Birthday: " + str(cBirthday))
print("Anniversary: " + str(cAnniversary))
print("Thanksgiving: " + str(cThanksgiving))
print("Christmas: " + str(cChristmas))
print("New years: " + str(cNewyears))
print("Holiday: " + str(cHolidays))
print("Hanukkah: " + str(cHanukkah))
print("Valentines: " + str(cValentines))
print("Easter: " + str(cEaster))
print("Mothers day: " + str(cMothersday))
print("Fathers day: " + str(cFathersday))
print("Thanks: " + str(cThanks))
print("Thinking of you: " + str(cThinkingofyou))
print("Congratulations: " + str(cCongrats))
print("Death: " + str(cDeath))
print("Recovery: " + str(cRecovery))
print("Unknown: " + str(cUnknown))




def checkComment(comment, tag):

    if 'birthday' in comment:
      tag = 'Birthday'
   elif 'bday' in comment:
      tag = 'Birthday'
   elif 'annivers' in comment:
      tag = 'Anniversary'

   elif "valentine" in comment:
      tag = "Valentines"

   elif "v-day" in comment:
      tag = "Valentines"

   elif 'congrat' in comment:
      tag = 'Congratulations'

   elif 'thanksgiving' in comment:
      tag = 'Thanksgiving'

   elif 'hanukkah' in comment:
      tag = 'Hanukkah'
      
   elif 'christmas' in comment:
      tag = 'Christmas'

   elif 'easter' in comment:
      tag = 'Easter'

   elif 'xmas' in comment:
      tag = 'Christmas'

   elif 'new year' in comment:
      tag = 'Newyears' 

   elif 'holiday' in comment:
      tag = 'Holiday' 

   elif "death" in comment:
      tag = "death"   

   elif "loss" in comment:
      tag = "death"   

   elif "condolence" in comment:
      tag = "death"   

   elif "funeral" in comment:
      tag = "death" 

   elif "sorry" in comment:
      tag = "death" 

   elif 'prayers' in comment:
      tag = 'death'  

   elif 'will miss' in comment:
      tag = 'death'  

   elif 'sympathy' in comment:
      tag = 'death' 

   elif 'sympathies' in comment:
      tag = 'death' 

   elif 'in memory' in comment:
      tag = 'death' 

   elif 'our thoughts' in comment:
      tag = 'death' 

   elif 'my thoughts' in comment:
      tag = 'death' 

   elif 'deepest' in comment:
      tag = 'death' 

   elif 'spirit' in comment:
      tag = 'death' 

   elif 'mourning' in comment:
      tag = 'death' 

   elif 'known' in comment:
      tag = 'death' 

   elif 'praying' in comment:
      tag = 'death' 

   elif 'memories' in comment:
      tag = 'death' 

   elif 'memory' in comment:
      tag = 'death' 

   elif 'memoria' in comment:
      tag = 'death' 

   elif 'my heart goes out' in comment:
      tag = 'death' 

   elif 'peace' in comment:
      tag = 'recovery'

   elif 'get well' in comment:
      tag = 'recovery'

   elif 'get better' in comment:
      tag = 'recovery'

   elif 'recovery' in comment:
      tag = 'recovery'

   elif 'feeling better' in comment:
      tag = 'recovery'

   elif 'feeling' in comment and 'better' in comment:
      tag = 'recovery'

   elif 'feel better' in comment:
      tag = 'recovery' 

   elif 'heal' in comment:
      tag = 'recovery' 

   elif 'best wishes' in comment:
      tag = 'bestwishes'

   elif 'thank you' in comment:
      tag = 'Thanks'

   elif 'think of you' in comment:
      tag = 'Thinkingofyou'

   elif 'thinking of you' in comment:
      tag = 'Thinkingofyou'

   elif 'thinking about you' in comment:
      tag = 'Thinkingofyou'

   elif 'thanks' in comment:
      tag = 'Thanks'

   elif "happy mother" in comment:
      tag  = "Mothers"
         
   elif "mother" in comment and 'day' in comment:
      tag  = "Mothers"

   elif "moms" in comment and 'day' in comment:
      tag  = "Mothers"

   elif "father" in comment and 'day' in comment:
      tag  = "Fathers"

   else:
      tag = "unknown"

   return tag
