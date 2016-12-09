import collections
import matplotlib.pyplot as plt
import math
import random
import numpy as np
import pickle


# 可能会用到的数学方法
# check right
class MyMathTools:
    def __init__(self):
        pass

    # 求出交叉点信息，返回交叉点坐标
    # check right
    def crossPoint(self, Up1, Down1, Up2, Down2):

        '''

        :param Up1: 直线X的第一个点
        :param Down1: 直线X的第二个点
        :param Up2: 直线Y的第一个点
        :param Down2: 直线Y的第二个点
        :return: 两条*线段*的交叉点
        '''

        # pointCross = []

        # print('L1')
        # print(Up1)
        # print(Down1)
        #
        # print('L2')
        # print(Up2)
        # print(Down2)

        # 直线L1：
        k1 = (Down1[1] - Up1[1])/(Down1[0] - Up1[0])
        b1 = Up1[1] - k1*Up1[0]

        # 直线L2:
        k2 = (Down2[1] - Up2[1])/(Down2[0] - Up2[0])
        b2 = Up2[1] - k2*Up2[0]

        # 求出交点
        x = (b2 - b1)/(k1 - k2)
        y = k1*x + b1

        point_cross = [x, y]

        # print('pointCross')
        # print(pointCross)
        return point_cross


# 飞行航班类，包含航班的各种信息和一些需要用到的方法
class AirPlane:
    '''
    航班类
    '''

    def __init__(self, airNum, UpPoint, DownPoint, uptime, UpPointName, DownPointName):

        '''
        初始化航班类
        :param airNum: 航班编号
        :param UpPoint: 航班起飞点
        :param DownPoint: 航班降落点
        :param uptime: 航班起飞时间
        :param UpPointName: 航班起飞点名称
        :param DownPointName: 航班降落点名称
        '''

        self.number = airNum
        self.Up = UpPoint
        self.Down = DownPoint
        self.upTime = uptime
        self.UpName = UpPointName
        self.DownName = DownPointName

    # 计算航班经过某个给定点的时间
    # check right
    def time_through_the_point(self, pointLocation):

        '''

        求出当前航班通过指定地点的时间
        :param pointLocation: 待求取的位置坐标
        :return: 通过的具体时间

        '''

        distance = math.sqrt(np.square(pointLocation[1] - self.Up[1]) + np.square(pointLocation[0] - self.Up[0]))

        time = float(self.upTime) + float(distance)

        return time

    # 判断交叉点是否安全
    # 如果没有交叉，直接返回True 否则判定交叉点是否满足时间间隔
    def ifCrossSafe(self, comparedAir):

        # ifCross 用于判断航线是否交叉， 如果不交叉，直接返回True
        # 否则生成交叉点

        '''
        此函数主要用于判定两个航线是否交叉，如果不交叉，返回True（安全），
        否则计算两个航班通过的时间是否满足限制，如果是，则返回True， 否则返回False
        :param comparedAir: 用于对比的航班
        :return: 返回 True 表示交叉安全，False表示交叉不安全，需要调整时间
        '''

        ifCross = False

        if self.Up[1] > comparedAir.Up[1] and self.Down[1] < comparedAir.Down[1]:
            ifCross = True

        elif self.Up[1] < comparedAir.Up[1] and self.Down[1] > comparedAir.Down[1]:
            ifCross = True

        if not ifCross:
            return True
            # print('safe')

        else:
            mathtool = MyMathTools()
            CrossPoint = mathtool.crossPoint(Up1 = self.Up, Down1 = self.Down, Up2 = comparedAir.Up, Down2 = comparedAir.Down)
            # print(CrossPoint)

            if 20 >= self.time_through_the_point(CrossPoint) - comparedAir.time_through_the_point(CrossPoint) >= 5:
                return True
                # print('safe')
            elif 20 >= comparedAir.time_through_the_point(CrossPoint) - self.time_through_the_point(CrossPoint) >= 5:
                return True
                # print('safe')
            else:
                return False
                # print('not safe')

    def sameUpPointCheck(self, comparedAir):

        '''
        是否满足同一个起飞点的限制条件
        如果不是同一个起飞点，自动忽略
        如果是同一个起飞点，判断是否满足限制条件

        :param comparedAir: 用于进行对比的航班
        :return: True 表示符合限制， False 表示不符合限制
        '''

        # print(self.Up)
        # print(comparedAir.Up)

        if self.Up == comparedAir.Up:
            # todo:还存在未知问题
            if 20 >= abs(self.upTime - comparedAir.upTime) >= 0.5:
                return True
            # elif 20 >= comparedAir.upTime - self.upTime >= 0.5:
            #     return True
            else:
                return False
        else:
            return True

    # 是否满足同一个降落点的限制条件
    # 如果不是同一个降落点，自动忽略
    # 如果是同一个降落点，判断是否满足限制条件
    # 1 理论上，后来加入的时间都在后面
    def sameDownPointCheck(self, comparedAir):

        '''
        是否满足降落点限制

        :param comparedAir: 用于判断是否是同一个降落点
        :return: True表示满足条件 False表示不满足条件
        '''

        if self.Down == comparedAir.Down:
            selftime = self.upTime + math.sqrt(np.square(self.Down[1] - self.Up[1]) + np.square(self.Down[0] - self.Up[0]))
            comparedAirtime = comparedAir.upTime + math.sqrt(np.square(comparedAir.Down[1] - comparedAir.Up[1]) + np.square(comparedAir.Down[0] - comparedAir.Up[0]))

            # print(selftime)
            # print(comparedAirtime)

            # if 20 >= selftime - comparedAirtime >= 5:
            #     return True
            if 20 >= abs(comparedAirtime - selftime) >= 5:
                return True
            else:
                return False
        else:
            return True


