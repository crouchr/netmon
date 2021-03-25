netmon
======


REQS
----
- eliminate OpsView
- per second rtt and packet loss
- subnet to subnet
- use EC2
- generate alarms
- log into grafana
- configuration via Chef 


todo
====

create a class to define a host
each host is defined with a rtt threshold
each host is defined with a packet loss threshold

add other destinations - 192.168.1.1

send large packets to check for fragmentation issues
run iperf tests


iperf3 now running on mr-dell, PI, j1900 and kube

My thoughts
===========
replace ping with fping and add packet loss to the metrics

get a three-way using a containers:
mr-dell <-> kube
mr-dell <-> j1900
kube <-> j1900

get en EC2 instance in devvelopmentaws running docker and upload the container there 
in a known subnet (Internet)


NOTES from Steve
================
Use EC2 instances so can add other tools
Later tests = path tests e.g. MTU and large frames
Test from every subnet to every subnet
measure jitter at some point
key is in generating the confg - not easy to do by hand

Grafana visualisation
A -B
A-B
A-C etc
for investigating a particular src or destination
i.e. need to get the Grafan a taggin correct

later tests = DNS, http, SIP options

he feeds JSON file into a telegraf-based container