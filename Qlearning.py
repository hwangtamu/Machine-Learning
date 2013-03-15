#Q learning Algorithm implemented by Han Wang

import random
import matplotlib.pyplot as plt
M = {}

# find max Q function for s and a
def max_q(M):
    tmp = []
    for a in M['action']:
        tmp.append(M['action'][a]['q'])
    return max(tmp)

if __name__ == '__main__':
    #build matrix
    for i in range(9):
        M[i] = {}
        M[i]['name'] = 'S'+str(i+1)
        M[i]['label'] = [i/3+1,i%3+1]
        M[i]['action'] = {}

    #define actions and their destinations
    M['actions'] = ['right','left','down','up']
    for item in range(9):
        if M[item]['label'][1] < 3:
            M[item]['action']['right'] = {}
            M[item]['action']['right']['dest'] = (M[item]['label'][0]-1)*3+M[item]['label'][1]
        if M[item]['label'][1] > 1:
            M[item]['action']['left'] = {}
            M[item]['action']['left']['dest'] = (M[item]['label'][0]-1)*3+M[item]['label'][1]-2
        if M[item]['label'][0] < 3:
            M[item]['action']['down'] = {}
            M[item]['action']['down']['dest'] = (M[item]['label'][0])*3+M[item]['label'][1]-1
        if M[item]['label'][0] > 1:
            M[item]['action']['up'] = {}
            M[item]['action']['up']['dest'] = (M[item]['label'][0]-2)*3+M[item]['label'][1]-1
    for item in range(9):
        for a in M[item]['action']:
            M[item]['action'][a]['q'] = 0
            if M[item]['action'][a]['dest'] == 5:
                M[item]['action'][a]['reward'] = 100
            else:
                M[item]['action'][a]['reward'] = 0
    M[5]['action'] = {}

    #some tables required
    M['table'] = []
    M['record'] = [300]
    M['abs'] = []
    M['sum'] = [0]
    for i in range(9):
        M['table'].append([0,0,0,0])

    #Q learning iteration
    while True:
        # random pick a state
        state = random.randint(0,8)
        while state != 5:
            if state == 5:
                break
            #random pick a legal action
            a = list(M[state]['action'])[random.randint(0,len(M[state]['action'])-1)]
            if M[state]['action'][a]['dest'] == 5:
                M[state]['action'][a]['q'] = 100
                break
            else:
                M[state]['action'][a]['q'] = 0.9*max_q(M[M[state]['action'][a]['dest']])
                state = M[state]['action'][a]['dest']
        s = 0
        for item in range(9):
            for a in M[item]['action']:
                s += M[item]['action'][a]['q']
        M['record'].append(s)
        M['abs'].append(abs(M['record'][-1]-M['record'][-2]))
        M['sum'].append(M['sum'][-1]+M['abs'][-1])
        if sum(M['abs'][-10:]) == 0:
            break


    #fill in data
    for item in range(9):
        if item != 5:
            for a in M[item]['action']:
                M['table'][item][M['actions'].index(a)] = M[item]['action'][a]['q']

    #print result
    print '\t',
    for i in range(len(M['actions'])):
        print M['actions'][i]+'\t',
    print
    for i in range(len(M['table'])):
        print M[i]['name']+'\t',
        for j in range(4):
            print str(M['table'][i][j])+'\t',
        print
    print M['sum']
    plt.plot(M['sum'])
    plt.show()
