from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QLineEdit
from PyQt5.uic import loadUi
import sqlite3 as sql
from PyQt5.QtGui import QIcon



class Login(QDialog): #вікно входу
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction) #Подключаю кнопку к функции логин
        self.registerbutton.clicked.connect(self.gotocreate) #Подключаю кнопку к функции гоутукриейт
        self.hidebutton.clicked.connect(self.hidepassword)

    def loginfunction(self):
        email = self.email.text()  #переменная емейл будет равна тексту в поле емейл
        password = self.password.text() # тоже самое но пароль

        if len(email) == 0 or len(password) == 0 :
            self.errorla.setText("Не всі поля заповнені")

        else:
            conn = sql.connect('accounts.db')
            cur = conn.cursor()
            Query_ = 'SELECT password FROM users WHERE email = \''+email+"\'" #по емейлу дивимося пароль в базі
            cur.execute(Query_)
            myresult = cur.fetchone()[0]# переменная стает равна значению выше как числу
            if myresult == password:# проверка равности пароля в базе и ввденому паролю
                choose = ChooseDialog()
                widget.addWidget(choose)
                widget.setCurrentIndex(widget.currentIndex()+1)

            else:
                self.errorla.setText("Неправильний логін або пароль")
            conn.close()

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)# переключает окна

    def hidepassword(self):
        if self.password.echoMode() == QLineEdit.Normal:
            self.password.setEchoMode(QLineEdit.Password)# пароль выиглядає як *
        else:
            self.password.setEchoMode(QLineEdit.Normal)#нормальный пароль


class CreateAcc(QDialog): #вікно реєстрації
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createaccount.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)#підключає до кнопки функцію createaccfun..
        self.goinbutton.clicked.connect(self.goinfunction)

    def createaccfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmPassword = self.confirmpasswordfield.text()

        if len(user) == 0 or len(password) == 0 or len(confirmPassword) == 0 :
            self.errorla.setText("Не всі поля заповнені")
        elif password != confirmPassword :
            self.errorla.setText("Паролі не одинакові")
        else:
            conn = sql.connect('accounts.db')#підключаюсь до бази даних
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM users WHERE email=?', (user,))
            checkUsername = cur.fetchone()[0]
            if checkUsername == 0:
                user_info = [user, password]
                cur.execute('INSERT INTO users (email, password) VALUES (?,?)', user_info)#записує в базу користувачів логін і пароль

                conn.commit()#підтверджую завершення виконання строчки више
                conn.close()#припиняє роботу бази даних

                goin = Login()
                widget.addWidget(goin)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.errorla.setText('Такий юзер уже існуе')




    def goinfunction(self):
        goin = Login()
        widget.addWidget(goin)
        widget.setCurrentIndex(widget.currentIndex()+1)# переключає вікна




class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Додати")

        self.setWindowTitle("Додати курсанта")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("ПІБ")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItem("1 Курс")
        self.branchinput.addItem("2 Курс")
        self.branchinput.addItem("3 Курс")
        self.branchinput.addItem("4 Курс")
        self.branchinput.addItem("5 Курс")
        self.branchinput.addItem("6 Курс")
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItem("1 Група")
        self.seminput.addItem("2 Група")
        self.seminput.addItem("3 Група")
        self.seminput.addItem("4 Група")
        self.seminput.addItem("5 Група")

        layout.addWidget(self.seminput)

        self.zvaninput = QLineEdit()
        self.zvaninput.setPlaceholderText("Звання")
        layout.addWidget(self.zvaninput)

        self.posadainput = QLineEdit()
        self.posadainput.setPlaceholderText("Посада")
        layout.addWidget(self.posadainput)

        self.balinput = QLineEdit()
        self.balinput.setPlaceholderText("Середній бал")
        layout.addWidget(self.balinput)



        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Номер телефона")
        self.mobileinput.setInputMask('+380 99 999 99 99')
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Адрес")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        name = ""
        branch = ""
        sem = -1
        zvan = ""
        posada = ""
        bal = -1
        mobile = -1
        address = ""

        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        sem = self.seminput.itemText(self.seminput.currentIndex())
        zvan = self.zvaninput.text()
        posada = self.posadainput.text()
        bal = self.balinput.text()
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            self.conn = sql.connect("database.db")
            self.c = self.conn.cursor()
            cadet_info = [name,branch,sem,zvan,posada,bal,mobile,address]
            self.c.execute("INSERT INTO cadet (name,branch,sem,zvan,posada,bal,mobile,address) VALUES (?,?,?,?,?,?,?,?)",cadet_info)
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Успішно','Курсант доданий до бази.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Помилка', 'Не вийшло додати.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Пошук")

        self.setWindowTitle("Пошук курсанта")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("ПІБ")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):

        searchrol = self.searchinput.text()
        try:
            self.conn = sql.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute('SELECT * from cadet WHERE name=\''+searchrol+"\'")
            row = result.fetchone()
            serachresult = "ID : "+str(row[0])+'\n'+"ПІБ : "+str(row[1])+'\n'+"Курс : "+str(row[2])+'\n'+"Група : "+str(row[3])+'\n'+"Звання : "+str(row[4] +"Посада : "+str(row[5])+'\n'+"Середній бал : "+str(row[6])+'\n'+"Адрес : "+str(row[7]))
            QMessageBox.information(QMessageBox(), 'Успішно', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Помилка', 'Не змогли знайти такого курсанта.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Видалити")

        self.setWindowTitle("Видалити курсанта")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.deleteinput.setPlaceholderText("ПІБ")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delname = self.deleteinput.text()
        try:
            self.conn = sql.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute('DELETE from cadet WHERE name=\''+delname+"\'")
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Успішно','Видалили курсанта')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Помилка', 'Не змогли видалити курсанта з бази.')


