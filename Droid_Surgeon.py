#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                            DROID SURGEON  ·  v1.1.1
                    Advanced Android Device Management Suite
================================================================================
License: GNU General Public License v3.0 (GPL-3.0)
================================================================================
"""

import sys, os, re, time, shutil, subprocess, threading, functools, platform
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFrame, QLabel, QPushButton, QLineEdit, QTextEdit, QPlainTextEdit,
    QComboBox, QGroupBox, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QMessageBox, QInputDialog, QDialog,
    QDialogButtonBox, QSlider, QCheckBox, QStatusBar, QStackedWidget,
    QFileDialog, QSizePolicy, QAbstractItemView, QTabWidget, QSizeGrip,
    QToolButton, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QSize, QPoint, QSettings
from PyQt5.QtGui import QFont, QColor, QPalette, QKeySequence


# ═══════════════════════════════════════════════════════════════════════════
#                              THEME
# ═══════════════════════════════════════════════════════════════════════════

class T:
    BG_VOID      = "#05080f"
    BG_DEEP      = "#080d16"
    BG_BASE      = "#0b1220"
    BG_PANEL     = "#0f1728"
    BG_PANEL_HI  = "#142034"
    BG_ELEVATED  = "#1a2740"
    BG_INPUT     = "#0a1120"

    B_DIM        = "#1a2842"
    B            = "#243a5c"
    B_HI         = "#314d75"
    B_ACCENT     = "#4a7099"

    CYAN         = "#4fb8d4"
    CYAN_DIM     = "#2d7a94"
    CYAN_DEEP    = "#0f2d3a"

    GREEN        = "#4aad6e"
    GREEN_DIM    = "#1e5233"
    GREEN_DEEP   = "#0a2018"
    RED          = "#cf5560"
    RED_DIM      = "#5e2028"
    RED_DEEP     = "#1f0a0e"
    AMBER        = "#cf9a3c"
    AMBER_DIM    = "#5c4118"
    AMBER_DEEP   = "#1f1608"

    TEXT_HI      = "#dce7f2"
    TEXT         = "#94a8be"
    TEXT_DIM     = "#5c7089"
    TEXT_MUTED   = "#3a4756"

    FONT_UI      = "Inter, Segoe UI, Ubuntu, Sans"
    FONT_MONO    = "JetBrains Mono, Consolas, monospace"


# ═══════════════════════════════════════════════════════════════════════════
#                              UI SCALE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class Scale:
    """Global UI scale factor — 0.7 to 1.4 (70% to 140%)."""
    value = 1.0

    @classmethod
    def set(cls, v):
        cls.value = max(0.7, min(1.4, float(v)))

    @classmethod
    def px(cls, base):
        return max(1, int(round(base * cls.value)))

    @classmethod
    def pt(cls, base):
        return max(6, int(round(base * cls.value)))


def build_stylesheet():
    s = Scale.px

    return f"""
    QMainWindow, QWidget {{
        background: transparent;
        color: {T.TEXT};
        font-family: {T.FONT_UI};
        font-size: {Scale.pt(10)}pt;
    }}
    QMainWindow {{
        background: qradialgradient(cx:0.5, cy:0.4, radius:1.4,
            stop:0 {T.BG_BASE}, stop:0.7 {T.BG_DEEP}, stop:1 {T.BG_VOID});
    }}

    QFrame#panel {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {T.BG_PANEL}, stop:1 {T.BG_DEEP});
        border: 1px solid {T.B};
        border-radius: {s(7)}px;
    }}
    QFrame#statCard {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 {T.BG_PANEL_HI}, stop:1 {T.BG_PANEL});
        border: 1px solid {T.B};
        border-radius: {s(7)}px;
    }}
    QFrame#statCard:hover {{
        border-color: {T.B_HI};
    }}

    QPushButton {{
        background: {T.BG_PANEL_HI};
        border: 1px solid {T.B_HI};
        border-radius: {s(5)}px;
        padding: {s(7)}px {s(14)}px;
        color: {T.TEXT};
        font-weight: 500;
        font-size: {Scale.pt(9)}pt;
        min-height: {s(22)}px;
        outline: none;
    }}
    QPushButton:hover {{
        background: {T.BG_ELEVATED};
        border-color: {T.B_ACCENT};
        color: {T.TEXT_HI};
    }}
    QPushButton:pressed {{
        background: {T.BG_DEEP};
        border-color: {T.CYAN_DIM};
        color: {T.CYAN};
    }}
    QPushButton:disabled {{
        background: {T.BG_DEEP};
        border-color: {T.B_DIM};
        color: {T.TEXT_MUTED};
    }}

    QPushButton#primary {{
        background: {T.BG_PANEL_HI};
        border: 1px solid {T.B_HI};
        border-left: 2px solid {T.CYAN_DIM};
        color: {T.TEXT_HI};
    }}
    QPushButton#primary:hover {{
        background: {T.BG_ELEVATED};
        border-color: {T.CYAN_DIM};
        border-left: 2px solid {T.CYAN};
        color: {T.CYAN};
    }}

    QPushButton#success {{
        background: {T.BG_PANEL_HI};
        border: 1px solid {T.B_HI};
        border-left: 2px solid {T.GREEN_DIM};
        color: {T.TEXT_HI};
    }}
    QPushButton#success:hover {{
        background: {T.GREEN_DEEP};
        border-color: {T.GREEN};
        border-left: 2px solid {T.GREEN};
        color: {T.GREEN};
    }}

    QPushButton#danger {{
        background: {T.BG_PANEL_HI};
        border: 1px solid {T.B_HI};
        border-left: 2px solid {T.RED_DIM};
        color: {T.TEXT_HI};
    }}
    QPushButton#danger:hover {{
        background: {T.RED_DEEP};
        border-color: {T.RED};
        border-left: 2px solid {T.RED};
        color: {T.RED};
    }}

    QPushButton#warning {{
        background: {T.BG_PANEL_HI};
        border: 1px solid {T.B_HI};
        border-left: 2px solid {T.AMBER_DIM};
        color: {T.TEXT_HI};
    }}
    QPushButton#warning:hover {{
        background: {T.AMBER_DEEP};
        border-color: {T.AMBER};
        border-left: 2px solid {T.AMBER};
        color: {T.AMBER};
    }}

    QPushButton#ghost {{
        background: transparent;
        border: 1px solid {T.B_HI};
        color: {T.TEXT_DIM};
    }}
    QPushButton#ghost:hover {{
        background: rgba(79,184,212,0.06);
        border-color: {T.CYAN_DIM};
        color: {T.CYAN};
    }}

    QPushButton#tabBtn {{
        background: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        padding: {s(11)}px {s(12)}px;
        color: {T.TEXT_DIM};
        font-weight: 600;
        font-size: {Scale.pt(8)}pt;
        letter-spacing: 1px;
    }}
    QPushButton#tabBtn:hover {{
        color: {T.TEXT};
        background: rgba(79,184,212,0.04);
    }}
    QPushButton#tabBtn:checked {{
        color: {T.CYAN};
        border-bottom: 2px solid {T.CYAN};
        background: rgba(79,184,212,0.07);
    }}

    QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox {{
        background: {T.BG_INPUT};
        border: 1px solid {T.B};
        border-radius: {s(5)}px;
        padding: {s(6)}px {s(12)}px;
        color: {T.TEXT_HI};
        font-family: {T.FONT_MONO};
        font-size: {Scale.pt(9)}pt;
        min-height: {s(20)}px;
        selection-background-color: {T.CYAN_DIM};
        selection-color: {T.TEXT_HI};
    }}
    QLineEdit:focus, QPlainTextEdit:focus, QTextEdit:focus,
    QSpinBox:focus, QComboBox:focus {{
        border-color: {T.CYAN_DIM};
        background: #0c1626;
    }}
    QComboBox::drop-down {{ border: none; width: {s(22)}px; }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {T.CYAN_DIM};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background: {T.BG_PANEL};
        border: 1px solid {T.B_HI};
        color: {T.TEXT};
        selection-background-color: {T.CYAN_DIM};
        outline: none;
    }}
    QTextEdit, QPlainTextEdit {{
        background: rgba(5,8,15,0.75);
        font-family: {T.FONT_MONO};
        font-size: {Scale.pt(9)}pt;
        padding: {s(8)}px;
        color: {T.TEXT};
    }}

    QGroupBox {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 rgba(15,23,40,0.5), stop:1 rgba(8,13,22,0.5));
        border: 1px solid {T.B};
        border-radius: {s(7)}px;
        margin-top: {s(16)}px;
        padding: {s(14)}px {s(12)}px {s(12)}px {s(12)}px;
        font-weight: 600;
        color: {T.CYAN};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: {s(12)}px;
        top: 2px;
        padding: 1px {s(10)}px;
        color: {T.CYAN};
        background: {T.BG_DEEP};
        border: 1px solid {T.B_HI};
        border-radius: 3px;
        font-size: {Scale.pt(8)}pt;
        letter-spacing: 1.3px;
    }}

    QScrollBar:vertical {{
        background: rgba(5,8,15,0.5);
        width: {s(9)}px;
        border-radius: 4px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {T.B_HI};
        border-radius: 4px;
        min-height: {s(28)}px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {T.CYAN_DIM}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QScrollBar:horizontal {{
        background: rgba(5,8,15,0.5);
        height: {s(9)}px;
        border-radius: 4px;
    }}
    QScrollBar::handle:horizontal {{
        background: {T.B_HI};
        border-radius: 4px;
        min-width: {s(28)}px;
    }}
    QScrollBar::handle:horizontal:hover {{ background: {T.CYAN_DIM}; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

    QTableWidget {{
        background: rgba(5,8,15,0.6);
        border: 1px solid {T.B};
        border-radius: {s(6)}px;
        gridline-color: rgba(36,58,92,0.4);
        color: {T.TEXT};
        font-family: {T.FONT_MONO};
        font-size: {Scale.pt(9)}pt;
        outline: none;
    }}
    QTableWidget::item {{ padding: {s(5)}px {s(8)}px; border: none; }}
    QTableWidget::item:selected {{
        background: {T.CYAN_DEEP};
        color: {T.TEXT_HI};
    }}
    QTableWidget::item:alternate {{ background: rgba(20,32,52,0.3); }}
    QHeaderView::section {{
        background: {T.BG_PANEL_HI};
        color: {T.CYAN};
        padding: {s(7)}px {s(10)}px;
        border: none;
        border-right: 1px solid {T.B};
        border-bottom: 1px solid {T.B_HI};
        font-weight: 600;
        font-size: {Scale.pt(8)}pt;
        letter-spacing: 1px;
    }}
    QHeaderView::section:last {{ border-right: none; }}

    QProgressBar {{
        background: rgba(5,8,15,0.6);
        border: 1px solid {T.B};
        border-radius: {s(4)}px;
        text-align: center;
        height: {s(14)}px;
        color: {T.TEXT_HI};
        font-size: {Scale.pt(8)}pt;
        font-weight: 600;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
            stop:0 {T.CYAN_DIM}, stop:0.5 {T.CYAN}, stop:1 {T.CYAN_DIM});
        border-radius: 3px;
    }}

    QCheckBox {{ spacing: {s(8)}px; color: {T.TEXT}; }}
    QCheckBox::indicator {{
        width: {s(14)}px;
        height: {s(14)}px;
        border-radius: 3px;
        border: 1px solid {T.B_HI};
        background: {T.BG_INPUT};
    }}
    QCheckBox::indicator:checked {{
        background: {T.CYAN_DIM};
        border-color: {T.CYAN};
    }}

    QSlider::groove:horizontal {{
        border: 1px solid {T.B};
        height: {s(5)}px;
        background: {T.BG_INPUT};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {T.CYAN};
        border: 1px solid {T.CYAN};
        width: {s(13)}px;
        margin: -{s(5)}px 0;
        border-radius: {s(6)}px;
    }}

    QTabWidget::pane {{
        background: rgba(5,8,15,0.5);
        border: 1px solid {T.B};
        border-radius: {s(6)}px;
        top: -1px;
    }}
    QTabBar::tab {{
        background: {T.BG_PANEL};
        color: {T.TEXT_DIM};
        border: 1px solid {T.B};
        border-bottom: none;
        border-top-left-radius: {s(5)}px;
        border-top-right-radius: {s(5)}px;
        padding: {s(7)}px {s(16)}px;
        margin-right: 3px;
        font-weight: 600;
        font-size: {Scale.pt(8)}pt;
    }}
    QTabBar::tab:selected {{
        background: {T.BG_PANEL_HI};
        color: {T.CYAN};
        border-color: {T.B_HI};
    }}
    QTabBar::tab:hover:!selected {{
        background: {T.BG_PANEL_HI};
        color: {T.TEXT};
    }}

    QStatusBar {{
        background: {T.BG_DEEP};
        color: {T.TEXT_DIM};
        border-top: 1px solid {T.B};
        font-family: {T.FONT_MONO};
        font-size: {Scale.pt(8)}pt;
    }}
    QStatusBar::item {{ border: none; }}

    QToolTip {{
        background: {T.BG_PANEL_HI};
        color: {T.CYAN};
        border: 1px solid {T.CYAN_DIM};
        padding: {s(4)}px {s(8)}px;
        border-radius: 3px;
        font-family: {T.FONT_MONO};
        font-size: {Scale.pt(8)}pt;
    }}

    QMenuBar {{
        background: {T.BG_DEEP};
        color: {T.TEXT_DIM};
        border-bottom: 1px solid {T.B};
    }}
    QMenuBar::item {{ padding: {s(5)}px {s(12)}px; }}
    QMenuBar::item:selected {{
        background: {T.CYAN_DEEP};
        color: {T.CYAN};
    }}
    QMenu {{
        background: {T.BG_PANEL};
        border: 1px solid {T.B_HI};
        color: {T.TEXT};
    }}
    QMenu::item {{ padding: {s(6)}px {s(20)}px; }}
    QMenu::item:selected {{
        background: {T.CYAN_DEEP};
        color: {T.TEXT_HI};
    }}
    """


# ═══════════════════════════════════════════════════════════════════════════
#                              SIGNALS
# ═══════════════════════════════════════════════════════════════════════════

class SignalBus(QObject):
    log          = pyqtSignal(str, str)
    stats        = pyqtSignal(dict)
    scrcpy_out   = pyqtSignal(str)
    scrcpy_state = pyqtSignal(str)
    fb_out       = pyqtSignal(str)
    processes    = pyqtSignal(list)
    packages     = pyqtSignal(list)
    files        = pyqtSignal(str, list)
    logcat_line  = pyqtSignal(str)
    net_out      = pyqtSignal(str)
    term_out     = pyqtSignal(str)
    scale_change = pyqtSignal(float)


# ═══════════════════════════════════════════════════════════════════════════
#                              HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def run(args, timeout=20):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL)
        return (r.returncode == 0, (r.stdout or "").strip(), (r.stderr or "").strip())
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except FileNotFoundError:
        return False, "", "binary not found"
    except Exception as e:
        return False, "", str(e)[:200]


def which(cmd): return shutil.which(cmd) is not None


def human_bytes(n):
    try: n = float(n)
    except Exception: return "N/A"
    for u in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if n < 1024: return f"{n:.2f} {u}"
        n /= 1024
    return f"{n:.2f} EB"


def human_time(sec):
    try: sec = int(sec)
    except Exception: return "N/A"
    d, sec = divmod(sec, 86400)
    h, sec = divmod(sec, 3600)
    m, s = divmod(sec, 60)
    if d: return f"{d}d {h}h {m}m"
    if h: return f"{h}h {m}m {s}s"
    if m: return f"{m}m {s}s"
    return f"{s}s"


# ═══════════════════════════════════════════════════════════════════════════
#                              STAT CARD
# ═══════════════════════════════════════════════════════════════════════════

class StatCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("statCard")
        self.setMinimumHeight(Scale.px(100))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(Scale.px(14), Scale.px(10), Scale.px(14), Scale.px(10))
        lay.setSpacing(Scale.px(3))

        head = QHBoxLayout()
        head.setSpacing(6)
        self.title = QLabel(title.upper())
        self.title.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-size: {Scale.pt(7)}pt; font-weight: 700; "
            f"letter-spacing: 2px; background: transparent;"
        )
        head.addWidget(self.title)
        head.addStretch()

        self.badge = QLabel("")
        self.badge.setStyleSheet(
            f"color: {T.TEXT_MUTED}; font-size: {Scale.pt(7)}pt; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        head.addWidget(self.badge)
        lay.addLayout(head)

        self.value = QLabel("—")
        self.value.setStyleSheet(
            f"color: {T.TEXT_HI}; font-size: {Scale.pt(20)}pt; font-weight: 700; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        lay.addWidget(self.value)

        self.sub = QLabel("")
        self.sub.setStyleSheet(
            f"color: {T.TEXT_MUTED}; font-size: {Scale.pt(7)}pt; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        lay.addWidget(self.sub)

        self.bar = QProgressBar()
        self.bar.setMaximumHeight(Scale.px(3))
        self.bar.setTextVisible(False)
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setStyleSheet(f"""
            QProgressBar {{
                background: {T.B_DIM};
                border: none;
                border-radius: 1px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {T.CYAN_DIM}, stop:1 {T.CYAN});
                border-radius: 1px;
            }}
        """)
        lay.addWidget(self.bar)

    def apply_scale(self):
        self.setMinimumHeight(Scale.px(100))
        self.title.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-size: {Scale.pt(7)}pt; font-weight: 700; "
            f"letter-spacing: 2px; background: transparent;"
        )
        self.badge.setStyleSheet(
            f"color: {T.TEXT_MUTED}; font-size: {Scale.pt(7)}pt; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        self.sub.setStyleSheet(
            f"color: {T.TEXT_MUTED}; font-size: {Scale.pt(7)}pt; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        self.bar.setMaximumHeight(Scale.px(3))

    def set(self, value, sub="", badge="", color=None, percent=None):
        self.value.setText(str(value))
        self.sub.setText(sub)
        self.badge.setText(badge)
        c = color or T.TEXT_HI
        self.value.setStyleSheet(
            f"color: {c}; font-size: {Scale.pt(20)}pt; font-weight: 700; "
            f"font-family: {T.FONT_MONO}; background: transparent;"
        )
        if percent is not None:
            self.bar.setValue(max(0, min(100, int(percent))))


# ═══════════════════════════════════════════════════════════════════════════
#                              MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════

class DroidSurgeon(QMainWindow):

    TABS = [
        "DASH", "CTRL", "MIRROR", "BOOT", "NET",
        "PKG", "FILES", "PROC", "LOG", "SH", "HELP"
    ]

    def __init__(self):
        super().__init__()
        self.settings = QSettings("DroidSurgeon", "Config")

        try:
            saved_scale = float(self.settings.value("ui_scale", 1.0))
            Scale.set(saved_scale)
        except Exception:
            Scale.set(1.0)

        self.bus = SignalBus()
        self.bus.log.connect(self._on_log)
        self.bus.stats.connect(self._on_stats)
        self.bus.scrcpy_out.connect(self._on_scrcpy_log)
        self.bus.scrcpy_state.connect(self._on_scrcpy_state)
        self.bus.fb_out.connect(self._on_fb_log)
        self.bus.processes.connect(self._on_processes)
        self.bus.packages.connect(self._on_packages)
        self.bus.files.connect(self._on_files)
        self.bus.logcat_line.connect(self._on_logcat_line)
        self.bus.net_out.connect(self._on_net_out)
        self.bus.term_out.connect(self._on_term_out)

        self.device = None
        self.fb_device = None
        self.scrcpy = None
        self.scrcpy_running = False
        self.logcat_proc = None
        self.tab_btns = {}
        self.stat_cards = []
        self.cur_file_path = "/sdcard"
        self.cur_logcat_filter = ""
        self.scrcpy_version = None
        self._stats_lock = threading.Lock()
        self._scrcpy_help_cache = None

        self.setWindowTitle("DROID SURGEON  ·  v1.1.1")
        self.resize(1200, 720)
        self.setMinimumSize(720, 480)

        self._build()
        self._detect_tools()
        self._refresh_adb()
        self._refresh_fb()

        self.sizegrip = QSizeGrip(self)
        self.sizegrip.resize(16, 16)
        self.sizegrip.move(self.width() - 16, self.height() - 16)

        self.timer = QTimer()
        self.timer.timeout.connect(self._poll)
        self.timer.start(4000)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "sizegrip"):
            self.sizegrip.move(self.width() - 16, self.height() - 16)
            self.sizegrip.raise_()

    # ════════════════════════════════════════════════════════════════════
    #                              BUILD
    # ════════════════════════════════════════════════════════════════════

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(Scale.px(10), Scale.px(8), Scale.px(10), Scale.px(6))
        root.setSpacing(Scale.px(8))

        root.addWidget(self._build_header())
        root.addWidget(self._build_tabbar())

        self.stack = QStackedWidget()
        self.stack.addWidget(self._tab_dashboard())
        self.stack.addWidget(self._tab_control())
        self.stack.addWidget(self._tab_mirror())
        self.stack.addWidget(self._tab_fastboot())
        self.stack.addWidget(self._tab_network())
        self.stack.addWidget(self._tab_packages())
        self.stack.addWidget(self._tab_files())
        self.stack.addWidget(self._tab_processes())
        self.stack.addWidget(self._tab_logcat())
        self.stack.addWidget(self._tab_terminal())
        self.stack.addWidget(self._tab_help())
        root.addWidget(self.stack, 1)

        status = QStatusBar()
        self.setStatusBar(status)

        self.status_msg = QLabel("SYSTEM READY")
        self.status_msg.setStyleSheet(
            f"color: {T.TEXT}; font-family: {T.FONT_MONO}; "
            f"font-size: {Scale.pt(8)}pt; letter-spacing: 1px; padding-left: 6px;"
        )
        status.addWidget(self.status_msg)

        self.status_dev = QLabel("DEV : —")
        self.status_dev.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-family: {T.FONT_MONO}; "
            f"font-size: {Scale.pt(8)}pt; letter-spacing: 1px;"
        )
        status.addPermanentWidget(self.status_dev)

        self.status_clock = QLabel("")
        self.status_clock.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-family: {T.FONT_MONO}; "
            f"font-size: {Scale.pt(8)}pt; letter-spacing: 1px; padding-right: 8px;"
        )
        status.addPermanentWidget(self.status_clock)
        self._tick()
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._tick)
        self.clock_timer.start(1000)

    def _tick(self):
        self.status_clock.setText(datetime.now().strftime("%H:%M:%S"))

    def _build_header(self):
        f = QFrame()
        f.setObjectName("panel")
        f.setFixedHeight(Scale.px(64))
        lay = QHBoxLayout(f)
        lay.setContentsMargins(Scale.px(16), Scale.px(8), Scale.px(16), Scale.px(8))
        lay.setSpacing(Scale.px(12))

        logo = QWidget()
        logo.setFixedSize(Scale.px(32), Scale.px(32))
        logo.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {T.CYAN_DIM}, stop:1 {T.CYAN_DEEP});
                border: 1px solid {T.CYAN_DIM};
                border-radius: 5px;
            }}
        """)
        llo = QVBoxLayout(logo)
        llo.setContentsMargins(0, 0, 0, 0)
        ll = QLabel("DS")
        ll.setAlignment(Qt.AlignCenter)
        ll.setStyleSheet(
            f"color: {T.CYAN}; font-size: {Scale.pt(12)}pt; font-weight: 900; "
            f"background: transparent;"
        )
        llo.addWidget(ll)
        lay.addWidget(logo)

        tb = QVBoxLayout()
        tb.setSpacing(1)
        t = QLabel("DROID SURGEON")
        t.setStyleSheet(
            f"color: {T.TEXT_HI}; font-size: {Scale.pt(12)}pt; font-weight: 700; "
            f"letter-spacing: 3px; background: transparent;"
        )
        s = QLabel("ANDROID DEVICE MANAGEMENT  ·  v1.1.1  ·  GPL-3.0")
        s.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-size: {Scale.pt(7)}pt; font-weight: 500; "
            f"letter-spacing: 2px; background: transparent;"
        )
        tb.addWidget(t)
        tb.addWidget(s)
        lay.addLayout(tb)
        lay.addStretch()

        self.pill_adb = self._pill("ADB")
        self.pill_fb  = self._pill("FASTBOOT")
        self.pill_sc  = self._pill("MIRROR")
        for p in (self.pill_adb, self.pill_fb, self.pill_sc):
            lay.addWidget(p)

        self.scale_btn = QToolButton()
        self.scale_btn.setText("UI")
        self.scale_btn.setToolTip("Interface scale (Ctrl+ / Ctrl-)")
        self.scale_btn.setPopupMode(QToolButton.InstantPopup)
        self.scale_btn.setCursor(Qt.PointingHandCursor)
        self.scale_btn.setStyleSheet(f"""
            QToolButton {{
                background: {T.BG_PANEL_HI};
                border: 1px solid {T.B_HI};
                border-radius: 4px;
                padding: {Scale.px(4)}px {Scale.px(10)}px;
                color: {T.TEXT};
                font-weight: 600;
                font-size: {Scale.pt(8)}pt;
            }}
            QToolButton:hover {{
                background: {T.BG_ELEVATED};
                border-color: {T.CYAN_DIM};
                color: {T.CYAN};
            }}
            QToolButton::menu-indicator {{ image: none; width: 0; }}
        """)

        scale_menu = QMenu(self.scale_btn)
        for label, value in [
            ("Compact  (70%)",  0.70),
            ("Small    (80%)",  0.80),
            ("Medium   (90%)",  0.90),
            ("Default  (100%)", 1.00),
            ("Large    (110%)", 1.10),
            ("XL       (125%)", 1.25),
            ("XXL      (140%)", 1.40),
        ]:
            act = QAction(label, self)
            act.triggered.connect(functools.partial(self._set_scale, value))
            scale_menu.addAction(act)
        self.scale_btn.setMenu(scale_menu)
        lay.addWidget(self.scale_btn)

        return f

    def _pill(self, label):
        lbl = QLabel(f"●  {label}")
        lbl.setStyleSheet(f"""
            QLabel {{
                color: {T.TEXT_MUTED};
                background: rgba(15,23,40,0.6);
                border: 1px solid {T.B_DIM};
                border-radius: 10px;
                padding: {Scale.px(2)}px {Scale.px(10)}px;
                font-size: {Scale.pt(7)}pt;
                font-weight: 700;
                letter-spacing: 1px;
                font-family: {T.FONT_MONO};
            }}
        """)
        return lbl

    def _set_pill(self, pill, label, state):
        colors = {
            "off":  (T.TEXT_MUTED, "rgba(15,23,40,0.6)",   T.B_DIM),
            "ok":   (T.GREEN,      "rgba(74,173,110,0.08)", T.GREEN_DIM),
            "warn": (T.AMBER,      "rgba(207,154,60,0.08)", T.AMBER_DIM),
            "err":  (T.RED,        "rgba(207,85,96,0.08)",  T.RED_DIM),
            "live": (T.CYAN,       "rgba(79,184,212,0.10)", T.CYAN_DIM),
        }
        fg, bg, br = colors.get(state, colors["off"])
        pill.setText(f"●  {label}")
        pill.setStyleSheet(f"""
            QLabel {{
                color: {fg};
                background: {bg};
                border: 1px solid {br};
                border-radius: 10px;
                padding: {Scale.px(2)}px {Scale.px(10)}px;
                font-size: {Scale.pt(7)}pt;
                font-weight: 700;
                letter-spacing: 1px;
                font-family: {T.FONT_MONO};
            }}
        """)

    def _build_tabbar(self):
        f = QFrame()
        f.setObjectName("panel")
        lay = QHBoxLayout(f)
        lay.setContentsMargins(Scale.px(6), 0, Scale.px(6), 0)
        lay.setSpacing(0)

        for i, name in enumerate(self.TABS):
            btn = QPushButton(name)
            btn.setObjectName("tabBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(functools.partial(self._switch, i))
            lay.addWidget(btn)
            self.tab_btns[i] = btn
            if i == 0: btn.setChecked(True)
        lay.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(f)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedHeight(Scale.px(48))
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        return scroll

    def _switch(self, idx):
        for i, b in self.tab_btns.items():
            b.setChecked(i == idx)
        self.stack.setCurrentIndex(idx)
        name = self.TABS[idx]
        if name == "PROC": self._load_processes()
        elif name == "PKG": self._load_packages()
        elif name == "FILES": self._load_files(self.cur_file_path)

    # ════════════════════════════════════════════════════════════════════
    #                              SCALE APPLY
    # ════════════════════════════════════════════════════════════════════

    def _set_scale(self, value):
        try:
            Scale.set(value)
            self.settings.setValue("ui_scale", Scale.value)

            # FIX: QApplication.instance() instead of QApplication
            app = QApplication.instance()
            if app is not None:
                app.setStyleSheet(build_stylesheet())

            # Schedule rebuild for next event loop cycle
            QTimer.singleShot(50, self._rebuild_ui)
            self._log("ok", f"UI scale → {int(Scale.value * 100)}%")
        except Exception as e:
            self._log("err", f"Scale change failed: {str(e)[:120]}")

    def _rebuild_ui(self):
        """Rebuild UI safely without losing state."""
        try:
            current_tab = self.stack.currentIndex() if hasattr(self, "stack") else 0
            was_maximized = self.isMaximized()
            geom = self.geometry()

            # Tear down
            old = self.centralWidget()
            self.setCentralWidget(QWidget())
            if old is not None:
                old.deleteLater()

            # Reset state
            self.stat_cards = []
            self.tab_btns = {}

            # Rebuild (uses _build which creates new central widget)
            self._build()

            # Restore state
            if hasattr(self, "stack") and 0 <= current_tab < self.stack.count():
                self._switch(current_tab)

            if was_maximized:
                self.showMaximized()
            else:
                self.setGeometry(geom)
        except Exception as e:
            self._log("err", f"UI rebuild failed: {str(e)[:150]}")

    # ════════════════════════════════════════════════════════════════════
    #                              DASHBOARD
    # ════════════════════════════════════════════════════════════════════

    def _tab_dashboard(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        cards_scroll = QScrollArea()
        cards_scroll.setWidgetResizable(True)
        cards_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cards_scroll.setFixedHeight(Scale.px(130))
        cards_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        cards_inner = QWidget()
        cards_inner.setMinimumWidth(Scale.px(700))
        row = QHBoxLayout(cards_inner)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(Scale.px(10))

        self.c_battery = StatCard("Battery")
        self.c_storage = StatCard("Storage")
        self.c_memory  = StatCard("Memory")
        self.c_thermal = StatCard("Thermal")
        self.c_uptime  = StatCard("Uptime")
        self.stat_cards = [self.c_battery, self.c_storage, self.c_memory,
                           self.c_thermal, self.c_uptime]
        for c in self.stat_cards:
            c.setMinimumWidth(Scale.px(180))
            row.addWidget(c)
        cards_scroll.setWidget(cards_inner)
        lay.addWidget(cards_scroll)

        split = QHBoxLayout()
        split.setSpacing(Scale.px(10))

        ov = QGroupBox("DEVICE OVERVIEW")
        ov_lay = QVBoxLayout(ov)
        ov_lay.setContentsMargins(Scale.px(12), Scale.px(20), Scale.px(12), Scale.px(12))
        self.overview = QTextEdit()
        self.overview.setReadOnly(True)
        ov_lay.addWidget(self.overview)
        split.addWidget(ov, 2)

        qa = QGroupBox("QUICK ACTIONS")
        qa_lay = QVBoxLayout(qa)
        qa_lay.setContentsMargins(Scale.px(12), Scale.px(20), Scale.px(12), Scale.px(12))
        qa_lay.setSpacing(Scale.px(5))

        actions = [
            ("REFRESH DEVICE",   "primary", self._refresh_adb),
            ("SCREENSHOT",       "ghost",   self._screenshot),
            ("START RECORD",     "warning", self._start_record),
            ("STOP RECORD",      "danger",  self._stop_record),
            ("",                 "",        None),
            ("REBOOT SYSTEM",    "warning", functools.partial(self._reboot, None)),
            ("REBOOT RECOVERY",  "warning", functools.partial(self._reboot, "recovery")),
            ("REBOOT BOOTLOADER","warning", functools.partial(self._reboot, "bootloader")),
            ("",                 "",        None),
            ("FACTORY RESET",    "danger",  self._factory_reset),
        ]
        for text, kind, cb in actions:
            if not text:
                sep = QFrame()
                sep.setFixedHeight(1)
                sep.setStyleSheet(f"background: {T.B_DIM}; border: none;")
                qa_lay.addWidget(sep)
                continue
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(cb)
            qa_lay.addWidget(b)
        qa_lay.addStretch()

        split.addWidget(qa, 1)
        lay.addLayout(split, 1)

        return scroll

    # ════════════════════════════════════════════════════════════════════
    #                              CONTROL
    # ════════════════════════════════════════════════════════════════════

    def _tab_control(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        sel = QFrame()
        sel.setObjectName("panel")
        sel_lay = QHBoxLayout(sel)
        sel_lay.setContentsMargins(Scale.px(12), Scale.px(8), Scale.px(12), Scale.px(8))
        sel_lay.setSpacing(Scale.px(8))

        lbl = QLabel("TARGET")
        lbl.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-size: {Scale.pt(8)}pt; font-weight: 700; "
            f"letter-spacing: 2px; background: transparent;"
        )
        sel_lay.addWidget(lbl)

        self.dev_combo = QComboBox()
        self.dev_combo.setMinimumWidth(Scale.px(180))
        self.dev_combo.currentIndexChanged.connect(self._on_dev_sel)
        sel_lay.addWidget(self.dev_combo)

        r = QPushButton("REFRESH")
        r.setObjectName("primary")
        r.setFixedHeight(Scale.px(28))
        r.clicked.connect(self._refresh_adb)
        sel_lay.addWidget(r)
        sel_lay.addStretch()

        self.dev_state = QLabel("DISCONNECTED")
        self.dev_state.setStyleSheet(self._state_label_style("err"))
        sel_lay.addWidget(self.dev_state)
        lay.addWidget(sel)

        hw = QGroupBox("HARDWARE KEY EVENTS")
        hw_lay = QGridLayout(hw)
        hw_lay.setSpacing(Scale.px(4))

        keys = [
            ("VOL+",  "KEYCODE_VOLUME_UP",      "primary"),
            ("VOL-",  "KEYCODE_VOLUME_DOWN",    "primary"),
            ("PWR",   "KEYCODE_POWER",          "warning"),
            ("HOME",  "KEYCODE_HOME",           "success"),
            ("BACK",  "KEYCODE_BACK",           "danger"),
            ("MENU",  "KEYCODE_MENU",           "primary"),
            ("APPS",  "KEYCODE_APP_SWITCH",     "primary"),
            ("MUTE",  "KEYCODE_VOLUME_MUTE",    "warning"),
            ("CAM",   "KEYCODE_CAMERA",         "primary"),
            ("ENT",   "KEYCODE_ENTER",          "success"),
            ("DEL",   "KEYCODE_DEL",            "danger"),
            ("PLAY",  "KEYCODE_MEDIA_PLAY_PAUSE","primary"),
            ("NEXT",  "KEYCODE_MEDIA_NEXT",     "primary"),
            ("PREV",  "KEYCODE_MEDIA_PREVIOUS", "primary"),
            ("WAKE",  "KEYCODE_WAKEUP",         "success"),
            ("SLEEP", "KEYCODE_SLEEP",          "warning"),
            ("B+",    "KEYCODE_BRIGHTNESS_UP",  "primary"),
            ("B-",    "KEYCODE_BRIGHTNESS_DOWN","primary"),
            ("SYSRQ", "KEYCODE_SYSRQ",          "primary"),
            ("SRCH",  "KEYCODE_SEARCH",         "primary"),
        ]
        for i, (text, code, kind) in enumerate(keys):
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.clicked.connect(functools.partial(self._send_key, code))
            hw_lay.addWidget(b, i // 5, i % 5)
        lay.addWidget(hw)

        dp = QGroupBox("D-PAD")
        dp_lay = QGridLayout(dp)
        dp_lay.setSpacing(Scale.px(6))
        dp_lay.setContentsMargins(Scale.px(40), Scale.px(20), Scale.px(40), Scale.px(20))

        dpad = [
            ("UP",     "KEYCODE_DPAD_UP",     0, 1),
            ("LEFT",   "KEYCODE_DPAD_LEFT",   1, 0),
            ("CENTER", "KEYCODE_DPAD_CENTER", 1, 1),
            ("RIGHT",  "KEYCODE_DPAD_RIGHT",  1, 2),
            ("DOWN",   "KEYCODE_DPAD_DOWN",   2, 1),
        ]
        for txt, code, r, c in dpad:
            b = QPushButton(txt)
            b.setObjectName("primary" if txt != "CENTER" else "success")
            b.setMinimumHeight(Scale.px(40))
            b.setMinimumWidth(Scale.px(70))
            b.clicked.connect(functools.partial(self._send_key, code))
            dp_lay.addWidget(b, r, c)
        lay.addWidget(dp)

        tg = QGroupBox("TOUCH GESTURES")
        tg_lay = QHBoxLayout(tg)
        tg_lay.setSpacing(Scale.px(6))

        for label, cb, kind in [
            ("TAP",        self._dlg_tap,   "primary"),
            ("SWIPE",      self._dlg_swipe, "primary"),
            ("LONG",       self._dlg_long,  "warning"),
            ("PINCH",      self._dlg_pinch, "primary"),
            ("SCROLL ↑",   self._scroll_up, "ghost"),
            ("SCROLL ↓",   self._scroll_dn, "ghost"),
        ]:
            b = QPushButton(label)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(32))
            b.clicked.connect(cb)
            tg_lay.addWidget(b)
        lay.addWidget(tg)

        vol = QGroupBox("VOLUME")
        vol_lay = QHBoxLayout(vol)
        vol_lay.setSpacing(Scale.px(8))

        self.vol_slider = QSlider(Qt.Horizontal)
        self.vol_slider.setRange(0, 15)
        self.vol_slider.setValue(7)
        vol_lay.addWidget(self.vol_slider)

        self.vol_label = QLabel("7 / 15")
        self.vol_label.setStyleSheet(
            f"color: {T.CYAN}; font-family: {T.FONT_MONO}; "
            f"font-size: {Scale.pt(9)}pt; font-weight: 700; min-width: {Scale.px(50)}px;"
        )
        self.vol_slider.valueChanged.connect(
            lambda v: self.vol_label.setText(f"{v} / 15"))
        vol_lay.addWidget(self.vol_label)

        apply_vol = QPushButton("APPLY")
        apply_vol.setObjectName("success")
        apply_vol.setFixedWidth(Scale.px(70))
        apply_vol.clicked.connect(self._apply_volume)
        vol_lay.addWidget(apply_vol)
        lay.addWidget(vol)

        lay.addStretch()
        return scroll

    def _state_label_style(self, kind):
        colors = {
            "err":  (T.RED,   T.RED_DIM),
            "ok":   (T.GREEN, T.GREEN_DIM),
            "warn": (T.AMBER, T.AMBER_DIM),
        }
        fg, br = colors.get(kind, colors["err"])
        return f"""
            QLabel {{
                color: {fg};
                background: rgba(0,0,0,0.35);
                border: 1px solid {br};
                border-radius: 10px;
                padding: {Scale.px(2)}px {Scale.px(10)}px;
                font-size: {Scale.pt(7)}pt;
                font-weight: 700;
                letter-spacing: 1px;
                font-family: {T.FONT_MONO};
            }}
        """

    # ════════════════════════════════════════════════════════════════════
    #                              MIRROR
    # ════════════════════════════════════════════════════════════════════

    def _tab_mirror(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        ctrl = QGroupBox("SCRCPY CONTROLS")
        ctrl_lay = QHBoxLayout(ctrl)
        ctrl_lay.setSpacing(Scale.px(6))

        self.btn_start_mirror = QPushButton("START")
        self.btn_start_mirror.setObjectName("success")
        self.btn_start_mirror.setMinimumHeight(Scale.px(32))
        self.btn_start_mirror.clicked.connect(self._start_scrcpy)
        ctrl_lay.addWidget(self.btn_start_mirror)

        self.btn_stop_mirror = QPushButton("STOP")
        self.btn_stop_mirror.setObjectName("danger")
        self.btn_stop_mirror.setMinimumHeight(Scale.px(32))
        self.btn_stop_mirror.setEnabled(False)
        self.btn_stop_mirror.clicked.connect(self._stop_scrcpy)
        ctrl_lay.addWidget(self.btn_stop_mirror)

        fs = QPushButton("FULLSCREEN")
        fs.setObjectName("primary")
        fs.setMinimumHeight(Scale.px(32))
        fs.clicked.connect(self._mirror_fs)
        ctrl_lay.addWidget(fs)

        rot = QPushButton("ROTATE")
        rot.setObjectName("primary")
        rot.setMinimumHeight(Scale.px(32))
        rot.clicked.connect(self._mirror_rotate)
        ctrl_lay.addWidget(rot)

        scr = QPushButton("SCREENSHOT")
        scr.setObjectName("primary")
        scr.setMinimumHeight(Scale.px(32))
        scr.clicked.connect(self._screenshot)
        ctrl_lay.addWidget(scr)

        ctrl_lay.addStretch()
        lay.addWidget(ctrl)

        opts = QGroupBox("STREAM SETTINGS")
        opts_lay = QGridLayout(opts)
        opts_lay.setSpacing(Scale.px(8))

        opts_lay.addWidget(QLabel("Bitrate:"), 0, 0)
        self.opt_bitrate = QComboBox()
        self.opt_bitrate.addItems(["2 Mbps", "4 Mbps", "8 Mbps", "16 Mbps", "32 Mbps"])
        self.opt_bitrate.setCurrentIndex(2)
        opts_lay.addWidget(self.opt_bitrate, 0, 1)

        opts_lay.addWidget(QLabel("FPS:"), 0, 2)
        self.opt_fps = QComboBox()
        self.opt_fps.addItems(["60", "30", "24", "15"])
        opts_lay.addWidget(self.opt_fps, 0, 3)

        opts_lay.addWidget(QLabel("Max Size:"), 1, 0)
        self.opt_size = QComboBox()
        self.opt_size.addItems(["1920", "1600", "1280", "1024", "854", "640"])
        self.opt_size.setCurrentIndex(2)
        opts_lay.addWidget(self.opt_size, 1, 1)

        opts_lay.addWidget(QLabel("Orientation:"), 1, 2)
        self.opt_rot = QComboBox()
        self.opt_rot.addItems(["0", "90", "180", "270"])
        opts_lay.addWidget(self.opt_rot, 1, 3)

        self.opt_noaudio = QCheckBox("Disable Audio")
        self.opt_noaudio.setChecked(True)
        opts_lay.addWidget(self.opt_noaudio, 2, 0, 1, 2)

        self.opt_turnoff = QCheckBox("Turn Screen Off")
        opts_lay.addWidget(self.opt_turnoff, 2, 2, 1, 2)

        self.opt_always_top = QCheckBox("Always on Top")
        opts_lay.addWidget(self.opt_always_top, 3, 0, 1, 2)

        self.opt_fullscreen = QCheckBox("Start Fullscreen")
        opts_lay.addWidget(self.opt_fullscreen, 3, 2, 1, 2)

        lay.addWidget(opts)

        st = QGroupBox("SESSION MONITOR")
        st_lay = QVBoxLayout(st)
        st_lay.setContentsMargins(Scale.px(12), Scale.px(20), Scale.px(12), Scale.px(12))

        self.mirror_status = QLabel(
            "MIRROR OFFLINE\n\nNo active scrcpy session."
        )
        self.mirror_status.setAlignment(Qt.AlignCenter)
        self.mirror_status.setMinimumHeight(Scale.px(120))
        self.mirror_status.setStyleSheet(f"""
            QLabel {{
                background: rgba(5,8,15,0.6);
                border: 1px dashed {T.B};
                border-radius: 6px;
                color: {T.TEXT_DIM};
                font-family: {T.FONT_MONO};
                font-size: {Scale.pt(9)}pt;
                padding: {Scale.px(16)}px;
            }}
        """)
        st_lay.addWidget(self.mirror_status)

        self.mirror_log = QTextEdit()
        self.mirror_log.setReadOnly(True)
        self.mirror_log.setMaximumHeight(Scale.px(100))
        st_lay.addWidget(self.mirror_log)
        lay.addWidget(st, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              FASTBOOT
    # ════════════════════════════════════════════════════════════════════

    def _tab_fastboot(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        sel = QFrame()
        sel.setObjectName("panel")
        sel_lay = QHBoxLayout(sel)
        sel_lay.setContentsMargins(Scale.px(12), Scale.px(8), Scale.px(12), Scale.px(8))
        sel_lay.setSpacing(Scale.px(8))

        lbl = QLabel("FASTBOOT")
        lbl.setStyleSheet(
            f"color: {T.TEXT_DIM}; font-size: {Scale.pt(8)}pt; font-weight: 700; "
            f"letter-spacing: 2px; background: transparent;"
        )
        sel_lay.addWidget(lbl)

        self.fb_combo = QComboBox()
        self.fb_combo.setMinimumWidth(Scale.px(180))
        sel_lay.addWidget(self.fb_combo)

        rb = QPushButton("REFRESH")
        rb.setObjectName("warning")
        rb.setFixedHeight(Scale.px(28))
        rb.clicked.connect(self._refresh_fb)
        sel_lay.addWidget(rb)
        sel_lay.addStretch()

        self.fb_state = QLabel("DISCONNECTED")
        self.fb_state.setStyleSheet(self._state_label_style("err"))
        sel_lay.addWidget(self.fb_state)
        lay.addWidget(sel)

        cmds = QGroupBox("FASTBOOT OPERATIONS")
        cmds_lay = QGridLayout(cmds)
        cmds_lay.setSpacing(Scale.px(4))

        fb_cmds = [
            ("REBOOT",        "reboot",              "warning"),
            ("REBOOT BOOT",   "reboot-bootloader",   "warning"),
            ("REBOOT RECOV",  "reboot-recovery",     "warning"),
            ("REBOOT FB",     "reboot-fastboot",     "warning"),
            ("GETVAR ALL",    "getvar-all",          "primary"),
            ("GETVAR PROD",   "getvar-product",      "primary"),
            ("OEM INFO",      "oem-device-info",     "primary"),
            ("OEM UNLOCK",    "oem-unlock",          "danger"),
            ("OEM LOCK",      "oem-lock",            "danger"),
            ("ERASE USERDATA","erase-userdata",      "danger"),
            ("ERASE CACHE",   "erase-cache",         "warning"),
            ("FORMAT USERDATA","format-userdata",    "danger"),
            ("FLASH BOOT",    "flash-boot",          "primary"),
            ("FLASH RECOVERY","flash-recovery",      "primary"),
            ("FLASH SYSTEM",  "flash-system",        "primary"),
            ("FLASH VBMETA",  "flash-vbmeta",        "primary"),
            ("FLASH ZIP",     "flash-all",           "primary"),
            ("SLOT A",        "set-active-a",        "primary"),
            ("SLOT B",        "set-active-b",        "primary"),
            ("FLASH UNLOCK",  "flashing-unlock",     "danger"),
            ("FLASH LOCK",    "flashing-lock",       "danger"),
            ("CONTINUE",      "continue",            "success"),
        ]
        for i, (text, cmd, kind) in enumerate(fb_cmds):
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.clicked.connect(functools.partial(self._fb_cmd, cmd))
            cmds_lay.addWidget(b, i // 5, i % 5)
        lay.addWidget(cmds)

        out = QGroupBox("FASTBOOT OUTPUT")
        out_lay = QVBoxLayout(out)
        out_lay.setContentsMargins(Scale.px(12), Scale.px(20), Scale.px(12), Scale.px(12))

        self.fb_out = QTextEdit()
        self.fb_out.setReadOnly(True)
        out_lay.addWidget(self.fb_out)

        row = QHBoxLayout()
        c = QPushButton("CLEAR")
        c.setObjectName("danger")
        c.clicked.connect(self.fb_out.clear)
        row.addWidget(c)

        e = QPushButton("EXPORT")
        e.setObjectName("warning")
        e.clicked.connect(self._export_fb)
        row.addWidget(e)
        row.addStretch()
        out_lay.addLayout(row)
        lay.addWidget(out, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              NETWORK
    # ════════════════════════════════════════════════════════════════════

    def _tab_network(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        cards_scroll = QScrollArea()
        cards_scroll.setWidgetResizable(True)
        cards_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cards_scroll.setFixedHeight(Scale.px(130))
        cards_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        cards_inner = QWidget()
        cards_inner.setMinimumWidth(Scale.px(620))
        stats = QHBoxLayout(cards_inner)
        stats.setContentsMargins(0, 0, 0, 0)
        stats.setSpacing(Scale.px(10))

        self.net_ip     = StatCard("Local IP")
        self.net_wifi   = StatCard("Wi-Fi SSID")
        self.net_signal = StatCard("Signal")
        self.net_con    = StatCard("Connections")
        for s in (self.net_ip, self.net_wifi, self.net_signal, self.net_con):
            s.setMinimumWidth(Scale.px(150))
            stats.addWidget(s)
            self.stat_cards.append(s)
        cards_scroll.setWidget(cards_inner)
        lay.addWidget(cards_scroll)

        diag = QGroupBox("NETWORK DIAGNOSTICS")
        diag_lay = QGridLayout(diag)
        diag_lay.setSpacing(Scale.px(4))

        cmds = [
            ("LOCAL IP",       "primary", ["shell", "ip", "-4", "addr", "show", "wlan0"]),
            ("IP ADDRESSES",   "primary", ["shell", "ip", "addr", "show"]),
            ("ROUTING",        "primary", ["shell", "ip", "route"]),
            ("NEIGHBORS",      "primary", ["shell", "ip", "neigh"]),
            ("INTERFACES",     "primary", ["shell", "ifconfig", "-a"]),
            ("DNS",            "primary", ["shell", "getprop", "net.dns1"]),
            ("WIFI STATE",     "primary", ["shell", "dumpsys", "wifi"]),
            ("OPEN PORTS",     "warning", ["shell", "netstat", "-tuln"]),
            ("ESTABLISHED",    "warning", ["shell", "netstat", "-an"]),
            ("PING 8.8.8.8",   "success", ["shell", "ping", "-c", "3", "8.8.8.8"]),
            ("PING 1.1.1.1",   "success", ["shell", "ping", "-c", "3", "1.1.1.1"]),
            ("WIFI ON",        "success", ["shell", "svc", "wifi", "enable"]),
            ("WIFI OFF",       "danger",  ["shell", "svc", "wifi", "disable"]),
            ("DATA ON",        "success", ["shell", "svc", "data", "enable"]),
            ("DATA OFF",       "danger",  ["shell", "svc", "data", "disable"]),
            ("AIRPLANE ON",    "warning", ["shell", "settings", "put", "global",
                                            "airplane_mode_on", "1"]),
            ("AIRPLANE OFF",   "primary", ["shell", "settings", "put", "global",
                                            "airplane_mode_on", "0"]),
            ("WIFI MAC",       "primary", ["shell", "cat",
                                            "/sys/class/net/wlan0/address"]),
            ("ADB TCPIP",      "primary", "SPECIAL_TCPIP"),
            ("ADB CONNECT",    "primary", "SPECIAL_CONNECT"),
        ]
        for i, (text, kind, args) in enumerate(cmds):
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.clicked.connect(functools.partial(self._net_cmd, text, args))
            diag_lay.addWidget(b, i // 5, i % 5)
        lay.addWidget(diag)

        out = QGroupBox("OUTPUT")
        out_lay = QVBoxLayout(out)
        out_lay.setContentsMargins(Scale.px(12), Scale.px(20), Scale.px(12), Scale.px(12))
        self.net_out = QTextEdit()
        self.net_out.setReadOnly(True)
        out_lay.addWidget(self.net_out)

        row = QHBoxLayout()
        c = QPushButton("CLEAR")
        c.setObjectName("danger")
        c.clicked.connect(self.net_out.clear)
        row.addWidget(c)

        e = QPushButton("EXPORT")
        e.setObjectName("warning")
        e.clicked.connect(self._export_net)
        row.addWidget(e)
        row.addStretch()
        out_lay.addLayout(row)
        lay.addWidget(out, 1)

        return scroll

    def _net_cmd(self, label, args):
        if not self.device:
            self.net_out.append("ERR: no device connected")
            return

        if args == "SPECIAL_TCPIP":
            self.net_out.append(f"\n▸ ADB TCPIP 5555")
            ok, out, err = run(["adb", "-s", self.device, "tcpip", "5555"], timeout=10)
            if out: self.net_out.append(out)
            if err: self.net_out.append(f"[stderr] {err}")
            if not out and not err:
                self.net_out.append("TCP/IP mode may not be supported on this device")
            return

        if args == "SPECIAL_CONNECT":
            ip, ok = QInputDialog.getText(self, "ADB over Wi-Fi", "Device IP:")
            if ok and ip.strip():
                self.net_out.append(f"\n▸ adb connect {ip.strip()}:5555")
                ok2, out2, err2 = run(["adb", "connect",
                                       f"{ip.strip()}:5555"], timeout=10)
                if out2: self.net_out.append(out2)
                if err2: self.net_out.append(f"[stderr] {err2}")
            return

        self.net_out.append(f"\n{'─' * 50}")
        self.net_out.append(f"  {label}")
        self.net_out.append('─' * 50)

        def work():
            ok, out, err = run(["adb", "-s", self.device] + args, timeout=20)
            if out:
                lines = out.splitlines()
                if len(lines) > 400:
                    lines = lines[:400] + [f"... ({len(lines) - 400} more lines)"]
                self.bus.net_out.emit("\n".join(lines))
            if err:
                self.bus.net_out.emit(f"[stderr] {err}")
            if not out and not err:
                self.bus.net_out.emit("[no output]")
            self.bus.net_out.emit("")
        threading.Thread(target=work, daemon=True).start()

    def _on_net_out(self, text):
        self.net_out.append(text)

    def _export_net(self):
        name = f"network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(name, "w") as f:
            f.write(self.net_out.toPlainText())
        self._log("ok", f"exported · {name}")

    # ════════════════════════════════════════════════════════════════════
    #                              PACKAGES
    # ════════════════════════════════════════════════════════════════════

    def _tab_packages(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        bar = QGroupBox("PACKAGE MANAGER")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setSpacing(Scale.px(4))

        r = QPushButton("REFRESH")
        r.setObjectName("primary")
        r.setMinimumHeight(Scale.px(30))
        r.clicked.connect(self._load_packages)
        bar_lay.addWidget(r)

        self.pkg_filter = QComboBox()
        self.pkg_filter.addItems(["All", "System", "User"])
        self.pkg_filter.setFixedWidth(Scale.px(100))
        self.pkg_filter.currentIndexChanged.connect(self._load_packages)
        bar_lay.addWidget(self.pkg_filter)

        self.pkg_search = QLineEdit()
        self.pkg_search.setPlaceholderText("Filter...")
        self.pkg_search.textChanged.connect(self._filter_pkgs)
        bar_lay.addWidget(self.pkg_search, 1)

        bar_lay.addStretch()

        for text, cb, kind in [
            ("INFO",    self._pkg_info,      "primary"),
            ("CLEAR",   self._pkg_clear,     "warning"),
            ("STOP",    self._pkg_stop,      "warning"),
            ("DISABLE", self._pkg_disable,   "danger"),
            ("ENABLE",  self._pkg_enable,    "success"),
            ("UNINST",  self._pkg_uninstall, "danger"),
        ]:
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.clicked.connect(cb)
            bar_lay.addWidget(b)

        lay.addWidget(bar)

        self.pkg_table = QTableWidget()
        self.pkg_table.setColumnCount(4)
        self.pkg_table.setHorizontalHeaderLabels(["Package", "Type", "UID", "Path"])
        self.pkg_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.pkg_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.pkg_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pkg_table.setAlternatingRowColors(True)
        self.pkg_table.setSortingEnabled(True)
        lay.addWidget(self.pkg_table, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              FILES
    # ════════════════════════════════════════════════════════════════════

    def _tab_files(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        bar = QGroupBox("FILE BROWSER")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setSpacing(Scale.px(4))

        self.path_input = QLineEdit("/sdcard")
        self.path_input.returnPressed.connect(
            lambda: self._load_files(self.path_input.text()))
        bar_lay.addWidget(self.path_input, 1)

        for text, cb, kind in [
            ("GO",     lambda: self._load_files(self.path_input.text()), "primary"),
            ("UP",     self._file_up,     "primary"),
            ("HOME",   lambda: self._load_files("/sdcard"), "primary"),
            ("REFR",   lambda: self._load_files(self.cur_file_path), "primary"),
            ("PULL",   self._file_download, "success"),
            ("DEL",    self._file_delete,   "danger"),
            ("MKDIR",  self._file_mkdir,    "warning"),
        ]:
            b = QPushButton(text)
            b.setObjectName(kind)
            b.setMinimumHeight(Scale.px(30))
            b.clicked.connect(cb)
            bar_lay.addWidget(b)

        lay.addWidget(bar)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(
            ["Name", "Type", "Size", "Perm", "Owner"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.setAlternatingRowColors(True)
        self.file_table.doubleClicked.connect(self._file_open)
        lay.addWidget(self.file_table, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              PROCESSES
    # ════════════════════════════════════════════════════════════════════

    def _tab_processes(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        bar = QGroupBox("PROCESS CONTROL")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setSpacing(Scale.px(4))

        r = QPushButton("REFRESH")
        r.setObjectName("primary")
        r.setMinimumHeight(Scale.px(30))
        r.clicked.connect(self._load_processes)
        bar_lay.addWidget(r)

        k = QPushButton("KILL")
        k.setObjectName("danger")
        k.setMinimumHeight(Scale.px(30))
        k.clicked.connect(self._kill_proc)
        bar_lay.addWidget(k)

        kb = QPushButton("KILL BG")
        kb.setObjectName("danger")
        kb.setMinimumHeight(Scale.px(30))
        kb.clicked.connect(self._kill_bg)
        bar_lay.addWidget(kb)

        bar_lay.addStretch()

        self.proc_search = QLineEdit()
        self.proc_search.setPlaceholderText("Filter...")
        self.proc_search.setFixedWidth(Scale.px(200))
        self.proc_search.textChanged.connect(self._filter_procs)
        bar_lay.addWidget(self.proc_search)

        lay.addWidget(bar)

        self.proc_table = QTableWidget()
        self.proc_table.setColumnCount(5)
        self.proc_table.setHorizontalHeaderLabels(
            ["PID", "PPID", "USER", "STAT", "CMD"])
        self.proc_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.proc_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.proc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proc_table.setAlternatingRowColors(True)
        self.proc_table.setSortingEnabled(True)
        lay.addWidget(self.proc_table, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              LOGCAT
    # ════════════════════════════════════════════════════════════════════

    def _tab_logcat(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        bar = QGroupBox("LOGCAT")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setSpacing(Scale.px(4))

        self.btn_log_start = QPushButton("START")
        self.btn_log_start.setObjectName("success")
        self.btn_log_start.setMinimumHeight(Scale.px(30))
        self.btn_log_start.clicked.connect(self._logcat_start)
        bar_lay.addWidget(self.btn_log_start)

        self.btn_log_stop = QPushButton("STOP")
        self.btn_log_stop.setObjectName("danger")
        self.btn_log_stop.setMinimumHeight(Scale.px(30))
        self.btn_log_stop.setEnabled(False)
        self.btn_log_stop.clicked.connect(self._logcat_stop)
        bar_lay.addWidget(self.btn_log_stop)

        clr = QPushButton("CLEAR")
        clr.setObjectName("warning")
        clr.setMinimumHeight(Scale.px(30))
        clr.clicked.connect(self._logcat_clear)
        bar_lay.addWidget(clr)

        sv = QPushButton("SAVE")
        sv.setObjectName("primary")
        sv.setMinimumHeight(Scale.px(30))
        sv.clicked.connect(self._logcat_save)
        bar_lay.addWidget(sv)

        bar_lay.addWidget(QLabel("Level:"))
        self.log_level = QComboBox()
        self.log_level.addItems(["V", "D", "I", "W", "E", "F"])
        self.log_level.setCurrentIndex(2)
        self.log_level.setFixedWidth(Scale.px(55))
        bar_lay.addWidget(self.log_level)

        bar_lay.addWidget(QLabel("Grep:"))
        self.log_filter = QLineEdit()
        self.log_filter.setPlaceholderText("filter...")
        self.log_filter.setFixedWidth(Scale.px(150))
        self.log_filter.textChanged.connect(self._filter_logcat)
        bar_lay.addWidget(self.log_filter)

        bar_lay.addStretch()
        lay.addWidget(bar)

        self.logcat_view = QPlainTextEdit()
        self.logcat_view.setReadOnly(True)
        self.logcat_view.setMaximumBlockCount(5000)
        lay.addWidget(self.logcat_view, 1)

        return page

    # ════════════════════════════════════════════════════════════════════
    #                              TERMINAL
    # ════════════════════════════════════════════════════════════════════

    def _tab_terminal(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(10))

        bar = QGroupBox("QUICK COMMANDS")
        bar_lay = QHBoxLayout(bar)
        bar_lay.setSpacing(Scale.px(4))

        quick = [
            ("pm list pkgs",  ["shell", "pm", "list", "packages"]),
            ("battery",       ["shell", "dumpsys", "battery"]),
            ("getprop",       ["shell", "getprop"]),
            ("wm size",       ["shell", "wm", "size"]),
            ("df -h",         ["shell", "df", "-h"]),
            ("uptime",        ["shell", "uptime"]),
            ("top",           ["shell", "top", "-n", "1"]),
            ("ps -A",         ["shell", "ps", "-A"]),
            ("ls /sdcard",    ["shell", "ls", "/sdcard"]),
            ("cpuinfo",       ["shell", "cat", "/proc/cpuinfo"]),
        ]
        for text, args in quick:
            b = QPushButton(text)
            b.setObjectName("ghost")
            b.setMinimumHeight(Scale.px(28))
            b.clicked.connect(functools.partial(self._term_run_args, args))
            bar_lay.addWidget(b)
        bar_lay.addStretch()
        lay.addWidget(bar)

        self.term_out = QPlainTextEdit()
        self.term_out.setReadOnly(True)
        self.term_out.setStyleSheet(f"""
            QPlainTextEdit {{
                background: rgba(5,8,15,0.8);
                border: 1px solid {T.B};
                border-radius: 6px;
                color: {T.TEXT};
                padding: {Scale.px(8)}px;
            }}
        """)
        lay.addWidget(self.term_out, 1)

        inp_row = QHBoxLayout()
        inp_row.setSpacing(Scale.px(6))

        prompt = QLabel("$")
        prompt.setStyleSheet(
            f"color: {T.CYAN}; font-size: {Scale.pt(13)}pt; font-weight: 900; "
            f"font-family: {T.FONT_MONO};"
        )
        inp_row.addWidget(prompt)

        self.term_input = QLineEdit()
        self.term_input.setPlaceholderText("adb shell ls /sdcard")
        self.term_input.returnPressed.connect(self._term_exec)
        inp_row.addWidget(self.term_input, 1)

        run_btn = QPushButton("RUN")
        run_btn.setObjectName("success")
        run_btn.setFixedWidth(Scale.px(70))
        run_btn.setMinimumHeight(Scale.px(30))
        run_btn.clicked.connect(self._term_exec)
        inp_row.addWidget(run_btn)

        lay.addLayout(inp_row)
        return page

    # ════════════════════════════════════════════════════════════════════
    #                              HELP
    # ════════════════════════════════════════════════════════════════════

    def _tab_help(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(Scale.px(8))

        tabs = QTabWidget()

        ov = QTextEdit()
        ov.setReadOnly(True)
        ov.setPlainText("""DROID SURGEON  ·  OVERVIEW

Professional desktop suite for Android device management,
built on top of ADB, Fastboot, and Scrcpy.

CAPABILITIES
  · Full ADB control (keys, gestures, D-pad)
  · Live screen mirroring via Scrcpy
  · Fastboot flashing, erasing, slot switching
  · Package management
  · Device file browser
  · Process viewer & terminator
  · Real-time Logcat stream
  · Network diagnostics
  · Dashboard with battery / storage / memory / thermal

UI SCALE
  Use the "UI" button in the top-right corner to adjust
  interface size. Choose from 70% to 140%. The setting is
  saved and restored on next launch.

  Keyboard:
    Ctrl+Plus   → increase scale
    Ctrl+Minus  → decrease scale
    Ctrl+0      → reset to 100%

LICENSE
  GNU General Public License v3.0
""")
        tabs.addTab(ov, "Overview")

        qs = QTextEdit()
        qs.setReadOnly(True)
        qs.setPlainText("""QUICK START

1. INSTALL PREREQUISITES
   Debian / Ubuntu / Kali:
     sudo apt install android-tools-adb android-tools-fastboot \\
                      scrcpy python3-pyqt5

   Arch:
     sudo pacman -S android-tools scrcpy python-pyqt5

2. ENABLE USB DEBUGGING
   · Settings → About phone → tap Build number 7x
   · Settings → Developer options → USB debugging ON

3. CONNECT
   · Plug USB cable
   · Accept RSA fingerprint on device
   · Refresh in CTRL tab

4. MIRROR
   · MIRROR tab → configure → START

5. FASTBOOT
   · adb reboot bootloader
   · BOOT tab → REFRESH → operations

TROUBLESHOOTING
  · "no devices"       → adb kill-server && adb start-server
  · "unauthorized"     → accept RSA prompt on phone
  · scrcpy missing     → install scrcpy package
  · fastboot missing   → install android-tools-fastboot
""")
        tabs.addTab(qs, "Quick Start")

        sc = QTextEdit()
        sc.setReadOnly(True)
        sc.setPlainText("""KEYBOARD SHORTCUTS

  1  →  Dashboard
  2  →  Control
  3  →  Mirror
  4  →  Fastboot
  5  →  Network
  6  →  Packages
  7  →  Files
  8  →  Processes
  9  →  Logcat
  0  →  Terminal

  F5           →  Refresh ADB + Fastboot
  F11          →  Toggle fullscreen
  Ctrl+Plus    →  Increase UI scale
  Ctrl+Minus   →  Decrease UI scale
  Ctrl+0       →  Reset UI scale
  Ctrl+Q       →  Quit
""")
        tabs.addTab(sc, "Shortcuts")

        adb = QTextEdit()
        adb.setReadOnly(True)
        adb.setPlainText("""ADB CHEATSHEET

DEVICE
  adb devices
  adb kill-server && adb start-server

APPS
  adb install -r app.apk
  adb uninstall com.example
  adb shell pm list packages
  adb shell pm list packages -3
  adb shell pm clear com.example
  adb shell am force-stop com.example

FILES
  adb pull /sdcard/file.txt
  adb push local.txt /sdcard/
  adb shell ls -la /sdcard

CAPTURE
  adb exec-out screencap -p > screen.png
  adb shell screenrecord /sdcard/rec.mp4

POWER
  adb reboot
  adb reboot recovery
  adb reboot bootloader

SHELL
  adb shell input tap X Y
  adb shell input swipe X1 Y1 X2 Y2 [dur]
  adb shell input text "hello"
  adb shell dumpsys battery

FASTBOOT
  fastboot devices
  fastboot flash boot boot.img
  fastboot flash recovery recovery.img
  fastboot erase userdata
  fastboot oem unlock
  fastboot reboot
""")
        tabs.addTab(adb, "ADB Cheatsheet")

        lic = QTextEdit()
        lic.setReadOnly(True)
        lic.setPlainText("""                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are
designed to take away your freedom to share and change the works.
By contrast, the GNU General Public License is intended to guarantee
your freedom to share and change all versions of a program--to make
sure it remains free software for all its users.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that
you have the freedom to distribute copies of free software (and
charge for them if you wish), that you receive source code or can
get it if you want it, that you can change the software or use
pieces of it in new free programs, and that you know you can do
these things.

  To protect your rights, we need to prevent others from denying
you these rights or asking you to surrender the rights.  Therefore,
you have certain responsibilities if you distribute copies of the
software, or if you modify it: responsibilities to respect the
freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too,
receive or can get the source code.  And you must show them these
terms so they know their rights.

  Developers that use the GNU GPL protect your rights with two
steps: (1) assert copyright on the software, and (2) offer you
this License giving you legal permission to copy, distribute
and/or modify it.

  For the developers' and authors' protection, the GPL clearly
explains that there is no warranty for this free software.  For
both users' and authors' sake, the GPL requires that modified
versions be marked as changed, so that their problems will not be
attributed erroneously to authors of previous versions.

  Finally, every program is threatened constantly by software
patents.  States should not allow patents to restrict development
and use of software on general-purpose computers, but in those
that do, we wish to avoid the special danger that patents applied
to a free program could make it effectively proprietary.  To
prevent this, the GPL assures that patents cannot be used to
render the program non-free.

────────────────────────────────────────────────────────────────

  This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

  You should have received a copy of the GNU General Public
License along with this program.  If not, see
<https://www.gnu.org/licenses/>.

────────────────────────────────────────────────────────────────

  Full text: https://www.gnu.org/licenses/gpl-3.0.txt
  SPDX identifier: GPL-3.0-or-later
""")
        tabs.addTab(lic, "License (GPLv3)")

        ab = QTextEdit()
        ab.setReadOnly(True)
        ab.setPlainText(f"""DROID SURGEON  ·  v1.1.1

Advanced Android Device Management Suite
Built with Python and PyQt5.

STACK
  · Python {platform.python_version()}
  · Qt {__import__('PyQt5.QtCore', fromlist=['QT_VERSION_STR']).QT_VERSION_STR}
  · Platform: {platform.system()} {platform.release()}
  · {platform.machine()}

LICENSE
  GNU General Public License v3.0
  SPDX: GPL-3.0-or-later

CREDITS
  ADB       · Android Debug Bridge
  Fastboot  · Android Fastboot protocol
  Scrcpy    · Genymobile screen mirroring
  PyQt5     · Riverbank Computing

© 2026 Engineering Division
""")
        tabs.addTab(ab, "About")

        lay.addWidget(tabs)
        return page

    # ════════════════════════════════════════════════════════════════════
    #                              TOOLS
    # ════════════════════════════════════════════════════════════════════

    def _detect_tools(self):
        if which("adb"):
            ok, out, _ = run(["adb", "version"])
            v = out.split("\n")[0].split()[-1] if ok and out else "?"
            self._log("ok", f"adb · v{v}")
        else:
            self._log("err", "adb NOT installed")
            QMessageBox.critical(self, "Missing Tool",
                "ADB is not installed.\n\n"
                "sudo apt install android-tools-adb")

        if which("fastboot"):
            self._log("ok", "fastboot detected")
        else:
            self._log("warn", "fastboot NOT installed")

        if which("scrcpy"):
            ok, out, err = run(["scrcpy", "--version"])
            txt = (out or "") + "\n" + (err or "")
            m = re.search(r"scrcpy\s+([\d.]+)", txt)
            self.scrcpy_version = m.group(1) if m else "?"
            self._log("ok", f"scrcpy · v{self.scrcpy_version}")
        else:
            self._log("warn", "scrcpy NOT installed")

    def _refresh_adb(self):
        self.dev_combo.clear()
        ok, out, _ = run(["adb", "devices"])
        devs = []
        if ok:
            for line in out.splitlines()[1:]:
                p = line.split()
                if len(p) >= 2 and p[1] == "device":
                    devs.append(p[0])

        if devs:
            for d in devs:
                self.dev_combo.addItem(d)
            self.device = devs[0]
            self._set_pill(self.pill_adb, f"ADB · {len(devs)}", "ok")
            self.dev_state.setText(f"{len(devs)} DEVICE(S)")
            self.dev_state.setStyleSheet(self._state_label_style("ok"))
            self.status_dev.setText(f"DEV : {self.device}")
            self._log("ok", f"device · {self.device}")
            self._fetch_stats()
        else:
            self.dev_combo.addItem("[no device]")
            self.device = None
            self._set_pill(self.pill_adb, "ADB", "off")
            self.dev_state.setText("DISCONNECTED")
            self.dev_state.setStyleSheet(self._state_label_style("err"))
            self.status_dev.setText("DEV : —")
            self._log("warn", "no adb devices")

    def _adb(self, args, timeout=15):
        if not self.device: return ""
        ok, out, _ = run(["adb", "-s", self.device] + args, timeout=timeout)
        return out

    def _refresh_fb(self):
        self.fb_combo.clear()
        ok, out, _ = run(["fastboot", "devices"])
        devs = [l.split()[0] for l in out.splitlines() if l.strip()] if ok else []

        if devs:
            for d in devs:
                self.fb_combo.addItem(d)
            self.fb_device = devs[0]
            self._set_pill(self.pill_fb, f"FASTBOOT · {len(devs)}", "ok")
            self.fb_state.setText(f"{len(devs)} DEVICE(S)")
            self.fb_state.setStyleSheet(self._state_label_style("ok"))
            self._log("ok", f"fastboot · {self.fb_device}")
        else:
            self.fb_combo.addItem("[no device]")
            self.fb_device = None
            self._set_pill(self.pill_fb, "FASTBOOT", "off")
            self.fb_state.setText("DISCONNECTED")
            self.fb_state.setStyleSheet(self._state_label_style("err"))

    def _on_dev_sel(self, idx):
        if idx < 0: return
        txt = self.dev_combo.currentText()
        if "[no device]" not in txt:
            self.device = txt
            self.status_dev.setText(f"DEV : {self.device}")
            self._fetch_stats()

    # ════════════════════════════════════════════════════════════════════
    #                              STATS
    # ════════════════════════════════════════════════════════════════════

    def _fetch_stats(self):
        if not self.device: return
        if self._stats_lock.locked(): return
        threading.Thread(target=self._stats_worker, daemon=True).start()

    def _stats_worker(self):
        if not self._stats_lock.acquire(blocking=False): return
        try:
            d = {}
            batt = self._adb(["shell", "dumpsys", "battery"])
            level = 0; status = "N/A"; temp = 0; volt = 0; health = "N/A"
            for ln in batt.splitlines():
                ln = ln.strip()
                if ln.startswith("level:"):
                    try: level = int(ln.split(":")[1])
                    except: pass
                if ln.startswith("status:"):
                    code = ln.split(":")[1].strip()
                    status = {"1":"UNKNOWN","2":"CHARGING","3":"DISCHARGING",
                              "4":"NOT CHARGING","5":"FULL"}.get(code, "N/A")
                if ln.startswith("temperature:"):
                    try: temp = int(ln.split(":")[1]) / 10
                    except: pass
                if ln.startswith("voltage:"):
                    try: volt = int(ln.split(":")[1]) / 1000
                    except: pass
                if ln.startswith("health:"):
                    code = ln.split(":")[1].strip()
                    health = {"1":"UNKNOWN","2":"GOOD","3":"OVERHEAT","4":"DEAD",
                              "5":"OVERVOLT","6":"FAILURE","7":"COLD"}.get(code,"N/A")
            d["battery"] = level
            d["battery_status"] = status
            d["battery_temp"] = temp
            d["battery_voltage"] = volt
            d["battery_health"] = health

            df = self._adb(["shell", "df", "/data"])
            stor_pct = 0; stor_used = 0; stor_total = 0
            for ln in df.splitlines():
                if "/data" in ln:
                    p = ln.split()
                    if len(p) >= 4:
                        try:
                            stor_total = int(p[1]); stor_used = int(p[2])
                            stor_pct = int((stor_used / stor_total) * 100) if stor_total else 0
                        except: pass
            d["storage_pct"] = stor_pct
            d["storage_used"] = stor_used * 1024
            d["storage_total"] = stor_total * 1024

            mem = self._adb(["shell", "cat", "/proc/meminfo"])
            tot = 0; avail = 0
            for ln in mem.splitlines():
                if ln.startswith("MemTotal:"):
                    try: tot = int(ln.split()[1])
                    except: pass
                elif ln.startswith("MemAvailable:"):
                    try: avail = int(ln.split()[1])
                    except: pass
            used = tot - avail
            d["mem_pct"] = int((used / tot) * 100) if tot else 0
            d["mem_used"] = used * 1024
            d["mem_total"] = tot * 1024

            up = self._adb(["shell", "cat", "/proc/uptime"])
            up_sec = 0
            try: up_sec = int(float(up.split()[0]))
            except: pass
            d["uptime"] = up_sec

            info = {
                "model":        self._adb(["shell", "getprop", "ro.product.model"]),
                "brand":        self._adb(["shell", "getprop", "ro.product.brand"]),
                "device":       self._adb(["shell", "getprop", "ro.product.device"]),
                "android":      self._adb(["shell", "getprop", "ro.build.version.release"]),
                "sdk":          self._adb(["shell", "getprop", "ro.build.version.sdk"]),
                "build":        self._adb(["shell", "getprop", "ro.build.id"]),
                "cpu_abi":      self._adb(["shell", "getprop", "ro.product.cpu.abi"]),
                "kernel":       self._adb(["shell", "uname", "-r"]),
                "serial":       self.device,
                "bootloader":   self._adb(["shell", "getprop", "ro.bootloader"]),
                "hardware":     self._adb(["shell", "getprop", "ro.hardware"]),
                "manufacturer": self._adb(["shell", "getprop", "ro.product.manufacturer"]),
            }
            d["info"] = info
            self.bus.stats.emit(d)
        except Exception as e:
            self._log("err", f"stats error · {str(e)[:120]}")
        finally:
            self._stats_lock.release()

    def _on_stats(self, d):
        b = d.get("battery", 0)
        bc = T.GREEN if b > 30 else (T.AMBER if b > 15 else T.RED)
        self.c_battery.set(f"{b}%", d.get("battery_status", "—"),
                           f"{d.get('battery_voltage', 0):.2f}V", bc, b)

        s = d.get("storage_pct", 0)
        sc = T.GREEN if s < 70 else (T.AMBER if s < 90 else T.RED)
        self.c_storage.set(f"{s}%",
            f"{human_bytes(d.get('storage_used', 0))} / {human_bytes(d.get('storage_total', 0))}",
            "USED", sc, s)

        m = d.get("mem_pct", 0)
        mc = T.GREEN if m < 60 else (T.AMBER if m < 85 else T.RED)
        self.c_memory.set(f"{m}%",
            f"{human_bytes(d.get('mem_used', 0))} / {human_bytes(d.get('mem_total', 0))}",
            "USED", mc, m)

        th = d.get("battery_temp", 0)
        tc = T.GREEN if th < 40 else (T.AMBER if th < 48 else T.RED)
        self.c_thermal.set(f"{th:.1f}°C", d.get("battery_health", "—"), "BATTERY",
                           tc, min(int(th * 2), 100))

        self.c_uptime.set(human_time(d.get("uptime", 0)),
                          "SINCE LAST BOOT", "", T.CYAN)

        info = d.get("info", {})
        lines = [
            f"  MODEL            :  {info.get('model','—')}",
            f"  MANUFACTURER     :  {info.get('manufacturer','—')}",
            f"  BRAND            :  {info.get('brand','—')}",
            f"  CODENAME         :  {info.get('device','—')}",
            f"  ANDROID          :  {info.get('android','—')}   (API {info.get('sdk','—')})",
            f"  BUILD ID         :  {info.get('build','—')}",
            f"  CPU ABI          :  {info.get('cpu_abi','—')}",
            f"  HARDWARE         :  {info.get('hardware','—')}",
            f"  BOOTLOADER       :  {info.get('bootloader','—')}",
            f"  KERNEL           :  {info.get('kernel','—')}",
            f"  SERIAL           :  {info.get('serial','—')}",
        ]
        self.overview.setText("\n".join(lines))

    # ════════════════════════════════════════════════════════════════════
    #                              CONTROL
    # ════════════════════════════════════════════════════════════════════

    def _send_key(self, code):
        if not self.device: return
        self._adb(["shell", "input", "keyevent", code])
        self._log("info", f"key · {code}")

    def _reboot(self, mode):
        if not self.device: return
        label = (mode or "system").upper()
        r = QMessageBox.question(self, "Reboot",
            f"Reboot to {label}?", QMessageBox.Yes | QMessageBox.No)
        if r != QMessageBox.Yes: return
        self._adb(["reboot"] + ([mode] if mode else []))
        self._log("warn", f"reboot → {label}")

    def _factory_reset(self):
        if not self.device: return
        r = QMessageBox.warning(self, "FACTORY RESET",
            "Erase ALL DATA?\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            self._adb(["shell", "recovery", "--wipe_data"])
            self._log("danger", "factory reset")

    def _apply_volume(self):
        if not self.device: return
        lvl = self.vol_slider.value()
        for _ in range(15):
            self._adb(["shell", "input", "keyevent", "KEYCODE_VOLUME_DOWN"])
        for _ in range(lvl):
            self._adb(["shell", "input", "keyevent", "KEYCODE_VOLUME_UP"])
        self._log("info", f"volume → {lvl}")

    def _screenshot(self):
        if not self.device: return
        name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(name, "wb") as f:
            r = subprocess.run(
                ["adb", "-s", self.device, "exec-out", "screencap", "-p"],
                stdout=f, stderr=subprocess.PIPE, timeout=20)
        if r.returncode == 0:
            self._log("ok", f"screenshot · {name}")
        else:
            self._log("err", "screenshot failed")

    def _start_record(self):
        if not self.device: return
        name = f"record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        self._log("warn", f"recording · {name}")
        def rec():
            self._adb(["shell", "screenrecord", "--size", "1280x720",
                       "--bit-rate", "6000000", f"/sdcard/{name}"], timeout=300)
        threading.Thread(target=rec, daemon=True).start()

    def _stop_record(self):
        if not self.device: return
        self._adb(["shell", "pkill", "-INT", "screenrecord"])
        self._log("info", "recording stopped")

    def _dlg_tap(self):
        r = self._multi("TAP", ["X", "Y"], ["500", "500"])
        if r:
            self._adb(["shell", "input", "tap", str(r[0]), str(r[1])])
            self._log("info", f"tap ({r[0]}, {r[1]})")

    def _dlg_swipe(self):
        r = self._multi("SWIPE", ["X1","Y1","X2","Y2","Dur"],
                        ["200","800","200","200","300"])
        if r:
            self._adb(["shell", "input", "swipe", *map(str, r)])
            self._log("info", "swipe")

    def _dlg_long(self):
        r = self._multi("LONG PRESS", ["X","Y","Dur"], ["500","500","1200"])
        if r:
            self._adb(["shell", "input", "swipe",
                       str(r[0]), str(r[1]), str(r[0]), str(r[1]), str(r[2])])
            self._log("info", "long press")

    def _dlg_pinch(self):
        r = self._multi("PINCH", ["CX","CY","Off"], ["540","960","300"])
        if r:
            cx, cy, off = r
            self._adb(["shell", "input", "swipe",
                       str(cx-off), str(cy), str(cx+off), str(cy), "250"])
            self._log("info", "pinch")

    def _scroll_dn(self):
        self._adb(["shell", "input", "swipe", "540", "1600", "540", "600", "300"])
        self._log("info", "scroll down")

    def _scroll_up(self):
        self._adb(["shell", "input", "swipe", "540", "600", "540", "1600", "300"])
        self._log("info", "scroll up")

    def _multi(self, title, labels, defaults):
        dlg = QDialog(self)
        dlg.setStyleSheet(build_stylesheet())
        dlg.setWindowTitle(title)
        dlg.setMinimumWidth(Scale.px(300))
        v = QVBoxLayout(dlg)
        v.setContentsMargins(Scale.px(16), Scale.px(16), Scale.px(16), Scale.px(16))
        v.setSpacing(Scale.px(8))

        inputs = []
        for lab, dflt in zip(labels, defaults):
            row = QHBoxLayout()
            l = QLabel(lab + ":")
            l.setFixedWidth(Scale.px(70))
            l.setStyleSheet(f"color: {T.TEXT_DIM}; font-weight: 600;")
            row.addWidget(l)
            inp = QLineEdit(dflt)
            row.addWidget(inp)
            v.addLayout(row)
            inputs.append(inp)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        v.addWidget(btns)

        if dlg.exec_() == QDialog.Accepted:
            try:
                return [float(i.text()) if "." in i.text() else int(i.text())
                        for i in inputs]
            except: return None
        return None

    # ════════════════════════════════════════════════════════════════════
    #                              SCRCPY
    # ════════════════════════════════════════════════════════════════════

    def _scrcpy_supports(self, flag):
        if not which("scrcpy"): return False
        if self._scrcpy_help_cache is None:
            ok, out, err = run(["scrcpy", "--help"], timeout=5)
            self._scrcpy_help_cache = (out or "") + (err or "")
        return flag in self._scrcpy_help_cache

    def _start_scrcpy(self):
        if not self.device:
            self._log("err", "no device")
            return
        if self.scrcpy_running: return
        if not which("scrcpy"):
            self._log("err", "scrcpy not installed")
            return

        bitrate = self.opt_bitrate.currentText().split()[0]
        size    = self.opt_size.currentText()
        fps     = self.opt_fps.currentText()
        rot     = self.opt_rot.currentText()

        cmd = [
            "scrcpy", "-s", self.device,
            "--max-size", size,
            "--max-fps", fps,
            "--video-bit-rate", f"{bitrate}M",
            "--window-title", f"DROID SURGEON · {self.device}",
        ]

        if rot != "0":
            if self._scrcpy_supports("--display-orientation"):
                cmd += ["--display-orientation", rot]
            elif self._scrcpy_supports("--rotation"):
                cmd += ["--rotation", rot]

        if self.opt_noaudio.isChecked() and self._scrcpy_supports("--no-audio"):
            cmd.append("--no-audio")
        if self.opt_fullscreen.isChecked() and self._scrcpy_supports("--fullscreen"):
            cmd.append("--fullscreen")
        if self.opt_always_top.isChecked() and self._scrcpy_supports("--always-on-top"):
            cmd.append("--always-on-top")
        if self.opt_turnoff.isChecked() and self._scrcpy_supports("--turn-screen-off"):
            cmd.append("--turn-screen-off")

        try:
            self.scrcpy = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, stdin=subprocess.DEVNULL)
            self.scrcpy_running = True
            self.btn_start_mirror.setEnabled(False)
            self.btn_stop_mirror.setEnabled(True)
            self._set_pill(self.pill_sc, "MIRROR · LIVE", "live")

            self.mirror_status.setText(
                f"STREAMING\n\n"
                f"  Device  :  {self.device}\n"
                f"  Bitrate :  {bitrate} Mbps\n"
                f"  FPS     :  {fps}\n"
                f"  Size    :  {size}px\n"
                f"  Orient  :  {rot}°"
            )
            self.mirror_status.setStyleSheet(f"""
                QLabel {{
                    background: rgba(10,40,25,0.35);
                    border: 1px solid {T.GREEN_DIM};
                    border-radius: 6px;
                    color: {T.GREEN};
                    font-family: {T.FONT_MONO};
                    font-size: {Scale.pt(9)}pt;
                    padding: {Scale.px(16)}px;
                }}
            """)
            self._log("ok", "scrcpy started")
            threading.Thread(target=self._monitor_scrcpy, daemon=True).start()
        except Exception as e:
            self._log("err", f"scrcpy failed · {str(e)[:120]}")

    def _monitor_scrcpy(self):
        while self.scrcpy and self.scrcpy.poll() is None:
            try:
                ln = self.scrcpy.stdout.readline()
                if ln: self.bus.scrcpy_out.emit(ln.rstrip())
            except: break
            time.sleep(0.05)
        self.bus.scrcpy_state.emit("stopped")

    def _stop_scrcpy(self):
        if self.scrcpy:
            try:
                self.scrcpy.terminate()
                self.scrcpy.wait(timeout=3)
            except:
                self.scrcpy.kill()
            self.scrcpy = None
            self._on_scrcpy_state("stopped")

    def _on_scrcpy_state(self, state):
        self.scrcpy_running = False
        self.btn_start_mirror.setEnabled(True)
        self.btn_stop_mirror.setEnabled(False)
        self._set_pill(self.pill_sc, "MIRROR", "off")
        self.mirror_status.setText("MIRROR OFFLINE\n\nNo active session.")
        self.mirror_status.setStyleSheet(f"""
            QLabel {{
                background: rgba(5,8,15,0.6);
                border: 1px dashed {T.B};
                border-radius: 6px;
                color: {T.TEXT_DIM};
                font-family: {T.FONT_MONO};
                font-size: {Scale.pt(9)}pt;
                padding: {Scale.px(16)}px;
            }}
        """)
        self._log("warn", "scrcpy stopped")

    def _on_scrcpy_log(self, line):
        self.mirror_log.append(line)

    def _mirror_fs(self):
        if self.scrcpy_running:
            run(["xdotool", "search", "--name",
                 f"DROID SURGEON · {self.device}",
                 "windowactivate", "key", "Alt+f"], timeout=3)

    def _mirror_rotate(self):
        if self.scrcpy_running:
            run(["xdotool", "search", "--name",
                 f"DROID SURGEON · {self.device}",
                 "windowactivate", "key", "r"], timeout=3)

    # ════════════════════════════════════════════════════════════════════
    #                              FASTBOOT
    # ════════════════════════════════════════════════════════════════════

    def _fb_cmd(self, cmd):
        if not self.fb_device:
            self._log("err", "no fastboot device")
            return

        if cmd == "getvar-all": args = ["getvar", "all"]
        elif cmd == "getvar-product": args = ["getvar", "product"]
        elif cmd == "oem-device-info": args = ["oem", "device-info"]
        elif cmd == "oem-unlock":
            if QMessageBox.warning(self, "UNLOCK",
                "ERASE ALL DATA?\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
            args = ["oem", "unlock"]
        elif cmd == "oem-lock":
            if QMessageBox.warning(self, "LOCK",
                "May ERASE ALL DATA.\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
            args = ["oem", "lock"]
        elif cmd == "erase-userdata":
            if QMessageBox.warning(self, "ERASE USERDATA",
                "ERASE ALL DATA?\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
            args = ["erase", "userdata"]
        elif cmd == "erase-cache": args = ["erase", "cache"]
        elif cmd == "format-userdata":
            if QMessageBox.warning(self, "FORMAT USERDATA",
                "ERASE ALL DATA?\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
            args = ["format", "userdata"]
        elif cmd in ("flash-boot", "flash-recovery", "flash-system", "flash-vbmeta"):
            p, _ = QFileDialog.getOpenFileName(self, "image",
                os.path.expanduser("~"), "Images (*.img);;All (*)")
            if not p: return
            part = cmd.split("-")[1]
            if part == "vbmeta":
                args = ["flash", "vbmeta",
                        "--disable-verity", "--disable-verification", p]
            else:
                args = ["flash", part, p]
        elif cmd == "flash-all":
            p, _ = QFileDialog.getOpenFileName(self, "ZIP",
                os.path.expanduser("~"), "Zip (*.zip);;All (*)")
            if not p: return
            args = ["update", p]
        elif cmd == "set-active-a": args = ["--set-active=a"]
        elif cmd == "set-active-b": args = ["--set-active=b"]
        elif cmd == "flashing-unlock": args = ["flashing", "unlock"]
        elif cmd == "flashing-lock": args = ["flashing", "lock"]
        elif cmd == "continue": args = ["continue"]
        else: args = cmd.split()

        self.bus.fb_out.emit(f"\n> fastboot {' '.join(args)}")
        threading.Thread(target=self._fb_run, args=(args,), daemon=True).start()

    def _fb_run(self, args):
        ok, out, err = run(["fastboot", "-s", self.fb_device] + args, timeout=90)
        if out:
            for ln in out.splitlines():
                self.bus.fb_out.emit(f"  {ln}")
        if err:
            for ln in err.splitlines():
                self.bus.fb_out.emit(f"  [!] {ln}")

    def _on_fb_log(self, line):
        self.fb_out.append(line)

    def _export_fb(self):
        name = f"fastboot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(name, "w") as f:
            f.write(self.fb_out.toPlainText())
        self._log("ok", f"exported · {name}")

    # ════════════════════════════════════════════════════════════════════
    #                              PACKAGES
    # ════════════════════════════════════════════════════════════════════

    def _load_packages(self):
        if not self.device: return
        mode = self.pkg_filter.currentText()
        flag = {"All": None, "System": "-s", "User": "-3"}[mode]

        def work():
            args = ["shell", "pm", "list", "packages", "-f"]
            if flag: args.insert(3, flag)
            out = self._adb(args, timeout=25)
            pkgs = []
            for ln in out.splitlines():
                m = re.match(r"package:(.+)=(.+)", ln)
                if m:
                    path, name = m.group(1), m.group(2)
                    is_sys = "/system" in path or "/product" in path
                    pkgs.append({
                        "name": name, "path": path,
                        "type": "SYS" if is_sys else "USR",
                        "uid": "—"
                    })
            self.bus.packages.emit(pkgs)
        threading.Thread(target=work, daemon=True).start()

    def _on_packages(self, pkgs):
        self.pkg_table.setSortingEnabled(False)
        self.pkg_table.setRowCount(len(pkgs))
        for i, p in enumerate(pkgs):
            self.pkg_table.setItem(i, 0, QTableWidgetItem(p["name"]))
            self.pkg_table.setItem(i, 1, QTableWidgetItem(p["type"]))
            self.pkg_table.setItem(i, 2, QTableWidgetItem(p["uid"]))
            self.pkg_table.setItem(i, 3, QTableWidgetItem(p["path"]))
        self.pkg_table.setSortingEnabled(True)
        self._log("info", f"{len(pkgs)} packages")

    def _filter_pkgs(self, text):
        text = text.lower()
        for i in range(self.pkg_table.rowCount()):
            hide = False
            if text:
                row = " ".join(
                    (self.pkg_table.item(i, j).text()
                     if self.pkg_table.item(i, j) else "")
                    for j in range(self.pkg_table.columnCount())
                ).lower()
                hide = text not in row
            self.pkg_table.setRowHidden(i, hide)

    def _pkg_sel(self):
        r = self.pkg_table.currentRow()
        if r < 0: return None
        itm = self.pkg_table.item(r, 0)
        return itm.text() if itm else None

    def _pkg_info(self):
        pkg = self._pkg_sel()
        if not pkg: return
        out = self._adb(["shell", "dumpsys", "package", pkg], timeout=15)
        dlg = QDialog(self)
        dlg.setStyleSheet(build_stylesheet())
        dlg.setWindowTitle(f"Package — {pkg}")
        dlg.resize(Scale.px(700), Scale.px(500))
        v = QVBoxLayout(dlg)
        v.setContentsMargins(Scale.px(12), Scale.px(12), Scale.px(12), Scale.px(12))
        te = QTextEdit()
        te.setReadOnly(True)
        te.setPlainText(out[:50000])
        v.addWidget(te)
        btns = QDialogButtonBox(QDialogButtonBox.Close)
        btns.rejected.connect(dlg.reject)
        btns.accepted.connect(dlg.accept)
        v.addWidget(btns)
        dlg.exec_()

    def _pkg_clear(self):
        pkg = self._pkg_sel()
        if not pkg: return
        if QMessageBox.question(self, "Clear Data",
            f"Clear data for {pkg}?",
            QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        self._adb(["shell", "pm", "clear", pkg])
        self._log("warn", f"cleared · {pkg}")

    def _pkg_stop(self):
        pkg = self._pkg_sel()
        if not pkg: return
        self._adb(["shell", "am", "force-stop", pkg])
        self._log("warn", f"stopped · {pkg}")

    def _pkg_disable(self):
        pkg = self._pkg_sel()
        if not pkg: return
        if QMessageBox.question(self, "Disable",
            f"Disable {pkg}?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        self._adb(["shell", "pm", "disable-user", "--user", "0", pkg])
        self._log("warn", f"disabled · {pkg}")

    def _pkg_enable(self):
        pkg = self._pkg_sel()
        if not pkg: return
        self._adb(["shell", "pm", "enable", pkg])
        self._log("ok", f"enabled · {pkg}")

    def _pkg_uninstall(self):
        pkg = self._pkg_sel()
        if not pkg: return
        if QMessageBox.warning(self, "Uninstall",
            f"Uninstall {pkg}?\n\nCannot be undone.",
            QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        out = self._adb(["uninstall", pkg], timeout=25)
        self._log("ok" if "Success" in out else "warn", f"uninstall · {pkg}")

    # ════════════════════════════════════════════════════════════════════
    #                              FILES
    # ════════════════════════════════════════════════════════════════════

    def _load_files(self, path):
        if not self.device: return
        self.cur_file_path = path
        self.path_input.setText(path)

        def work():
            out = self._adb(["shell", "ls", "-la", path], timeout=15)
            entries = []
            for ln in out.splitlines():
                if ln.startswith("total") or not ln.strip(): continue
                parts = ln.split(maxsplit=7)
                if len(parts) < 8: continue
                perm = parts[0]; size = parts[4]
                owner = parts[2]; name = parts[7]
                if name in (".", ".."): continue
                is_dir = perm.startswith("d")
                is_link = perm.startswith("l")
                typ = "DIR" if is_dir else ("LINK" if is_link else "FILE")
                entries.append({
                    "name": name, "type": typ, "size": size,
                    "perm": perm, "owner": owner,
                })
            self.bus.files.emit(path, entries)
        threading.Thread(target=work, daemon=True).start()

    def _on_files(self, path, entries):
        self.file_table.setRowCount(len(entries))
        for i, e in enumerate(entries):
            self.file_table.setItem(i, 0, QTableWidgetItem(e["name"]))
            self.file_table.setItem(i, 1, QTableWidgetItem(e["type"]))
            self.file_table.setItem(i, 2, QTableWidgetItem(
                human_bytes(e["size"]) if e["size"].isdigit() else e["size"]))
            self.file_table.setItem(i, 3, QTableWidgetItem(e["perm"]))
            self.file_table.setItem(i, 4, QTableWidgetItem(e["owner"]))
        self._log("info", f"browsed · {path}  ({len(entries)})")

    def _file_open(self):
        r = self.file_table.currentRow()
        if r < 0: return
        name = self.file_table.item(r, 0).text()
        typ = self.file_table.item(r, 1).text()
        if typ == "DIR":
            new_path = os.path.join(self.cur_file_path, name).replace("//", "/")
            self._load_files(new_path)

    def _file_up(self):
        parent = os.path.dirname(self.cur_file_path.rstrip("/")) or "/"
        self._load_files(parent)

    def _file_download(self):
        r = self.file_table.currentRow()
        if r < 0: return
        name = self.file_table.item(r, 0).text()
        remote = os.path.join(self.cur_file_path, name)
        local, _ = QFileDialog.getSaveFileName(self, "Save As", name)
        if not local: return
        def work():
            ok, out, err = run(
                ["adb", "-s", self.device, "pull", remote, local], timeout=120)
            self._log("ok" if ok else "err", f"pull {name} → {local}")
        threading.Thread(target=work, daemon=True).start()

    def _file_delete(self):
        r = self.file_table.currentRow()
        if r < 0: return
        name = self.file_table.item(r, 0).text()
        remote = os.path.join(self.cur_file_path, name)
        if QMessageBox.question(self, "Delete",
            f"Delete {remote}?",
            QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        self._adb(["shell", "rm", "-rf", remote])
        self._log("warn", f"deleted · {remote}")
        self._load_files(self.cur_file_path)

    def _file_mkdir(self):
        name, ok = QInputDialog.getText(self, "New Directory", "Name:")
        if not (ok and name): return
        remote = os.path.join(self.cur_file_path, name)
        self._adb(["shell", "mkdir", "-p", remote])
        self._log("ok", f"mkdir · {remote}")
        self._load_files(self.cur_file_path)

    # ════════════════════════════════════════════════════════════════════
    #                              PROCESSES
    # ════════════════════════════════════════════════════════════════════

    def _load_processes(self):
        if not self.device: return
        def work():
            out = self._adb(["shell", "ps", "-A", "-o",
                             "PID,PPID,USER,STAT,NAME"], timeout=20)
            rows = []
            for ln in out.splitlines()[1:]:
                p = ln.split(maxsplit=4)
                if len(p) < 5: continue
                rows.append([p[0], p[1], p[2], p[3], p[4]])
            self.bus.processes.emit(rows)
        threading.Thread(target=work, daemon=True).start()

    def _on_processes(self, rows):
        self.proc_table.setSortingEnabled(False)
        self.proc_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                self.proc_table.setItem(i, j, QTableWidgetItem(str(v)))
        self.proc_table.setSortingEnabled(True)
        self._log("info", f"{len(rows)} processes")

    def _filter_procs(self, text):
        text = text.lower()
        for i in range(self.proc_table.rowCount()):
            hide = False
            if text:
                row = " ".join(
                    (self.proc_table.item(i, j).text()
                     if self.proc_table.item(i, j) else "")
                    for j in range(self.proc_table.columnCount())
                ).lower()
                hide = text not in row
            self.proc_table.setRowHidden(i, hide)

    def _kill_proc(self):
        r = self.proc_table.currentRow()
        if r < 0: return
        pid = self.proc_table.item(r, 0).text()
        name = self.proc_table.item(r, 4).text()
        if QMessageBox.question(self, "Kill",
            f"Kill PID {pid} ({name})?",
            QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        self._adb(["shell", "kill", "-9", pid])
        self._log("warn", f"killed · {name} ({pid})")
        self._load_processes()

    def _kill_bg(self):
        if QMessageBox.warning(self, "Kill Background",
            "Kill ALL background apps?",
            QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes: return
        self._adb(["shell", "am", "kill-all"])
        self._log("warn", "background apps killed")
        self._load_processes()

    # ════════════════════════════════════════════════════════════════════
    #                              LOGCAT
    # ════════════════════════════════════════════════════════════════════

    def _logcat_start(self):
        if not self.device: return
        if self.logcat_proc: return
        lvl = self.log_level.currentText()
        try:
            self.logcat_proc = subprocess.Popen(
                ["adb", "-s", self.device, "logcat", f"*:{lvl}"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, stdin=subprocess.DEVNULL)
        except Exception as e:
            self._log("err", f"logcat failed · {e}")
            return
        self.btn_log_start.setEnabled(False)
        self.btn_log_stop.setEnabled(True)
        self._log("ok", f"logcat · level {lvl}")
        threading.Thread(target=self._logcat_reader, daemon=True).start()

    def _logcat_reader(self):
        while self.logcat_proc and self.logcat_proc.poll() is None:
            try:
                ln = self.logcat_proc.stdout.readline()
                if ln: self.bus.logcat_line.emit(ln.rstrip())
            except: break
            time.sleep(0.01)

    def _on_logcat_line(self, ln):
        if self.cur_logcat_filter and self.cur_logcat_filter.lower() not in ln.lower():
            return
        self.logcat_view.appendPlainText(ln)
        sb = self.logcat_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _logcat_stop(self):
        if self.logcat_proc:
            try:
                self.logcat_proc.terminate()
                self.logcat_proc.wait(timeout=2)
            except:
                self.logcat_proc.kill()
            self.logcat_proc = None
        self.btn_log_start.setEnabled(True)
        self.btn_log_stop.setEnabled(False)
        self._log("warn", "logcat stopped")

    def _logcat_clear(self):
        self.logcat_view.clear()

    def _logcat_save(self):
        name = f"logcat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(name, "w") as f:
            f.write(self.logcat_view.toPlainText())
        self._log("ok", f"saved · {name}")

    def _filter_logcat(self, text):
        self.cur_logcat_filter = text.strip()

    # ════════════════════════════════════════════════════════════════════
    #                              TERMINAL (FIXED)
    # ════════════════════════════════════════════════════════════════════

    def _term_exec(self):
        cmd = self.term_input.text().strip()
        if not cmd: return
        self.term_input.clear()
        self._term_run_args(cmd.split())

    def _term_run_args(self, args):
        """Run an ADB command in a background thread — safe."""
        if not self.device:
            self.bus.term_out.emit("ERR: no device connected")
            return
        self.bus.term_out.emit(f"\n$ adb -s {self.device} {' '.join(args)}")

        def work():
            try:
                if not args or args[0] != "adb":
                    full = ["-s", self.device] + args
                else:
                    full = args[1:]
                ok, out, err = run(["adb"] + full, timeout=25)
                if out:
                    self.bus.term_out.emit(out[:20000])
                if err:
                    self.bus.term_out.emit(f"[stderr] {err}")
                if not out and not err:
                    self.bus.term_out.emit("[no output]")
            except Exception as e:
                self.bus.term_out.emit(f"[error] {str(e)[:200]}")

        threading.Thread(target=work, daemon=True).start()

    def _on_term_out(self, text):
        self.term_out.appendPlainText(text)

    # ════════════════════════════════════════════════════════════════════
    #                              LOG
    # ════════════════════════════════════════════════════════════════════

    def _log(self, level, msg):
        self.bus.log.emit(level, msg)

    def _on_log(self, level, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        prefix = {"info": "·", "ok": "✓", "warn": "!", "err": "✗", "danger": "!"}.get(level, "·")
        fg = {
            "info": T.TEXT, "ok": T.GREEN, "warn": T.AMBER,
            "err": T.RED, "danger": T.RED,
        }.get(level, T.TEXT)

        html = (f'<span style="color:{T.TEXT_MUTED}">[{ts}]</span> '
                f'<span style="color:{fg}">{prefix} {msg}</span>')

        if hasattr(self, "term_out") and self.term_out is not None:
            self.term_out.appendHtml(html)

        if hasattr(self, "status_msg") and self.status_msg is not None:
            self.status_msg.setText(msg.upper()[:80])
            self.status_msg.setStyleSheet(
                f"color: {fg}; font-family: {T.FONT_MONO}; "
                f"font-size: {Scale.pt(8)}pt; letter-spacing: 1px; padding-left: 6px;")

    # ════════════════════════════════════════════════════════════════════
    #                              POLL
    # ════════════════════════════════════════════════════════════════════

    def _poll(self):
        if self.device:
            ok, _, _ = run(["adb", "-s", self.device, "shell", "echo", "1"], timeout=3)
            if not ok:
                self._log("warn", "device went offline")
                self._refresh_adb()
            else:
                self._fetch_stats()

    # ════════════════════════════════════════════════════════════════════
    #                              SHORTCUTS
    # ════════════════════════════════════════════════════════════════════

    def keyPressEvent(self, event):
        key = event.key()
        mods = event.modifiers()

        if mods & Qt.ControlModifier and key == Qt.Key_Q:
            self.close()
            return
        if mods & Qt.ControlModifier and key in (Qt.Key_Plus, Qt.Key_Equal):
            self._set_scale(Scale.value + 0.1)
            return
        if mods & Qt.ControlModifier and key == Qt.Key_Minus:
            self._set_scale(Scale.value - 0.1)
            return
        if mods & Qt.ControlModifier and key == Qt.Key_0:
            self._set_scale(1.0)
            return

        if Qt.Key_1 <= key <= Qt.Key_9:
            self._switch(key - Qt.Key_1)
        elif key == Qt.Key_0:
            self._switch(9)
        elif key == Qt.Key_F5:
            self._refresh_adb()
            self._refresh_fb()
        elif key == Qt.Key_F11:
            self.showNormal() if self.isFullScreen() else self.showFullScreen()
        else:
            super().keyPressEvent(event)


# ═══════════════════════════════════════════════════════════════════════════
#                              ENTRY
# ═══════════════════════════════════════════════════════════════════════════

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Droid Surgeon")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(T.BG_DEEP))
    palette.setColor(QPalette.WindowText, QColor(T.TEXT))
    palette.setColor(QPalette.Base, QColor(T.BG_INPUT))
    palette.setColor(QPalette.AlternateBase, QColor(T.BG_PANEL))
    palette.setColor(QPalette.Text, QColor(T.TEXT_HI))
    palette.setColor(QPalette.Button, QColor(T.BG_PANEL_HI))
    palette.setColor(QPalette.ButtonText, QColor(T.TEXT))
    palette.setColor(QPalette.Highlight, QColor(T.CYAN_DEEP))
    palette.setColor(QPalette.HighlightedText, QColor(T.TEXT_HI))
    palette.setColor(QPalette.ToolTipBase, QColor(T.BG_PANEL))
    palette.setColor(QPalette.ToolTipText, QColor(T.CYAN))
    app.setPalette(palette)

    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(build_stylesheet())

    win = DroidSurgeon()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
