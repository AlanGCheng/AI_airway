# 优化点：起点终点不等，同时航线不等距离
import math
import numpy as np
import random
import matplotlib.pyplot as plt


# 一些数学工具
class MyMathTools:

    # 求出交叉点信息，返回交叉点坐标
    @staticmethod
    def cross_point(up1, down1, up2, down2):

        # 直线L1：
        k1 = (down1[1] - up1[1])/(down1[0] - up1[0])
        b1 = up1[1] - k1*up1[0]

        # 直线L2:
        k2 = (down2[1] - up2[1])/(down2[0] - up2[0])
        b2 = up2[1] - k2*up2[0]

        # 求出交点
        x = (b2 - b1)/(k1 - k2)
        y = k1*x + b1

        point_cross = [x, y]

        return point_cross


# 飞机类
class AirPlane:

    # number Up Down up_time
    def __init__(self, air_num, up_point, down_point, up_time):

        self.number = air_num
        self.Up = up_point
        self.Down = down_point
        self.up_time = up_time

    # 计算航班经过某个给定点的时间
    def time_through_the_point(self, point_location):

        distance = math.sqrt(np.square(point_location[1] - self.Up[1]) + np.square(point_location[0] - self.Up[0]))
        time = float(self.up_time) + float(distance)

        return time

    # 判断交叉点是否安全，安全返回True，否则返回False
    def if_cross_safe(self, compared_air):

        # if_cross 用于判断航线是否交叉， 如果不交叉，直接返回True

        if_cross = False

        if self.Up[1] > compared_air.Up[1] and self.Down[1] < compared_air.Down[1]:
            if_cross = True

        elif self.Up[1] < compared_air.Up[1] and self.Down[1] > compared_air.Down[1]:
            if_cross = True

        if not if_cross:
            return True
            # print('safe')

        else:
            math_tool = MyMathTools()
            cross_point = math_tool.cross_point(up1 = self.Up, down1 = self.Down, up2 = compared_air.Up, down2 = compared_air.Down)
            # print(cross_point)

            if 20 >= self.time_through_the_point(cross_point) - compared_air.time_through_the_point(cross_point) >= 5:
                return True
                # print('safe')
            elif 20 >= compared_air.time_through_the_point(cross_point) - self.time_through_the_point(cross_point) >= 5:
                return True
                # print('safe')
            else:
                return False
                # print('not safe')

    # 判断同一起点是否安全
    def same_up_point_check(self, compared_air, min_safe_time=0.5, max_safe_time=20):

        if self.Up == compared_air.Up:
            # todo:还存在未知问题
            if max_safe_time >= abs(self.up_time - compared_air.up_time) >= min_safe_time:
                return True
            # elif 20 >= compared_air.up_time - self.up_time >= 0.5:
            #     return True
            else:
                return False
        else:
            return True

    # 判断同一终点是否安全
    def same_down_point_check(self, compared_air, min_safe_time=5, max_safe_time=20):

        if self.Down == compared_air.Down:
            self_time = self.up_time + math.sqrt(np.square(self.Down[1] - self.Up[1]) + np.square(self.Down[0] - self.Up[0]))
            compared_time = compared_air.up_time + math.sqrt(np.square(compared_air.Down[1] - compared_air.Up[1]) +
                                                             np.square(compared_air.Down[0] - compared_air.Up[0]))

            if max_safe_time >= abs(compared_time - self_time) >= min_safe_time:
                return True
            else:
                return False
        else:
            return True


# 生成给定数目起点终点的随机航线
class AirWayGenWithRandomPoint:

    # 起点终点数量不等，每个终点降落不同数量的航班
    @staticmethod
    def gene_new_air_way(up_point_num=12, down_point_num=10, min_distance=100, max_distance=300):

        # 设置起飞点，假设起飞点都是定值
        up_point_list = []
        for i in range(0, up_point_num):
            point = [0, 20 * i]
            up_point_list.append(point)

        # 设置降落点，基于随机距离
        down_point_list = []
        for i in range(0, down_point_num):
            point = [min_distance + (max_distance - min_distance) * random.randrange(1, 10) / 10, 20 * i]
            down_point_list.append(point)

        airway_list = []
        for i in range(0, 24):
            start = random.choice(up_point_list)
            end = random.choice(down_point_list)

            air_way = []
            air_way.append(start)
            air_way.append(end)

            airway_list.append(air_way)

        return airway_list


