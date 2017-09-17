import socket, struct, os, sys, argparse, string, re, time, rstr
from datetime import date, datetime
from random import *

## Trials
TRIALS = 10000

## Generates
GEN_SIZE = 100

## Fitness Structure
EVAL_STRUCT = {}
STRUCT = []

## Default length for all the values except bool is 4
DEF_BIN_RANGE = 63
DEF_OCT_RANGE = 4095
DEF_INT_RANGE = 9999
DEF_HEX_RANGE = 65535
DEF_LENGTH_TP = 10
DEF_LENGTH_STR = 20

DEF_LENGTH_CODE = 3
DEF_LENGTH_KEY = 4

DEF_DATE_RANGE = 99999999999

def gen_bool(mode=''):
    if (mode == 'f'):
        return choice([True, False])
    return choice('01')
def gen_binary(length=DEF_BIN_RANGE):
    return bin(randint(-length, length))
def gen_octal(length=DEF_OCT_RANGE):
    return oct(randint(-length, length))
def gen_decimal(length=DEF_INT_RANGE):
    return randint(-length, length)
def gen_hex(length=DEF_HEX_RANGE):
    return hex(randint(-length, length))
def gen_float():
    return uniform(0, 9999)

def gen_tel():
    return '0' + choice(map(str, xrange(1,9))) + ''.join(choice(string.digits) for i in xrange(DEF_LENGTH_TP-2))

def gen_serialno(fmt='s', default='', code_len=DEF_LENGTH_CODE, key_len=DEF_LENGTH_KEY):
    if fmt=='s':
        if(default):
            return  ''.join(choice(string.digits) for i in xrange (key_len)) + default
        else:
            return ''.join(choice(string.digits) for i in xrange (key_len)) + ''.join(choice(string.ascii_letters) for i in xrange (code_len))
    elif fmt=='p':
        if(default):
            return  default + ''.join(choice(string.digits) for i in xrange (key_len))
        else:
            return ''.join(choice(string.ascii_letters) for i in xrange (code_len)) + ''.join(choice(string.digits) for i in xrange (key_len))

def gen_string(length=DEF_LENGTH_STR, mode='s'):
    if mode == 's' or mode == '':
        return ''.join(choice(string.ascii_letters) for i in xrange (randint(1, DEF_LENGTH_STR)))
    elif mode == 'm':
            return ''.join(choice(string.ascii_letters + ' '*15) for i in xrange (randint(1, DEF_LENGTH_STR)))             ##  string : space = 52 : 15    
def gen_ascii(length=DEF_LENGTH_STR, case='', mode='s'):
    if mode == 's' or mode == '':
        return ''.join([choice(string.ascii_letters + string.digits) for n in xrange(randint(1, DEF_LENGTH_STR))])
    elif mode=='m':
        return ''.join([choice(string.ascii_letters + string.digits + ' '*15) for n in xrange(randint(1, DEF_LENGTH_STR))])         ##  string : space = 52 : 15

def gen_ip():
    return socket.inet_ntoa(struct.pack('>I', randint(1, 0xffffffff)))

def gen_date():
    return str(date.fromtimestamp(uniform(1, DEF_DATE_RANGE)))

def generator(fmt):
    ev=[]
    for field in fmt:
        if field[0].lower() == 'string':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format[1] = ev_format[1].lower()
            ev_format[2] = ev_format[2].lower()
            ev_format.append(gen_string(mode=field[1].lower()))
            ev.append(ev_format)
        elif field[0].lower() == 'ascii':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format[1] = ev_format[1].lower()
            ev_format[2] = ev_format[2].lower()
            ev_format.append(gen_ascii(mode=field[1].lower()))
            ev.append(ev_format)
        elif field[0].lower() == 'tel':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_tel())
            ev.append(ev_format)
        elif field[0].lower() == 'serialno':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format[1] = ev_format[1].lower()
            ev_format[2] = ev_format[2].lower()
            ev_format.append(gen_serialno(default=field[1], fmt=field[2].lower()))
            ev.append(ev_format)
        elif field[0].lower() == 'ip':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_ip())
            ev.append(ev_format)
        elif field[0].lower() == 'bool':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            if field[1]:
                ev_format.append(gen_bool(mode=field[1].lower()))
            else:
                ev_format.append(gen_bool(mode=''))
            ev.append(ev_format)
        elif field[0].lower() == 'binary':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_binary())
            ev.append(ev_format)
        elif field[0].lower() == 'octal':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_octal())
            ev.append(ev_format)
        elif field[0].lower() == 'decimal':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_decimal())
            ev.append(ev_format)
        elif field[0].lower() == 'hex':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_hex())
            ev.append(ev_format)
        elif field[0].lower() == 'date':
            ev_format = [ x for x in field ]
            ev_format[0] = ev_format[0].lower()
            ev_format.append(gen_date())
            ev.append(ev_format)
    return ev