# 此类主要用于生成航线
class AirWay:
    def __init__(self):
        pass

    # 生成简单航线
    def easyAirWay():
        '''
        航线设置思路：
        所有起飞点和降落点在同一个水平线上
        起飞点之间相距20个单位间隔，降落点同样
        起飞点和降落点之间的垂直距离是100个单位距离
        航线暂时设置为从起飞点1 飞到 降落点12 的交叉航线，以此类推

        :return:airWay:是航线列表 airUpPoint:记录每个起飞点的坐标  airDownPoint：记录每个降落点坐标
        '''

        airUp = []
        for i in range(1,13):
            airUp.append('U' + str(i))

        airDown = []
        for i in range(1,13):
            airDown.append("D" + str(i))

        airUpPoint = collections.OrderedDict()
        originPoint = [0, 0]
        for item in airUp:
            airUpPoint.setdefault(item, originPoint)
            originPoint =[0, originPoint[1] + 20]

        airDownPoint = collections.OrderedDict()
        originPoint = [200, 0]
        for item in airDown:
            airDownPoint.setdefault(item, originPoint)
            originPoint =[200, originPoint[1] + 20]

        # print(airUp)
        # print(airDown)

        # print(airUpPoint)
        # print(airDownPoint)

        airWay = []
        for i in range(0, 12):
            airWay.append(['', ''])

        i = 0
        for item in airUpPoint.keys():
            airWay[i][0] = item
            i += 1

        i = 0
        for item in airDownPoint.keys().__reversed__():
            airWay[i][1] = item
            i += 1

        return airWay, airUpPoint, airDownPoint

    # 生成随机航线
    def randomAirWay():
        airWay = []

        airUpPoint = collections.OrderedDict()
        airDwonPoint = collections.OrderedDict()

        airUp = []
        for i in range(1,13):
            airUp.append('U' + str(i))

        airDown = []
        for i in range(1,13):
            airDown.append("D" + str(i))

        airUpPoint = collections.OrderedDict()
        originPoint = [0, 0]
        for item in airUp:
            airUpPoint.setdefault(item, originPoint)
            originPoint =[0, originPoint[1] + 20]

        airDownPoint = collections.OrderedDict()
        originPoint = [200, 0]
        for item in airDown:
            airDownPoint.setdefault(item, originPoint)
            originPoint =[200, originPoint[1] + 20]

        # 目标产生24条航线，12个起飞点，12个降落点

        airWay = []
        for i in range(0, 12):
            airWay.append(['', ''])

        i = 0
        for item in airUpPoint.keys():
            airWay[i][0] = item
            i += 1

        # 降落点随机安排
        # todo: 完善线路生成
        downPointList = list(airDownPoint.keys())
        for i in range(0, 12):
            # downPointList

            item = random.choice(downPointList)
            downPointList.remove(item)

            airWay[i][1] = item
            # i += 1

        return airWay, airUpPoint, airDownPoint

    # 随机生成航线，同时在同一个起飞点有不同的航线
    def randomDiffAirWay():

        airWay = []

        airUp = []
        for i in range(1, 13):
            airUp.append('U' + str(i))
        newAirUp = airUp + airUp


        airDown = []
        for i in range(1, 13):
            airDown.append("D" + str(i))
        newAirDown = airDown + airDown


        airUpPoint = collections.OrderedDict()
        originPoint = [0, 0]
        for item in airUp:
            airUpPoint.setdefault(item, originPoint)
            originPoint =[0, originPoint[1] + 20]

        airDownPoint = collections.OrderedDict()
        originPoint = [200, 0]
        for item in airDown:
            airDownPoint.setdefault(item, originPoint)
            originPoint =[200, originPoint[1] + 20]

        for i in range(0, 24):
            upitem = random.choice(newAirUp)
            downItem = random.choice(newAirDown)
            airWay.append([upitem, downItem])

            # print(upitem)
            # print(downItem)

            newAirUp.remove(upitem)
            newAirDown.remove(downItem)

        return airWay, airUpPoint, airDownPoint


