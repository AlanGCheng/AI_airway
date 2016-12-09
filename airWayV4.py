# todo:111111 最新版本问题，首先基于随机航线进行可视化优化
# todo:此版本简化问题：在航线上面设置滞空点，并且考虑不同的起点终点情况下的路径规划
# 起点终点不等数量
# 起点终点距离不相等
# 终点考虑滞空情况（森林防火的灭火）并且此时限制其他的航班
# 终点的优先级设计（动态进行规划）

import matplotlib.pyplot as plt
# 图像问题，在每个线的中点标出此条航线的起飞时间
from airWayV2 import AirPlane
import random
from airWayV3 import AirPlanPlus


# 航班初始化：将航班数据进行初始化
class AirInit:
    def __init__(self):
        pass

    # 将航班信息和航线信息进行初始化
    def air_init(air_way_list):

        count = 0
        air_list = []
        for air_way in air_way_list:

            air = AirPlane(airNum=count, UpPoint=air_way[0], DownPoint=air_way[1], uptime=0, UpPointName='start', DownPointName='end')
            count += 1
            air_list.append(air)

        return air_list


# 进行绘图
class PlotAll:
    def __init__(self):
        pass

    def plot_point(self, list1, list2):

        for item in list1:
            plt.plot(item, '--')

        for item in list2:
            plt.plot(item, '--')

        plt.show()

    def plot_air_way(self, air_way_list):

        plt.axis([0, 300, 0, 250])

        # 将航班起落点进行标记
        xlist = []
        ylist = []
        for air_way in air_way_list:
            for item in air_way:
                xlist.append(item[0])
                ylist.append(item[1])
        plt.plot(xlist, ylist, 'bo')

        # 画出航班的航线
        # print('hello')
        for air_way in air_way_list:
            # print(air_way)
            [[x1, y1], [x2, y2]] = air_way

            # print('------')
            # print(x1)
            # print(y1)
            # print(x2)
            # print(y2)
            # print('------')

            plt.plot([x1, x2], [y1, y2])
            plt.text((x1+x2)/2, (y1+y2)/2, 'time')

        plt.show()

    def plot_air_way_with_time(self, air_list):
        pass


# 起点终点数量不等，每个终点降落不同数量的航班
class AirWayGenWithRandomPoint:
    def __init__(self):
        pass

    # 生成起点终点不相等，距离不相等的一组航班降落点
    def gene_new_air_way(self, up_point_num=12, down_point_num=10, fire_point_num=10, min_distance=100, max_distance=300):
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
        plot = PlotAll()
        plot.plot_air_way(air_way_list)

        # print('generate the new airway ')

    # 检查航线是否符合规范
    # def air_way_check(self):
    #     pass

    # 给定的每一个点，设定优先级
    # def set_priority_each(self):
    #     pass

    # 指定一个点，然后设置优先级
    # def set_priority_specially(self):
    #     pass

    # def generate_stay_point(self):
    #     pass

        return air_way_list


class ResultShow:
    def __init__(self):
        pass


class AirPlanV4(AirPlanPlus):
    def __init__(self):
        self.count = 0

    def plan_with_non_equal_point(self, air_list, exist_air):
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


                plt.axis([0, 400, 0, 400])

                for item in exist_air:
                    air_str = item.UpName + ' to ' + item.DownName + ':' + str(item.upTime)
                    plt.plot([item.Up[0], item.Down[0]], [item.Up[1], item.Down[1]], '--')
                    plt.text((item.Up[0] + item.Down[0])/3, (item.Up[1] + item.Down[1])/3, item.upTime)
                    print(air_str)

                plt.show()


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
    a = AirWayGenWithRandomPoint()
    air_way_list = a.gene_new_air_way()

    init = AirInit()
    air_info_list = AirInit.air_init(air_way_list=air_way_list)

    plan = AirPlanPlus()

    for i in range(1, 100000):

        air_list = air_info_list.copy()

        for item in air_list:
            item.upTime = 0

        # print(len(air_list))
        # plan.air_plan_of_2d(air_list, [])
        AirPlanV4.air_plan_of_2d(air_list, [])
