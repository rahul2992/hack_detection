import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import re

def intertime(time_list):
	num = len(time_list)
	diff = []
	#print time_list
	for i in xrange(0, len(time_list) - 1):
		tmp = time_list[i+1] - time_list[i]
		diff.append(tmp)
	avg_inter_time = sum(diff)/num
	return avg_inter_time

file = 'ds_1_with_fields.csv'

data = pd.read_csv(file)

#start_time = []
#for time in data['start_time']:
	#t = datetime.datetime.fromtimestamp(time/1e3)
	#start_time.append(t)
#start_time = pd.Series(start_time)
#data = pd.concat([data, start_time], axis = 1)
#data = data.drop('start_time', axis = 1)
#data = data.rename(columns = {0: 'start_time'})


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
		
dataset = pd.DataFrame({'source_ip': src, 'num_packets': packets, 'num_bytes': bytes,
						'start_time': st_time})
						
#print dataset.head(20)		

tmp_mov = 0
stopper_mov = []
num_recs = len(stopper)
for j in xrange(0, num_recs):
	tmp_mov = sum(stopper[0:j+1])
	stopper_mov.append(tmp_mov)
test, test2 = [], []
lprev = 1
s_packets, s_num_attempts, s_source, s_avg_packets, s_bytes, s_avg_bytes, time_lst, s_avg_intertime = [], [], [], [], [], [], [], []
for j in xrange(0, len(stopper_mov)-1):
	split = stopper_mov[j]
	split_u = stopper_mov[j+1]
	#print 'split', split
	#print 'split_u', split_u
	recv_tmp = dataset.iloc[split:split_u, :]
	recv_source = recv_tmp.groupby('source_ip').groups
	#print 'recv:', recv_source
	
	#Creating the feature matrix
	for src, index_lst in recv_source.iteritems():
		#Number of attempts by each receiver
		#print 'source:', src
		num_attempts_tmp = len(index_lst)
		s_num_attempts.append(num_attempts_tmp)
		s_source.append(src)
		#test2.append(src)
		for index in index_lst:
			#Avg. number of packets by source
			s_packets_tmp = dataset['num_packets'].iloc[index]
			s_packets.append(s_packets_tmp)
			#Avg. number of bytes by source
			s_bytes_tmp = dataset['num_bytes'].iloc[index]
			s_bytes.append(s_bytes_tmp)
			
			#time intervals
			time = data['start_time'].iloc[index]
			time_lst.append(time)
			#print time
			
			#Count to find average
			lprev = len(index_lst)
			
			if (index == index_lst[len(index_lst) - 1]):
				#packets
				#test.append(index)
				avg_packets = sum(s_packets)/lprev
				s_avg_packets.append(avg_packets)
				s_packets = []
		
				#bytes
				avg_bytes = sum(s_bytes)/lprev
				s_avg_bytes.append(avg_bytes)
				s_bytes = []
				
				#Time 
				#print len(time_lst)
				time_sorted = sorted(time_lst)
				#print 'sorted', len(time_lst)
				avg_intertime = intertime(time_sorted)
				s_avg_intertime.append(avg_intertime)
				time_lst = []
				
print 'source', len(s_source)
print 'num_attempts', len(s_num_attempts)
print 'packet', len(s_avg_packets)
print 'bytes', len(s_avg_bytes)
print 'time', len(s_avg_intertime)

features = pd.DataFrame({'source_ip': s_source, 'num_attempts': s_num_attempts,
						 'avg_num_packets': s_avg_packets, 'avg_num_bytes': s_avg_bytes,
						 'avg_intertime': s_avg_intertime})
						 
attempts = features['num_attempts'].values
plt.hist(attempts, bins = 100, range = (0, 1000), alpha = 0.8)
plt.show()

packets = features['avg_num_packets'].values
plt.hist(attempts, bins = 100, range = (0, 200), alpha = 0.8)
plt.show()

attempts = features['avg_intertime'].values
plt.hist(attempts, bins = 100, range = (1000, 5000), alpha = 0.8)
plt.show()


				

		