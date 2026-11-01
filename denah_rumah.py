import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QRadioButton, QButtonGroup, QGroupBox, QMessageBox
)
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

# ==========================================
# 1. BAGIAN LOGIKA ALGORITMA (KALKULASI)
# ==========================================
class AlgoritmaGaris:
    @staticmethod
    def dda(x1, y1, x2, y2):
        koordinat_piksel = []
        dx = x2 - x1
        dy = y2 - y1
        
        steps = max(abs(dx), abs(dy))
        if steps == 0: return [(x1, y1)]
            
        x_inc = dx / steps
        y_inc = dy / steps
        
        x = x1
        y = y1
        
        for _ in range(int(steps) + 1):
            koordinat_piksel.append((round(x), round(y)))
            x += x_inc
            y += y_inc
            
        return koordinat_piksel

    @staticmethod
    def bresenham(x1, y1, x2, y2):
        koordinat_piksel = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy
        
        while True:
            koordinat_piksel.append((x1, y1))
            if x1 == x2 and y1 == y2: break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        return koordinat_piksel


# ==========================================
# 2. BAGIAN UI: KANVAS QPIXMAP + PENGGARIS + ZOOM + CTRL MOUSE
# ==========================================
class KanvasGambar(QWidget):
    koordinat_diklik = pyqtSignal(int, int)
    zoom_berubah = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        
        self.kertas_gambar = QPixmap(4000, 4000)
        self.kertas_gambar.fill(Qt.GlobalColor.white)
        
        self.tebal_garis = 3
        self.lebar_penggaris = 40 
        
        self.riwayat_semua_garis = [] 
        self.langkah_sekarang = -1    
        self.skala = 1.0 

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.save()
        painter.translate(self.lebar_penggaris, self.lebar_penggaris)
        painter.scale(self.skala, self.skala)
        painter.drawPixmap(0, 0, self.kertas_gambar)
        painter.restore()
        
        painter.fillRect(0, 0, self.width(), self.lebar_penggaris, QColor("#f5f5f5"))
        painter.fillRect(0, 0, self.lebar_penggaris, self.height(), QColor("#f5f5f5"))
        painter.fillRect(0, 0, self.lebar_penggaris, self.lebar_penggaris, QColor("#e8e8e8"))
        
        pen_teks = QPen(Qt.GlobalColor.black)
        painter.setPen(pen_teks)
        font = QFont("Arial", 7)
        painter.setFont(font)
        
        painter.drawText(self.lebar_penggaris - 20, self.lebar_penggaris - 18, 15, 15, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom, "0")

        kelipatan_kecil = 10
        kelipatan_besar = 50
        
        if self.skala <= 0.5:
            kelipatan_kecil = 20
            kelipatan_besar = 100
        elif self.skala >= 2.0:
            kelipatan_kecil = 5
            kelipatan_besar = 25

        # Penggaris X
        max_x_logis = int((self.width() - self.lebar_penggaris) / self.skala)
        for x_logis in range(0, max_x_logis + kelipatan_besar, kelipatan_kecil):
            x_layar = int(x_logis * self.skala) + self.lebar_penggaris
            if x_layar > self.width(): continue 
            
            if x_logis % kelipatan_besar == 0:
                painter.drawLine(x_layar, self.lebar_penggaris - 8, x_layar, self.lebar_penggaris)
                if x_logis != 0: 
                    painter.drawText(x_layar - 15, 2, 30, 15, Qt.AlignmentFlag.AlignCenter, str(x_logis))
            else:
                painter.drawLine(x_layar, self.lebar_penggaris - 4, x_layar, self.lebar_penggaris)
                
        # Penggaris Y
        max_y_logis = int((self.height() - self.lebar_penggaris) / self.skala)
        for y_logis in range(0, max_y_logis + kelipatan_besar, kelipatan_kecil):
            y_layar = int(y_logis * self.skala) + self.lebar_penggaris
            if y_layar > self.height(): continue
            
            if y_logis % kelipatan_besar == 0:
                painter.drawLine(self.lebar_penggaris - 8, y_layar, self.lebar_penggaris, y_layar)
                if y_logis != 0: 
                    painter.drawText(2, y_layar - 7, self.lebar_penggaris - 12, 15, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(y_logis))
            else:
                painter.drawLine(self.lebar_penggaris - 4, y_layar, self.lebar_penggaris, y_layar)
                
        pen_batas = QPen(QColor("#ccc"))
        painter.setPen(pen_batas)
        painter.drawLine(0, self.lebar_penggaris, self.width(), self.lebar_penggaris)
        painter.drawLine(self.lebar_penggaris, 0, self.lebar_penggaris, self.height())

    def mousePressEvent(self, event):
        x_mouse = int(event.position().x())
        y_mouse = int(event.position().y())
        
        x_area_kanvas = x_mouse - self.lebar_penggaris
        y_area_kanvas = y_mouse - self.lebar_penggaris
        
        if x_area_kanvas >= 0 and y_area_kanvas >= 0:
            x_asli = int(x_area_kanvas / self.skala)
            y_asli = int(y_area_kanvas / self.skala)
            self.koordinat_diklik.emit(x_asli, y_asli)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        if self.skala < 5.0:  
            self.skala = round(self.skala + 0.2, 1)
            self.zoom_berubah.emit(self.skala)
            self.update()
            
    def zoom_out(self):
        if self.skala > 0.4:  
            self.skala = round(self.skala - 0.2, 1)
            self.zoom_berubah.emit(self.skala)
            self.update()
            
    def zoom_reset(self):
        self.skala = 1.0
        self.zoom_berubah.emit(self.skala)
        self.update()

    def tambah_ke_riwayat(self, list_titik):
        self.riwayat_semua_garis = self.riwayat_semua_garis[:self.langkah_sekarang + 1]
        self.riwayat_semua_garis.append(list_titik)
        self.langkah_sekarang += 1
        self.render_ulang_dari_riwayat()

    def aksi_undo(self):
        if self.langkah_sekarang >= 0:
            self.langkah_sekarang -= 1
            self.render_ulang_dari_riwayat()

    def aksi_redo(self):
        if self.langkah_sekarang < len(self.riwayat_semua_garis) - 1:
            self.langkah_sekarang += 1
            self.render_ulang_dari_riwayat()

    def render_ulang_dari_riwayat(self):
        self.kertas_gambar.fill(Qt.GlobalColor.white)
        painter = QPainter(self.kertas_gambar)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        
        pen = QPen(Qt.GlobalColor.darkBlue)
        pen.setWidth(self.tebal_garis)
        painter.setPen(pen)
        
        for i in range(self.langkah_sekarang + 1):
            garis = self.riwayat_semua_garis[i]
            for x, y in garis:
                painter.drawPoint(x, y)
                
        painter.end()
        self.update() 

    def bersihkan_kanvas(self):
        self.riwayat_semua_garis.clear()
        self.langkah_sekarang = -1
        self.render_ulang_dari_riwayat()


