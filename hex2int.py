def hex2int(hex):
    number = 0
    hex.reverse()
    for byte in hex:
        number = number * 256 + byte
    return number

def hex2int_2c(hex):
    mb = hex.pop()
    if mb >= 128:
        hex.reverse()
        mb = 0xFF - mb
        num = mb
        for b in hex:
            num = num*256+(0xFF-b)
        return -(num + 1)
    else:
        return hex2int(hex+[mb]) 