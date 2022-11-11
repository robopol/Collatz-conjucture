import math
import sys

import matplotlib.pyplot as plt

print("""
****************************************************************************************
Collatz conjecture : 3n

Author: Ing. Robert Polak
Contact Info: robopol@robopol.sk
website: https://www.robopol.sk
Purpose:
        Collatz hypothesis test 3n,  
        n_int=int((3**a-2**a)/(2**b-3**a))
        
        delta=abs((3**a/2**b)*n_int-n_int) 

type: console program 
Copyright notice: This code is Open Source and should remain so.
To end the program, press 0 and the enter.
****************************************************************************************
""")
# def function enter numbers in the console.
def get_input():
    while True:
        try:
            print("Choose enter 1 for 3n-1 or 2 for 3n+1:")
            input_string=sys.stdin.readline()
            mode_collatz=int(input_string)            
            print("Enter the number fractal- begin, a=:")
            input_string=sys.stdin.readline()
            Num_1=int(input_string)
            print("Enter the number fractal- end, a=:")
            Num_2=int(sys.stdin.readline())

        except Exception:
            print("Please insert integer values")
            continue
        break
    return mode_collatz,Num_1, Num_2 

# Infinite while loop console. Main program
while True:
    # define constants
    min_list=[]; a_list=[]; delta_list=[]; difference_list=[]    
    # input numbers
    num=get_input()       
    # end of program    
    if num[0]==0 or num[1] == 0 or num[2] == 0:
        break         
    # define constant
    a=num[1]; max=num[2]
    # 3n-1
    if num[0]==1:
        # calculate collatz loop 3n
        while a<=max:        
            b=int((a*math.log(3))/math.log(2))
            n=(3**a-2**a)/(3**a-2**b)
            temp=n-int(n)
            if temp>=0.5:
                n_int=int(n)+1
            else:
                n_int=int(n)
            delta=abs((3**a/2**b)*n_int-n_int)
                                   
            a_list.append(a); min_list.append(delta); delta_list.append([a,delta])
            a+=1
            if a==num[1]+10: print("waiting...")    
        # plot graph
        plt.title(f'3n-1: Δ=abs((3**a/2**b)*n_int-n_int) for a={num[1]} ... a={num[2]}')
        plt.grid(True)           
        plt.xlabel("variable a: - the number of vertices")
        plt.ylabel("variable Δ: - remainder")
        plt.plot(a_list,min_list) 
        print("End of program")
        print("Field Δ is:, Δ=",delta_list)
        print("--------------------------------------------------------------------------------------")
        # condition for difference
        if num[1]+665<=num[2]:
            for i in range(len(delta_list)-666):
                difference_list.append(min_list[i+665]-min_list[i])
            print("Difference,(period T=665):",difference_list)    
        plt.show()
    # 3n+1
    if num[0]==2:
        # calculate collatz loop 3n
        while a<=max:        
            b=int((a*math.log(3))/math.log(2))+1
            n=(3**a-2**a)/(2**b-3**a)
            temp=n-int(n)
            if temp>=0.5:
                n_int=int(n)+1
            else:
                n_int=int(n)
            delta=abs((3**a/2**b)*n_int-n_int)
                                   
            a_list.append(a); min_list.append(delta); delta_list.append([a,delta])
            a+=1
            if a==num[1]+10: print("waiting...")    
        # plot graph
        plt.title(f'3n: Δ=abs((3**a/2**b)*n_int-n_int) for a={num[1]} ... a={num[2]}')
        plt.grid(True)           
        plt.xlabel("variable a: - the number of vertices")
        plt.ylabel("variable Δ: - remainder")
        plt.plot(a_list,min_list) 
        print("End of program")
        print("Field Δ is:, Δ=",delta_list)
        print("--------------------------------------------------------------------------------------")
        # condition for difference
        if num[1]+665<=num[2]:
            for i in range(len(delta_list)-666):
                difference_list.append(min_list[i+665]-min_list[i])
            print("Difference,(period T=665):",difference_list)    
        plt.show() 