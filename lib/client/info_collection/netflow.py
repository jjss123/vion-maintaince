#coding:utf-8
from collections import namedtuple

def netdevs():
    ''' RX and TX bytes for each of the network devices '''
    with open('/proc/net/dev') as f:
        net_dump = f.readlines()

    device_data={}
    data = namedtuple('data',['rx','tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = {"recv":float(line[1].split()[0])/(1024.0*1024.0),
                                                "sent":float(line[1].split()[8])/(1024.0*1024.0)}

    return device_data
if __name__=='__main__':
    netdevs = netdevs()
    for dev in netdevs.keys():
        print '{0}: {1} MiB {2} MiB'.format(dev, netdevs[dev]['recv'], netdevs[dev]['sent'])
