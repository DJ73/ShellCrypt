def gen(seed):
    """ seed taken is a string of 4 characters """
    element = str(int(seed)**2).strip('0')
    while True:
        yield element
        element = str(int(element)**2).strip('0')
        while len(element)>4:
            if len(element)%2==0:
                element = element[1:-1]
            else:
                element = element[:-1]
 
