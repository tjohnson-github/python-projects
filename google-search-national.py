import util
import sys
import time
import datetime




searchList = {"local flower delivery", 
          "local flowers", 
          "local flowers near me",
          "flowers same day delivery", 
          "local flower shop",
          "local florist",
          "local florist shop",
          "local florist near me",
          "local flower delivery washington dc",
          "local flower delivery kensington md",
          "local flower delivery olney md",

          } 



rankList = list()

d = datetime.datetime.now().strftime('%m/%d/%Y')


for searchText in searchList: 
   try:
      rank = util.googleSearch(searchText, "localflowersonline", 100)
      print("Rank: {0} : {1}".format(rank,searchText))
      rankList.append(rank)
      time.sleep(30)
   except Exception as ex:
      print("Error: {0}".format(ex))
      time.sleep(300)
      pass

rank = sum(rankList)/len(rankList)
print("National Rank: {0} : {1}".format(rank,"Average"))
log = "echo {0},{1},{2},,{3},{4},{5},{6},{7} >> google-daily-national.csv".format(d,rank,rank,rankList[0],rankList[1],rankList[2],rankList[3],rankList[4])

print("CMD: {0}".format(log))

util.runCmd(log)


print("Rank: {0} : {1}".format(sum(rankList)/len(rankList),"Average"))