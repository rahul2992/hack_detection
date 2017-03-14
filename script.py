import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import re

file = 'ds_1_with_fields.csv'

data = pd.read_csv(file)

start_time = []
for time in data['start_time']:
	t = datetime.datetime.fromtimestamp(time/1e3).strftime('%Y-%m-%d %H:%M:%S')
	start_time.append(t)
start_time = pd.Series(start_time)
data = pd.concat([data, start_time], axis = 1)
data = data.drop('start_time', axis = 1)
data = data.rename(columns = {0: 'start_time'})


num_sourceip = data['source_ip'].value_counts()
num_destinationip = data['destination_ip'].value_counts()
num_destports = data['destination_port'].value_counts()
num_sourceports = data['source_port'].value_counts()
num_num_packets = data['num_packets'].value_counts()
num_num_bytes = data['num_bytes'].value_counts()

#plt.hist(num_sourceip, bins = 100, range = (0,1000), alpha = 0.5)
#plt.hist(num_destinationip, bins = 100, range = (0, 1000), alpha = 0.5)
#plt.show()

#plt.hist(num_sourceports, bins = 100, range = (0, 10), alpha = 0.5)
#plt.hist(num_destports, bins = 100, range = (0, 10), alpha = 0.5)
#plt.show()

#plt.hist(num_num_packets, bins = 100, alpha = 0.8, range = (0,10))
#plt.hist(num_num_bytes, bins = 100, alpha = 0.8, range = (0,100))
#plt.show()

ip_regex = r"^([0-9]{2,3}\.[a-zA-Z0-9]{5})\.([a-zA-Z0-9]{5})\.([a-zA-Z0-9]{1,3}$)"

iprecv_last_two = []
for ip in data['destination_ip']:
	temp_ip = re.findall(ip_regex, ip)
	iprecv_last_two.append(temp_ip)

a = pd.Series(iprecv_last_two)

ip_recv_l1, ip_recv_l2, ip_recv_f1 = [], [], []
for ipa in iprecv_last_two:
	ip_recv_f1.append(ipa[0][0])
	ip_recv_l1.append(ipa[0][1])
	ip_recv_l2.append(ipa[0][2])

ip_recv_l1 = pd.Series(ip_recv_l1)
ip_recv_l2 = pd.Series(ip_recv_l2)
ip_recv_f1 = pd.Series(ip_recv_f1)


data = pd.concat([data, ip_recv_l1, ip_recv_l2, ip_recv_f1], axis = 1)
data = data.rename( columns = {0: 'ip_l1', 1: 'ip_l2', 2: 'ip_f1'})
data = data.drop('destination_ip', axis = 1)
data = data.drop('flags', axis = 1)
data = data.drop('site', axis = 1)
data = data.drop('asn', axis = 1)

#Create a dataframe for every receiver, with columns source, number of attempts, 
#average size of packet, average time difference between attempts, and avg. bytes
 
#Find number of sub regions in the data set
receivers = data.groupby('ip_f1').groups

#print data.head(20)

i = 0
src, packets, bytes, st_time, stopper = [], [], [], [], []
for rec in receivers:
	indexlist = receivers[rec]
	stopper.append(i)
	i = 0
	for index in indexlist:
		src_tmp = data['source_ip'].iloc[index]
		packets_tmp = data['num_packets'].iloc[index]
		bytes_tmp = data['num_bytes'].iloc[index]
		st_time_tmp = data['start_time'].iloc[index]
		
		src.append(src_tmp)
		packets.append(packets_tmp)
		bytes.append(bytes_tmp)
		st_time.append(st_time_tmp)
		
		i += 1
		
		
		
	



