#!/usr/bin/env python
#coding=utf-8
import os,sys
import socket
import time
import uuid
import wmi
import psutil
import datetime

# function of Get CPU State;
def getCPUstate(interval=1):
    cpu1 = psutil.cpu_count()
    print("CPU logic:", cpu1)
    return ("CPU utilization: " + str(psutil.cpu_percent(interval)) + "%")

def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory:%5s%% %6s/%s" % (
        phymem.percent,
        str(int(phymem.used / 1024 / 1024)) + "M",
        str(int(phymem.total / 1024 / 1024)) + "M"
    )
    return line

def getsysversion():
    ret = []
    c = wmi.WMI ()
    cpuname = c.Win32_Processor()[0].name
    bios = c.Win32_BIOS()[0]
    for sys in c.Win32_OperatingSystem():
        print("System Version:%s" % sys.Caption, "kernel:%s" % sys.BuildNumber)
        ret.append("System Version:%s" % sys.Caption+"kernel:%s" % sys.BuildNumber)
        print("OS Architecture:"+sys.OSArchitecture)
        ret.append("OS Architecture:"+sys.OSArchitecture)
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
                print("Physical disk: "+physical_disk.Caption)
                ret.append("Physical disk: "+physical_disk.Caption)
                break
#获取硬盘使用百分情况
    for disk in c.Win32_LogicalDisk (DriveType=3):
        print(disk.Caption, "Disk %0.2f%% free" % (100.0 * int(disk.FreeSpace)/int(disk.Size)))
        ret.append(disk.Caption+"Disk %0.2f%% free" % (100.0 * int(disk.FreeSpace)/int(disk.Size)))
    for bios_id in c.Win32_BIOS():
        print("BIOS Version:", bios.name)
        ret.append("BIOS Version:"+bios.name)
        print("BIOS SerialNumber:"+bios_id.SerialNumber.strip())
        ret.append("BIOS SerialNumber:"+bios_id.SerialNumber.strip())
        print("BIOS vender:", bios.Manufacturer)
        ret.append("BIOS vender:"+bios.Manufacturer)
        print('BIOS Release Date:', bios.ReleaseDate[0:8])
        ret.append('BIOS Release Date:'+bios.ReleaseDate[0:8])
    for cpu in c.Win32_Processor():
        print("CPU SKU:"+cpuname)
        ret.append("CPU SKU:"+cpuname)
        print("CPU SerialNumber:"+cpu.ProcessorId.strip())
        ret.append("CPU SerialNumber:"+cpu.ProcessorId.strip())
    print(getCPUstate())
    ret.append(getCPUstate())
    print(getMemorystate())
    ret.append(getMemorystate())
    return ret

# 获取Mac地址
def get_mac_address():
  mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
  return ":".join([mac[e:e+2] for e in range(0,11,2)])

# 获取主机名
hostname = socket.gethostname()
#获取IP
ip = socket.gethostbyname(hostname)
infolist = []
print("Host name:",hostname)
infolist = getsysversion()
print("IP:",ip)
print("Mac Address:",get_mac_address())
with open(os.getcwd()+"\\"+hostname+"_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".txt",'w') as f:
    f.write("Host name:"+hostname+"\n")
    for i in infolist:
        f.write(i+"\n")
    f.write("IP:"+ip+"\n")
    f.write("Mac Address:"+get_mac_address()+"\n")
    f.write("Current system time : "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]+"\n")
print("Log exists in the "+os.getcwd()+"\nExit after 10s...")
time.sleep(10)
sys.exit(0)
