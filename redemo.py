from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QIcon
import requests
import json

from requests.api import head

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('re.ui')
        self.ui.params_text.setColumnWidth(1, 100)
        self.ui.yes.clicked.connect(self.yes)

        self.ui.add_button.clicked.connect(self.add_list)
        self.ui.increase_button.clicked.connect(self.increase_list)

        self.ui.headadd_button.clicked.connect(self.headadd_list)
        self.ui.headincrease_button.clicked.connect(self.headincrease_list)

        self.ui.clearre_button.clicked.connect(self.clearre)
        self.ui.clearurl_button.clicked.connect(self.clearurl)
        self.ui.clearall_button.clicked.connect(self.clearall)

        self.ui.search_button.clicked.connect(self.get_hearders)

    # 点击添加参数
    def add_list(self):
        num = self.ui.params_text.rowCount()
        if(num == 0):
            self.ui.params_text.insertRow(num)
        else:
            try:
                self.ui.params_text.item(num-1,0).text()
                self.ui.params_text.item(num-1,1).text()
                self.ui.params_text.insertRow(num)
            except:
                QMessageBox.critical(self.ui,'错误','参数为空！')

    # 点击删除参数
    def increase_list(self):
        num = self.ui.params_text.rowCount()
        self.ui.params_text.removeRow(num-1)
    


    # 点击添加请求头
    def headadd_list(self):
        num = self.ui.headers_text.rowCount()
        if(num == 0):
            self.ui.headers_text.insertRow(num)
        else:
            try:
                self.ui.headers_text.item(num-1,0).text()
                self.ui.headers_text.item(num-1,1).text()
                self.ui.headers_text.insertRow(num)
            except:
                QMessageBox.critical(self.ui,'错误','参数为空！')

    # 点击删除请求头
    def headincrease_list(self):
        num = self.ui.headers_text.rowCount()
        self.ui.headers_text.removeRow(num-1)


    # 清除响应内容
    def clearre(self):
        self.ui.retext.setText("")

    # 清除url
    def clearurl(self):
        self.ui.url.clear()

    # 全部清空
    def clearall(self):
        self.clearre()
        self.clearurl()


    #点击确认
    def yes(self):
        url = self.ui.url.text()#请求的url
        data = self.get_value()#请求所带的参数
        method = self.ui.method.currentText()#请求方式
        head = self.get_headvalue()#请求所带的参数
        print(url,data,method,head)
        if(not len(url)):
            QMessageBox.critical(self.ui,'错误','url为空！')
        else:
            self.clearre()
            re = self.re_text(url,method,data,head)
            self.ui.retext.insertPlainText(re.text)



    #发送请求返回获取的响应
    def re_text(self,ul,met,par=None,head=None):
        try:
            result = requests.request(met,ul,timeout=5,params=par,headers=head)
            result.encoding = result.apparent_encoding
            return result
        except:
            QMessageBox.critical(self.ui,'错误','请求出错！')
            return None
    
    # 获取参数并返回字典类型
    def get_value(self):
        params = {}
        num = self.ui.params_text.rowCount()
        for i in range(0,num):
            par = self.ui.params_text.item(i,0).text()
            val = self.ui.params_text.item(i,1).text()
            params[par] = val
        return params

    # 获取请求头并返回字典类型
    def get_headvalue(self):
        head = {}
        num = self.ui.headers_text.rowCount()
        for i in range(0,num):
            par = self.ui.headers_text.item(i,0).text()
            val = self.ui.headers_text.item(i,1).text()
            head[par] = val
        return head


    #获取请求头并返回字典类型
    def get_hearders(self):
        params = {}
        num = self.ui.hearders_text.rowCount()
        for i in range(0,num):
            par = self.ui.hearders_text.item(i,0).text()
            val = self.ui.hearders_text.item(i,1).text()
            params[par] = val
        print(params)


app = QApplication([])
app.setWindowIcon(QIcon('logo.jpg'))
stats = Stats()
stats.ui.show()
app.exec_()