# 航班初始化：将航班数据进行初始化
class AirInit:

    # 将航班信息和航线信息进行初始化
    @staticmethod
    def air_init(list_of_air_way):

        count = 0
        a_list = []
        for air_way in list_of_air_way:

            air = AirPlane(air_num=count, up_point=air_way[0], down_point=air_way[1], up_time=0)
            count += 1
            a_list.append(air)

        return a_list


# 航班计划
class AirPlan:

    # 保存所有的航班计划，防止出现重复的航班计划
    def __init__(self):
        self.air_plan_list = []

    # 将选定航班和list 进行对比，如果安全，返回修改值的air，否则返回 -1
    @staticmethod
    def if_safe_up(air, exist_air_list, time_limit=100000):

        # 对于每一个元素，对比三种限制，满足可以加入， 不满足则不可以加入
        # 同时，总体起飞时间限制在 time_limit 分钟内
        for item in exist_air_list:

            if_correct = False

            while not if_correct and air.up_time <= time_limit:

                if air.if_cross_safe(item):
                    if air.same_up_point_check(item):
                        if air.same_down_point_check(item):
                            if_correct = True

                if not if_correct:
                    air.up_time += 0.5

            if air.up_time > time_limit:
                air.up_time = 0
                return -1

        return air.up_time

    # 航班起飞计划
    @staticmethod
    def air_plan(air_list, exist_air):

        # 随机选择一个初始起飞点， 也可以自己指派
        if len(air_list) > 0:
            root_air = random.choice(air_list)
            air_list.remove(root_air)
        else:
            return False

        if len(air_list) == 0:
            # 当余下的航班为0时，如果当前航班可以，则加入航班计划，否则清空序列

            time = AirPlan.if_safe_up(root_air, exist_air)
            if time == -1:
                del air_list, exist_air
                return False
            else:
                root_air.up_time = time
                exist_air.append(root_air)

                AirPlt.plot_air_way_with_time(exist_air)

                return True
        else:
            # 当前的航班不为0 ，如果当前的航班可以，则加入序列，继续递归过程，否则，清空序列，结束当前线路
            time = AirPlan.if_safe_up(root_air, exist_air)
            if time == -1:
                del air_list, exist_air
                return False
            else:
                root_air.up_time = time
                exist_air.append(root_air)
                AirPlan.air_plan(air_list, exist_air)


class AirPlt:

    # 画出所有的航线
    @staticmethod
    def plot_airway(list_air_way, x_length=300, y_length=250):

        plt.axis([0, x_length, 0, y_length])

        # 画出线
        for item in list_air_way:
            [up, down] = item
            plt.plot([up[0], down[0]], [up[1], down[1]], 'bo')
            plt.plot([up[0], down[0]], [up[1], down[1]])

        plt.show()

        print('print done')

    # 画出航班起飞时间
    @staticmethod
    def plot_air_way_with_time(list_air, x_length=300, y_length=250):

        plt.axis([0, x_length, 0, y_length])

        for air in list_air:

            plt.plot([air.Up[0], air.Down[0]], [air.Up[1], air.Down[1]], 'bo')
            plt.plot([air.Up[0], air.Down[0]], [air.Up[1], air.Down[1]])
            plt.text((air.Up[0] + air.Down[0])/2, (air.Up[1] + air.Down[1])/2, str(air.up_time))
            print(air.up_time)

        plt.show()
        print('print done')


def easy_use():

    # 获取航线
    air_way_list = AirWayGenWithRandomPoint.gene_new_air_way()
    # AirPlt.plot_airway(air_way_list)

    # 初始化航班
    air_list = AirInit.air_init(air_way_list)

    # 循环执行飞行计划
    limit = 100
    plan = AirPlan()

    # count = 0
    for i in range(1, limit):

        the_list = air_list.copy()
        exist_list = []

        plan.air_plan(the_list, exist_list)

        # print(count)
        if len(exist_list) > 15:
            AirPlt.plot_air_way_with_time(exist_list)

        # count += 1

if __name__ == "__main__":
    easy_use()
