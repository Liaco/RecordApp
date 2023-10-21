import configparser
import datetime
import os
import re
import subprocess

import xlwings as xw
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QMessageBox, QVBoxLayout, QWidget)

import src.input_ui
import src.main1_ui
from src.auto_record import RecordData
from src.sentence_slice import sentence_slice


class BusyProgress(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel(self)
        movie = QMovie('./asset/Vp3R.gif')
        label.setMovie(movie)
        movie.start()
        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.show()

    def close(self) -> bool:
        return super().close()


class InputWin(QWidget):
    def __init__(self, mianwin, base_path):
        super().__init__()
        self.base_path = base_path
        self.mainwin = mianwin
        self.win = src.input_ui.Ui_Input()
        self.win.setupUi(self, base_path)
        self.win.pushButton.clicked.connect(self.done_button)
        self.state = False
        settings = configparser.ConfigParser()
        settings.read(os.path.join(base_path, './conf/sub.ini'))
        if 'Sub' in settings:
            window_settings = settings['Sub']
            x = int(window_settings['x'])
            y = int(window_settings['y'])
            width = int(window_settings['width'])
            height = int(window_settings['height'])
            self.setGeometry(x, y, width, height)
        self.show()

    def done_button(self):
        text = self.win.textEdit.toPlainText().strip()
        self.win.textEdit.clear()
        if text != '':
            sentence_lists = text.splitlines()
            sentence_list, del_sentence = sentence_slice(sentence_lists)
            for sentence in sentence_list:
                self.mainwin.ui.textEdit.append(sentence)
            for sentence in del_sentence:
                self.mainwin.ui.textEdit.append(sentence)
            QMessageBox.information(self, "Info", "Done")
            self.state = True
            self.close()
            self.mainwin.show()

        else:
            QMessageBox.information(self, "Info", "No text")
            self.state = True
            self.close()
            self.mainwin.show()

    def closeEvent(self, event):
        if self.state:
            self.mainwin.show()
            event.accept()
            return
        reply = QMessageBox.question(
            self, "Confirm Close", "Are you sure you want to close this window?")
        if reply == QMessageBox.StandardButton.Yes:
            self.done_button()
        else:
            event.ignore()
        settings = configparser.ConfigParser()
        settings['Sub'] = {
            'x': str(self.geometry().x()),
            'y': str(self.geometry().y()),
            'width': str(self.geometry().width()),
            'height': str(self.geometry().height())
        }
        with open(os.path.join(self.base_path, './conf/sub.ini'), 'w') as configfile:
            settings.write(configfile)


class AutoRecord(QMainWindow):
    dist_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, size, save_path) -> None:
        super().__init__()
        self.ui = src.main1_ui.Ui_AutoRecord()
        self.ui.setupUi(self, size, self.dist_dir)
        self.ui.actionnew.triggered.connect(self.new_menu)
        self.ui.actionOpen.triggered.connect(self.Open_menu)
        self.ui.actionClose.triggered.connect(self.close_menu)
        self.ui.actionSave.triggered.connect(self.save_menu)
        self.ui.actionCheck.triggered.connect(self.check_button)
        self.ui.Done.clicked.connect(self.done_button)
        self.ui.Send.clicked.connect(self.send)
        self.ui.Import.clicked.connect(self.import_button)
        self.ui.actionUndo.triggered.connect(self.undo_button)
        self.ui.textEdit.installEventFilter(self)
        self.state = False
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Not Readly')
        self.index = 0
        self.save_path = save_path

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj is self.ui.textEdit:
            if event.key() == Qt.Key.Key_Return and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.send()
                return True
        return super().eventFilter(obj, event)

    def send(self):
        if not self.state:
            QMessageBox.warning(self, 'Warning', 'Please open table first')
            return
        texts = self.ui.textEdit.toPlainText().strip().split('\n')
        try:
            for text in texts:
                if bool(re.search(r'\d+', text)):
                    self.ui.textEdit.clear()
                    message = RecordData(
                        text, self.workbook, self.file_name).run()
                    self.ui.listWidget.addItem(message)
                    scroll_bar = self.ui.listWidget.verticalScrollBar()
                    scroll_bar.setValue(scroll_bar.maximum())
                    QApplication.processEvents()
                else:
                    QMessageBox.warning(self, 'Warning', 'No num to record')
            self.check_button(state=True)
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'{e}')

    def sele_save_path(self):
        folder_dialog = QFileDialog.getExistingDirectory(
            caption="Select Folder", directory="")
        try:
            if folder_dialog[0]:
                self.save_path = folder_dialog[0]
        except:
            pass

    def new_menu(self):
        try:
            self.current_date = datetime.datetime.now().strftime('%m%d')
            self.file_name = f"./Output/Tables/统计表_{self.current_date}2.xlsx"
            self.app = xw.App(visible=True, add_book=False)
            self.workbook = self.app.books.open(
                os.path.join(self.dist_dir, 'asset', 'templet.xlsx'))
            self.workbook.save(self.file_name)
            self.state = True
            self.status_bar.showMessage('Readly')
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'{e}')

    def Open_menu(self):
        desktop_path = os.path.expanduser("~/Desktop")
        file_dialog_result = QFileDialog.getOpenFileName(
            caption="Open File",
            directory=desktop_path,
            filter="EXCEL files (*.xlsx *.xls);;All Files (*)"
        )

        if file_dialog_result[0]:  # Check if a file was selected
            # Extract the file path from the tuple
            file_path = file_dialog_result[0]
            if os.path.isfile(file_path):
                self.app = xw.App(visible=True, add_book=False)
                self.workbook = self.app.books.open(file_path)
                self.workbook.save()
                self.state = True
                self.status_bar.showMessage('Ready')

    def save_menu(self):
        try:
            self.workbook.save()
        except Exception as e:
            QMessageBox.warning(self, 'Warning', f'{e}')

    def close_menu(self):
        if not self.state:
            QMessageBox.warning(self, 'Info', 'Please open table first')
            return
        state = QMessageBox.question(self, "Info", "Confirm to Close?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)
        if state == QMessageBox.StandardButton.Yes:
            try:
                self.workbook.save()
                self.workbook.close()
                self.app.quit()
                self.state = False
                self.status_bar.showMessage("Not Readly")
            except Exception as e:
                QMessageBox.warning(
                    self, "Warning", f"{e}")

    def done_button(self):
        if not self.state:
            QMessageBox.warning(self, 'Warning', 'Please open table first')
            return
        if self.save_path == 'None':
            QMessageBox.warning(
                self, 'Warning', 'Please select a path to save')
            self.sele_save_path()
            return
        self.setEnabled(False)
        # self.sub = BusyProgress()
        self.show()
        QApplication.processEvents()
        try:
            path = os.path.join(self.dist_dir, "Output", "Pic")
            RecordData('0', self.workbook, self.file_name).end(self.dist_dir)
            self.finished()
            if os.name == 'posix':
                subprocess.call(["open", path])

            elif os.name == 'nt':
                subprocess.call(["explorer", path], shell=True)

        except Exception as e:
            QMessageBox.warning(self, 'Warning', f"{e}")
            self.setEnabled(True)
            # self.sub.close()
            QApplication.processEvents()

    def finished(self):
        self.setEnabled(True)
        # self.sub.close()
        QApplication.processEvents()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Confirm Close", "Are you sure you want to close this window?")
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            settings = configparser.ConfigParser()
            settings['Window'] = {
                'x': str(self.geometry().x()),
                'y': str(self.geometry().y()),
                'width': str(self.geometry().width()),
                'height': str(self.geometry().height()),
                'size': str(self.ui.splitter.sizes()),
                'save_path': str(self.save_path)
            }
            with open(os.path.join(self.dist_dir, './conf/main.ini'), 'w') as configfile:
                settings.write(configfile)

            if self.state:
                try:
                    self.workbook.save()
                    self.workbook.close()
                    self.app.quit()
                except Exception as e:
                    QMessageBox.warning(self, 'Warning', f'{e}')

        else:
            event.ignore()

    def import_button(self):
        self.hide()
        self.win = InputWin(self, self.dist_dir)

    # def undo_button(self):
    #     if not text_last:
    #         QMessageBox.warning(self, "Warning", "No text to undo")
    #         return
    #     text = text_last.pop()
    #     message = RecordData(text, self.workbook,
    #                          self.file_name).run(mode=False)
    #     last_item = self.ui.listWidget.takeItem(self.ui.listWidget.count() - 1)
    #     if last_item is not None:
    #         last_item = None

    def undo_button(self):
        select_item = self.ui.listWidget.selectedItems()
        if not select_item:
            QMessageBox.information(
                self, 'Info', 'Please select item to recall')
            return
        for item in select_item:
            text = RecordData(item.text().splitlines()[0][7:], self.workbook,
                              self.file_name).callback()
            # print(type(text))
            print(text)
            if '无法录入' in text:
                QMessageBox.warning(self, 'Warning', "Can't recall this item")
                return
            self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def check_button(self, state=None):
        items = [self.ui.listWidget.item(i).text()
                 for i in range(self.ui.listWidget.count())]
        if not items:
            QMessageBox.information(self, 'Info', 'No recoder')
            return
        del_items = [i for i, item in enumerate(items) if "无法录入" in item]
        if not del_items:
            if not state:
                QMessageBox.information(self, 'Info', 'No failed recoder')
            return
        for item in del_items[::-1]:
            x = self.ui.listWidget.takeItem(item)
            if x is not None:
                x = x.text()
                x = x.splitlines()[0]
                self.ui.textEdit.append(f'{x[7:]}\n')
        if len(del_items) == 1:
            QMessageBox.information(
                self, 'Info', f'Find {len(del_items)} recoder')
            return
        QMessageBox.information(
            self, 'Info', f'Find {len(del_items)} recoders')


if __name__ == '__main__':
    app = QApplication([])
    dist_dir = os.path.dirname(os.path.abspath(__file__))
    settings = configparser.ConfigParser()
    settings.read(os.path.join(dist_dir, './conf/main.ini'))
    if 'Window' in settings:
        window_settings = settings['Window']
        x = int(window_settings['x'])
        y = int(window_settings['y'])
        width = int(window_settings['width'])
        height = int(window_settings['height'])
        size = eval(window_settings['size'])
        save_path = window_settings['save_path']
        win = AutoRecord(size, save_path)
        win.setGeometry(x, y, width, height)
    else:
        win = AutoRecord([300, 120], None)
    win.show()
    app.exec()
