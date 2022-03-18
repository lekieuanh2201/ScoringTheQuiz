from PyQt5 import QtCore, QtWidgets, QtGui
import gui, os, obj_detective

class myApp(gui.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.setupUi(self)
        self.btn_browse.clicked.connect(self.loadImg)
        self.btn_chamDiem.clicked.connect(self.score)
        self.btn_chamLai.clicked.connect(self.reScore)
    
    def loadImg(self, filename=None):
        if not filename:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Photo', QtCore.QDir.currentPath(), 'Images (*.png *.jpg)')
            self.imgPath = filename
            # print(filename)
            self.tenAnh.setText(os.path.basename(filename))
            if not filename:
                return
            
    def score(self):
        soCauHoi = self.inp_soCauHoi.value()
        ans_predict = obj_detective.objDect(path=self.imgPath, number_ans=soCauHoi)
        string_ans = self.tb_nhapDA.toPlainText()
        ans = []
        for c in string_ans.split(','):
            ans.append(c)
        self.answer = ans
       
        score = 0
        string_predict = ""
        for i in range(0, soCauHoi):
            string_predict += ans_predict[i] + " ,"
            if ans[i] == ans_predict[i]:
                score += 1 
                
        print(string_predict)
        self.tb_DAout.setText(string_predict)   
        
        score = str(10*score/self.inp_soCauHoi.value())
        self.Diem.setText("<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">"+score+"</span></p></body></html>")

    def reScore(self):
        soCauHoi = self.inp_soCauHoi.value()
        score = 0
        str_ans = self.tb_nhapDA.toPlainText()
        ans = []
        for c in str_ans.split(','):
            ans.append(c)
        print(ans)
        string_ans = self.tb_DAout.toPlainText()
        DAout=[]
        for c in string_ans.split(' ,'):
            DAout.append(c)
        print(DAout)
        for i in range(0, soCauHoi):
            if DAout[i]==ans[i]:
                score+=1
        score = str(10*score/self.inp_soCauHoi.value())
        self.Diem.setText("<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">"+score+"</span></p></body></html>")
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    nhom17 = myApp()
    nhom17.show()
    app.exec_()