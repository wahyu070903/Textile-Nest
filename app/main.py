import sys
import style
import cv2
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QDockWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
    QFrame, QSizePolicy, QGraphicsView, QGraphicsScene, QStyle,
    QGroupBox, QFormLayout, QSlider, QComboBox, QSpinBox, QCheckBox,
    QStatusBar, QSplitter, QCheckBox, QFileDialog, QGraphicsScene
)
from PySide6.QtGui import QPixmap, QImage
from camera import Camera
from method.canny import CannyMethod

def make_icon(letter: str, bg: str = "#0078d4") -> QIcon:
    size = 24
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(bg))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(1, 1, size - 2, size - 2, 5, 5)
    painter.setPen(QColor("white"))
    font = QFont()
    font.setBold(True)
    font.setPointSize(11)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, letter)
    painter.end()
    return QIcon(pixmap)

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("SidePanel")
        self.setMinimumWidth(220)
        self.setMaximumWidth(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("Left Panel — Fabric Detection")
        header.setObjectName("PanelHeader")
        layout.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(10)

        detect_group = QGroupBox("Deteksi Kain")
        form = QFormLayout(detect_group)
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Canny Contour", 
            "Edge Detection", 
            "AI Segmentation"
        ])
        
        form.addRow("Metode:", self.method_combo)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(120)
        form.addRow("Threshold:", self.threshold_slider)

        self.min_area_spin = QSpinBox()
        self.min_area_spin.setRange(0, 100000)
        self.min_area_spin.setValue(500)
        form.addRow("Min Area (px):", self.min_area_spin)

        self.auto_detect_check = QCheckBox("Auto-detect real-time")
        self.auto_detect_check.setChecked(True)
        form.addRow(self.auto_detect_check)

        body_layout.addWidget(detect_group)

        self.detect_btn = QPushButton("Deteksi Sekarang")
        self.detect_btn.setObjectName("PrimaryButton")
        body_layout.addWidget(self.detect_btn)

        shapes_group = QGroupBox("Show Layer")
        shapes_layout = QVBoxLayout(shapes_group)
        
        self.layer_check_normal = QCheckBox("Normal Layer")
        self.layer_check_invert = QCheckBox("Invert Layer")
        self.layer_check_edges = QCheckBox("Edges Layer")
        self.layer_check_pattern = QCheckBox("Pattern Layer")

        self.layer_check_normal.setChecked(True)
        self.layer_check_normal.toggled.connect(self.on_normal_toggled)
        self.layer_check_invert.toggled.connect(self.on_invert_toggled)

        layer_mode = self.layer_check_edges
        shapes_layout.addWidget(self.layer_check_normal)
        shapes_layout.addWidget(self.layer_check_invert)
        shapes_layout.addWidget(self.layer_check_edges)
        shapes_layout.addWidget(self.layer_check_pattern)
        body_layout.addWidget(shapes_group)

        body_layout.addStretch()
        layout.addWidget(body)

    def on_normal_toggled(self, checked):
        if checked:
            self.layer_check_invert.setChecked(False)

    def on_invert_toggled(self, checked):
        if checked:
            self.layer_check_normal.setChecked(False)

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("SidePanel")
        self.setMinimumWidth(220)
        self.setMaximumWidth(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("Right Panel — Pattern")
        header.setObjectName("PanelHeader")
        layout.addWidget(header)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(10)

        pattern_group = QGroupBox("Pattern Generator")
        form = QFormLayout(pattern_group)
        self.pattern_type = QComboBox()
        self.pattern_type.addItems(["Seam Allowance", "Grainline", "Notch Marker", "Grading"])
        form.addRow("Tipe:", self.pattern_type)

        self.seam_allowance_spin = QSpinBox()
        self.seam_allowance_spin.setRange(0, 50)
        self.seam_allowance_spin.setValue(10)
        self.seam_allowance_spin.setSuffix(" mm")
        form.addRow("Seam Allowance:", self.seam_allowance_spin)

        self.smooth_check = QCheckBox("Smooth Edges")
        self.smooth_check.setChecked(True)
        form.addRow(self.smooth_check)

        body_layout.addWidget(pattern_group)

        self.generate_btn = QPushButton("Buat Pattern")
        self.generate_btn.setObjectName("PrimaryButton")
        body_layout.addWidget(self.generate_btn)

        layers_group = QGroupBox("Layer Pattern")
        layers_layout = QVBoxLayout(layers_group)
        self.layers_list = QListWidget()
        self.layers_list.addItems(["Outline", "Seam Line", "Grainline", "Label"])
        layers_layout.addWidget(self.layers_list)
        body_layout.addWidget(layers_group)

        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)
        self.export_dxf_btn = QPushButton("Export ke DXF")
        self.export_pdf_btn = QPushButton("Export ke PDF")
        export_layout.addWidget(self.export_dxf_btn)
        export_layout.addWidget(self.export_pdf_btn)
        body_layout.addWidget(export_group)

        body_layout.addStretch()
        layout.addWidget(body)


