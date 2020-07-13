
import util
import sys
import time
import datetime


with open("trans_ids.txt") as f:
   for line in f:
      line = line.strip('\n')
      print("Trans_id: {0}".format(line))         
      util.PayPal_Trackers2(line)