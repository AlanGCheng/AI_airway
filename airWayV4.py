# todo:最新版本问题，首先基于随机航线进行可视化优化
# todo:此版本简化问题：在航线上面设置滞空点，并且考虑不同的起点终点情况下的路径规划
# 起点终点不等数量
# 起点终点距离不相等
# 终点考虑滞空情况（森林防火的灭火）并且此时限制其他的航班
# 终点的优先级设计（动态进行规划）

import matplotlib.pyplot as plt
from airWayV2 import AirPlane
import random


class AirInit:
    # 航班初始化：将航班数据进行初始化

    @staticmethod
    def air_init(list_of_air_way):
        # 将航班信息和航线信息进行初始化

        count = 0
        a_list = []
        for air_way in list_of_air_way:

            air = AirPlane(airNum=count, UpPoint=air_way[0], DownPoint=air_way[1], uptime=0, UpPointName='start', DownPointName='end')
            count += 1
            a_list.append(air)

        return a_list


class PlotAll:
    # 绘图函数集合

    @staticmethod
    def plot_point(list1, list2):
        # 画出两个列表中的点

        for item1 in list1:
            plt.plot(item1, '--')

        for item2 in list2:
            plt.plot(item2, '--')

        plt.show()

    @staticmethod
    def plot_air_way(list_of_air_way):
        # 画出航线

        plt.axis([0, 300, 0, 250])

        # 将航班起落点进行标记
        x_list = []
        y_list = []
        for air_way in list_of_air_way:
            for item1 in air_way:
                x_list.append(item1[0])
                y_list.append(item1[1])
        plt.plot(x_list, y_list, 'bo')

        # 画出航班的航线
        for air_way in list_of_air_way:
            [[x1, y1], [x2, y2]] = air_way

            plt.plot([x1, x2], [y1, y2])
            plt.text((x1+x2)/2, (y1+y2)/2, 'time')

        plt.show()


class AirWayGenWithRandomPoint:
    # 起点终点数量不等，每个终点降落不同数量的航班

    @staticmethod
    def gene_new_air_way(up_point_num=12, down_point_num=10, fire_point_num=10, min_distance=100, max_distance=300):
        # 生成起点终点不相等，距离不相等的一组航班降落点

        # 在二维图像上面生成随机的起飞降落点，然后设置直线线路，对交叉点再进行检测
        # 在起点和终点不等的情况下，首先假设每个终点可以接受的航班数量是无限的，
        # 这样能够保证飞机飞往着火点之后能够尽快返航

        # 设置起飞点，假设起飞点都是定值
        up_point_list = []
        for i in range(0, up_point_num):
            point = [0, 20*i]
            up_point_list.append(point)

        # 设置降落点，基于随机距离
        down_point_list = []
        for i in range(0, down_point_num):

            # print(random.randrange(1, 10)/10)
            # print(min_distance + (max_distance-min_distance)*random.randrange(1, 10)/10)

            point = [min_distance + (max_distance - min_distance)*random.randrange(1, 10)/10, 20*i]
            down_point_list.append(point)
        # print()

        air_way_list = []
        for i in range(0, 24):

            start = random.choice(up_point_list)
            end = random.choice(down_point_list)

            air_way = []
            air_way.append(start)
            air_way.append(end)

            # print(air_way)

            air_way_list.append(air_way)

        # print(air_way_list)

        # air_way_list = []
        # ----------------------------------------------------------
        # 画图
        # plot = PlotAll()
        # plot.plot_air_way(air_way_list)
        # ----------------------------------------------------------

        return air_way_list


class AirPlanV4():
    # def __init__(self):
    #     self.count = 0

    # 将当前的航班 now_air 和 exist_air_list 进行对比，看是否满足安全起飞条件
    # 同时，会对当前航班进行处理，但是又会符合一定的限制（如：起飞时间不能超过多少分钟）
    # todo:搞清楚 pyhon 如何修改传递值 如果不可以，对函数进行返回值改造
    @staticmethod
    def if_safe_up(now_air, exist_air_list, time_limit=100000):

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

    @staticmethod
    def plan_with_non_equal_point(air_list, exist_air):
        # print('run good')

        # 随机选择一个初始起飞点， 也可以自己指派
        if len(air_list) > 0:
            root_air = random.choice(air_list)
            # print(root_air)
            air_list.remove(root_air)
        else:
            return False

        if len(air_list) == 0:
            # 当余下的航班为0时，如果当前航班可以，则加入航班计划，否则清空序列

            time = AirPlanV4.if_safe_up(root_air, exist_air)
            if time == -1:
                # print('del')
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

                plt.axis([0, 400, 0, 400])

                for item in exist_air:
                    air_str = item.UpName + ' to ' + item.DownName + ':' + str(item.upTime)
                    plt.plot([item.Up[0], item.Down[0]], [item.Up[1], item.Down[1]], '--')
                    plt.text((item.Up[0] + item.Down[0])/3, (item.Up[1] + item.Down[1])/3, item.upTime)
                    print(air_str)

                plt.show()

                print('------------------------------------------------------')

                return True

        else:
            # 当前的航班不为0 ，如果当前的航班可以，则加入序列，继续递归过程，否则，清空序列，结束当前线路
            time = AirPlanV4.if_safe_up(root_air, exist_air)
            if time == -1:

                del air_list, exist_air
                return False
            else:

                root_air.upTime = time
                exist_air.append(root_air)
                AirPlanV4.plan_with_non_equal_point(air_list, exist_air)

if __name__ == "__main__":
    # 首先生成随机的飞行路线
    a = AirWayGenWithRandomPoint()
    air_way_list = a.gene_new_air_way()

    # 基于已有的飞行路线对航班进行初始化
    init = AirInit()
    air_info_list = AirInit.air_init(air_way_list)

    for i in range(1, 100000):

        a_list = air_info_list.copy()

        for item in a_list:
            item.upTime = 0

        e_air = []
        AirPlanV4.plan_with_non_equal_point(a_list, e_air)