def eval_tel(field):
    if field[0] == 'tel':
        if str(field[1]).isdigit():
            return True
        else:
            return False
    else :
        return False
    
## Sructure : 'bool', 'mode: full | 0, 1'
def eval_bool(field):
    n_element = len(field)
    if (field[n_element-2] == 'f') and (field[n_element-1] in (True, False)):
        return True
    elif (field[n_element-2] == '') and (field[n_element-1] in (0, 1)):
        return True
    else:
        return False

## Sructure : 'binary', 'min value', 'max value'
def eval_binary(field):
    n_element = len(field)
    if (bin(field[n_element-3]) <= field[n_element-1] <= bin(field[n_element-2])):
        return True
    else:
        return False

## Sructure : 'octal', 'min value, 'max value'
def eval_octal(field):
    n_element = len(field)
    if (oct(field[n_element-3]) <= field[n_element-1] <= oct(field[n_element-2])):
        return True
    else:
        return False

## Sructure : 'decimal', 'min value', 'max value'
def eval_decimal(field):
    n_element = len(field)
    if (field[n_element-3] <= field[n_element-1] <= field[n_element-2]):
        return True
    else:
        return False
    
## Sructure : 'hex', 'min value', 'max value'
def eval_hex(field):
    n_element = len(field)
    if (hex(field[n_element-3]) <= field[n_element-1] <= hex(field[n_element-2])):
        return True
    else:
        return False

## Sructure : 'string | ascii', 'single | multiple', 'uppercase | lowecase', 'min size', 'max size'
def eval_any_string(field):
    n_element = len(field)
    if (field[n_element-3] <= len(field[n_element-1]) <= field[n_element-2]):
        if (field[n_element-5]=='m'):
            if (len(field[n_element-1].split()) >= 2):
                if (field[n_element-4] == 'l'):
                    field[n_element-1] = field[n_element-1].lower()
                elif(field[n_element-4] == 'u'):
                    field[n_element-1] = field[n_element-1].upper()
                return True
            else:
                return False
        elif (field[n_element-5]=='s' or field[n_element-5]==''):
            if (field[n_element-4] == 'l'):
                field[n_element-1] = field[n_element-1].lower()
            elif(field[n_element-4] == 'u'):
                field[n_element-1] = field[n_element-1].upper()
            return True
    else:
        return False

## Sructure : 'date', 'starting date', 'ending date'
def eval_date(field):
    n_element = len(field)
    d1 = time.mktime(datetime.strptime(field[n_element-3], "%Y-%m-%d").timetuple())
    d2 = time.mktime(datetime.strptime(field[n_element-2], "%Y-%m-%d").timetuple())
    d  = time.mktime(datetime.strptime(field[n_element-1], "%Y-%m-%d").timetuple())
    if ( d1 <= d <= d2 ):
        return True
    else:
        return False
    
## Sructure : 'ip', 'starting ip', 'ending ip'
def eval_ip(field):
    n_element = len(field)
    ip1 = struct.unpack("!L", socket.inet_aton(field[n_element-3]))[0]
    ip2 = struct.unpack("!L", socket.inet_aton(field[n_element-2]))[0]
    ip = struct.unpack("!L", socket.inet_aton(field[n_element-1]))[0]
    if ( ip1 <= ip <= ip2 ):
        return True
    else:
        return False


