#!/usr/bin/env python3
import re
import sys
import struct
import hashlib
import socket

# inspired by C3CTF's POW
def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

if __name__ == '__main__':
    oooserver = "whooo-are-u.challenges.ooo"
    ooohelper = "whooo-are-u-helper.challenges.ooo"
    oooport = 5000
    x = 0
    y = 0
    testparam = " -f "
 
    f = open("cmd.sh", 'r')
    cmdlist = f.readlines()
    f.close()   
    
    for line in cmdlist:
        cmdlist[y] = re.sub(" ", testparam, line)    
        y = y + 1
 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ooohelper, oooport))

    while 1:
        data = s.recv(1024)
        if bytes(data) == "":
            break
        
        print(data) 
        
        flagmatch = re.findall('([a-zA-Z0-9]{64})', data.decode())
        if flagmatch:
            print("FLAG FOUND!!!")
        
        chalmatch = re.search("Challenge: (.*)\\nn: (.*)\\nS", data.decode())
        if chalmatch:
            print("Challenge: " + chalmatch.group(1))
            print("n: " + chalmatch.group(2))
            challenge = chalmatch.group(1)
            n = int(chalmatch.group(2))
            solution = solve_pow(challenge, n)
            print("Solution: " + str(solution))
            solution = str(solution) + "\n"
            s.send(bytes(solution.encode('ascii')))

        nocapacity = re.search("No capacity available.", data.decode())
        if nocapacity:
            print("No capacity available.")
            break

        shellfound = re.search("nobody@whooo-are-u-helper", data.decode())
        if shellfound:
            if x <= (len(cmdlist) - 1):
                print("Sending " + str(cmdlist[x]))    
                #cmd = cmdlist[x] + "\n"
                cmd = cmdlist[x]
                s.send(bytes(cmd.encode('ascii')))
                x = x + 1
                continue
            else:
                break
        
    s.shutdown(socket.SHUT_WR)
    s.close()

