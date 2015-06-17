#!/usr/bin/python3
# -*- coding: utf-8 -*-

ff=open('../docker/syslog.csv')
ff2=open('../docker/syslog2.csv',mode='w')

a=ff.readlines()

N=len(a)

ff.close()


for iii in range(N):
    line=a[iii]
    if iii==0:
        line='['+line
    if iii==(N-1):
        line=line.strip()+']'
    if line.endswith('}\n') and iii!=(N-1):
        line=line.replace('}\n','},\n')
    ff2.write(line)

ff2.close()