class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("Camera View")
        header.setObjectName("PanelHeader")
        layout.addWidget(header)

        frame = QFrame()
        frame.setObjectName("CameraViewFrame")
        frame_layout = QVBoxLayout(frame)

        self.view = QGraphicsView()
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.NoFrame)
        self.view.setStyleSheet("border: none; background-color: #202020;")
        self.scene = QGraphicsScene()
        self.scene.addText("Live Camera Feed").setDefaultTextColor(QColor("#9a9a9a"))
        self.view.setScene(self.scene)
        frame_layout.addWidget(self.view)

        controls = QHBoxLayout()
        self.start_btn = QPushButton("Start Camera")
        self.stop_btn = QPushButton("Stop Camera")
        self.capture_btn = QPushButton("Capture Frame")

        self.capture_btn.clicked.connect(self.captureImage)
        self.start_btn.clicked.connect(self.openCamera)
        self.stop_btn.clicked.connect(self.stopCamera)

        controls.addWidget(self.start_btn)
        controls.addWidget(self.stop_btn)
        controls.addWidget(self.capture_btn)
        controls.addStretch()
        frame_layout.addLayout(controls)

        layout.addWidget(frame)

        self.imageUpdate = None
        self.imagePath = None
        self.imageData = None
        self.imageCaptured = None
        self.isImageCaptured = False

        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.pixmap_item = self.scene.addPixmap(QPixmap())
        
    def captureImage(self):
        if self.imageUpdate is None:
            print("No frame available")
            return

        # Simpan frame terakhir
        self.imageCaptured = self.imageUpdate.copy()
        self.isImageCaptured = True

        # Hentikan stream
        self.stopCamera()

        # Tampilkan hasil capture
        rgb = cv2.cvtColor(self.imageCaptured, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape

        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(image)

        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        print("Image captured")        

    def openImage(self):    #fungsi percobaan
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )

        if not filename:
            return
        
        self.imagePath = filename
        self.imageData = cv2.imread(filename)

        if self.imageData is None:
            print("Failed to load image")
            return

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        pixmap = QPixmap(self.imagePath)
        self.scene.addPixmap(pixmap)
        
    def openCamera(self):
        self.camera = Camera(port=1, width=1280, height=720)
        self.timer.start(30)
    
    def updateFrame(self):
        ret, self.imageUpdate = self.camera.read()
        if not ret:
            return

        self.methods = {
            "Canny Contour": CannyMethod(),
            # "Edge Detection": EdgeMethod(),
            # "AI Segmentation": AISegmentMethod()
        }

        method_name = self.left_panel.method_combo.currentText()
        realtime_detect = self.left_panel.auto_detect_check.isChecked()
        edge_layer_visibility = self.left_panel.layer_check_edges.isChecked()

        edge_layer = self.imageUpdate.copy()
        if realtime_detect and edge_layer_visibility:
            edges = self.methods[method_name].process(edge_layer)
            if edges is not None:
                    edge_layer[edges > 0] = (0, 255, 0)
                    rgb = cv2.cvtColor(edge_layer, cv2.COLOR_BGR2RGB)
    
        else:
            rgb = cv2.cvtColor(self.imageUpdate, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape
        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(self.pixmap_item.boundingRect())
        self.view.fitInView(
            self.scene.sceneRect(),
            Qt.KeepAspectRatioByExpanding
        )
    
    def stopCamera(self):
        self.timer.stop()
        if self.camera:
            self.camera.release()
            self.camera = None

        self.scene.clear()
        self.scene.addText("Live Camera Feed").setDefaultTextColor(QColor("#9a9a9a"))
        self.pixmap_item = self.scene.addPixmap(QPixmap())
        self.view.setScene(self.scene)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     if self.scene.items():
    #         self.view.fitInView(
    #             self.scene.sceneRect(),
    #             Qt.KeepAspectRatio
    #         )

    def closeEvent(self, event):
        self.stopCamera()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fabric Pattern Detector")
        self.resize(1280, 800)

        self._build_menu_bar()
        self._build_toolbar()
        self._build_central_widget()
        self._build_status_bar()

    def _build_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("New Project", self, triggered=lambda: self._status("New Project")))
        file_menu.addAction(QAction("Open...", self, triggered=lambda: self._status("Open")))
        file_menu.addAction(QAction("Save", self, triggered=lambda: self._status("Save")))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Import DXF...", self, triggered=lambda: self._status("Import DXF")))
        file_menu.addSeparator()
        exit_action = QAction("Exit", self, triggered=self.close)
        file_menu.addAction(exit_action)

        views_menu = menu_bar.addMenu("Views")
        self.toggle_left_action = QAction("Left Panel", self, checkable=True, checked=True)
        self.toggle_left_action.triggered.connect(self._toggle_left_panel)
        self.toggle_right_action = QAction("Right Panel", self, checkable=True, checked=True)
        self.toggle_right_action.triggered.connect(self._toggle_right_panel)
        views_menu.addAction(self.toggle_left_action)
        views_menu.addAction(self.toggle_right_action)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(QAction("About", self, triggered=lambda: self._status("Fabric Pattern Detector v1.0")))

    def _build_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(22, 22))
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        new_action = QAction(make_icon("N", "#0078d4"), "New Project", self)
        new_action.triggered.connect(lambda: self._status("New Project"))

        open_action = QAction(make_icon("O", "#5c9c3d"), "Open", self)
        open_action.triggered.connect(lambda: self._status("Open"))

        save_action = QAction(make_icon("S", "#c47b12"), "Save", self)
        save_action.triggered.connect(lambda: self._status("Save"))

        import_action = QAction(make_icon("D", "#8a4fbf"), "Import DXF", self)
        import_action.triggered.connect(lambda: self._status("Import DXF"))

        for action in (new_action, open_action, save_action):
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(import_action)

    def _build_central_widget(self):
        self.splitter = QSplitter(Qt.Horizontal)

        self.left_panel = LeftPanel()
        self.camera_view = CameraView()
        self.right_panel = RightPanel()
        self.camera_view.left_panel = self.left_panel

        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.camera_view)
        self.splitter.addWidget(self.right_panel)

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)
        self.splitter.setSizes([260, 700, 260])

        self.setCentralWidget(self.splitter)

    def _build_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def _status(self, text: str):
        self.statusBar().showMessage(text, 3000)

    def _toggle_left_panel(self, checked: bool):
        self.left_panel.setVisible(checked)

    def _toggle_right_panel(self, checked: bool):
        self.right_panel.setVisible(checked)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(style.VS_LIGHT_QSS)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()