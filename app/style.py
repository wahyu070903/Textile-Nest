VS_LIGHT_QSS = """
    QMainWindow {
        background-color: #f3f3f3;
    }

    QMenuBar {
        background-color: #f3f3f3;
        color: #1e1e1e;
        border-bottom: 1px solid #d4d4d4;
        padding: 2px;
    }
    QMenuBar::item {
        background: transparent;
        padding: 4px 10px;
    }
    QMenuBar::item:selected {
        background: #e6e6e6;
        border-radius: 3px;
    }
    QMenu {
        background-color: #ffffff;
        border: 1px solid #d4d4d4;
        padding: 4px;
    }
    QMenu::item {
        padding: 5px 24px 5px 12px;
        border-radius: 3px;
    }
    QMenu::item:selected {
        background-color: #e8e8e8;
    }
    QMenu::separator {
        height: 1px;
        background: #e0e0e0;
        margin: 4px 6px;
    }

    QToolBar {
        background-color: #f8f8f8;
        border-bottom: 1px solid #d4d4d4;
        padding: 4px;
        spacing: 6px;
    }
    QToolButton {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        color: #1e1e1e;
    }
    QToolButton:hover {
        background-color: #e6e6e6;
        border: 1px solid #d4d4d4;
    }
    QToolButton:pressed {
        background-color: #d6d6d6;
    }

    QStatusBar {
        background-color: #f3f3f3;
        border-top: 1px solid #d4d4d4;
        color: #444444;
    }

    QSplitter::handle {
        background-color: #e0e0e0;
    }
    QSplitter::handle:hover {
        background-color: #cfe8ff;
    }

    #PanelHeader {
        background-color: #f3f3f3;
        border-bottom: 1px solid #d4d4d4;
        padding: 8px;
        font-weight: 600;
        color: #1e1e1e;
    }

    #SidePanel {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
    }

    #CameraViewFrame {
        background-color: #202020;
        border: 1px solid #d4d4d4;
    }

    #CameraLabel {
        color: #9a9a9a;
        font-size: 14px;
    }

    QGroupBox {
        font-weight: 600;
        color: #1e1e1e;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        margin-top: 12px;
        background-color: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px;
    }

    QListWidget {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 3px;
    }
    QListWidget::item {
        padding: 6px;
    }
    QListWidget::item:selected {
        background-color: #cfe8ff;
        color: #1e1e1e;
    }

    QPushButton {
        background-color: #ffffff;
        border: 1px solid #c9c9c9;
        border-radius: 4px;
        padding: 6px 12px;
        color: #1e1e1e;
    }
    QPushButton:hover {
        background-color: #f0f0f0;
        border-color: #0078d4;
    }
    QPushButton:pressed {
        background-color: #e0e0e0;
    }
    QPushButton#PrimaryButton {
        background-color: #0078d4;
        color: white;
        border: none;
    }
    QPushButton#PrimaryButton:hover {
        background-color: #106ebe;
    }

    QComboBox, QSpinBox {
        background-color: #ffffff;
        border: 1px solid #c9c9c9;
        border-radius: 4px;
        padding: 3px 6px;
    }

    QLabel {
        color: #1e1e1e;
    }
"""