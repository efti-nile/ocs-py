import ocs, ocs_parser
import serial

par = ocs_parser.Parser()
opclosens = ocs.Ocs()
ser = serial.Serial('COM7', 115200)

    
while True:
    opclosens.lnd(par.lnd(list(ser.read(30))))
    

'''while True:
    dump = list(open(dumpPath, 'rb').read())

    if offset == 0 and realTime:
        offset = len(dump)
    
    numNewBytes = (len(dump) - offset) - n * 12
    
    for chunk in [dump[offset+n*12+i*12:offset+n*12+i*12+12] for i in range(0, numNewBytes // 12)]:
        OpCloSens.lnd(
            (hex2int_2c(chunk[0:2]), hex2int_2c(chunk[2:4]), hex2int_2c(chunk[4:6])),
            (hex2int_2c(chunk[6:8]), hex2int_2c(chunk[8:10]), hex2int_2c(chunk[10:12]))
        )

    n = n + numNewBytes // 12

    print(n)
            
    time.sleep(1);'''    
    
'''dump = list(open(dumpPath, 'rb').read())

numNewBytes = len(dump) - n * 12

for chunk in [dump[n*12+i*12:n*12+i*12+12] for i in range(0, numNewBytes // 12)]:
    OpCloSens.lnd(
        (hex2int_2c(chunk[0:2]), hex2int_2c(chunk[2:4]), hex2int_2c(chunk[4:6])),
        (hex2int_2c(chunk[6:8]), hex2int_2c(chunk[8:10]), hex2int_2c(chunk[10:12]))
    )

n = n + numNewBytes // 12'''


