import socket
import select
import sys
import pickle

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

def addBinaryUtil(a, b) : 
	result = "" 
	s = 0
	i = len(a) - 1 
	j = len(b) - 1
	while (i >= 0 or j >= 0) : 
		s += (ord(a[i]) - ord('0')) if(i >= 0) else 0 
		s += (ord(b[j]) - ord('0')) if(j >= 0) else 0
		result = chr(s % 2 + ord('0')) + result 
		s //= 2; 
		if i == 0 :
			if s == 1 :
				result = addBinaryUtil(result, '1')
		i -= 1 
		j -= 1
	return result
 
def addBinary(arr, n) : 
	result = "" 
	for i in range(n) : 
		result = addBinaryUtil(result, arr[i]) 
	return result

def flip(c) : 
    return '1' if (c == '0') else '0'
  
def OnesComplement(bin) : 
    n = len(bin)  
    ones = "" 
    twos = "" 
    for i in range(n): 
        ones += flip(bin[i])  
    return ones

def factors(num) :
	for i in range(2, num) :
		if num%i == 0 :
			break
	if i == (num-1) :
		return -1
	else :
		return i

def divideString(string, n) :
	temp = 0
	length = len(string)  
	chars = int(length/n)  
	equalStr = []
	if(length % n != 0) :  
			print("Sorry this string cannot be divided into " + str(n) +" equal parts.")  
	else :  
		for i in range(0, length, chars) :    
			part = string[ i : i+chars]  
			equalStr.append(part)
	res = addBinary(equalStr, n)
	checkSum = OnesComplement(res)
	equalStr.append(checkSum)
	return equalStr

def func(msg) :
	lst = []
	flag = '0'
	firstFactor = factors(len(msg))
	if firstFactor == -1 :
		msg += '0'
		firstFactor = factors(len(msg))
		flag = '1'
	lst.append(flag)
	lst.extend(divideString(msg, firstFactor))
	return lst

def verifyData(lst) :
	arr = []
	for i in range(1, len(lst) - 1) :
		arr.append(lst[i])
	print(arr)
	res = addBinary(arr, len(arr))
	res = addBinaryUtil(res, lst[len(lst)-1])
	res = OnesComplement(res)
	temp = "0" * (len(lst[1]))
	if res == temp :
		return 1
	else :
		return 0

#Driver Code
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
port = 10113
s.connect((IP_address, port))
while True:
    inputStream_list = [sys.stdin , s]
    read_sockets,write_socket,error_socket = select.select(inputStream_list,[],[])
    for socks in read_sockets:
        if socks == s:
            lt = socks.recv(2048)
            lt = pickle.loads(lt)
            string = ""
            if verifyData(lt) == 1 :
                for i in range(1, len(lt) - 1) :
                    string += lt[i]
                if lt[0] == '1' :
                    string = string[:-1]
                string = BinaryToString(string)
                print(string)
            else :
                print("--- Invalid Data ---")
        else :
            msg = input()
            if msg == 'bye' or msg == 'Bye':
                s.close()
                inputStream_list.remove(s)
                break
            msg = ''.join(format(ord(i), 'b') for i in msg)
            l = func(msg)
            l = pickle.dumps(l)
            s.send(l)
    if s not in inputStream_list:
        break
s.close()
