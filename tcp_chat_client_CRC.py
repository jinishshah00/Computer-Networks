import socket
import select
import sys

def xor(a, b) : 
    result = [] 
    for i in range(1, len(b)): 
        if a[i] == b[i]: 
            result.append('0') 
        else: 
            result.append('1') 
    return ''.join(result) 
  

def mod2div(divident, divisor) :
    pick = len(divisor) 
    tmp = divident[0 : pick] 
    while pick < len(divident): 
        if tmp[0] == '1': 
            tmp = xor(divisor, tmp) + divident[pick] 
        else:  
            tmp = xor('0'*pick, tmp) + divident[pick] 
        pick += 1
    if tmp[0] == '1': 
        tmp = xor(divisor, tmp) 
    else: 
        tmp = xor('0'*pick, tmp) 
    checkword = tmp 
    return checkword 
  
def encodeData(data, key) :
    l_key = len(key) 
    appended_data = data + '0'*(l_key-1) 
    remainder = mod2div(appended_data, key) 
    codeword = data + remainder 
    return codeword 

def decodeData(data, key) :
    rem = mod2div(data, key)
    temp = "0" * (len(key) - 1)
    if rem == temp :
        data = BinaryToString(data)
        print("-----received data is correct -----")
        print("<received>\n"+ data)
    else:
        print('-----Incorrect Data -----')

def BinaryToDecimal(binary) : 
	binary1 = binary 
	decimal, i, n = 0, 0, 0
	while(binary != 0): 
		dec = binary % 10
		decimal = decimal + dec * pow(2, i) 
		binary = binary//10
		i += 1
	return decimal	 

def BinaryToString(binData) :   
    strData =' '
    for i in range(0, len(binData), 7): 
        tempData = int(binData[i:i + 7])  
        decimalData = BinaryToDecimal(tempData) 
        strData = strData + chr(decimalData) 
    return strData

#Driver Code
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
port = 17066
s.connect((IP_address, port))
key = '1101'
while True:
    inputStream_list = [sys.stdin , s]
    read_sockets,write_socket,error_socket = select.select(inputStream_list,[],[])
    for socks in read_sockets:
        if socks == s:
            msg = socks.recv(2048)
            msg = msg.decode()
            decodeData(msg, key)
        else:
            msg = input()
            if msg == 'bye' or msg == 'Bye':
                s.close()
                inputStream_list.remove(s)
                break
            msg = ''.join(format(ord(i), 'b') for i in msg)
            msg = encodeData(msg, key)
            msg = msg.encode()
            s.send(msg)
            msg = msg.decode()
            print('\t <You> \n\t'+ msg)
    if s not in inputStream_list:
        break
s.close()
