import collections
import matplotlib.pyplot as plt
import math
import random
import pylab
import numpy.linalg as linalg
import numpy as np


# 可能会用到的数学方法
class MyMathTools:
    def __init__(self):
        pass

    # 求出交叉点信息，返回交叉点坐标
    def crossPoint(self, Up1, Down1, Up2, Down2):

        '''

        :param Up1: 直线X的第一个点
        :param Down1: 直线X的第二个点
        :param Up2: 直线Y的第一个点
        :param Down2: 直线Y的第二个点
        :return: 两条*线段*的交叉点
        '''

        pointCross = []

        # 直线L1：
        k1 = (Down1[1] - Up1[1])/(Down1[0] - Up1[0])
        b1 = Up1[1] - k1*Up1[0]

        # 直线L2:
        k2 = (Down2[1] - Up2[1])/(Down2[0] - Up2[0])
        b2 = Up2[1] - k2*Up2[0]

        # 求出交点
        x = (b2 - b1)/(k1 - k2)
        y = k1*x + b1

        pointCross = [x, y]

        return pointCross


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

    # 判断当前航班和给定的航班是否有交叉
    # 输入： 进行比较的航班
    # 输出： 如果没有交叉就返回False， 如果有交叉就返回交叉点信息
    # def ifCross(self, comparedAir):
    #
    #     ifCross = False
    #     CrossPoint = []
    #
    #     if self.Up[1] > comparedAir.Up[1] and self.Down[1] < comparedAir.Down[1]:
    #         ifCross = True
    #     elif self.Up[1] < comparedAir.Up[1] and self.Down[1] > comparedAir.Down[1]:
    #         ifCross = True
    #     else:
    #         pass
    #
    #     # 如果交叉的话，求出交叉的点
    #     if ifCross:
    #         # cross = linalg.solve((y - self.Down[1])/(self.Up[1] - self.Down[1]) = (x - self.Down[0])/(self.Up[0] - self.Down[0]), (y - comparedAir.Down[1])/(comparedAir.Up[1] - comparedAir.Down[1]) = (x - comparedAir.Down[0])/(comparedAir.Up[0] - comparedAir.Down[0]))
    #         # a = np.array([],[])
    #         x0 = self.Down[0]
    #         y0 = self.Down[1]
    #
    #         x1 = self.Up[0]
    #         y1 = self.Up[1]
    #
    #         x2 = comparedAir.Down[0]
    #         y2 = comparedAir.Down[1]
    #
    #         x3 = comparedAir.Up[0]
    #         y3 = comparedAir.Up[1]
    #
    #         x = x2 + (x3-x2)*(y-y2) / (y3-y2)
    #         y = ( (y0-y1)*(y3-y2)*x0 + (y3-y2)*(x1-x0)*y0 + (y1-y0)*(y3-y2)*x2 + (x2-x3)*(y1-y0)*y2 ) / ( (x1-x0)*(y3-y2) + (y0-y1)*(x3-x2) )
    #
    #         CrossPoint = [x, y]
    #
    #
    #     if ifCross:
    #         return False
    #     else:
    #         return CrossPoint

    # 计算出经过某点的时间
    # 所有的时间都是以分钟为单位

    # 计算航班经过某个给定点的时间
    def timeThroughThePoint(self, pointLocation):

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
        CrossPoint = []

        # print('INFO')
        # print(self.Up)
        # print(self.Down)
        # print('----')
        # print(comparedAir.Up)
        # print(comparedAir.Down)
        # print("DONE")

        if self.Up[1] > comparedAir.Up[1] and self.Down[1] < comparedAir.Down[1]:
            ifCross = True
            # print('cross ture')
        elif self.Up[1] < comparedAir.Up[1] and self.Down[1] > comparedAir.Down[1]:
            ifCross = True
            # print("cross true")

        # # 如果不交叉，则航线是安全的，直接返回True
        # if not ifCross:
        #     return True

        # # 如果交叉的话，求出交叉的点
        # if ifCross:
        #     # cross = linalg.solve((y - self.Down[1])/(self.Up[1] - self.Down[1]) = (x - self.Down[0])/(self.Up[0] - self.Down[0]), (y - comparedAir.Down[1])/(comparedAir.Up[1] - comparedAir.Down[1]) = (x - comparedAir.Down[0])/(comparedAir.Up[0] - comparedAir.Down[0]))
        #     # a = np.array([],[])
        #     x0 = self.Down[0]
        #     y0 = self.Down[1]
        #
        #     x1 = self.Up[0]
        #     y1 = self.Up[1]
        #
        #     x2 = comparedAir.Down[0]
        #     y2 = comparedAir.Down[1]
        #
        #     x3 = comparedAir.Up[0]
        #     y3 = comparedAir.Up[1]
        #
        #     y = ((y0-y1)*(y3-y2)*x0 + (y3-y2)*(x1-x0)*y0 + (y1-y0)*(y3-y2)*x2 + (x2-x3)*(y1-y0)*y2 ) / ( (x1-x0)*(y3-y2) + (y0-y1)*(x3-x2) )
        #     x = x2 + (x3-x2)*(y-y2) / (y3-y2)
        #
        #     CrossPoint = [x, y]


        # 如果不交叉，直接返回True，表示交叉是安全的
        if not ifCross:
            return True
            # print('safe')
        else:
            # cross = linalg.solve((y - self.Down[1])/(self.Up[1] - self.Down[1]) = (x - self.Down[0])/(self.Up[0] - self.Down[0]), (y - comparedAir.Down[1])/(comparedAir.Up[1] - comparedAir.Down[1]) = (x - comparedAir.Down[0])/(comparedAir.Up[0] - comparedAir.Down[0]))
            # a = np.array([],[])
            # x0 = self.Down[0]
            # y0 = self.Down[1]
            #
            # x1 = self.Up[0]
            # y1 = self.Up[1]
            #
            # x2 = comparedAir.Down[0]
            # y2 = comparedAir.Down[1]
            #
            # x3 = comparedAir.Up[0]
            # y3 = comparedAir.Up[1]
            #
            # y = ((y0-y1)*(y3-y2)*x0 + (y3-y2)*(x1-x0)*y0 + (y1-y0)*(y3-y2)*x2 + (x2-x3)*(y1-y0)*y2 ) / ( (x1-x0)*(y3-y2) + (y0-y1)*(x3-x2) )
            # x = x2 + (x3-x2)*(y-y2) / (y3-y2)

            # CrossPoint = [x, y]

            mathtool = MyMathTools()
            CrossPoint = mathtool.crossPoint(Up1 = self.Up, Down1 = self.Down, Up2 = comparedAir.Up, Down2 = comparedAir.Down)
            # print(CrossPoint)

            if 20 >= self.timeThroughThePoint(CrossPoint) - comparedAir.timeThroughThePoint(CrossPoint) >= 5:
                return True
                # print('safe')
            elif 20 >= comparedAir.timeThroughThePoint(CrossPoint) - self.timeThroughThePoint(CrossPoint) >= 5:
                return True
                # print('safe')
            else:
                return False
                # print('not safe')

    # 是否满足同一个起飞点的限制条件
    # 如果不是同一个起飞点，自动忽略
    # 如果是同一个起飞点，判断是否满足限制条件
    def sameUpPointCheck(self, comparedAir):
        if self.Up == comparedAir.Up:
            # if self.upTime - comparedAir.upTime >= 0.5 and self.upTime - comparedAir.upTime <= 20:
            #     return True
            if comparedAir.upTime - self.upTime >= 0.5 and comparedAir.upTime - self.upTime <= 20:
                return True
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

        :param comparedAir: 用于判断是否是同一个降落点
        :return: True表示满足条件 False表示不满足条件
        '''

        if self.Down == comparedAir.Down:
            selftime = self.upTime + math.sqrt((self.Down[1] - self.Up[1])^2 + (self.Down[0] - self.Up[0])^2)
            comparedAirtime = comparedAir.upTime + math.sqrt((comparedAir.Down[1] - comparedAir.Up[1])^2 + (comparedAir.Down[0] - comparedAir.Up[0])^2)

            # if 20 >= selftime - comparedAirtime >= 5:
            #     return True
            if 20 >= comparedAirtime - selftime >= 5:
                return True
            else:
                return False
        else:
            return True


# 此类主要用于生成航线
class AirWay:
    def __init__(self):
        pass

    # 给定：航线起飞地点；航班平均速度；生成数据的时间间隔；时间限制
    # 输出：一个2列矩阵
    # 功能描述： 在满足从起点到终点的条件下, 同时满足时间限制， 随机生成一条线路
    # 为了保证在每一段时间之内符合平均速度，将随机数设置为偏角，然后每次的距离是固定的
    # 两者之间的距离就是到达的最小时间，基于此保证到达时间不超过最大时间
    # airStart 和 airEnd 都是元组型数据

    # def generateAirWay(airStart, airEnd, airVel, timeStep, minTime, maxTime):
    #
    #     # todo:如何保证生成的序列是在最小时间和最大时间之间的动态数据，而不是正好保证最大时间和最小时间（使用随机数，获取在最小时间基础上增加的比例）
    #     timeLimit = minTime + (maxTime - minTime) * random.random(0.2, 1)
    #
    #     #
    #     num = random.random(0, 1)
    #
    #     # 开始生成循环
    #     startPoint = airStart
    #     nextPoint = 0
    #
    #     airWay = []
    #     airWay.append(airStart)
    #     while nextPoint != airEnd:
    #         startPoint = nextPoint
    #         nextPoint = (startPoint[0] + timeStep * airVel * math.cos(random.random(0, 6.28)),
    #                      startPoint[0] + timeStep * airVel * math.sin(random.random(0, 6.28)))
    #
    #
    #         # 使用动态规划，在随机确定的时间中找到最佳的随机路线


    '''
    航线设置思路：
    所有起飞点和降落点在同一个水平线上
    起飞点之间相距20个单位间隔，降落点同样
    起飞点和降落点之间的垂直距离是100个单位距离
    航线暂时设置为从起飞点1 飞到 降落点12 的交叉航线，以此类推
    '''
    def easyAirWay():
        '''

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
        for i in range(0,12):
            airWay.append(['', ''])

        i = 0
        for item in airUpPoint.keys():
            airWay[i][0] = item
            i += 1

        i = 0
        for item in airDownPoint.keys().__reversed__():
            airWay[i][1] = item
            i += 1

        # for item in airUpPoint.keys(), airDownPoint.keys().__reversed__():
        #     print(item)
        #     # (item1, item2) = item
        #
        #     # airWay.append([item1, item2])

        # print(airWay)
        return airWay, airUpPoint, airDownPoint


