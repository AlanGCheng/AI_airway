from airWayV2 import AirPlane


# 新的air类，暂时不进行考虑
class AirPlaneV4(AirPlane):
    # 这个类继承自之前的AirPlane类
    # 主要需要考虑到以下几个点
    # 1. 新加属性 是否滞空 _ifstay ，滞空的开始时间 _startstaytime ， 滞空的结束时间 _endstaytime
    #
    # 2. 判断在最新的地图下面，航班能否安全飞行，如果不行，时间延后
    # todo:2.1 新想法，如果着火点在航线上面，那么会让经过设置为此航线的先走，并且在设置点滞空，如果不是，
    # 选择航线最为靠近的点，并且滞空后返航

    # @AirPlane.__init__(airNum=0, UpPoint=0, DownPoint=0, uptime=0, UpPointName=0, DownPointName=0)
    def __init__(self, start_stay_time=0, end_stay_time=0, stay_priority=0, stay_point=0):
        AirPlane.__init__(self)
        self._if_stay = False
        self._start_stay_time = start_stay_time
        self._end_stay_time = end_stay_time
        self._priority = stay_priority
        self._stay_point = stay_point

    def if_cross_safe(self, compared_air):
        pass

    def if_stay_safe(self):
        pass

    def if_up_safe(self):
        pass

    def if_down_safe(self):
        pass
