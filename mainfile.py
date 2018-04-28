#基于三次拉格朗日插值计算的图像放大
#date:2018/4/28
#name:Huang Weihao

from IPS import Image
import matplotlib.pyplot as plt
import time
import psutil
import  os
import numpy as np

def memory_usage_psutil():     # 返回内存使用情况（单位：MB）
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem


start=time.clock()          #设置时间起点
im = plt.imread("/users/wangfeng/Downloads/lena512color.tiff")
while(1):
    k=int(input("Please enter the length of the image (greater then or equal to {}):\n".format(len(im))))
    if k<=len(im):          #判断输入数值是否满足要求，是则执行语句，否则返回错误提示，并重新输入
        print("The valve you entered does not meet the requirement. Please enter again.\n")
    else:
        break
while(1):
    l=int(input("Please enter the height of the image (greater then or equal to {}):\n".format(len(im[0]))))
    if l<=len(im[0]):       #判断输入数值是否满足要求，是则执行语句，否则返回错误提示，并重新输入
        print("The valve you entered does not meet the requirement. Please enter again.\n")
    else:
        break
img=np.zeros((k,l,3))
for i in range(3):
    img[::,::,i]=Image.scale(k,l,im[::,::,i])
plt.imshow(np.uint8(img))
plt.show()
plt.imsave('lena.jpg', np.uint8(img))
print('Program running consumes {} MB of memory.\n'.format(memory_usage_psutil()))    #返回内存使用情况（仅供参考）
end=time.clock()            #设置时间终点
print('The program runs for {} seconds.\n'.format(end-start))                         #返回运行时间（仅供参考）