class AirWayPlan:
    def __init__(self):
        pass

    # # 是否满足起飞时间限制
    # def limitOfUpTime(self, item1time, item2time, ifSamePoint=False):
    #     if not ifSamePoint:
    #         if item1time - item2time > 0.5 or item1time - item2time < 0.5:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True
    #
    # # 是否满足降落时间限制
    # def limitOfDownTime(self, item1time, item2time, ifSamePoint=False):
    #     if not ifSamePoint:
    #         if item1time - item2time >= 5 and item1time - item2time <= 20:
    #             return True
    #         elif item2time - item1time >= 5 and item2time - item1time <= 20:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True
    #
    # # 是否满足空间限制（交叉点距离）
    # # 通过交叉点的时间必须在 0.5 分钟以上
    # def limitOfLocation(self, item1, item2):
    #
    #     if item1.ifCross(item2):
    #         return True
    #     else:
    #         crossPoint = item1.ifCross(item2)
    #
    #     item1time = item1.timeThroughThePoint(crossPoint)
    #     item2time = item2.timeThroughThePoint(crossPoint)
    #
    #     if item1time - item2time > 0 and item1time - item2time <= 0.5:
    #         return False
    #     elif item2time - item1time > 0 and item2time - item1time <= 0.5:
    #         return False
    #     else:
    #         return True
    #
    # # 是否满足其他航线限制
    # def limitOfOtherWay(self, airWayList):
    #     pass

    # 生成起飞时间序列
    # 基本策略：在保持符合最低条件的情况下要有最高条件，减少资源浪费
    # 基本定义： 开始时间以0为初始，单位为分钟
    # airWay 是一组航班信息列表
    def generateAirUpTime(self, airPlaneList, airUpPoint, airDownPoint):

        # 随机选取一个初始起飞点,初始起飞时间为0
        rootAir = random.choice(airPlaneList)
        airPlaneList.remove(rootAir)
        rootAir.upTime = 0

        # 已经分配好时间的列表
        existAirTime = []
        existAirTime.append(rootAir)
        # print(rootAir.upTime)

        # 在循环中遍历选择起飞点
        # 下一个起飞点应该满足如下条件：满足所有已有的起飞限制
        # 此条件可以简化为，起飞时间满足在所有的交叉点都比已有的线路慢0.5分钟以上（设置安全值0.6分钟），
        # 同同时满足同一个起飞点起飞时间限制和同一个降落点的降落时间限制
        # 时间步长设置为 0.01
        for i in range(1, 24):
            nextWay = random.choice(airPlaneList)

            # 对于已经存在且确定的航线，使得满足每一个航班信息：
            ifCorrect = False

            while ifCorrect == False:
                for item in existAirTime:
                    # todo:限制条件模拟

                    # 判断是否交叉
                    if nextWay.ifCrossSafe(item):
                        # print('cross safe')
                        if nextWay.sameUpPointCheck(item):
                            # print('up correct')
                            if nextWay.sameDownPointCheck(item):
                                # print('down correct')
                                # print('alright')
                                # if nextWay.upTime - item.upTime > 1:
                                ifCorrect = True

                if ifCorrect == False:
                    item.upTime += 0.01
                    # print('item')
                    # print(item.upTime)

            existAirTime.append(nextWay)
            # print(nextWay.upTime)
            airPlaneList.remove(nextWay)

        return existAirTime


