import os
import myknx
import asyncio
import knx
import __main__
from asgiref.sync import async_to_sync


class wpf:
### Class defining the WPF stiebel eltron objects monitored
### each object hold the CAN BUS variable and the object's CAN message definition (elster table)
### additionally, the object's KNX group address and data point type are also stored 
### object.setval(value) will send the CAN read value to the knx bus
### object.print() will print its definition

        
        def __init__(self,xknx,nom,grpaddr,dpt,candest,unit,bus):
                self.xknx=xknx          # xknx instance
                self.nom = nom          # name of the object eg T Source
                self.grpaddr=grpaddr    # corresponding KNX group address
                self.dpt=dpt            # KNX data point type (1 ... 13)
                self.candest=candest    # can destination module 1=3, 2=6, 3=9, 4=C
                self.unit=unit          # can unit number, appears in front of fa byte in request
                self.val=0              # value read from can bus and sent to KNX bus
                self.bus=bus            # can bus

        def __str__(self):
                return f"{self.nom}({self.grpaddr}.{self.dpt} @ {self.candest} {self.unit} )"
        
        

        def print(self):
                print (self.nom,'\t',self.grpaddr,'\t',self.dpt,'\t',self.unit,' current value:',self.val,end='\n\n')

        @async_to_sync
        async def setval(self,val):

                global xknx
                self.val = val
                if __main__.debug: print('set ',self.nom, ' in knx group ',self.grpaddr, 'to ', val)
#                encval = myknx.encode_dpt9(val)
#                print(self.grpaddr,'   ', encval)
#                comd = "/usr/lib/knxd/groupwrite ip:192.168.1.18 "+self.grpaddr+' '+encval[0]+' '+encval[1] +">/dev/null"
#                print(comd)
#                os.system(comd) 

#
                self.xknx.write(self.grpaddr,val,knx.encode_dt_temp)

