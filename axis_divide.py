
import numpy as np
def axis_Divide(value,flag,zero_point=None):
    # [3, 6, 9, 12]
    zero_point=np.array(zero_point)
    zero_point.sort()
    # flag=0
    if flag==0:
        return value<zero_point[0]
    if flag>0 and flag<len(zero_point):
        return value>zero_point[flag-1] and value<zero_point[flag]
    if flag==len(zero_point):
        return value>zero_point[flag-1]

    # zero_point=[3,6,9,12]


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    xx=[i for i in range(20)]
    flags=[3,6,9,12]
    for i in range(len(flags)+1):
        y=[]
        for x in xx:
            if axis_Divide(x,i):
                y.append(1)
            else:
                y.append(0)
        plt.plot(xx,y,label=i)
    plt.legend()
    plt.show()

    # x=np.array([2,3,2,1])
    # x.sort()
    # print(x)
    # x=np.linspace(0,10,3)
    # print(x)