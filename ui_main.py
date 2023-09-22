# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwspdMT.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QListView, QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget


class Ui_main_window(object):
    def setupUi(self, main_window: QMainWindow):
        if not main_window.objectName():
            main_window.setObjectName("main_window")
        main_window.setWindowModality(Qt.NonModal)
        main_window.setEnabled(True)
        main_window.resize(800, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QSize(500, 500))
        main_window.setMaximumSize(QSize(800, 800))
        main_window.setAnimated(False)
        self.window = main_window
        self.main_widget = QWidget(main_window)
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout = QHBoxLayout(self.main_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.proc_list_header = QLabel(self.main_widget)
        self.proc_list_header.setObjectName("label")

        self.verticalLayout_3.addWidget(self.proc_list_header)

        self.list_view = QListView(self.main_widget)
        self.list_view.setObjectName("list_view")

        self.verticalLayout_3.addWidget(self.list_view)

        self.refresh_procs_bt = QPushButton(self.main_widget)
        self.refresh_procs_bt.setObjectName("refresh_procs_bt")

        self.verticalLayout_3.addWidget(self.refresh_procs_bt)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dll_inject_stats_header = QLabel(self.main_widget)
        self.dll_inject_stats_header.setObjectName("label_2")
        self.dll_inject_stats_header.setAutoFillBackground(False)
        self.dll_inject_stats_header.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.dll_inject_stats_header)

        self.inject_statu_label = QLabel(self.main_widget)
        self.inject_statu_label.setObjectName("inject_statu_label")

        self.horizontalLayout_3.addWidget(self.inject_statu_label)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.user_name_header = QLabel(self.main_widget)
        self.user_name_header.setObjectName("label_6")
        self.user_name_header.setAutoFillBackground(False)
        self.user_name_header.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.user_name_header)

        self.login_user_name_label = QLabel(self.main_widget)
        self.login_user_name_label.setObjectName("login_user_name_label")

        self.horizontalLayout_5.addWidget(self.login_user_name_label)

        self.horizontalLayout_5.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pid_header = QLabel(self.main_widget)
        self.pid_header.setObjectName("label_7")
        self.pid_header.setAutoFillBackground(False)
        self.pid_header.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.pid_header)

        self.proc_id_label = QLabel(self.main_widget)
        self.proc_id_label.setObjectName("proc_id_label")

        self.horizontalLayout_4.addWidget(self.proc_id_label)

        self.horizontalLayout_4.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.port_header = QLabel(self.main_widget)
        self.port_header.setObjectName("label_4")
        self.port_header.setAutoFillBackground(False)
        self.port_header.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.port_header)

        self.bind_prot_label = QLabel(self.main_widget)
        self.bind_prot_label.setObjectName("bind_prot_label")

        self.horizontalLayout_2.addWidget(self.bind_prot_label)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.inject_dll_bt = QPushButton(self.main_widget)
        self.inject_dll_bt.setObjectName("inject_dll_bt")

        self.verticalLayout_2.addWidget(self.inject_dll_bt)

        self.sync_login_status_bt = QPushButton(self.main_widget)
        self.sync_login_status_bt.setObjectName("sync_login_status_bt")
        self.sync_login_status_bt.setEnabled(False)

        self.verticalLayout_2.addWidget(self.sync_login_status_bt)

        self.enable_msg_callback = QPushButton(self.main_widget)
        self.enable_msg_callback.setObjectName("enable_msg_callback")
        self.enable_msg_callback.setEnabled(False)

        self.verticalLayout_2.addWidget(self.enable_msg_callback)

        self.verticalSpacer = QSpacerItem(20, 479, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.wx_path_label = QLabel(self.main_widget)
        self.wx_path_label.setObjectName("wx_path_label")
        self.wx_path_label.setTextFormat(Qt.PlainText)
        self.wx_path_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.wx_path_label)

        self.select_wx_path_bt = QPushButton(self.main_widget)
        self.select_wx_path_bt.setObjectName("select_wx_path_bt")

        self.verticalLayout_2.addWidget(self.select_wx_path_bt)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.log_label = QLabel(self.main_widget)
        self.log_label.setObjectName("label_3")

        self.verticalLayout.addWidget(self.log_label)

        self.log_area = QPlainTextEdit(self.main_widget)
        self.log_area.setObjectName("log_area")

        self.clean_log_bt = QPushButton(self.main_widget)
        self.clean_log_bt.setObjectName("clean_log_bt")

        self.verticalLayout.addWidget(self.log_area)
        self.verticalLayout.addWidget(self.clean_log_bt)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        main_window.setCentralWidget(self.main_widget)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)

    # setupUi

    def retranslateUi(self, main_window: QMainWindow):
        main_window.setWindowTitle("main_window")
        self.refresh_procs_bt.setText("刷新进程")
        self.dll_inject_stats_header.setText("DLL注入状态:")
        self.proc_list_header.setText("进程列表:")
        self.user_name_header.setText("登陆用户:")
        self.port_header.setText("绑定端口:")
        self.inject_statu_label.setText("未知")
        self.login_user_name_label.setText("未同步")
        self.pid_header.setText("进程ID")
        self.proc_id_label.setText("0")
        self.bind_prot_label.setText("0")
        self.inject_dll_bt.setText("注入dll")
        self.sync_login_status_bt.setText("同步登录状态")
        self.enable_msg_callback.setText("启用消息回调")
        self.wx_path_label.setText("微信路径暂未选择")
        self.select_wx_path_bt.setText("选择微信路径")
        self.log_label.setText("日志")
        self.clean_log_bt.setText("清空日志")
        self.wx_path_label.setText("微信路径暂未选择")

    # retranslateUi
