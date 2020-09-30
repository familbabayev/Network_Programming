# Client-Server based UDP basic console application

## Scenario
The Spotify regional server warehouse provides music streaming services for the billions of clients 24/7. Spotify servers responding time are depend on clients load number. Because of this reason, the clients must wait for responding with regarding the next time schedule:

* First Interval: From 00:00 till 11:59 the maximum wait time is 1 second

* Second interval: From 12:00 till 16:59 the maximum wait time is 2 seconds

* Third Interval: From 17:00 till 23:59 the maximum wait time is 4 seconds

The backoffs of these intervals are increased exponentially by next factors:

* For the first and third intervals: doubles each iteration
* For the second interval: triples on each iteration

## Installation
```
git clone https://github.com/familbabayev/Network_Programming/tree/master/Lab1(UDP_Backoff)
```
Application uses built-in python 3.7.4 packages. No additional requirements.

## Usage
For server:
```
python3 UDP_Backoff_OOP.py server "" [-p]
```
For client:
```
python3 UDP_Backoff_OOP.py client [hostname] [-p]
```
The default value for port number is 1060.  