class ChooseDialog(QDialog):
    def __init__(self):
        super(ChooseDialog,self).__init__()
        loadUi("choose.ui",self)
        self.infobutton.clicked.connect(self.openmain)
        self.marksbutton.clicked.connect(self.openmain2)

    def openmain(self):
        self.mainwindow = MainWindow()
        self.mainwindow.show()
        widget.close()

    def openmain2(self):
        self.mainwindow = MainWindow2()
        self.mainwindow.show()
        widget.close()



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowIcon(QIcon('logo.png'))
        self.conn = sql.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS cadet(roll INTEGER PRIMARY KEY AUTOINCREMENT ,name TEXT,branch TEXT,sem INTEGER,zvan TEXT,posada TEXT,bal REAL,mobile INTEGER,address TEXT)")
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")

        self.setWindowTitle("АСУКурсант")

        self.setMinimumSize(1200, 600)

        self.tableWidget = QTableWidget() #таблиця в центрі
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("ID", "ПІБ", "Курс", "Група","Звання","Посада","Середній бал", "Телефон","Адрес"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "Додати курсанта", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Додати курсанта")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_red = QAction(QIcon("icon/paper.png"), "Редагувати відомості", self)
        btn_ac_red.triggered.connect(self.red)
        btn_ac_red.setStatusTip("Редагувати")
        toolbar.addAction(btn_ac_red)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Оновити",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Оновити таблицю")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Пошук", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Пошук курсанта")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/trash.png"), "Видалити", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Видалити курсанта")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.png"),"Додати курсанта", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Пошук курсанта", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/trash.png"), "Видалити", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)


    def loaddata(self):
        self.connection = sql.connect("database.db")
        query = "SELECT * FROM cadet"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def red(self):
        dlg = RedDialog()
        dlg.exec_()

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

class RedDialog(QDialog):
    def __init__(self):
        super(RedDialog, self).__init__()

        self.setWindowTitle("Редагування курсантів")

        self.setMinimumSize(900, 600)

class MainWindow2(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow2, self).__init__(*args, **kwargs)

        self.setWindowIcon(QIcon('logo.png'))


        self.setWindowTitle("Оцінки курсантів")

        self.setMinimumSize(1000, 600)

        self.marksWidget = QTableWidget()
        self.setCentralWidget(self.marksWidget)
        self.marksWidget.setAlternatingRowColors(True)
        self.marksWidget.setColumnCount(6)
        self.marksWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.marksWidget.setSortingEnabled(True)
        self.marksWidget.horizontalHeader().setSortIndicatorShown(True)
        self.marksWidget.horizontalHeader().setStretchLastSection(True)
        self.marksWidget.verticalHeader().setVisible(False)
        self.marksWidget.verticalHeader().setCascadingSectionResizes(False)
        self.marksWidget.verticalHeader().setStretchLastSection(False)
        self.marksWidget.setHorizontalHeaderLabels(
            ("ПІБ", "ЗСП", "СА", "ТРПЗ", "ТПР", "ФВ"))




app=QApplication(sys.argv)

mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Вхід в програму")#назва сверху
widget.setWindowIcon(QIcon('logo.png'))#иконка
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()