## Sructure : 'serialno', 'common word', 'suffix|prefix', 'uppercase | lowecase'
def eval_serialno(field):
    n_element = len(field)
    if(field[n_element-3] == 's' and field[n_element-4] and field[n_element-1].endswith(field[n_element-4])):
        if (field[n_element-2] == 'u'):
            field[n_element-1] = field[n_element-1].upper()
            return True
        elif (field[n_element-2] == 'l'):
            field[n_element-1] = field[n_element-1].lower()
            return True
        elif (field[n_element-2] == ''):
            field[n_element-1] = field[n_element-1]
            return True
    elif (field[n_element-3] == 's' and field[n_element-2] == 'u' and (re.search(r'\d+$', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1].upper()
            return True
    elif (field[n_element-3] == 's' and field[n_element-2] == 'l' and (re.search(r'\d+$', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1].lower()
            return True
    elif (field[n_element-3] == 's' and field[n_element-2] == '' and (re.search(r'^\d+', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1]
            return True
    elif(field[n_element-3] == 'p' and field[n_element-4] and field[n_element-1].startswith(field[n_element-4])):
        if (field[n_element-2] == 'u'):
            field[n_element-1] = field[n_element-1].upper()
            return True
        elif (field[n_element-2] == 'l'):
            field[n_element-1] = field[n_element-1].lower()
            return True
        elif (field[n_element-2] == 's'):
            field[n_element-1] = field[n_element-1]
            return True
    elif (field[n_element-3] == 'p' and field[n_element-2] == 'u' and (re.search(r'^\d+', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1].upper()
            return True
    elif (field[n_element-3] == 'p' and field[n_element-2] == 'l' and (re.search(r'^\d+', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1].lower()
            return True
    elif (field[n_element-3] == 'p' and field[n_element-2] == '' and (re.search(r'\d+$', field[n_element-1]).group()).isdigit()):
            field[n_element-1] = field[n_element-1]
            return True
    else:
        return False

def evaluator(fmt):
    breaker = 0
    for field in fmt:
        if (field[0] == 'string' or field[0] == 'ascii'):
            if not (eval_any_string(field)):
                breaker=1
                break
        elif (field[0] == 'serialno'):
            if not (eval_serialno(field)):
                breaker=1
                break
        elif (field[0] == 'tel'):
            if not(eval_tel(field)):
                breaker=1
                break
        elif (field[0] == 'bool'):
            if not (eval_bool(field)):
                breaker=1
                break
        elif (field[0] == 'binary'):
            if not (eval_binary(field)):
                breaker=1
                break
        elif (field[0] == 'octal'):
            if not (eval_octal(field)):
                breaker=1
                break
        elif (field[0] == 'decimal'):
            if not (eval_decimal(field)):
                breaker=1
                break
        elif (field[0] == 'hex'):
            if not (eval_hex(field)):
                breaker=1
                break
        elif (field[0] == 'date'):
            if not (eval_date(field)):
                breaker=1
                break
        elif (field[0] == 'ip'):
            if not (eval_ip(field)):
                breaker=1
                break
    if (not breaker):
        return fmt

def fitness(fmt):
    fit = 0
    arr = []
    for field in fmt:
        if (field[0] in ('string', 'ascii')):
            fit = fit + len(field[5])
            arr.append(field)
        elif (field[0] == 'serialno'):
            ## There is no functionality of serial number to calculate the fitness. Due to that in here it is ignored
            arr.append(field)
        elif (field[0] == 'tel'):
            ## There is no functionality of telephone number to calculate the fitness. Due to that in here it is ignored
            arr.append(field)
        elif (field[0] == 'ip'):
            ip_high = struct.unpack("!L", socket.inet_aton(field[2]))[0]
            ip_low = struct.unpack("!L", socket.inet_aton(field[1]))[0]
            ip = struct.unpack("!L", socket.inet_aton(field[3]))[0]
            fit = fit + int(ip) - int(ip_low)
            arr.append([field[0], ip_low, ip_high, field[3]])
        elif (field[0] == 'date'):
            d_high = time.mktime(datetime.strptime(field[2], "%Y-%m-%d").timetuple())
            d_low = time.mktime(datetime.strptime(field[1], "%Y-%m-%d").timetuple())
            d  = time.mktime(datetime.strptime(field[3], "%Y-%m-%d").timetuple())
            fit = fit + int((d-abs(d_low))/86400)
            arr.append((field[0], d_low, d_high, field[3]))
        elif (field[0] == 'binary'):
            fit = fit + int(field[3], 2)
            arr.append(field)
        elif (field[0] == 'octal'):
            fit = fit + int(field[3], 8)
            arr.append(field)
        elif (field[0] == 'decimal'):
            fit = fit + int(field[3])
            arr.append(field)
        elif (field[0] == 'hex'):
            fit = fit + int(field[3], 16)
            arr.append(field)
        elif (field[0] == 'bool' ):
            fit = fit + field[2]
            arr.append(field)
    if fit in EVAL_STRUCT.keys():
        EVAL_STRUCT[fit].append(arr)
    else:
        EVAL_STRUCT[fit] = (arr)

## if mode set to m include=' ' use the max to reproduce string
def reproduce(dictionary):
    for key in sorted(dictionary.keys(), reverse=True):
        testcase = []
        for arr in dictionary[key]:
            testcase.append(arr[len(arr)-1])
        STRUCT.append(testcase)

        for i in xrange(1, GEN_SIZE):
            new_test = []
            for element in dictionary[key]:
                if element[0] in ('string', 'ascii'):
                    if (element[1] == 'm'):
                        new_test.append(rstr.rstr(element[len(element)-1], len(element[len(element)-1]), element[4], include=' ',))
                    elif (element[1] == 's'):
                        new_test.append(rstr.rstr(element[len(element)-1]), len(element[len(element)-1]), element[4])
                    continue
                elif element[0] == 'serialno':
                    new_test.append(element[4].replace(filter(str.isdigit, str(element[4])), str(randint(1000, 9999))))
                    continue
                elif element[0] == 'tel':
                    new_test.append(gen_tel())
                    continue
                elif element[0] == 'ip':
                    new_test.append(socket.inet_ntoa(struct.pack('>I', randint(struct.unpack("!L", socket.inet_aton(element[3]))[0] , element[2]))))
                    continue
                elif element[0] == 'date':
                    new_test.append(str(date.fromtimestamp(uniform(time.mktime(datetime.strptime(element[3], "%Y-%m-%d").timetuple()) , element[2]))))
                    continue
                elif element[0] == 'bool':
                    new_test.append(gen_bool())
                    continue
                elif element[0] == 'binary':
                    if int(element[3], 2) < element[2]:
                        new_test.append(bin(randint(int(element[3], 2), element[2])))
                    else:
                        new_test.append(bin(randint(element[2], int(element[3], 2))))
                    continue
                elif element[0] == 'octal':
                    new_test.append(oct(randint(int(element[3], 8), element[2])))
                    continue
                elif element[0] == 'decimal':
                    new_test.append(randint(element[3], element[2]))
                    continue
                elif element[0] == 'hex':
                    new_test.append(hex(randint(int(element[3], 16), element[2])))
                    continue
            STRUCT.append(new_test)

def details():
    print("Initial Trials : "),
    print(TRIALS)
    print("Evaluated Test Cases : "),
    print(len(EVAL_STRUCT.keys()))
    print("Reproduced Test Cases : "),
    print(len(STRUCT))

##
##  This is the main function
##  User have to edit the argument field to get the required output
##
            
def main():
    for i in xrange(TRIALS):

        ##      ------- COMMENT THE UNWANTED FIELDS -------
        
        ##
        ##  --  START of Argument Field --
        ##


        ## GENERATE
        gen = generator(
            [
                
            ##  -- IP                   |       FORMAT  :   'IP', Staring IP, Ending IP
            ('IP','100.100.100.100', '255.255.255.0'),
            ##  -- IP

            ##  -- STRING               |       FORMAT  :   'ASCII', MODE ('S', 'M'), CASE ('L', 'U'), Min Length, Max Length
            ('STRING', 'M', 'U', 10, 20),
            ##  -- STRING

            ##  -- ASCII                |       FORMAT  :   'ASCII', MODE ('S', 'M'), CASE ('L', 'U'), Min Length, Max Length
            ('ASCII','M', 'U', 10, 20),
            ##  -- ASCII

            ##  -- SERIAL NO            |       FORMAT  :   'SERIALNO', KEY_CODE, PLACING ('S', 'P'), CASE ('L', 'U')
            ('SERIALNO', 'EMP', 'S', ''),
            ##  -- SERIAL NO

            ##  -- BOOL                 |       FORMAT  :   'BOOL', MODE ('f', '')
            ('BOOL','f'),
            ##  -- BOOL

            ##  -- BINARY               |       FORMAT  :   'BINARY', Min Value, Max Value
            ('BINARY', 9, 15),
            ##  -- BINARY

            ##  -- OCTAL                |       FORMAT  :   'OCTAL', Min Value, Max Value
            ('OCTAL', 100, 4095),
            ##  -- OCTAL

            ##  -- DECIMAL              |       FORMAT  :   'DECIMAL', Min Value, Max Value
            ('DECIMAL',1000, 9999),
            ##  -- DECIMAL

            ##  -- HEX                  |       FORMAT  :   'HEX', Min Value, Max Value
            ('HEX',1000, 65535),
            ##  -- HEX

            ##  -- DATE                 |       FORMAT  :   'DATE', Starting Date, Ending Date
            ('DATE','1970-01-02','2020-01-02'),
            ##  -- DATE

            ##  -- TEL                  |       FORMAT  :   'TEL'
            ('TEL',)
            ##  -- TEl
            
            ]
        )

        ##
        ##  -- END of Argument Field --
        ##

        ## EVALUATE
        selected = evaluator(gen)
        if (selected):
            ## FITNESS
            fitness(selected)

    ## REPRODUCE
    reproduce(EVAL_STRUCT)
    ## Printing Test Cases
    for test in STRUCT:
        print(test)
    details()

if __name__=='__main__':
    main()
