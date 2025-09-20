import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QProgressBar, QDialog, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings

# PyInstaller uyumluluğu için
try:
    import builtins
    sys.modules['__builtin__'] = builtins
except ImportError:
    pass

import speedtest

# Çeviri sözlüğü
TRANSLATIONS = {
    'tr': {
        'window_title': 'Runner SpeedTest',
        'connection_status': 'Bağlantı Durumu: Bağlantı Bekleniyor...',
        'connection_measuring': 'Bağlantı Durumu: Ölçüyor...',
        'connection_completed': 'Bağlantı Durumu: Tamamlandı',
        'connection_error': 'Bağlantı Durumu: Hata!',
        'ping': 'Ping',
        'download': 'İndirme',
        'upload': 'Yükleme',
        'start': 'Başlat',
        'about': 'Hakkında',
        'close': 'Kapat',
        'language': 'Dil',
        'logo_not_found': 'Logo bulunamadı.',
        'speedtest_failed': 'Speedtest başarısız',
        'about_text': '''
            <h2>Runner SpeedTest</h2>
            <p>Bu uygulama, internet bağlantı hızınızı ölçmek için geliştirilmiştir.</p>
            <p><b>Geliştirici:</b> ALG Yazılım Inc.©</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Yazılım</b> Pardus'a Göç'ü Destekler.</p>
            </br>
            <p><b>Sürüm:</b> 1.0</p>
        '''
    },
    'en': {
        'window_title': 'Runner SpeedTest',
        'connection_status': 'Connection Status: Waiting for Connection...',
        'connection_measuring': 'Connection Status: Measuring...',
        'connection_completed': 'Connection Status: Completed',
        'connection_error': 'Connection Status: Error!',
        'ping': 'Ping',
        'download': 'Download',
        'upload': 'Upload',
        'start': 'Start',
        'about': 'About',
        'close': 'Close',
        'language': 'Language',
        'logo_not_found': 'Logo not found.',
        'speedtest_failed': 'Speedtest failed',
        'about_text': '''
            <h2>Runner SpeedTest</h2>
            <p>This application is developed to measure your internet connection speed.</p>
            <p><b>Developer:</b> ALG Yazılım Inc.©</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Yazılım</b> Supports Migration to Pardus.</p>
            </br>
            <p><b>Version:</b> 1.0</p>
        '''
    }
}


def get_logo_path():
    if hasattr(sys, "_MEIPASS"):  # PyInstaller ile paketlenmişse
        return os.path.join(sys._MEIPASS, "runnerlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/runnerlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/runnerlo.png"
    elif os.path.exists("runnerlo.png"):
        return "runnerlo.png"
    return None


def get_icon_path():
    return get_logo_path()


LOGO_PATH = get_logo_path()
ICON_PATH = get_icon_path()


class SpeedTestThread(QThread):
    speed_test_completed = pyqtSignal(float, float, float)
    speed_test_failed = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, language='tr'):
        super().__init__()
        self.language = language

    def run(self):
        try:
            st = speedtest.Speedtest()
            self.progress_signal.emit(10)
            
            st.get_best_server()
            self.progress_signal.emit(30)
            
            ping = st.results.ping if st.results.ping else 0
            
            download_bits = st.download()
            download_speed = round(download_bits / 1024 / 1024, 2)
            self.progress_signal.emit(70)
            
            upload_bits = st.upload()
            upload_speed = round(upload_bits / 1024 / 1024, 2)
            self.progress_signal.emit(100)
            
            self.speed_test_completed.emit(ping, download_speed, upload_speed)
            
        except Exception as e:
            error_msg = f"{TRANSLATIONS[self.language]['speedtest_failed']}: {str(e)}"
            self.speed_test_failed.emit(error_msg)