if __name__ == "__main__":

    airWay, airUpPoint, airDownPoint = AirWay.easyAirWay()
    # print(airWay)
    # print(airUpPoint)
    # print(airDownPoint)

    airList = []
    for item in airWay:
        for i in range(1, 3):
            air = AirPlane(airNum=i, UpPoint=airUpPoint[item[0]], DownPoint=airDownPoint[item[1]], UpPointName=item[0], DownPointName=item[1], uptime=0)
            airList.append(air)

    plan = AirWayPlan()
    for item in plan.generateAirUpTime(airPlaneList=airList, airUpPoint=airUpPoint, airDownPoint=airDownPoint):
        print(str(item.number) + ':' + str(item.UpName) + 'to' + str(item.DownName) + ':' + str(item.upTime))



            # airUpName = list(airUpPoint.keys())
    # airDownName = list(airDownPoint.keys())
    # print(airUpName)
    # print(airDownName)
    #
    # airUpList = airUpPoint.keys() # 起飞点顺序集合
    # airDownList = airDownPoint.keys() # 降落点顺序集合
    # # 起飞点坐标集合
    # airUpPointList = []
    # for item in airUpPoint.keys():
    #     airUpPointList.append(airUpPoint[item])
    #
    # airDownPointList = []
    # for item in airDownPoint.keys():
    #     airDownPointList.append(airDownPoint[item])
    #
    # # print(airUpPointList)
    # # print(airDownPointList)
    #
    # airList = []
    # for point in range(0, 12):
    #     for num in range(1, 3):
    #         air = AirPlane(airNum=num, UpPoint=airUpPointList[point], DownPoint=airDownPointList[point],
    #                        uptime=0, UpPointName=airUpName[point], DownPointName=airDownName[point])
    #         airList.append(air)
    #
    # # for item in airList:
    # #     print(item.number)
    # #     print(item.Up)
    # #     print(item.Down)
    # #     print(item.upTime)
    #
    #
    # # airList = []
    # # for item in airWay:
    # #     for i in range(1,3):
    # #         air = AirPlane(i, airUpPoint[item[0]], airDownPoint[item[1]], 0)
    # #         airList.append(air)
    # plan = AirWayPlan()
    # # planlist = []
    # for item in plan.generateAirUpTime(airPlaneList=airList, airUpPoint=airUpPoint, airDownPoint=airDownPoint):
    #     print(str(item.number) + ':' + str(item.UpName) + 'to' + str(item.DownName) + ':' + str(item.upTime))


    # print(airUpPoint)
    # for key in airUpPoint.keys():
    #     plt.plot(airUpPoint[key])
    #
    # print(airDownPoint)
    # for key in airDownPoint.keys():
    #     plt.plot(airDownPoint[key])
    #
    # plt.show()
