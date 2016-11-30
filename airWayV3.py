'''
V3 版本的航线规划
处理的仍然是2维坐标
v2的主要问题就是无法跳出死循环，以及无法避免死循环的解所造成的影响

V3 的目标是将求解过程进行优化
需要解决一下问题
1. 对于给定的路线，能够产生出所有的线路规划集合
2. 优化算法，以适应新的三维坐标模式
3. 利用 idea 中的想法实现，保证动然三维最短路径同时起飞航线规划
'''

import pickle
from airWayV2 import MyMathTools, AirPlane, AirWay
import random
import matplotlib.pyplot as plt
import copy

class AirPlanPlus:
    def __init__(self):
        # 用于存储在给定的航班信息下的所有可能的航班起飞时间集合
        self.air_plan_list = []

    # 将当前的航班 now_air 和 exist_air_list 进行对比，看是否满足安全起飞条件
    # 同时，会对当前航班进行处理，但是又会符合一定的限制（如：起飞时间不能超过多少分钟）
    # todo:搞清楚 pyhon 如何修改传递值 如果不可以，对函数进行返回值改造
    def if_safe_up(self, now_air, exist_air_list, time_limit=100000):

        '''
        判断当前航班能否在已有的条件下起飞，如果可以，返回True，否则，返回False
        同时如果满足起飞限制，此函数会对航班的起飞时间进行修改

        :param now_air: 当前航班
        :param exist_air_list: 已经存在的航班限制列表
        :param time_limit: 时间限制
        :return: True表示满足条件，可以加入， False 表示不满足条件，不可以加入航班计划
        '''

        air = now_air

        # 对于每一个元素，对比三种限制，满足可以加入， 不满足则不可以加入
        # 同时，总体起飞时间限制在 time_limit 分钟内
        for item in exist_air_list:

            ifcorrect = False

            while not ifcorrect and air.upTime <= time_limit:
                # if nextWay.ifCrossSafe(item):
                #     print('cross safe')
                    # if nextWay.sameUpPointCheck(item):
                    #     print('up correct')
                        # if nextWay.sameDownPointCheck(item):

                if air.ifCrossSafe(item):
                    if air.sameUpPointCheck(item):
                        if air.sameDownPointCheck(item):
                            ifcorrect = True

                if not ifcorrect:
                    air.upTime += 0.5
                    # count += 1

            if air.upTime > time_limit:
                air.upTime = 0
                return -1

        return now_air.upTime

    def air_plan_of_2d(self, air_list, exist_air):
        '''
        递归方法： 基于已有的航班序列进行判断

        算法思路：
        首先随机选择一个航班，然后判断它是否能够安全起飞，如果可以，则加入当前的航班列表，并递归此流程
        否则，将整个列表删除（因为在此序列下无法产生有效的序列）

        :param air_list: 已有的航班序列
        :param exist_air: 未指派的航班序列
        :return:
        '''

        # air_plan = []

        # todo：保证算法已经穷尽了以 root_air 为起飞基准点的所有的可能
        # 解决方法1 ： 设计一个迭代算法，使得算法能够满足所有需求

        # 随机选择一个初始起飞点， 也可以自己指派
        if len(air_list) > 0:
            root_air = random.choice(air_list)
            air_list.remove(root_air)
            # air_list.remove(root_air)
        else:
            # print('error in this ')
            return False

        # print('now root air is :')
        # print(root_air.Up)
        # print(root_air.Down)

        # 输出
        # -----------------------------------------------
        # plan_num = 'the plan is :'
        # print('--------------------------------------------------------')
        # print(plan_num)
        #
        # for item in exist_air:
        #     air_str = str(item.UpName) + ' to ' + str(item.DownName) + ':' + str(item.upTime)
        #     print(air_str)
        #
        # self.air_plan_list.append(exist_air)
        # print('-------------------------------------------------------')
        # ------------------------------------------------

        # root_air = air_list[0]


        # todo: 保证航路的运行
        # todo: 保证 exist_air 的初始化
        # exist_air = []
        # exist_air.append(_air)

        # todo:如果有多种可以选择的方向，如何处理

        # 递归解决问题：
        # 如果没有航班未指派，那么判断当前航班能否加入航班计划，
        # 若能，加入，并且结束递归，否则，消除当前计划，并且结束递归
        # 如果有航班未指派，那么顺序选择航班，，如果满足条件，将余下的列表进入递归流程
        # 否则此方法不同，不进入递归流程

        # 构造函数，判断当前航班能否在限制条件下起飞
        # print('run this')
        if len(air_list) == 0: # 当余下的航班为0时，如果当前航班可以，则加入航班计划，否则清空序列

            time = self.if_safe_up(root_air, exist_air)
            if time == -1:
                del air_list, exist_air
                return False
            else:
                # root_air = self.if_safe_up(root_air, exist_air)
                root_air.upTime = time
                exist_air.append(root_air)

                # 输出
                # -----------------------------------------------
                plan_num = 'the plan is :'
                print(plan_num)

                for item in exist_air:
                    air_str = item.UpName + ' to ' + item.DownName + ':' + str(item.upTime)
                    print(air_str)

                print('------------------------------------------------------')

                return True
                # self.air_plan_list.append(exist_air)
                # ------------------------------------------------

                # print('run good')

        else: # 当前的航班不为0 ，如果当前的航班可以，则加入序列，继续递归过程，否则，清空序列，结束当前线路
            time = self.if_safe_up(root_air, exist_air)
            if time == -1:

                # print(self.if_safe_up(root_air, exist_air))

                del air_list, exist_air
                return False
            else:

                # print(self.if_safe_up(root_air, exist_air))
                # root_air = self.if_safe_up(root_air, exist_air)

                root_air.upTime = time
                exist_air.append(root_air)
                self.air_plan_of_2d(air_list, exist_air)

