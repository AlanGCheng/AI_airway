import


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
