import sys
import ctypes
import os
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

def is_admin():
    try:
        if sys.platform == "win32":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except:
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置无边框窗口且置顶
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # 初始化浏览器组件
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        # 加载目标网页
        self.browser.setUrl(QUrl("https://www.example.com"))

def main():
    # 非静默模式且非管理员权限时，请求提权（仅Windows）
    if "--silent" not in sys.argv:
        if sys.platform == "win32" and not is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                ' '.join([f'"{sys.argv[0]}"'] + sys.argv[1:] + ["--silent"]),  # 处理路径空格
                None,
                1
            )
            sys.exit()
    
    # 创建应用和窗口
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # 全屏显示（可选）
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
