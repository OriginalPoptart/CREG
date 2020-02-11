import libbcm2835._bcm2835 as soc
import my_lib
import select
import sys
import time
import datetime
import threading
import socket
import telepot
import numpy as np
import matplotlib.pyplot as plt
import chart_functions_d as cf
import mysql_data_save as mysql
import os
import glob

ads = my_lib.ADS1256()
idNumber = ads.ReadID()

print("\nADS1256 reported ID value: {}".format(idNumber))

SPICS = 23
control_pin=20 
channel_A  = 0x30
channel_B  = 0x34
read_am=1500
tim = []
ad0 = []
ad1 = []
ad2 = []
ad3 = []

def temperature_1():
    file = open('/sys/bus/w1/devices/10-000000084899/w1_slave')
    filecontent = file.read()
    file.close() 
    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature = float(stringvalue[2:]) / 1000
    t_1 = '%6.2f' % temperature 
    return(t_1)

def Voltage_Convert(Vref,voltage):
    _D_=(65536*voltage/Vref)   
    return (_D_)

def Write_DAC8532(channel, Data):  
    Data = int(Data)
    soc.bcm2835_gpio_write(SPICS,1)     
    soc.bcm2835_gpio_write(SPICS,0)
    soc.bcm2835_spi_transfer(channel)
    soc.bcm2835_spi_transfer((Data>>8))
    soc.bcm2835_spi_transfer((Data&0xff))    
    soc.bcm2835_gpio_write(SPICS,1)
    
def send_text(msg):
    try:
        bot = telepot.Bot(token=" ")
        chat_id = " "
        command = msg
        bot.sendMessage(chat_id, text=command)
        print("send text")
    except Exception,ex:
        print(str(ex))
        
def connect_as_reciever():
    ar0=[]
    ar1=[]
    d_t=[] 
    count=0
    while True:        
        try:
            TCP_PORT = 5555
            BUFFER_SIZE = 1024
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', TCP_PORT))
            s.listen(1)
            while 1:
                try:                
                    conn, addr = s.accept()
                    data = conn.recv(BUFFER_SIZE)                
                    if data =="":
                        print("nothing from tcp")
                        conn.close()
                    elif data=="read":
                        read_ad()                      
                        s_data="Read all AD"
                        conn.send(s_data)                       
                    else:
                        Write_DAC8532(0x30, Voltage_Convert(5.0,0.0+float(data)/1000))
                        
                        #set_value(data)
                        data2 = "DA is set"
                        conn.send(data2) 
                except Exception ,ex:
                    #print("ER - 1 :",ex)
                    conn.close()
                    #break
        except Exception ,ex:
            a=2
            #print("ER -2 :",ex)
            

def read_ad():
    try:
        temp1=0
        c=0
        d=0
        volt=0
        amper=0
        ft = time.time()       
        ads.SetInputMux(ads.MUX_AIN3, ads.MUX_AIN7)        
        time.sleep(0.05)
        volt=ads.ReadADC()
        ads.SetInputMux(ads.MUX_AIN0, ads.MUX_AIN4)
        time.sleep(0.05)
        while 1:
            time.sleep(0.0001)
            ad0.append(ads.ReadADC())            
            tim.append(datetime.datetime.now())
            ad1.append(0)            
            ad2.append(0)            
            ad3.append(0)
            c=c+1
            d=d+1 
            if c==read_am:                
                ads.SetInputMux(ads.MUX_AIN1, ads.MUX_AIN5)
                time.sleep(0.05)
                c=0
                while 1:
                    time.sleep(0.0001)
                    ad1.append(ads.ReadADC())
                    tim.append(datetime.datetime.now())
                    ad0.append(0)                    
                    ad2.append(0)                   
                    ad3.append(0)
                    c=c+1
                    d=d+1
                    if c==read_am:                         
                        ads.SetInputMux(ads.MUX_AIN2, ads.MUX_AIN6)
                        time.sleep(0.05)
                        c=0
                        while 1:
                            time.sleep(0.0001)
                            ad2.append(ads.ReadADC())                            
                            tim.append(datetime.datetime.now())
                            ad0.append(0)
                            ad1.append(0)
                            ad3.append(0)                            
                            c=c+1
                            d=d+1
                            if c==read_am:
                                ads.SetInputMux(ads.MUX_AIN3, ads.MUX_AIN7)
                                time.sleep(0.05)
                                c=0
                                while 1:
                                    time.sleep(0.0001)                                    
                                    ad3.append(ads.ReadADC())
                                    tim.append(datetime.datetime.now())
                                    ad0.append(0)                                    
                                    ad1.append(0)                                    
                                    ad2.append(0)
                                    c=c+1
                                    d=d+1
                                    if c==read_am:
                                        temp1=temperature_1()
                                        temp1_date=datetime.datetime.now()
                                        ads.SetInputMux(ads.MUX_AIN0, ads.MUX_AIN4)
                                        time.sleep(0.05)
                                        c=0
                                        break
                                break
                        break
                break 
        if float(d)>100000:
            print("too much data for chart it will crash skipping chart show")
        else:
            copy_0=ad0[:]
            copy_1=ad1[:]
            copy_2=ad2[:]
            copy_3=ad3[:]
            copy_t=tim[:]
            copy_tmp=temp1
            copy_tmp_date=temp1_date
            
            d_val,cdis=mysql.chck_da_is_set()
            if cdis=='1':              
                Write_DAC8532(0x30, Voltage_Convert(5.0,0.0+float(d_val)/1000))
                mysql.update_da_is_set()              
            
            #cf.show_chart(ad0,ad1,ad2,ad3,tim)            
            mysql.write_to_db(copy_0,copy_1,copy_2,copy_3,copy_t,copy_tmp,copy_tmp_date)
            
        del tim [:]
        del ad0 [:]
        del ad1 [:]       
        del ad2 [:]
        del ad3 [:]              
        d=0
        c=0
        
    except Exception, ex:
        send_text("Error from Raspi 15 : " + str(ex))
        print("er at read_0"+str(ex))
        
if not soc.bcm2835_init():    
    print ("noit")
else:
    soc.bcm2835_spi_begin()
    soc.bcm2835_spi_setBitOrder(soc.BCM2835_SPI_BIT_ORDER_LSBFIRST )
    soc.bcm2835_spi_setDataMode(soc.BCM2835_SPI_MODE1)
    soc.bcm2835_spi_setClockDivider(soc.BCM2835_SPI_CLOCK_DIVIDER_1024)
    soc.bcm2835_gpio_fsel(SPICS, soc.BCM2835_GPIO_FSEL_OUTP)
    soc.bcm2835_gpio_fsel(control_pin, soc.BCM2835_GPIO_FSEL_INPT)    
    soc.bcm2835_gpio_write(SPICS, 0)
    while True:
        read_ad()
        #connect_as_reciever() 
