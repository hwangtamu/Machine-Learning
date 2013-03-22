__author__ = 'han wang'
#Q learning Algorithm implemented by Han Wang

import random
import matplotlib.pyplot as plt
M = {}
delta = 0.76
E = [2,4,8]

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
            M[item]['action'][a]['q'] = float(0)
            M[item]['action'][a]['visited'] = []
            if M[item]['action'][a]['dest'] == 5:
                M[item]['action'][a]['reward'] = 100
            else:
                M[item]['action'][a]['reward'] = 0
    M[5]['action'] = {}



    #some tables required
    M['table'] = []
    M['record'] = [300]
    M['abs'] = []
    for i in range(9):
        M['table'].append([0,0,0,0])

    #Q learning iteration
    while True:
        # randomly pick a state
        state = random.randint(0,8)
        while state != 5:
            if state == 5:
                break
            #randomly pick a legal action
            a = list(M[state]['action'])[random.randint(0,len(M[state]['action'])-1)]
            alt = [x for x in list(M[state]['action']) if x != a][random.randint(0,len(M[state]['action'])-2)]
            alpha = 1/float(2+len(M[state]['action'][a]['visited']))
            d = random.randint(0,99)
            if d < delta*100:
                if M[state]['action'][a]['dest'] == 5:
                    M[state]['action'][a]['q'] = (1-alpha)*M[state]['action'][a]['q']+alpha*(100)
                    M[state]['action'][a]['visited'].append(100)
                    break
                else:
                    M[state]['action'][a]['q'] = (1-alpha)*M[state]['action'][a]['q']+ \
                                                 alpha*(0.9*max_q(M[M[state]['action'][a]['dest']]))
                    M[state]['action'][a]['visited'].append(0)
                state = M[state]['action'][a]['dest']
            if d >= delta*100:
                if M[state]['action'][alt]['dest'] == 5:
                    M[state]['action'][a]['q'] = (1-alpha)*M[state]['action'][a]['q']+alpha*(100)
                    M[state]['action'][a]['visited'].append(100)
                    break
                else:
                    M[state]['action'][a]['q'] = (1-alpha)*M[state]['action'][a]['q']+ \
                                                 alpha*(0.9*max_q(M[M[state]['action'][alt]['dest']]))
                    M[state]['action'][a]['visited'].append(0)
                state = M[state]['action'][alt]['dest']

        s = 0
        for item in range(9):
            for a in M[item]['action']:
                s += M[item]['action'][a]['q']
        M['record'].append(s)
        M['abs'].append(abs(M['record'][-1]-M['record'][-2]))

        #termination condition
        if sum(M['abs'][-10:]) < 0.01:
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
            print str('%.2f' % M['table'][i][j])+'\t',
        print
    for i in E:
        for a in M[i]['action']:
            print M[i]['name'],a,float(sum(M[i]['action'][a]['visited']))/len(M[i]['action'][a]['visited'])
    plt.plot(M['abs'])
    plt.show()
