import itertools
import numpy as np
import pandas as pd

## emission matrix
d = {'h' : [.4, .9],'g' : [.6, .1]}
em=pd.DataFrame(d,index=['r', 's'])

## transition matrix
g = {'r' : [.6, .2],'s' : [.4, .8]}
tr=pd.DataFrame(g,index=['r', 's'])

# intial testing with g,h,g and initial probabilities 0.5, 0.5
def forward(em,tr,obs):
    alpha_1s=0.5*em.loc['s',obs[0]]
    alpha_1r=0.5*em.loc['r',obs[0]]
    obs1=obs[1:]
    for x in obs1:
        a=alpha_1s*(tr.loc['s','r'])*em.loc['r',x]
        b=alpha_1r*(tr.loc['r','r'])*em.loc['r',x]
        c=alpha_1s*(tr.loc['s','s'])*em.loc['s',x]
        d=alpha_1r*(tr.loc['r','s'])*em.loc['s',x]
        alpha_1r=a+b
        alpha_1s=c+d
    alpha_1r=round(alpha_1r,4)
    alpha_1s=round(alpha_1s,4)

    z=alpha_1r+alpha_1s
    print('observed sequence {}'.format(obs))

    print('Total Probability of observed sequence is: {}'.format(z))
    print('probability of rain given the observed sequence is: {}'.format(alpha_1r))
    print('probability of sun given the observed sequence is: {}'.format(alpha_1s))

# testing with grumpy,happy

obs=['g','g','g','g']
forward(em,tr,obs)

# testing with grumpy,happy,grumpy,grumpy
obs=['h','h','h','h']
forward(em,tr,obs)


######## EXHAUSTIVE SEARCH ###


## setting up to create permutations with repetitions
states = ['r','s']
n = 2
 
def increment(arr):
    last = n - 1
    cut_off = len(states) - 1
 
    arr[last] += 1
 
    for i in range(last, 0, -1):
        if arr[i] > cut_off:
            arr[i] = 0
            arr[i - 1] += 1
        else:
            break
    return arr
 
def permutations(states, n):
    if len(states) <= 1: return
    if n == 0: return
 
    current = [0] * n
 
    out = []
    count = 0
 
    possibilities = len(states)**n
 
    while count < possibilities:
        new_permutation = []
 
        for i in range(0, n):
            j = current[i]
            new_permutation += [states[j]]
        out += [new_permutation]
 
        count += 1
        current = increment(current)
 
    return out
 
#print(permutations(states, n))
 
def exhaustive(tr,em,obs):
    obsv = len(obs)
    comb = list(itertools.product("sr",repeat=obsv))
    t= 0
    for i in comb:
        sub_t=0.5
        for j in range(1,obsv):
            if i[j-1] == "r":
                if i[j] == "r":
                    sub_t =  sub_t * tr.loc["r","r"]
                if i[j] == "s":
                    sub_t =  sub_t * tr.loc["r","s"]
            if i[j-1] == "s":
                if i[j] == "r":
                    sub_t =  sub_t * tr.loc["s","r"]
                if i[j] == "s":
                    sub_t =  sub_t * tr.loc["s","s"]
        for j in range(obsv):
            if i[j] == "r":
                if obs[j] == "h":
                    sub_t =  sub_t * em.loc["r","h"]
                if obs[j] == "g":
                    sub_t =  sub_t * em.loc["r","g"]
            if i[j] == "s":
                if obs[j] == "h":
                    sub_t =  sub_t * em.loc["s","h"]
                if obs[j] == "g":
                    sub_t =  sub_t * em.loc["s","g"]
        
        t = t + sub_t
    return t

exhaustive(tr,em,obs)