class AirWayPlan:
    def __init__(self):
        pass

    def generateAirUpTime(self, airPlaneList, airUpPoint, airDownPoint):

        # 随机选取一个初始起飞点,初始起飞时间为0
        # print(airPlaneList)

        rootAir = random.choice(airPlaneList)
        # print(rootAir)

        airPlaneList.remove(rootAir)
        # rootAir.upTime = 0

        # 已经分配好时间的列表
        existAirTime = []
        existAirTime.append(rootAir)
        # print(rootAir.upTime)

        # todo:设计程序，使得程序可以自动适应，同时，生成以某一条线路为初始点的所有可能集合
        # todo：需要考虑的问题主要有：1.如何跳出无法求解的死集合 2.优化算法，减少时间复杂度
        # 在循环中遍历选择起飞点
        # 下一个起飞点应该满足如下条件：满足所有已有的起飞限制
        # 此条件可以简化为，起飞时间满足在所有的交叉点都比已有的线路慢0.5分钟以上（设置安全值0.6分钟），
        # 同同时满足同一个起飞点起飞时间限制和同一个降落点的降落时间限制
        # 时间步长设置为 0.01
        # todo：第一步，程序能够得出一组解
        for i in range(1, 24):

            # 循环的是航线
            nextWay = random.choice(airPlaneList)
            airPlaneList.remove(nextWay)

            # 对于已经存在且确定的航线，使得满足每一个航班信息：
            ifCorrect = False

            # 对于每一个循环，直到跑出结果为止
            for item in existAirTime:
                count = 0
                while ifCorrect == False:

                    count += 1
                    if count >= 60:
                        print('this way wrong')
                        break

                    # print(item.Up)
                    # print('now item ')
                    # print(item)

                    # todo:限制条件模拟

                    # 判断是否交叉
                    if nextWay.ifCrossSafe(item):
                        if nextWay.sameUpPointCheck(item):
                            if nextWay.sameDownPointCheck(item):
                                ifCorrect = True


                    if ifCorrect == False:
                        nextWay.upTime += 1

            existAirTime.append(nextWay)

        return existAirTime


if __name__ == "__main__":
    airWay, airUpPoint, airDownPoint = AirWay.randomDiffAirWay()

    airList = []
    for item in airWay:
        for i in range(1, 3):
            air = AirPlane(airNum=i, UpPoint=airUpPoint[item[0]], DownPoint=airDownPoint[item[1]], UpPointName=item[0], DownPointName=item[1], uptime=0)
            airList.append(air)

    plan = AirWayPlan()
    for item in plan.generateAirUpTime(airPlaneList=airList, airUpPoint=airUpPoint, airDownPoint=airDownPoint):
        print(str(item.number) + ':' + str(item.UpName) + 'to' + str(item.DownName) + ':' + str(item.upTime))

    # todo:线路生成完成后，编写动画类，模拟航线的顺序

    for item in airWay:
        pass

    plt.show()