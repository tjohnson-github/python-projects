import util
import sys
import time
import datetime




searchList = {"flower shop kensington md", 
          "flower shop olney md", 
          "flower shop washington dc",
          "flower shop in kensington md", 
          "flower shop in olney md", 
          "flower shop in washington dc",
          "florist kensington md", 
          "florist olney md", 
          "florist washington dc",
          "kensington md flower shop", 
          "olney md flower shop", 
          "washington dc flower shop",
          ""
          } 

keywords_dc = [
            "flower shop washington dc",
            "flower shop in washington dc", 
            "washington dc flower shop",
            "florist washington dc", 
            "florist in washington dc",
            "flower delivery washington dc",
            "flower delivery in washington dc",
            "same day flower delivery washington dc",
            "wedding flowers washington dc",
            "funeral flowers washington dc",
            "mothers day flowers washington dc", 
            "floral washington dc",
            "Washington DC florist",
            "Washington DC florists",
            "DC Metro Florist",
            "DC Metro Florists",
            "DC Florists",
            "DC Florist",
            "Washington DC Garden Center",
            "Washington DC Garden Center",
            "DC Garden Center",
            "DC Metro Florists",
            "DC Florists",
            "DC Florist"
            "florist near dc",
            "florist near washington dc",
            "flower shop near dc",
            "flower shop near washington dc"

           
            ]

keywords_olney = [
            "flower shop olney maryland", 
            
            "flower shop in olney maryland", 
           
            "olney maryland flower shop", 
           
            "florist olney maryland", 
           
            "florist in olney maryland", 
            "flower delivery olney maryland",
            "flower delivery in olney maryland", 
            "same day flower delivery olney maryland",
            "wedding flowers olney maryland",
            "funeral flowers olney maryland", 
            "mothers day flowers olney maryland", 
            "floral olney maryland", 
             "flower shop olney md", 
            
            "flower shop in olney md", 
           
            "olney md flower shop", 
           
            "florist olney md", 
           
            "florist in olney md", 
            "flower delivery olney md",
            "flower delivery in olney md", 
            "same day flower delivery olney md",
            "wedding flowers olney md",
            "funeral flowers olney md", 
            "mothers day flowers olney md", 
            "floral olney md",
            "florist near olney md",
             "flower shop near olney md"

           
            ]

keywords_kensington = ["flower shop kensington maryland", 
           
            "flower shop in kensington maryland", 
           
            "kensington maryland flower shop", 
           
            "florist kensington maryland", 
         
            "florist in kensington maryland", 
           
            "flower delivery kensington maryland", 
          
            "flower delivery in kensington maryland", 
           
            "same day flower delivery kensington maryland", 
           
            "wedding flowers kensington maryland", 
          
            "funeral flowers kensington maryland", 
      
            "mothers day flowers kensington maryland", 
          
            "floral kensington maryland", 
            "flowers kensington md",
            "flower shop kensington md", 
           
            "flower shop in kensington md", 
           
            "kensington md flower shop", 
           
            "florist kensington md", 
         
            "florist in kensington md", 
           
            "flower delivery kensington md", 
          
            "flower delivery in kensington md", 
           
            "same day flower delivery kensington md", 
           
            "wedding flowers kensington md", 
          
            "funeral flowers kensington md", 
      
            "mothers day flowers kensington md", 
          
            "floral kensington md", 
             "florist near kensington md",
             "flower shop near kensington md"
         
            ]


print("Start getting our Google ranking...");


rankList = list()

d = datetime.datetime.now().strftime('%m/%d/%Y')

print("Starting with Olney first...");

for searchText in keywords_olney: 
   try:
      rank = util.googleSearch(searchText, "johnsonsflorists.com",30)
      print("Rank: {0} : {1}".format(rank,searchText))
      rankList.append(rank)
      time.sleep(30)
   except Exception as ex:
      print("Error: {0}".format(ex))
      time.sleep(300)
      pass

rank = sum(rankList)/len(rankList)
print("Olney Rank: {0} : {1}".format(rank,"Average"))
log = "echo {0},{1},{2},,{3},{4},{5},{6},{7} >> google-daily-olney.csv".format(d,rank,rank,rankList[0],rankList[1],rankList[2],rankList[3],rankList[4])

print("CMD: {0}".format(log))

util.runCmd(log)

time.sleep(60)

rankList.clear()

print("Start Kensington...");

for searchText in keywords_kensington: 
   try:
      rank = util.googleSearch(searchText, "johnsonsflorists.com", 30)
      print("Rank: {0} : {1}".format(rank,searchText))
      rankList.append(rank)
      time.sleep(30)
   except Exception as ex:
      print("Error: {0}".format(ex))
      time.sleep(300)
      pass

rank = sum(rankList)/len(rankList)
print("Kensington Rank: {0} : {1}".format(rank,"Average"))
log = "echo {0},{1},{2},,{3},{4},{5},{6},{7} >> google-daily-kensington.csv".format(d,rank,rank,rankList[0],rankList[1],rankList[2],rankList[3],rankList[4])

print("CMD: {0}".format(log))

util.runCmd(log)

time.sleep(60)

rankList.clear()

print("Starting DC...");

for searchText in keywords_dc: 
   try:
      rank = util.googleSearch(searchText, "johnsonsflorists.com", 100)
      print("Rank: {0} : {1}".format(rank,searchText))
      rankList.append(rank)
      time.sleep(30)
   except Exception as ex:
      print("Error: {0}".format(ex))
      time.sleep(300)
      pass

rank = sum(rankList)/len(rankList)
print("DC Rank: {0} : {1}".format(rank,"Average"))
log = "echo {0},{1},{2},,{3},{4},{5},{6},{7} >> google-daily-dc.csv".format(d,rank,rank,rankList[0],rankList[1],rankList[2],rankList[3],rankList[4])

print("CMD: {0}".format(log))

util.runCmd(log)



print("Rank: {0} : {1}".format(sum(rankList)/len(rankList),"Average"))