# ==========================================
# 3. BAGIAN UI: JENDELA UTAMA & KONTROL
# ==========================================
class AplikasiUtama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tugas Grafik Komputer - DDA & Bresenham (Lengkap)")
        self.lagi_klik_awal = True 

        widget_utama = QWidget()
        self.setCentralWidget(widget_utama)
        layout_utama = QHBoxLayout(widget_utama)
        
        panel_kontrol = QVBoxLayout()
        
        grup_algo = QGroupBox("Pilih Algoritma")
        layout_algo = QVBoxLayout()
        self.radio_dda = QRadioButton("DDA")
        self.radio_bresenham = QRadioButton("Bresenham Line")
        self.radio_dda.setChecked(True)
        self.grup_tombol_algo = QButtonGroup()
        self.grup_tombol_algo.addButton(self.radio_dda)
        self.grup_tombol_algo.addButton(self.radio_bresenham)
        layout_algo.addWidget(self.radio_dda)
        layout_algo.addWidget(self.radio_bresenham)
        grup_algo.setLayout(layout_algo)
        panel_kontrol.addWidget(grup_algo)
        
        grup_koordinat = QGroupBox("Input Koordinat")
        layout_koordinat = QVBoxLayout()
        self.input_x1 = QLineEdit(); self.input_x1.setPlaceholderText("X1")
        self.input_y1 = QLineEdit(); self.input_y1.setPlaceholderText("Y1")
        self.input_x2 = QLineEdit(); self.input_x2.setPlaceholderText("X2")
        self.input_y2 = QLineEdit(); self.input_y2.setPlaceholderText("Y2")
        
        layout_baris1 = QHBoxLayout()
        layout_baris1.addWidget(QLabel("Awal (x1, y1):"))
        layout_baris1.addWidget(self.input_x1)
        layout_baris1.addWidget(self.input_y1)
        
        layout_baris2 = QHBoxLayout()
        layout_baris2.addWidget(QLabel("Akhir (x2, y2):"))
        layout_baris2.addWidget(self.input_x2)
        layout_baris2.addWidget(self.input_y2)
        
        layout_koordinat.addLayout(layout_baris1)
        layout_koordinat.addLayout(layout_baris2)
        
        self.btn_gambar_garis = QPushButton("Gambar Garis")
        self.btn_gambar_garis.setStyleSheet("background-color: #e3f2fd; color: black; font-weight: bold;")
        self.btn_gambar_garis.clicked.connect(self.aksi_gambar_garis)
        layout_koordinat.addWidget(self.btn_gambar_garis)
        grup_koordinat.setLayout(layout_koordinat)
        panel_kontrol.addWidget(grup_koordinat)
        
        # --- PANEL ZOOM ---
        grup_zoom = QGroupBox("Zoom Kanvas (Atau Ctrl+Scroll)")
        layout_zoom = QHBoxLayout()
        self.btn_zoom_out = QPushButton("🔍 -")
        self.btn_zoom_reset = QPushButton("100%") 
        self.btn_zoom_in = QPushButton("🔍 +")
        
        self.btn_zoom_out.clicked.connect(lambda: self.kanvas.zoom_out())
        self.btn_zoom_reset.clicked.connect(lambda: self.kanvas.zoom_reset())
        self.btn_zoom_in.clicked.connect(lambda: self.kanvas.zoom_in())
        
        layout_zoom.addWidget(self.btn_zoom_out)
        layout_zoom.addWidget(self.btn_zoom_reset)
        layout_zoom.addWidget(self.btn_zoom_in)
        grup_zoom.setLayout(layout_zoom)
        panel_kontrol.addWidget(grup_zoom)
        
        # --- PANEL UNDO & REDO (SUDAH DI TEMPAT YANG BENAR) ---
        layout_undo_redo = QHBoxLayout()
        
        self.btn_undo = QPushButton("↩ Undo (Ctrl+Z)")
        self.btn_undo.setStyleSheet("background-color: #fff9c4; color: black;")
        self.btn_undo.clicked.connect(self.trigger_undo)
        self.btn_undo.setShortcut("Ctrl+Z") 
        
        self.btn_redo = QPushButton("Redo ↪ (Ctrl+Y)")
        self.btn_redo.setStyleSheet("background-color: #c8e6c9; color: black;")
        self.btn_redo.clicked.connect(self.trigger_redo)
        self.btn_redo.setShortcut("Ctrl+Y") 
        
        layout_undo_redo.addWidget(self.btn_undo)
        layout_undo_redo.addWidget(self.btn_redo)
        panel_kontrol.addLayout(layout_undo_redo)
        
        self.btn_hapus = QPushButton("Hapus / Bersihkan Kanvas")
        self.btn_hapus.setStyleSheet("background-color: #ffebee; color: black; font-weight: bold;")
        self.btn_hapus.clicked.connect(self.aksi_hapus_kanvas)
        panel_kontrol.addWidget(self.btn_hapus)
        
        label_hint = QLabel("💡 <i>Hint: Klik langsung di kanvas untuk nentuin titik awal dan akhir secara otomatis. Gunakan <b>Ctrl + Scroll</b> untuk zoom.</i>")
        label_hint.setWordWrap(True)
        panel_kontrol.addWidget(label_hint)
        
        panel_kontrol.addStretch()
        
        self.kanvas = KanvasGambar()
        self.kanvas.koordinat_diklik.connect(self.tangani_klik_kanvas)
        self.kanvas.zoom_berubah.connect(self.update_label_zoom)
        
        layout_utama.addLayout(panel_kontrol, stretch=1)
        layout_utama.addWidget(self.kanvas, stretch=3)

    def update_label_zoom(self, skala):
        persen = int(skala * 100)
        self.btn_zoom_reset.setText(f"{persen}%")

    def trigger_undo(self):
        self.kanvas.aksi_undo()

    def trigger_redo(self):
        self.kanvas.aksi_redo()

    def tangani_klik_kanvas(self, x, y):
        if self.lagi_klik_awal:
            self.input_x1.setText(str(x))
            self.input_y1.setText(str(y))
            self.input_x2.clear()
            self.input_y2.clear()
            self.lagi_klik_awal = False
        else:
            self.input_x2.setText(str(x))
            self.input_y2.setText(str(y))
            self.aksi_gambar_garis()
            self.lagi_klik_awal = True

    def aksi_gambar_garis(self):
        try:
            x1 = int(self.input_x1.text())
            y1 = int(self.input_y1.text())
            x2 = int(self.input_x2.text())
            y2 = int(self.input_y2.text())
            
            if self.radio_dda.isChecked():
                titik_titik = AlgoritmaGaris.dda(x1, y1, x2, y2)
            else:
                titik_titik = AlgoritmaGaris.bresenham(x1, y1, x2, y2)
            
            self.kanvas.tambah_ke_riwayat(titik_titik)
            
        except ValueError:
            QMessageBox.warning(self, "Error Input", "Koordinatnya harus diisi pake angka bulat (integer) ya!")

    def aksi_hapus_kanvas(self):
        self.kanvas.bersihkan_kanvas()
        self.input_x1.clear(); self.input_y1.clear()
        self.input_x2.clear(); self.input_y2.clear()
        self.lagi_klik_awal = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    jendela = AplikasiUtama()
    jendela.resize(850, 550)
    jendela.show()
    sys.exit(app.exec())