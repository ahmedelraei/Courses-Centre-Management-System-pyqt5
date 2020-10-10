import sys, time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtChart import *
import sys
import pymysql
import os
import datetime
from os import path
import sys


class MovieSplashScreen(QSplashScreen):

    def __init__(self, movie, parent=None):
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())

        QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

    def sizeHint(self):
        return self.movie.scaledSize()


employee_id = 1
teachersIds  = []
teacher_codes  = []
names_list = []


mainUI, _ = loadUiType("main.ui")


class mainapp(QMainWindow, mainUI):
    def __init__(self, parent=None):
        super(mainapp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.handle_buttons()
        self.UI_Changes()
        self.show_all_Subjects()
        self.show_all_Grades()
        self.themes()
        self.show_all_teachers()
        self.show_all_students()
        #self.show_all_courses()
        self.employee_reports()
        self.autofetch()
        self.line_Edit()

    def themes(self):
        try:
            if not os.path.exists("Themes"):
                os.mkdir("Themes")

            if not os.path.exists("Themes/.defaultTheme/"):
                os.mkdir("Themes/.defaultTheme/")
                f = open('Themes/.defaultTheme/.default.thm', 'w')
                f.write('')
                f.close()

            if os.path.exists("Themes/.defaultTheme/.default.css"):
                f = open("Themes/.defaultTheme/.default.thm", "r")
                default = f.read()
                self.setStyleSheet('')
                self.setStyleSheet(default)

            themes = os.listdir("Themes")
            for theme in themes:
                if os.path.isfile("Themes/" + theme):
                    addedTheme = theme.split('.')[0]
                    self.comboBox_18.addItem(addedTheme)
        except Exception:
            QMessageBox.warning(self, "Process Error",
                                "Restart The Program . if the problem not solved contact The Support")

    def themesApply(self):
        try:
            theme = self.comboBox_18.currentText()
            f = open("Themes/" + theme + ".thm", "r")
            appliedTheme = f.read()
            self.setStyleSheet('')
            self.setStyleSheet(appliedTheme)
            f.close()
            #self.execute('''print("hello")''')
            #self.pushButton.setIcon(QIcon("resources/ICONS/Transactions-o.png"))
            #self.pushButton.setIconSize(QSize(50,50))
            self.update()
            f = open("Themes/.defaultTheme/.default.css", "w")
            f.write(appliedTheme)
            f.close()
        except FileNotFoundError:
            pass

    def DB_Connect(self):
        ## Connection between app and Database
        try:
            self.db = pymysql.connect(host="localhost", user="root", passwd="", database="Courses")
            self.cur = self.db.cursor()
            print("Connection Accepted")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Error', 'make sure mysql server is running')


    def handle_buttons(self):
        ## handles all Buttons

        self.pushButton.clicked.connect(self.open_dailyEvents_tab)
        self.pushButton_2.clicked.connect(self.open_Courses_tab)
        self.pushButton_3.clicked.connect(self.open_Clients_tab)
        self.pushButton_14.clicked.connect(self.open_emp_tab)
        self.pushButton_4.clicked.connect(self.open_dashboard_tab)
        self.pushButton_6.clicked.connect(self.open_history_tab)
        self.pushButton_7.clicked.connect(self.open_reports_tab)
        self.pushButton_5.clicked.connect(self.open_settings_tab)
        self.pushButton_10.clicked.connect(self.add_new_course)
        self.pushButton_26.clicked.connect(self.add_Subject)
        self.pushButton_32.clicked.connect(self.add_Grade)
        self.pushButton_18.clicked.connect(self.themesApply)
        self.pushButton_21.clicked.connect(self.add_new_student)
        self.pushButton_25.clicked.connect(self.add_new_teacher)
        self.pushButton_60.clicked.connect(self.Get_edit_teacher)
        self.pushButton_28.clicked.connect(self.edit_teacher)
        self.pushButton_65.clicked.connect(self.delete_employee)
        self.pushButton_64.clicked.connect(self.delete_teacher)
        self.pushButton_23.clicked.connect(self.retrieve_student)
        self.pushButton_66.clicked.connect(self.delete_student)


        # self.pushButton_29.clicked.connect(self.empTable_Search())

        self.signemp.clicked.connect(self.add_employee)
        self.signin.clicked.connect(self.handle_login)
        self.editprofile.triggered.connect(self.profilepage)
        self.pushButton_49.clicked.connect(self.editmyprofile)
        self.pushButton_42.clicked.connect(self.get_employee)
        self.pushButton_44.clicked.connect(self.edit_employee)
        self.pushButton_29.clicked.connect(self.empTable_Search)
        self.actionThemes.triggered.connect(self.open_themes_tab)
        self.actionLog_Out.triggered.connect(self.Log_out)

    def UI_Changes(self):

        ## UI Changes in login

        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.handle_login()

    ############################################



    def autofetch(self):

        global names_list

        self.cur.execute("SELECT name from employees")
        names =self.cur.fetchall()
        for name in names:
            names_list.append(name[0])

    def Auto_Complete(self, model):

        global names_list

        model.setStringList(names_list)

    def line_Edit(self):
        names_line_edit = self.lineEdit_51

        completer = QCompleter()
        names_line_edit.setCompleter(completer)

        model = QStringListModel()
        completer.setModel(model)
        self.Auto_Complete(model)


    #################### Log Out ######################

    def Log_out(self):

        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        self.menusettings.setDisabled(True)
        self.profile.setDisabled(True)
        self.groupBox_5.setDisabled(True)
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_14.setDisabled(True)
        self.pushButton_6.setDisabled(True)
        self.pushButton_7.setDisabled(True)
        self.pushButton_5.setDisabled(True)
        self.profile.setTitle('profile')

    def handle_login(self):
        ## handles login

        username = self.username.text()
        pwd = self.signinPWD.text()

        self.cur.execute("SELECT phone,password,id,name FROM employees")
        data = self.cur.fetchall()

        global employee_id

        if username != "" and pwd != "":

            for account in data:
                print(account)

                employee_id = account[2]

                if account[0] == username and account[1] == pwd:
                    print("##### Access Granted")
                    self.cur.execute("SELECT permission FROM employees WHERE id=%s", (employee_id))
                    query = self.cur.fetchone()
                    permission = query[0]
                    print(permission)
                    self.profile.setTitle(account[3])
                    self.menusettings.setEnabled(True)
                    self.profile.setEnabled(True)

                    if permission == "normal":
                        self.tabWidget.setCurrentIndex(2)

                        self.groupBox_5.setEnabled(True)
                        self.pushButton.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_3.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.tab_25.setDisabled(True)
                        self.tab_15.setDisabled(True)
                        break

                    if permission == "co-admin":
                        self.tabWidget.setCurrentIndex(5)
                        self.groupBox_5.setEnabled(True)
                        self.pushButton.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_3.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.pushButton_14.setEnabled(True)
                        self.pushButton_4.setEnabled(True)
                        self.pushButton_6.setEnabled(True)
                        self.pushButton_7.setEnabled(True)
                        self.tab_15.setDisabled(True)
                        break

                    if permission == "admin":
                        self.tabWidget.setCurrentIndex(5)
                        self.groupBox_5.setEnabled(True)
                        self.pushButton.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_3.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.pushButton_14.setEnabled(True)
                        self.pushButton_4.setEnabled(True)
                        self.pushButton_6.setEnabled(True)
                        self.pushButton_7.setEnabled(True)
                        break

                    if permission == "worker":
                        self.tabWidget.setCurrentIndex(2)
                        self.groupBox_5.setEnabled(True)
                        self.pushButton.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_3.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.tab_25.setDisabled(True)
                        self.tab_15.setDisabled(True)
                        break


    #QMessageBox.warning(self, "مستخدم غير موجود", "يرجي التأكد من البيانات المدخلة")

    def profilepage(self):
        self.tabWidget.setCurrentIndex(9)
        user = self.profile.title()
        self.label_3.setText("Hello, " + user)

        global employee_id

        self.cur.execute("SELECT phone,email FROM employees where id=%s", (employee_id))
        p = self.cur.fetchone()
        self.lineEdit_67.setText(str(p[0]))
        self.lineEdit_66.setText(str(p[1]))

    def editmyprofile(self):

        global employee_id

        phone = self.lineEdit_67.text()
        newpwd = self.lineEdit_65.text()
        newpwd2 = self.lineEdit_68.text()
        email = self.lineEdit_66.text()

        if newpwd == "":

            self.cur.execute('''UPDATE employees SET phone=%s,email=%s 
            where id=%s''', (phone, email, employee_id))
            self.db.commit()
            QMessageBox.information(self, "تم التعديل !", "تم تعديل البيانات بنجاح")

        elif newpwd == newpwd2:
            self.cur.execute('''UPDATE employees SET phone=%s,password=%s,email=%s 
            where id=%s''', (phone, newpwd, email, employee_id))
            self.db.commit()
            QMessageBox.information(self, "تم التعديل !", "تم تعديل البيانات بنجاح")
        else:
            QMessageBox.warning(self, "خطأ", "تأكد من تطابق كلمة السر")


    def handle_resetPassword(self):
        ## handles Reset Password processes
        pass

    def handle_todayWork(self):
        ## handles today Operations and transactions
        pass

    #################################################################################

    def show_all_courses(self):
        ## show all courses
        self.cur.execute('''SELECT grade,code,subject,teacher_id,price
            ,saturday,sunday,monday,tuesday,wednesday,thursday,friday FROM courses''')
        result = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        for row, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row)
            print("row::",row)
            for col, data in enumerate(row_data):
                if row_data.find(1) == 1:
                    if col == 5:
                        day = "السبت"
                        self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(day)))
                    if col == 6:
                        day = day +" | "+"الاحد"
                        print(data)
                        self.tableWidget_2.setItem(row, 5, QTableWidgetItem(str(day)))
                    if col == 7:
                        day = day +" | "+"الاثنين"
                        self.tableWidget_2.setItem(row,5,QTableWidgetItem(str(day)))
                        print(row)
                    if col == 8:
                        day = day +" | "+"الثلاثاء"
                        self.tableWidget_2.setItem(row,5,QTableWidgetItem(str(day)))
                        print(row)
                    if col == 9:
                        day = day +" | "+"الاربعاء"
                        self.tableWidget_2.setItem(row,5,QTableWidgetItem(str(day)))
                        print(row)
                    if col == 10:
                        day = day +" | "+"الخميس"
                        self.tableWidget_2.setItem(row,5,QTableWidgetItem(str(day)))
                        print(row)
                    if col == 11:
                        day = day +" | "+"الجمعة"
                        self.tableWidget_2.setItem(row,5,QTableWidgetItem(str(day)))
                        print(row)
                    row+=1


                elif col == 3:
                    self.cur.execute("SElECT name FROM teachers WHERE id = %s",(data))
                    Tname = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(Tname[0])))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(data)))

                self.tableWidget_2.resizeColumnsToContents()
                self.tableWidget_2.resizeRowsToContents()


    def add_new_course(self):
        ## add new Course

        #### Defaults

        day1 = 0
        day2 = 0
        day3 = 0
        day4 = 0
        day5 = 0
        day6 = 0
        day7 = 0
        t1   = None
        t2   = None
        t3   = None
        t4   = None
        t5   = None
        t6   = None
        t7   = None
        tt   = None

        global teacher_codes
        global teachersIds

        try:
            subject = self.comboBox_22.currentText()

            teacherCombobox = self.comboBox_14.currentIndex()

            teacher_id = teachersIds[teacherCombobox]

            price = self.lineEdit_5.text()
            grade = self.comboBox_4.currentText()  #####not required(in case of general course)
            ###### Code Generating ###########
            id = teacher_codes[teacherCombobox].replace("T", "").replace("-", "")
            code = "C-" + subject + id
            print(teacher_codes)
            ##################################
            if self.saturday.isChecked() == True:
                t1 = self.timeEdit_2.time().toString()
                day1 = 1
            if self.sunday.isChecked() == True:
                t2 = self.timeEdit_6.time().toString()
                day2 = 1
            if self.monday.isChecked() == True:
                t3 = self.timeEdit_8.time().toString()
                day3 = 1
            if self.tuesday.isChecked() == True:
                t4 = self.timeEdit_7.time().toString()
                day4 = 1
            if self.wednesday.isChecked() == True:
                t5 = self.timeEdit_10.time().toString()
                day5 = 1
            if self.thursday.isChecked() == True:
                t6 = self.timeEdit_9.time().toString()
                day6 = 1
            if self.friday.isChecked() == True:
                t7 = self.timeEdit_11.time().toString()
                day7 = 1

            #### everyday
            if self.everyday.isChecked() == True:
                day1 = 1
                day2 = 1
                day3 = 1
                day4 = 1
                day5 = 1
                day6 = 1
                day7 = 1
                tt = self.timeEdit_12.time().toString()

            desc = self.description.toPlainText()

            self.cur.execute('''INSERT INTO courses(subject,price,code,teacher_id,grade
            ,saturday,sunday,monday,tuesday,wednesday,thursday,friday,t1,t2,t3,t4,t5,t6,t7,tt,description)
			 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            ,(subject, price, code, teacher_id, grade, day1, day2, day3, day4, day5, day6, day7,
              t1,t2,t3,t4,t5,t6,t7,tt,desc))
            self.db.commit()
            QMessageBox.information(self, 'تمت', 'تمت اضافة الكورس بنجاح')
            self.show_all_teachers()

        except Exception as e2:
            print("e2:::" + str(e2))
            QMessageBox.warning(self, 'Error', 'make sure mysql is running or contact support')

    def edit_course(self):
        ## edit Course
        pass

    def delete_course(self):
        ## delete Course
        pass

    #################################################################################

    def add_new_student(self):
        ## add new student

        #### code generating #######################
        try:
            self.cur.execute("SELECT id FROM students")
            ids = self.cur.fetchall()
            print(ids)
            id_ = "ST"+str(ids[0][-1]+1)
            print("ST_ID: " + id_)
        except Exception as e:
            print(e)
            id_ = "ST"+"1"
        ############################################
        try:
            name = self.lineEdit_18.text()
            parent_phone = self.lineEdit_26.text()
            parent_phone2 = self.lineEdit_27.text()
            parentEmail = self.lineEdit_45.text()
            grade = self.comboBox_15.currentText()
            national_id = self.lineEdit_28.text()
            phone = self.lineEdit_25.text()
            email = self.lineEdit_47.text()
            join_date = datetime.datetime.now()

            self.cur.execute('''INSERT INTO students
            (name,grade,code,email,phone,parent_phone1,parent_phone2,parent_email,national_id,join_date)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
             (name,grade,id_,email,phone,parent_phone,parent_phone2,parentEmail,national_id,join_date))
            self.db.commit()
            QMessageBox.information(self,"تم","تم اضافة الطالب")
        except Exception as e:
            print(e)

        self.lineEdit_18.setText()
        self.lineEdit_26.setText()
        self.lineEdit_27.setText()
        self.lineEdit_45.setText()
        self.lineEdit_28.setText()
        self.lineEdit_25.setText()
        self.lineEdit_47.setText()


    def show_all_students(self):
        ## show all students

        try:
            self.cur.execute('''SELECT name,grade,code,email,phone
            ,parent_phone1,parent_phone2,parent_email,national_id,join_date FROM students''')
            result = self.cur.fetchall()

            self.tableWidget_5.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_5.insertRow(row_number)
                for col_number, data in enumerate(row_data):
                    self.tableWidget_5.setItem(row_number, col_number, QTableWidgetItem(str(data)))
                    self.tableWidget_5.resizeColumnsToContents()
                    self.tableWidget_5.resizeRowsToContents()
        except Exception as e:
            print(e)

    def retrieve_student(self):
        ## edit student

        searchKey = self.lineEdit_22.text()
        if self.comboBox_17.currentIndex() == 0:
            try:
                self.cur.execute("SELECT * FROM students where name=%s ", (searchKey))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الأسم بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 1:
            try:
                self.cur.execute("SELECT * FROM students where code=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الكود بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 5:
            try:
                self.cur.execute("SELECT * FROM students where national_id=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الرقم القومي بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 3:
            try:
                self.cur.execute("SELECT * FROM students where phone=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل رقم الهاتف بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 4:
            try:
                self.cur.execute("SELECT * FROM students where parent_phone1=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل رقم الهاتف بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 5:
            try:
                self.cur.execute("SELECT * FROM students where parent_phone2=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل رقم الهاتف بشكل صحيح")

        elif self.comboBox_17.currentIndex() == 2:
            try:
                self.cur.execute("SELECT * FROM students where email=%s ", (searchKey,))
                STdata = self.cur.fetchone()

                self.lineEdit_24.setText(str(STdata[1]))  ## name
                self.comboBox_16.setCurrentText(str(STdata[2]))   ## grade
                self.lineEdit_21.setText(str(STdata[3]))        ## code
                self.lineEdit_32.setText(str(STdata[9]))  ## national id
                self.lineEdit_60.setText(str(STdata[4]))  ## email
                self.lineEdit_46.setText(str(STdata[8]))  ## Parent Email
                self.lineEdit_31.setText(str(STdata[5]))  ## phone
                self.lineEdit_29.setText(str(STdata[6]))  ## Parent phone1
                self.lineEdit_30.setText(str(STdata[7]))  ## Parent phone2
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل البريد الالكتروني بشكل صحيح")


    def delete_student(self):
        ## delete student
        for currentQTableWidgetItem in self.tableWidget_5.selectedItems():
            current_row = currentQTableWidgetItem.row()
            print(current_row)

        delKey = self.tableWidget_5.item(current_row, 2).text()
        self.cur.execute("DELETE FROM students WHERE code=%s", (delKey))
        self.db.commit()
        self.show_all_students()

    #################################################################################
    ## Teachers

    def add_new_teacher(self):
        ## add new teacher
        try:
            name = self.lineEdit_35.text()
            national_id = self.lineEdit_34.text()
            email = self.lineEdit_49.text()
            phone = self.lineEdit_37.text()
            subject = self.comboBox_23.currentText()
            code = "T-" + str(national_id[-1] + national_id[-2] + national_id[-3])
            join_date = datetime.datetime.now()

            self.cur.execute(
                '''INSERT INTO teachers(name,email,phone,subject,code,join_date,national_id) VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                , (name, email, phone, subject, code, join_date, national_id))
            self.db.commit()
            QMessageBox.information(self, 'تمت', 'تمت اضافة المدرس بنجاح')
            self.show_all_teachers()

        except Exception as e2:
            print(e2)
            QMessageBox.warning(self, 'Error', 'make sure mysql is running or contact support')

    def show_all_teachers(self):
        ## show all teachers
        ###### comboboxes adding###########################################
        self.comboBox_6.clear()
        self.comboBox_14.clear()
        self.cur.execute("SELECT name,subject,code,id FROM teachers")
        teachers = self.cur.fetchall()
        global teacher_codes
        global teachersIds
        for teacher in teachers:
            teachersIds.append(teacher[3])
            teacher_codes.append(teacher[2])   ### appends t. code in the global list

            self.comboBox_6.addItem(str(teacher[0]) + ","' (' + teacher[1] + ')')
            self.comboBox_14.addItem(str(teacher[0]) + ","' (' + teacher[1] + ')')

        ####################################################################

        self.cur.execute("SELECT name,email,phone,subject,code,join_date,national_id FROM teachers")
        result = self.cur.fetchall()

        self.tableWidget_8.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.tableWidget_8.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget_8.setItem(row_number, col_number, QTableWidgetItem(str(data)))
                self.tableWidget_8.resizeColumnsToContents()
                self.tableWidget_8.resizeRowsToContents()

    def Get_edit_teacher(self):
        ## retrieve teacher to edit
        searchKey = self.lineEdit_92.text()
        if self.comboBox_32.currentIndex() == 0:
            try:
                self.cur.execute("SELECT * FROM teachers where name=%s ", (searchKey,))
                self.teacher_data = self.cur.fetchone()
                print("Teacher DATA[0]::")
                print(self.teacher_data[0])
                print(self.teacher_data[1])
                self.lineEdit_62.setText(str(self.teacher_data[1]))  ## name
                self.lineEdit_64.setText(str(self.teacher_data[5]))  ## national id
                self.lineEdit_63.setText(str(self.teacher_data[2]))  ## email
                self.lineEdit_61.setText(str(self.teacher_data[3]))  ## phone
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الأسم بشكل صحيح")

        elif self.comboBox_32.currentIndex() == 1:
            try:
                self.cur.execute("SELECT * FROM teachers where code=%s ", (searchKey,))
                self.teacher_data = self.cur.fetchone()
                print("SELF.Teacher_data:: " + str(self.teacher_data))
                print(self.teacher_data[1])
                self.lineEdit_62.setText(str(self.teacher_data[1]))  ## name
                self.lineEdit_64.setText(str(self.teacher_data[5]))  ## national id
                self.lineEdit_63.setText(str(self.teacher_data[2]))  ## email
                self.lineEdit_61.setText(str(self.teacher_data[3]))  ## phone
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الكود بشكل صحيح")

        elif self.comboBox_32.currentIndex() == 2:
            try:
                self.cur.execute("SELECT * FROM teachers where national_id=%s ", (searchKey,))
                self.teacher_data = self.cur.fetchone()
                print(self.teacher_data[1])
                self.lineEdit_62.setText(str(self.teacher_data[1]))  ## name
                self.lineEdit_64.setText(str(self.teacher_data[5]))  ## national id
                self.lineEdit_63.setText(str(self.teacher_data[2]))  ## email
                self.lineEdit_61.setText(str(self.teacher_data[3]))  ## phone
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل الرقم القومي بشكل صحيح")

        elif self.comboBox_32.currentIndex() == 3:
            try:
                self.cur.execute("SELECT * FROM teachers where phone=%s ", (searchKey,))
                self.teacher_data = self.cur.fetchone()
                print(self.teacher_data[1])
                self.lineEdit_62.setText(str(self.teacher_data[1]))  ## name
                self.lineEdit_64.setText(str(self.teacher_data[5]))  ## national id
                self.lineEdit_63.setText(str(self.teacher_data[2]))  ## email
                self.lineEdit_61.setText(str(self.teacher_data[3]))  ## phone
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "خطأ", "ادخل رقم الهاتف بشكل صحيح")
    def edit_teacher(self):
        try:
            name = self.lineEdit_62.text()
            national_id = self.lineEdit_64.text()
            email = self.lineEdit_63.text()
            phone = self.lineEdit_61.text()
            subject = self.comboBox_24.currentText()
            self.cur.execute('''
				UPDATE teachers SET name=%s,email=%s,phone=%s,subject=%s,national_id=%s
				WHERE id=%s
				''', (name, email, phone, subject, national_id, self.teacher_data[0]))
            self.db.commit()
            self.show_all_teachers()
            QMessageBox.information(self, 'تم التعديل', 'تم التعديل بنجاح')
        except Exception as e:
            print(e)

    def delete_teacher(self):
        ## delete teacher
        for currentQTableWidgetItem in self.tableWidget_8.selectedItems():
            current_row = currentQTableWidgetItem.row()
            print(current_row)

        delKey = self.tableWidget_8.item(current_row, 4).text()
        print("item::: " + delKey)

        self.cur.execute("DELETE FROM teachers WHERE code=%s", (delKey))
        self.db.commit()
        self.show_all_teachers()

    #################################################################################
    def employee_reports(self):

        self.cur.execute("SELECT SUM(salary) AS total FROM employees")
        total = self.cur.fetchone()[0]
        digits = len(str(total))
        self.lcdNumber.setDigitCount(digits)
        self.lcdNumber.display(total)

        self.cur.execute("SELECT AVG(salary) AS average FROM employees")
        res = self.cur.fetchone()[0]
        avg = round(res)
        digits = len(str(avg))
        self.lcdNumber_2.setDigitCount(digits)
        self.lcdNumber_2.display(avg)

        self.cur.execute("SELECT COUNT(gender) FROM employees")
        all = self.cur.fetchone()[0]
        self.cur.execute("SELECT COUNT(gender) FROM employees where gender='male'")
        males = self.cur.fetchone()[0]
        females = int(all) - int(males)

        male_percent = (males / all)*100
        female_percent = (females / all) * 100

        series = QPieSeries()
        label1 = "Males %.2f %%" %(float(male_percent))
        label2 = "Females %.2f %%" % (float(female_percent))
        series.append(label1, male_percent)
        series.append(label2, female_percent)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Gender Chart")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #chart.setTheme(QChart.ChartThemeDark)
        chart.setPlotAreaBackgroundVisible(False)
        chart.setBackgroundVisible(False)
        self.graphicsView.setStyleSheet("background: transparent;")
        self.graphicsView.setChart(chart)


    ##### History

    def show_history(self):
        ## show all history to the admin
        pass

    #################################################################################

    #### Students Reports

    def all_students_reports(self):
        ## report for all Students
        pass

    def students_filter_report(self):
        ## Show report for filtered Students
        pass

    def Student_Export_Report(self):
        ## Export Student Data to excel file
        pass

    #################################################################################

    #### Courses Reports

    def all_courses_reports(self):
        ## report for all Courses
        pass

    def courses_filter_report(self):
        ## Show report for filtered Courses
        pass

    def Courses_Export_Report(self):
        ## Export Courses Data to excel file
        pass

    #################################################################################

    #### Monthly Report

    def monthly_report(self):
        ## show report a month
        pass

    def monthly_report_export(self):
        ## Export Monthly Report
        pass

    #################################################################################

    #### Settings

    # Subjects

    def add_Subject(self):
        ## add new Subject
        subject_name = self.lineEdit_38.text()
        self.cur.execute('''
			INSERT INTO subjects(subject_name) VALUES(%s)
			''', (subject_name,))
        self.db.commit()
        print("Subject Added")
        QMessageBox.information(self, "تمت", "تمت اضافة المادة بنجاح")
        self.show_all_Subjects()

    def show_all_Subjects(self):
        self.comboBox_22.clear()
        self.comboBox_23.clear()
        self.comboBox_13.clear()
        self.comboBox_7.clear()
        self.comboBox_24.clear()

        self.cur.execute("SELECT subject_name FROM subjects")
        subjects = self.cur.fetchall()
        for subject in subjects:
            print(subject[0])
            self.comboBox_7.addItem(str(subject[0]))
            self.comboBox_22.addItem(str(subject[0]))
            self.comboBox_23.addItem(str(subject[0]))
            self.comboBox_13.addItem(str(subject[0]))
            self.comboBox_24.addItem(str(subject[0]))

    # Grades

    def add_Grade(self):
        ## add new Grade
        Grade_name = self.lineEdit_50.text()
        self.cur.execute('''
			INSERT INTO grades(grade_name) VALUES(%s)
			''', (Grade_name,))
        self.db.commit()
        print("Grade Added")
        QMessageBox.information(self, "تمت", "تمت اضافة الصف بنجاح")
        self.show_all_Subjects()

    def show_all_Grades(self):
        self.comboBox_4.clear()
        self.comboBox_5.clear()
        self.comboBox_15.clear()
        self.comboBox_16.clear()

        self.cur.execute("SELECT grade_name FROM grades")
        Grades = self.cur.fetchall()
        for Grade in Grades:
            self.comboBox_4.addItem(str(Grade[0]))
            self.comboBox_5.addItem(str(Grade[0]))
            self.comboBox_15.addItem(str(Grade[0]))
            self.comboBox_16.addItem(str(Grade[0]))

    #################################################################################

    #### Emplyees

    def add_employee(self):
        ## add new Employee

        name = self.empname.text()
        age = self.empage.text()
        gender = self.gender.currentText()
        email = self.empmail.text()
        phone = self.emp_phone.text()
        nat_id = self.empnat.text()
        salary = self.empsalary.text()
        date = datetime.datetime.now()
        pwd = self.emppass.text()
        pwd2 = self.emppass2.text()
        permission = self.pbox.currentText()
        if pwd == pwd2:

            try:
                self.cur.execute('''INSERT INTO 
				employees(name,age,gender,Email,phone,date,national_id,salary,password,permission)
				 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                                 , (name, age, gender, email, phone, date, nat_id, salary, pwd, permission))
                self.db.commit()
                QMessageBox.information(self, "تمت !", "تمت اضافة موظف جديد")

                self.employee_reports()

                ######## reset ########
                self.empname.setText("")
                self.empage.setText("")
                self.gender.setCurrentIndex(0)
                self.empmail.setText("")
                self.emp_phone.setText("")
                self.empnat.setText("")
                self.empsalary.setText("")
                self.emppass.setText("")
                self.emppass2.setText("")
                self.pbox.setCurrentIndex(0)

                self.empname.setFocus()

            except Exception as e:
                print("(add_employee) error: " + str(e))
                QMessageBox.warning(self, "Error", "Make Sure Mysql is Running or Contact Support")
        else:
            QMessageBox.warning(self, "خطأ", "كلمة السر غير متطابقة")


    def get_employee(self):
        try:
            ## edit employee
            nationalID = self.lineEdit_59.text()
            self.cur.execute('''SELECT id,name,age
			,phone,salary,email,password,permission FROM employees
			where national_id=%s''', (nationalID))
            temp = self.cur.fetchone()
            print(temp)
            # id   #name   #age   #phone  #salary  #email #pwd  #permission
            data = [temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], nationalID]

            f = open('.GET_EMP_CACHE.txt', 'w')
            f.write(str(temp[0]))

            self.lineEdit_55.setText(data[1])  ## name
            self.lineEdit_52.setText(str(data[2]))  ## age
            self.lineEdit_56.setText(data[3])  ## phone
            self.empsalary_2.setText(str(data[4]))  ## Salary
            self.lineEdit_54.setText(data[5])  ## email
            self.lineEdit_53.setText(nationalID)  ## nat. id
            self.lineEdit_57.setText(data[6])  ## pass
            self.lineEdit_58.setText(data[6])  ## pass2
            self.comboBox_25.setCurrentText(data[7])  ## permission

            self.lineEdit_55.setFocus()

        except Exception as e:
            print(e)

    def edit_employee(self):
        name = self.lineEdit_55.text()
        age = self.lineEdit_52.text()
        phone = self.lineEdit_56.text()
        email = self.lineEdit_54.text()
        natID = self.lineEdit_53.text()
        pwd = self.lineEdit_57.text()
        pwd2 = self.lineEdit_58.text()
        pm = self.comboBox_25.currentText()

        f = open('.GET_EMP_CACHE.txt', 'r')
        id = f.read()

        if pwd == pwd2:
            self.cur.execute('''UPDATE employees SET name=%s,email=%s,phone=%s,age=%s,national_id=%s
			,password=%s,permission=%s WHERE id=%s''', (name, email, phone, age, natID, pwd, pm, id))
            self.db.commit()
            QMessageBox.information(self, 'تم التعديل !', 'تم تعديل البيانات بنجاح')

            self.employee_reports()

            self.lineEdit_55.setText("")
            self.lineEdit_52.setText("")
            self.lineEdit_56.setText("")
            self.lineEdit_54.setText("")
            self.lineEdit_53.setText("")
            self.lineEdit_57.setText("")
            self.lineEdit_58.setText("")

            self.lineEdit_59.setFocus()

        else:
            QMessageBox.warning(self, 'غير متطابق !', 'كلمة السر غير متطابقة')

    def empTable(self):
        try:
            self.cur.execute("SELECT name,age,gender,email,phone,salary,date FROM employees")
            result = self.cur.fetchall()

            self.tableWidget_9.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_9.insertRow(row_number)
                for col_number, data in enumerate(row_data):
                    self.tableWidget_9.setItem(row_number, col_number, QTableWidgetItem(str(data)))
                    self.tableWidget_9.resizeColumnsToContents()
                    self.tableWidget_9.resizeRowsToContents()
        except Exception as e:
            print(e)

    def empTable_Search(self):

        keyword = self.lineEdit_51.text()
        filter = self.comboBox_26.currentIndex()

        try:

            if keyword == "":
                self.empTable()
            else:

                if filter == 0:  #### search by name

                    self.cur.execute('''SELECT name,age,gender,email,phone,salary,date 
					FROM employees where name=%s''', (keyword))
                    query = self.cur.fetchall()
                    print(query)

                elif filter == 1:  #### Search by nat. ID

                    self.cur.execute('''SELECT name,age,gender,email,phone,salary,date 
					FROM employees where national_id=%s''', (keyword))
                    query = self.cur.fetchall()

                elif filter == 2:  #### Search by phone

                    self.cur.execute('''SELECT name,age,gender,email,phone,salary,date 
					FROM employees where phone=%s''', (keyword))
                    query = self.cur.fetchall()

                elif filter == 3:  #### Search by salary

                    self.cur.execute('''SELECT name,age,gender,email,phone,salary,date 
					FROM employees where salary=%s''', (keyword))
                    query = self.cur.fetchall()

                self.tableWidget_9.setRowCount(0)

                for row_number, row_data in enumerate(query):
                    self.tableWidget_9.insertRow(row_number)
                    for col_number, data in enumerate(row_data):
                        self.tableWidget_9.setItem(row_number, col_number, QTableWidgetItem(str(data)))

        except Exception as e:
            msg = 'Sorry %s, Unfortunately un expected error Contact Support' % (self.profile.title())
            QMessageBox.warning(self, 'UNEXPECTED ERROR !', msg)
            print(e)

    def delete_employee(self):
        ## delete employee

        for currentQTableWidgetItem in self.tableWidget_9.selectedItems():
            current_row = currentQTableWidgetItem.row()

        delKey = self.tableWidget_9.item(current_row, 4).text()

        self.cur.execute("DELETE FROM employees WHERE phone=%s", (delKey))
        self.db.commit()
        self.empTable()
        self.employee_reports()

    #################################################################################

    #### admin

    def admin_report(self):
        ## send report to the admin
        pass

    #################################################################################

    #### Tabs

    def open_dailyEvents_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_Courses_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_Clients_tab(self):
        self.tabWidget.setCurrentIndex(4)

    def open_emp_tab(self):
        self.tabWidget.setCurrentIndex(10)
        self.empTable()

    def open_dashboard_tab(self):
        self.tabWidget.setCurrentIndex(5)

    def open_history_tab(self):
        self.tabWidget.setCurrentIndex(6)

    def open_reports_tab(self):
        self.tabWidget.setCurrentIndex(7)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(8)

    def open_themes_tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_5.setCurrentIndex(3)


def main():
    app = QApplication(sys.argv)
    window = mainapp()
    window.show()
    app.exec_()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    movie = QMovie("animation.gif")
    splash = MovieSplashScreen(movie)
    splash.show()

    start = time.time()

    while movie.state() == QMovie.Running and time.time() < start + 5:
        app.processEvents()

    window = mainapp()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())