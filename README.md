# hack_detection
Detecting brute force hacking attempts on AT&T servers

This was an interesting unsupervised machine learning problem. The dataset consisted of brute force attacks on a server. 
A brute force attack is simply, when a source ip repeatedly tries to attack machines on a sub network for access. Once they get an access, the algorithm uses a dictioniary method to try password combinations. 

The data set looked like this - 

127.0.0.2 128.1.2.3 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:03 Thu

127.0.0.2 129.1.3.8 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:04 Thu

127.0.0.2 129.1.3.9 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:04 Thu

127.0.0.2 129.1.1.1 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:03 Thu

127.0.0.2 129.1.2.2 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:03 Thu

127.0.0.2 129.1.4.3 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:03 Thu

127.0.0.2 129.1.10.1 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:03 Thu

127.0.0.2 129.1.3.3 TCP 6000 22 1 40 ----S- xxxxxx r 2014-09-04 00:03:04 Thu

127.0.0.3 129.1.1.4 TCP 9367 22 17 3219 -AP-SF xxxxxx r 2014-09-04 00:04:52 Thu

1. The same source ip address attempts to access different machines on a sub net. 
2. The port of attack is same
3. Inter attack time is very small
4. Size of packet is small (40 bytes) 

This clearly showed a pattern. For the problem, I created the following feature space for each destination (sub domain) - 

Source IP | Number of attempts | Average packet size | Average byte sent | Time difference between attakcs

With the feature matrix, clusters can be easily created by KNN or Kernel density estimates. 


