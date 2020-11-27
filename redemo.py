from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QIcon
import requests

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
        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.clearre_button.clicked.connect(self.clearre)
        self.ui.clearurl_button.clicked.connect(self.clearurl)
        self.ui.clearall_button.clicked.connect(self.clearall)

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
    
    # 清除参数表
    def clear(self):
        self.ui.params_text.clearContents()
        self.ui.params_text.setRowCount(0)

    # 清除响应内容
    def clearre(self):
        self.ui.retext.setText("")

    # 清除url
    def clearurl(self):
        self.ui.url.clear()

    # 全部清空
    def clearall(self):
        self.clear()
        self.clearre()
        self.clearurl()


    #点击确认
    def yes(self):
        url = self.ui.url.text()
        data = self.get_value()
        method = self.ui.method.currentText()
        if(url == ""):
            QMessageBox.critical(self.ui,'错误','url为空！')
        elif(not bool(data)):
            #清除之前的内容
            self.clearre()
            re,code = self.re_text(url,method)
            if(code):
                self.ui.retext.insertPlainText(re.text)
        elif(bool(data)):
            self.clearre()
            re,code = self.re_textpar(url,method,data)
            self.ui.retext.insertPlainText(re.text)



    #发送请求（不带参数的）返回获取的响应
    def re_text(self,ul,met):
        try:
            result = requests.request(met,ul)
            result.encoding = 'utf-8'
            return result,True
        except:
            QMessageBox.critical(self.ui,'错误','请求出错！')
            return "",False
    


    #发送请求（带参数的）返回获取的响应
    def re_textpar(self,ul,met,data):
        try:
            result = requests.request(met,ul,params=data)
            result.encoding = 'utf-8'
            return result,True
        except:
            QMessageBox.critical(self.ui,'错误','请求出错！')
            return "",False


    # 获取参数并返回字典类型
    def get_value(self):
        params = {}
        num = self.ui.params_text.rowCount()
        for i in range(0,num):
            par = self.ui.params_text.item(i,0).text()
            val = self.ui.params_text.item(i,1).text()
            params[par] = val
        return params



app = QApplication([])
app.setWindowIcon(QIcon('logo.jpg'))
stats = Stats()
stats.ui.show()
app.exec_()
