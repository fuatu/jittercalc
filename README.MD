# JitterCalc

We SREs in Trilogy as remote workers need to check the network quality as our connection 
is very important for our work. Also we need jitter calculation for some of the services or 
for interconnectivity of DCs. 

I was looking for a solution but couldn't find one.
So developed this one, free to use for everyone. 

## Binaries
The binaries are under bin folder.

## Some details to consider
- When the jitter for your gateway is low and the jitter for the external ip/host is high the problem may be with the ISP or the target site
- When both the jitter for gateway and external ip/host is high the problem is probably in your network
- When values are -10 it means ping failed
