#!/usr/bin/python3
from optparse import OptionParser
import sys
import subprocess
import uuid

def check():
	parser = OptionParser()
	parser.add_option('-H',help='hostaddress',dest='address')
	parser.add_option('-C',help='community',dest='community',default='public')
	parser.add_option('-w',help='warning threshold',dest='warning',default='80')
	parser.add_option('-c',help='critical threshold',dest='critical',default='90')
	parser.add_option('-S',help='string name',dest='statusMib',default="dpStatusMemoryStatus")
	parser.add_option('-i',help='active index',dest='index',default=0)
	parser.add_option('-m',help='mib table',action='store_true',dest='mib',default='/usr/share/snmp/mibs/DATAPOWER/drStatusMIB.txt')

	(options ,args)=parser.parse_args()
	activeIndex = options.index

	tmpfile=str(uuid.uuid4())

	str(subprocess.call("snmpwalk"+" -Oq"+" -v 2c"+" -c"+options.community+" "+options.address+" -m "+options.mib+" "+options.statusMib+" 2>/dev/null > /tmp/"+tmpfile,shell=True))

	file = open("/tmp/"+tmpfile,'r')

	data=[]
	for line in file:
		arr=line.split()
		data.append(arr)
	subprocess.call('rm -f /tmp/'+tmpfile,shell=True)
		
	defOutput 			= data[activeIndex][0]+"="+data[activeIndex][1]+""+data[activeIndex][2]
	perf0	= "'memoryUsage'="+data[0][1]+data[0][2]+";"+options.warning+";"+options.critical
	perf1 = "'totalMemory'="+data[1][1]+data[1][2]#+";"+options.warning+";"+options.critical
	perf2 = "'usedMemory'="+data[2][1]+data[2][2]#+";"+options.warning+";"+options.critical
	perf3	= "'freeMemory'="+data[3][1]+data[3][2]#+";"+options.warning+";"+options.critical
	perf4	= "'requestedMemory'="+data[4][1]+data[4][2]#+";"+options.warning+";"+options.critical
	perf5	= "'holdMemory'="+data[5][1]+data[5][2]+";"#+options.warning+";"+options.critical
	msg		= defOutput+"|"+perf0+" "+perf1+" "+perf2+" "+perf3+" "+perf4+" "+perf5

	if data[activeIndex][1] >= options.critical:
		print("CRIT - "+msg)
		sys.exit(2)
	elif data[activeIndex][1] >= options.warning and data[options.index][1] <= options.critical:
		print("WARN - "+msg)
		sys.exit(1)
	elif data[activeIndex][1] < options.warning:
		print("OK - "+msg)
		sys.exit(0)
	else :
		print("UNKW - Ups ... crazy stuff going on!")
		sys.exit(3)

if __name__ == "__main__":
	check()
