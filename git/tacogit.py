import sys
try:
  print('v' + str(round(float(sys.argv[1][1:]) + 0.01, 2)))
except:
  print('v1.00')
