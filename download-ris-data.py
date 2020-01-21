"""
@author: Cristel Pelsser
@date: 26/08/2016
"""

"""
Input:
- directory of where to store the files

Output:
-download files from the yesterday for monitors rrc0 to rrc16 at 
http://data.ris.ripe.net

doc on RIS data is available here:
https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/ris-raw-data
"""

import os
import sys
import datetime
import subprocess

# ---------------------------
def ensure_dir(d):
    if not os.path.exists(d):
        print("creating dir %s" % d)
        os.makedirs(d)
# ---------------------------

# -----------main------------
if __name__ == '__main__':

  if len(sys.argv) < 2:
    print("Usage: download-ris-data <output dir>")
    sys.exit()

  yesterday = datetime.date.today()-datetime.timedelta(1)
  print("downloading data from %s" % str(yesterday))
  year = yesterday.year
  if yesterday.month < 10:
    monthstr = "0%d" % yesterday.month
  else:
    monthstr = str(yesterday.month)
  if yesterday.day < 10:
    daystr = "0%d" % yesterday.day
  else:
    daystr = str(yesterday.day)

  outputdir = sys.argv[1]
  ensure_dir(outputdir)

  #construct url to download files and download
  for i in range(17):
    if i < 10:
      monitor = "rrc0%d" % i
    else:
      monitor = "rrc%d" % i
    url_dir="http://data.ris.ripe.net/%s/%d.%s/" % (monitor, year, monthstr)
    #print(os.path.join(outputdir,monitor))
    ensure_dir(os.path.join(outputdir,monitor))
    temp_out_dir=os.path.join(outputdir,monitor,"%d.%s" % (year,monthstr))
    ensure_dir(temp_out_dir)
    # there is a routing table every 8 hours
    for j in range(0,24,8):
      if j <10:
        hour = "0%d00" % j
      else:
        hour = "%d00" % j
      f = "bview.%d%s%s.%s.gz" % (year, monthstr, daystr, hour)
      url = "%s%s" % (url_dir, f)
      subprocess.call(['curl', url, "--output", os.path.join(temp_out_dir,f)])
      print(url)
  
  