if __name__ == "__main__":

    # 生成航班信息 并且返回起飞 降落点信息
    # airWay, airUpPoint, airDownPoint = AirWay.randomDiffAirWay()
    airWay, airUpPoint, airDownPoint = AirWay.easyAirWay()

    # 航线输出
    # print(airWay)
    # print(airUpPoint)
    # print(airDownPoint)

    # 画图
    # for i in range(0, 24):
    #     plt. (airUpPoint[airWay[i][0]], airUpPoint[airWay[i][1]])


    # 将所有的航班信息进行赋值， 生成航班列表
    # airList = []
    # for item in airWay:
    #     for i in range(1, 3):

            # print(airUpPoint[item[0]])
            # print(airDownPoint[item[1]])

            # air = AirPlane(airNum=i, UpPoint=airUpPoint[item[0]], DownPoint=airDownPoint[item[1]], UpPointName=item[0], DownPointName=item[1], uptime=0)

            # print(air.number)
            # print(air.Up)
            # print(air.Down)
            # print(air.UpName)
            # print(air.DownName)
            # print(air.upTime)

            # airList.append(air)

    # 简化，只设置12条航班
    simp_air_list = []
    for item in airWay:
        # print(airUpPoint[item[0]])
        # print(airDownPoint[item[1]])
        air = AirPlane(airNum=0, UpPoint=airUpPoint[item[0]], DownPoint=airDownPoint[item[1]], UpPointName=item[0],
                           DownPointName=item[1], uptime=0)
        # print(air.number)
        # print(air.Up)
        # print(air.Down)
        # print(air.UpName)
        # print(air.DownName)
        # print(air.upTime)

        simp_air_list.append(air)

    # for air in airList:
    #     print(air.Up)
    #     print(air.Down)

    # print(airList)

    air_plan_plus = AirPlanPlus()

    # 所有方法递归
    count = 0
    for i in range(1, 100000):

        air_list = simp_air_list.copy()

        for item in air_list:
            item.upTime = 0

        # print(len(air_list))
        air_plan_plus.air_plan_of_2d(air_list, [])
        # print('error route')
        count += 1
    # air_plan_list = air_plan_plus.air_plan_list

    # print(air_plan_list)

    # count = 1
    # for plan_list in air_plan_list:
    #
    #     plan_num = 'the plan No.' + count + 'is :'
    #     print(plan_num)
    #     count += 1
    #
    #     for item in plan_list:
    #         air_str = item.UpName + ' to ' + item.DownName + ':' + item.upTime
    #         print(air_str)