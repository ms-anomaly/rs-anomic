# RS-Anomic Dataset
The RS-Anomic dataset contains the performance metrics of 12 services, each having 19 performance metrics and varying numbers of response time metrics per service. Further, the anomaly data in the RS-Anomic dataset covers ten non-trivial anomalies that may occur in microservice applications. RS-Anomic contains 100464 normal and 14112 anomaly instances. This section describes the data collection process and various anomalies in the RS-Anomic dataset.

### Architecture of RobotShop ###
![alt text](https://github.com/ms-anomaly/rs-anomic/blob/main/images/application_architecture.png?raw=true)

The updated version of RobotShop consisting of implementations of collecting response times and simulating anomalies can be found [here](https://github.com/ms-anomaly/robot-shop)<br/>

### Data Usage
[normal_data.zip](https://github.com/ms-anomaly/rs-anomic/blob/main/normal_data.zip) and [anomaly_data.zip](https://github.com/ms-anomaly/rs-anomic/blob/main/anomaly_data.zip) consist of collected raw data in CSV format. Each behaviour consists of 24 CSVs (12 for cAdvisor data and 12 for response time data). Example of data loading and preprocessing is available in the load_data.py. To use load_data.py, extract normal_data.zip and anomaly_data.zip in the same folder and run load_data.py from the same folder (../rs-anomic$ python load_data.py). pytorch and pandas are required, tested on versions torch ```1.13.1+cu117``` and pandas ```1.5.3```.
<br/>
To reproduce the evaluation results evaluation of the state-of-the-art models [train.zip](https://github.com/ms-anomaly/rs-anomic/blob/main/train.zip) and [test.zip](https://github.com/ms-anomaly/rs-anomic/blob/main/test.zip) can be used. Training data consists of 80% of normal data since the models used for evaluation do not require anomalous data for the training phase, anomaly data are not used for training.
<br/> 
There are three testing scenarios with normal: anomalous behaviour ratios of 95:5, 90:10, and 60:40. For each scenario, 20% of normal data are merged with anomalous data respective to ratios. anomalous data consisted of ten anomaly types, with an equal number of samples for each type. <br/>
Due to the difference in the number of features for each microservice, the number of response times was unified to one feature by taking the summation of all response times recorded for each service

### Anomalous behaviours in RS-Anomic ###
These are the anomalies that are injected into the application to simulate anomalous behaviour. Also the commands for tools used for simulations are mentioned below for each anomaly. <br/>

* Service Down: If a microservice is not working and cannot respond to requests, it is referred to as a service down. Network problems, hardware malfunctions, or software glitches can cause service down. To simulate this issue, we manually terminated the service and observed how the remaining services continued functioning.

* High Concurrent User Load: When too many people try to access the microservice simultaneously, it can cause slow response times, timeouts, or service failures. To simulate a high concurrent user load, we used our load generation script to simulate 1500 concurrent users accessing the application. <br/>
Using our load generation script, we artificially generated 1000 users who are concurrently accessing the application.

* High CPU usage: A microservice with a poorly optimized algorithm, inefficient code, or increased load may cause the entire application to underperform, resulting in high CPU usage. To simulate high CPU usage, we ran 100 parallel threads that calculate the 1000000th Fibonacci number.<br />
```stress-ng --cpu 80 --cpu-load 25 --timeout 300s```

* High File I/O: This anomaly occurs when the microservice performs many file input/output operations leading to performance issues, such as slow response times and high CPU usage. We simulated high file I/O using a thread to read/write to a file continuously.<br />
```stress-ng --io 1 --hdd-bytes 100M --timeout 300s```

* Memory Leak: This fault occurs when a microservice is not releasing memory that is no longer needed. Over time, this can increase memory usage and cause the service to crash or become unresponsive. [Stress-ng](https://github.com/ColinIanKing/stress-ng) is used to continuously allocate memory without deallocating, which will simulate a memory leak.<br />
The following linux command is used to simulate 150 mb allocation over 30 minutes. We created a bash script where we simulate memory leak with rising memory allocation using this command with different parameters.<br />
```stress-ng --vm 1 --vm-bytes 150M -t 30m```

* Packet Loss: This anomaly occurs when packets of data sent between the microservice and other systems are lost due to network issues which result in slow response times, errors, or incomplete transactions. We use [Traffic Control(tc)](https://man7.org/linux/man-pages/man8/tc.8.html) to simulate network conditions where most packets are lost.<br />
The following Linux command is used to simulate 50% packet loss. <br />
```tc qdisc add dev eth0 root netem loss 50%```

* Response Time Delay: Response time delay occurs when a microservice takes longer than usual to respond to requests due to various factors, including high CPU usage, increased user load, network latency, or software bugs. <br/>
We simulate this behaviour by adding a delay time to API service calls.

* Out-of-Order Packets: Out-of-order packets in microservices is a common occurrence due to the distributed nature of the system and the use of asynchronous communication methods.<br />
The following command introduces packet reordering by 60% (reorder 60%) with a probability of 60%<br />
```tc qdisc add dev eth0 root netem delay 50ms reorder 60% 60%```

* Low Bandwidth: A significant deviation from the expected bandwidth usage can be caused by inefficient communication protocols, lack of load balancing, network hardware limitations, or improper network configurations.<br />
Using Traffic Control, this is simulated using the following command. It limits the bandwidth to 1 kbps and allows bursts of up to 64 kilobits with a latency of 100ms. <br />
```tc qdisc add dev eth0 root tbf rate 1kbps burst 64 latency 100ms```

* High Latency: Microservices rely heavily on network communication to interact with each other, and any increase in latency can cause delays in the response time of the microservices, leading to a degraded user experience.<br />
The following Traffic Control command is used to increase the overall latency of a Docker container to 1000ms.<br />
```tc qdisc add dev eth0 root netem delay 1000ms```
