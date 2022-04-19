# 经纬度计算脚本
# ylp
# 2022-4-19

from math import sin,cos,atan,acos,atan2,degrees,radians,tan
# 导入wx模块
import wx
class MyApp(wx.App):
    def OnInit(self):  # 初始化接口，子类覆盖父类的方法
        frame = wx.Frame(parent=None, title="经纬度计算")  # 新建框架
        panel = wx.Panel(frame, -1)  # 生成面板
        label1=wx.StaticText(panel,-1,"经度A",pos=(10,10))  #标签
        text1=wx.TextCtrl(panel,-1,pos=(80,10),size=(180,30),   #输入框
                           style=wx.TE_MULTILINE)

        label1a = wx.StaticText(panel, -1, "纬度A", pos=(10, 45))  # 标签
        text1a = wx.TextCtrl(panel, -1, pos=(80, 45), size=(180, 30),  # 输入框
                            style=wx.TE_MULTILINE)

        label2 = wx.StaticText(panel, -1, "经度B", pos=(10, 90))  # 标签
        text2 = wx.TextCtrl(panel, -1, pos=(80, 90), size=(180, 30),  # 输入框
                            style=wx.TE_MULTILINE)

        label2a = wx.StaticText(panel, -1, "维度B", pos=(10, 125))  # 标签
        text2a = wx.TextCtrl(panel, -1, pos=(80, 125), size=(180, 30),  # 输入框
                            style=wx.TE_MULTILINE)

        button1 = wx.Button(panel,-1, '开始计算', pos=(80, 165))  # 确定按钮位置
        # button2 = wx.Button(panel, -1, 'clear', pos=(180, 165))  # 确定按钮位置

        self.text1 = text1   # 方便跨函数调用
        self.text1a = text1a # 方便跨函数调用
        self.text2 = text2  # 方便跨函数调用
        self.text2a = text2a  # 方便跨函数调用
        self.button1 = button1      # 方便跨函数调用
        # self.button2 = button2      # 方便跨函数调用

        self.Bind(wx.EVT_BUTTON,  # 绑定事件，如果是按钮被点击
                  self.login,  # 激发的按钮事件
                  self.button1)  # 激发的按钮
        # self.Bind(wx.EVT_BUTTON,  # 绑定事件，如果是按钮被点击
        #           self.clear,  # 激发的按钮事件
        #           self.button2)  # 激发的按钮

        frame.Show()  # 显示
        return True

    #def OnButton1(self,event):  #事件的激发函数
        #self.button1.SetLabel("ni")
        #print(self.text1.GetValue())  #获取到输入的信息
    def login(self,event):      #事件的激发函数
        lonA = float(self.text1.GetValue())
        latA = float(self.text1a.GetValue())
        lonB = float(self.text2.GetValue())
        latB = float(self.text2a.GetValue())
        print(latA,lonA,latB,lonB)
        try:
            brng = getDegree(latA, lonA, latB, lonB)
            distance = getDistance(latA, lonA, latB, lonB)
            wx.MessageBox("方位角：%s，距离：%s"%(brng,distance), "info", wx.OK|wx.ICON_INFORMATION)
            print(brng,distance)
        except Exception:
            wx.MessageBox("输入有误", "info", wx.OK | wx.ICON_INFORMATION)
    def clear(self,event):
        pass

# 求两个经纬点的方位角
def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng

# 求两个经纬点的距离函数
def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB)) ** 2 / cos(x / 2) ** 2
    c2 = (sin(x) + x) * (sin(pA) - sin(pB)) ** 2 / sin(x / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance

app = MyApp()  # 启动
app.MainLoop()  # 进入消息循环