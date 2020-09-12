import middle_square_method

Caps = [chr(a) for a in range(65,91)]
Small = [chr(a) for a in range(97,123)]
Num = [chr(a) for a in range(48,58)]
ENCODE, DECODE = "encode", "decode"

"""
Convertors for Alphanumeric
"""

def caps(ROT, C):
    O = Caps.index(C)+ROT
    Cnew = Caps[O%26]
    return Cnew

def small(ROT, C):
    O = Small.index(C)+ROT
    Cnew = Small[O%26]
    return Cnew

def num(ROT, C):
    O = Num.index(C)+ROT
    Cnew = Num[O%10]
    return Cnew

"""
The Ceaser Cipher Control Unit
"""

def ceaser(ROT, C, ED = ENCODE):
    ROT = 52-int(ROT) if ED == DECODE else int(ROT)
    if C in Caps:
        return caps(ROT, C)
    elif C in Small:
        return small(ROT, C)
    elif C in Num:
        return num(ROT, C)
    else:
        return C

"""
Parsers for Files and Messages
"""

def msg_parse(CHR, ROT, ED = ENCODE):
    """ Basic TEXT replacement """
    Rots = middle_square_method.gen(str(ROT))
    XY = [(a,b) for a,b in zip(CHR,Rots)]
    TEXT = ''.join(map(lambda (x,y): ceaser(y, x, ED), XY))
    return TEXT

def file_parse(path, ROT, ED = ENCODE):
    """ Uses file as a string source """
    files = open(path)
    TEXT = msg_parse(files.read(),ROT,ED)
    return TEXT

"""
Send to File
"""

def writetofile(path, TEXT):
    """ TEXT is a list of characters including EOL characters """
    file = open(path, "w")
    file.write(''.join(TEXT))
    return None
