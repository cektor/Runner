import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QProgressBar, QMessageBox, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import speedtest


def get_logo_path():
    if hasattr(sys, "_MEIPASS"):  # PyInstaller ile paketlenmişse
        return os.path.join(sys._MEIPASS, "runnerlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/runnerlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/runnerlo.png"
    elif os.path.exists("runnerlo.png"):
        return "runnerlo.png"
    return None


def get_icon_path():
    if hasattr(sys, "_MEIPASS"):  # PyInstaller ile paketlenmişse
        return os.path.join(sys._MEIPASS, "runnerlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/runnerlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/runnerlo.png"
    elif os.path.exists("runnerlo.png"):
        return "runnerlo.png"
    return None


LOGO_PATH = get_logo_path()
ICON_PATH = get_icon_path()


class SpeedTestThread(QThread):
    speed_test_completed = pyqtSignal(float, float, float)  # Ping, Download, Upload
    speed_test_failed = pyqtSignal(str)
    progress_signal = pyqtSignal(int)  # Test sırasında ilerleme bilgisini iletmek için

    def run(self):
        try:
            # Speedtest objesini oluşturuyoruz
            st = speedtest.Speedtest()

            # En iyi sunucuyu seçiyoruz
            self.progress_signal.emit(10)  # Başlangıç ilerlemesi
            st.get_best_server()  # En iyi sunucu seçilir
            self.progress_signal.emit(30)  # Sunucu seçildi

            # Ping bilgisi alınıyor
            ping = st.results.ping
            # İndirme hızını Mbps cinsinden alıyoruz
            download_speed = st.download() / 1_000_000
            self.progress_signal.emit(60)  # İndirme testi tamamlanmak üzere

            # Yükleme hızını Mbps cinsinden alıyoruz
            upload_speed = st.upload() / 1_000_000
            self.progress_signal.emit(90)  # Yükleme testi tamamlanmak üzere

            # Test sonuçlarını sinyalle gönderiyoruz
            self.speed_test_completed.emit(ping, download_speed, upload_speed)
            self.progress_signal.emit(100)  # Test tamamlandığında %100

        except Exception as e:
            # Hata durumunda hata mesajını sinyalliyoruz
            self.speed_test_failed.emit(f"Speedtest failed: {str(e)}")


class AboutDialog(QDialog):
    """Hakkında penceresi."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hakkında")
        self.setFixedSize(300, 330)
        self.setStyleSheet("""
            background-color: #0f2734;
            color: white;
            font-family: Arial;
        """)

        layout = QVBoxLayout(self)
        about_label = QLabel(
            """
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
            """
        )
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        layout.addWidget(about_label)

        close_button = QPushButton("Kapat")
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

        # Butonu ortalamak için bir yatay layout kullanalım
        close_layout = QHBoxLayout()
        close_layout.addStretch()  # Sol boşluk
        close_layout.addWidget(close_button)
        close_layout.addStretch()  # Sağ boşluk

        layout.addLayout(close_layout)



class SpeedTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Runner SpeedTest")
        self.setGeometry(800, 200, 800, 600)
        self.setStyleSheet("""
            background-color: #0f2734;     
            color: white;
            font-family: 'Arial', sans-serif;
        """)
        self.setFixedSize(330, 550)  # Sabit boyut (width, height)

        # Uygulama ikonu
        if ICON_PATH:
            self.setWindowIcon(QIcon(ICON_PATH))

        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo_label = QLabel()
        self.set_logo()
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Bağlantı durumu etiketi
        self.connection_status_label = QLabel("Bağlantı Durumu: Bağlantı Bekleniyor...")
        self.connection_status_label.setWordWrap(True)
        self.connection_status_label.setFont(QFont("Arial", 14))
        self.connection_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.connection_status_label)

        # Ping, Download ve Upload hız etiketleri
        self.ping_label = QLabel("Ping: 0 ms")
        self.download_label = QLabel("İndirme: 0 Mbps")
        self.upload_label = QLabel("Yükleme: 0 Mbps")

        for label in [self.ping_label, self.download_label, self.upload_label]:
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 2px solid #8e44ad; border-radius: 10px; padding: 10px;")
            layout.addWidget(label)

        # Test Başlat Butonu
        self.start_button = QPushButton("Başlat")
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

        # Hakkında Butonu
        self.about_button = QPushButton("Hakkında")
        self.about_button.setFont(QFont("Arial", 10))
        self.about_button.setStyleSheet("""
            background-color: #34495e; 
            color: white; 
            border-radius: 10px;
            padding: 3px;
        """)
        self.about_button.clicked.connect(self.show_about_dialog)
        layout.addWidget(self.about_button)

        # Progress bar
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

        # Hız testi iş parçacığı
        self.speed_test_thread = SpeedTestThread()
        self.speed_test_thread.speed_test_completed.connect(self.display_speed_test_results)
        self.speed_test_thread.speed_test_failed.connect(self.handle_speed_test_error)
        self.speed_test_thread.progress_signal.connect(self.update_progress_bar)

    def set_logo(self):
        if LOGO_PATH:
            self.logo_label.setPixmap(QPixmap(LOGO_PATH).scaled(200, 100, Qt.KeepAspectRatio))
        else:
            self.logo_label.setText("Logo bulunamadı.")
            self.logo_label.setAlignment(Qt.AlignCenter)

    def start_speed_test(self):
        # Etiketleri sıfırlıyoruz
        self.ping_label.setText("Ping: 0 ms")
        self.download_label.setText("İndirme: 0 Mbps")
        self.upload_label.setText("Yükleme: 0 Mbps")

        self.connection_status_label.setText("Bağlantı Durumu: Ölçüyor...")
        self.start_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.speed_test_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def display_speed_test_results(self, ping, download_speed, upload_speed):
        self.ping_label.setText(f"Ping: {ping:.0f} ms")
        self.download_label.setText(f"İndirme: {download_speed:.2f} Mbps")
        self.upload_label.setText(f"Yükleme: {upload_speed:.2f} Mbps")
        self.connection_status_label.setText("Bağlantı Durumu: Tamamlandı")
        self.start_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    def handle_speed_test_error(self, error_message):
        self.connection_status_label.setText(f"Bağlantı Durumu: Hata! {error_message}")
        self.start_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())
