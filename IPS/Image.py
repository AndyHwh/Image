#This module is used for calculating the Adaptive Image Scaling Third-order Lagrange Interpolation
#date: 2018/4/28
#name: Huang Weihao

import numpy as np


def Larange_3(x,y,n,bool):    #三次拉格朗日插值函数
    x2=[]
    for i in range(4):                            #创建"横坐标"数组，用于拉格朗日插值运算
        x2.append(np.ones_like(n)*i)
    x2=np.array(x2)
    t=np.zeros_like(n)                            #初始化t
    for i in range(4):
        u=np.ones_like(n)                         #初始化u
        for j in range(4):
            if i!=j:
                t2 = (x2[i, ::, ::]) - (x2[j, ::, ::])    #分解复杂公式u*=(x+n-x2[j,::,::])/(x2[i,::,::])-(x2[j,::,::]),提高程序运行效率
                u1 = (x + n - x2[j, ::, ::])
                u2 = u1 / t2
                u *= u2
        u3 = u * y[::, ::, i]                     #同理分解复杂公式,提高程序运行效率
        t += u3
    return t*bool                                 #滤去布尔值为false的点，使其值为零

def scale(h,l,image):
    ims=[]
    for r in range(2):
        if r==1:
            image = ims.T             #为方便统一场向与行向的缩放，转置行向缩放后的图像并赋值给新数组，
            l=h
        col = len(image[0])
        row = len(image)
        x = (col - 1) / (l + 1)     # 获取各点距离
        d = np.zeros((row, l , 6))  # 用于储存差值点的六个临近像素原点


        #【位置获取】获取插值点位置，并将其临近六个像素原点赋给新的数组
        deltax = []
        for i in range(l):
            deltax.append((i + 1) * x - int((i + 1) * x))
            e = int((i + 1) * x) - 2
            f = int((i + 1) * x) + 4
            if e > 0 and f < col:
                d[::, i, ::] = image[::, e:f:]
            else:
                if e <= 0:
                    d[::, i, ::] = image[::, 0:6:]
                    continue
                if f >= col:
                    d[::, i, ::] = image[::, -6::]

        delta_x = []                                 #将一维的数组扩展成二维数组，用于拉格朗日插值运算
        for i in range(row):
            delta_x.append(deltax)
        delta_x=np.array(delta_x)

        n1 = np.ones_like(delta_x) * 2             #用于拉格朗日插值运算，delta_x+n,n与delta_x为同型二维数组
        n2 = np.ones_like(delta_x)
        n3 = np.zeros_like(delta_x)

        f1_ave = np.mean(d[::, ::, 0:4:], 2)        #求平均值
        f2_ave = np.mean(d[::, ::, 1:5:], 2)
        f3_ave = np.mean(d[::, ::, 2: :], 2)


        #【方差计算】分别计算方差式子的每一项。目的：将复杂的运算分解，提高程序运行效率
        c1_1 = np.square(d[::, ::, 0]);c1_2 = np.square(d[::, ::, 1]);c1_3 = 4 * np.square(f1_ave)
        S1_2 = c1_1+c1_2-c1_3              #计算第一组数据方差
        c2_1 = np.square(d[::, ::, 1]);c2_2 = np.square(d[::, ::, 4]);c2_3 = 4 * np.square(f2_ave)
        S2_2 = c2_1+c2_2-c2_3              #计算第二组数据方差
        c3_1 = np.square(d[::, ::, 4]);c3_2 = np.square(d[::, ::, 5]);c3_3 = 4 * np.square(f3_ave)
        S3_2 = c3_1+c3_2-c3_3              #计算第三组数据方差


        #【方差比较】先分别比较各方差大小，再求方差最小值。返回以数据类型为布尔变量的数组。目的：将复杂的运算分解，提高程序运行效率
        s1_1=(S1_2 < S2_2);s1_2=(S1_2 <= S3_2);s1_3=(s1_1 & s1_2)
        s2_1 = (S2_2 < S3_2);s2_2 = (S2_2 <= S1_2);s2_3 = (s2_1 & s2_2)
        s3_1 = (S3_2 <S1_2);s3_2 = (S3_2 <= S2_2)
        s3_4 = (S3_2 == S1_2) & (S1_2 == S2_2)                          #将三个方差均相同的点额外赋给s3_3
        s3_3 = (s3_1 & s3_2| s3_4)


        #【拉格朗日插值计算】
        ims1 = ims2 = ims3 = ims = np.zeros((row, l))
        ims1 = Larange_3(delta_x, d[::, ::, 0:4:], n1, s1_3)
        ims2 = Larange_3(delta_x, d[::, ::, 1:5:], n2, s2_3)
        ims3 = Larange_3(delta_x, d[::, ::, 2: :], n3, s3_3)
        ims = ims1 + ims2 + ims3

    return ims.T                             #返回转置会原形的放大后的图像