class AboutDialog(QDialog):
    def __init__(self, parent=None, language='tr'):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(TRANSLATIONS[language]['about'])
        self.setFixedSize(300, 330)
        self.setStyleSheet("""
            background-color: #0f2734;
            color: white;
            font-family: Arial;
        """)

        layout = QVBoxLayout(self)
        about_label = QLabel(TRANSLATIONS[language]['about_text'])
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        layout.addWidget(about_label)

        close_button = QPushButton(TRANSLATIONS[language]['close'])
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            background-color: #7d26b2;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
        """)
        close_button.setFixedSize(100, 40)
        close_button.setFont(QFont("Arial", 12))

        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_button)
        close_layout.addStretch()
        layout.addLayout(close_layout)


class SpeedTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # QSettings ile dil ayarını yükle
        self.settings = QSettings('ALGYazilim', 'RunnerSpeedTest')
        self.language = self.settings.value('language', 'tr')
        
        self.setGeometry(800, 200, 800, 600)
        self.setStyleSheet("""
            background-color: #0f2734;     
            color: white;
            font-family: 'Arial', sans-serif;
        """)
        self.setFixedSize(330, 580)

        if ICON_PATH:
            self.setWindowIcon(QIcon(ICON_PATH))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Dil seçimi
        lang_layout = QHBoxLayout()
        lang_label = QLabel()
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Türkçe', 'English'])
        self.language_combo.setCurrentIndex(0 if self.language == 'tr' else 1)
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.language_combo.setStyleSheet("""
            background-color: #34495e;
            color: white;
            border-radius: 5px;
            padding: 5px;
        """)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        self.logo_label = QLabel()
        self.set_logo()
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        self.connection_status_label = QLabel()
        self.connection_status_label.setWordWrap(True)
        self.connection_status_label.setFont(QFont("Arial", 14))
        self.connection_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.connection_status_label)

        self.ping_label = QLabel()
        self.download_label = QLabel()
        self.upload_label = QLabel()

        for label in [self.ping_label, self.download_label, self.upload_label]:
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 2px solid #8e44ad; border-radius: 10px; padding: 10px;")
            layout.addWidget(label)

        self.start_button = QPushButton()
        self.start_button.setFont(QFont("Arial", 16))
        self.start_button.setStyleSheet("""
            background-color: #7d26b2; 
            color: white; 
            border-radius: 15px;
            padding: 10px;
            font-weight: bold;
        """)
        self.start_button.clicked.connect(self.start_speed_test)
        layout.addWidget(self.start_button)

        self.about_button = QPushButton()
        self.about_button.setFont(QFont("Arial", 10))
        self.about_button.setStyleSheet("""
            background-color: #34495e; 
            color: white; 
            border-radius: 10px;
            padding: 3px;
        """)
        self.about_button.clicked.connect(self.show_about_dialog)
        layout.addWidget(self.about_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            background-color: #7d26b2;
            color: white;
            border-radius: 10px;
            height: 20px;
            text-align: center;
        """)
        layout.addWidget(self.progress_bar)

        self.speed_test_thread = SpeedTestThread(self.language)
        self.speed_test_thread.speed_test_completed.connect(self.display_speed_test_results)
        self.speed_test_thread.speed_test_failed.connect(self.handle_speed_test_error)
        self.speed_test_thread.progress_signal.connect(self.update_progress_bar)
        
        # UI'yi güncelle
        self.update_ui_language()

    def change_language(self, text):
        self.language = 'tr' if text == 'Türkçe' else 'en'
        self.settings.setValue('language', self.language)
        self.speed_test_thread.language = self.language
        self.update_ui_language()
    
    def update_ui_language(self):
        self.setWindowTitle(TRANSLATIONS[self.language]['window_title'])
        self.connection_status_label.setText(TRANSLATIONS[self.language]['connection_status'])
        self.ping_label.setText(f"{TRANSLATIONS[self.language]['ping']}: 0 ms")
        self.download_label.setText(f"{TRANSLATIONS[self.language]['download']}: 0 Mbps")
        self.upload_label.setText(f"{TRANSLATIONS[self.language]['upload']}: 0 Mbps")
        self.start_button.setText(TRANSLATIONS[self.language]['start'])
        self.about_button.setText(TRANSLATIONS[self.language]['about'])

    def set_logo(self):
        if LOGO_PATH:
            self.logo_label.setPixmap(QPixmap(LOGO_PATH).scaled(200, 100, Qt.KeepAspectRatio))
        else:
            self.logo_label.setText(TRANSLATIONS[self.language]['logo_not_found'])
            self.logo_label.setAlignment(Qt.AlignCenter)

    def start_speed_test(self):
        self.ping_label.setText(f"{TRANSLATIONS[self.language]['ping']}: 0 ms")
        self.download_label.setText(f"{TRANSLATIONS[self.language]['download']}: 0 Mbps")
        self.upload_label.setText(f"{TRANSLATIONS[self.language]['upload']}: 0 Mbps")

        self.connection_status_label.setText(TRANSLATIONS[self.language]['connection_measuring'])
        self.start_button.setVisible(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.speed_test_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def display_speed_test_results(self, ping, download_speed, upload_speed):
        self.ping_label.setText(f"{TRANSLATIONS[self.language]['ping']}: {ping:.0f} ms")
        self.download_label.setText(f"{TRANSLATIONS[self.language]['download']}: {download_speed:.2f} Mbps")
        self.upload_label.setText(f"{TRANSLATIONS[self.language]['upload']}: {upload_speed:.2f} Mbps")
        self.connection_status_label.setText(TRANSLATIONS[self.language]['connection_completed'])
        self.start_button.setVisible(True)
        self.progress_bar.setVisible(False)

    def handle_speed_test_error(self, error_message):
        self.connection_status_label.setText(f"{TRANSLATIONS[self.language]['connection_error']} {error_message}")
        self.start_button.setVisible(True)
        self.progress_bar.setVisible(False)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self, self.language)
        about_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())
