import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from controllers.main_controller import MainController


def main():
    print("=" * 60)
    print("SmartEnroll - Starting Application (MVC Architecture)")
    print("=" * 60)

    # ✅ CRITICAL: Enable High DPI scaling BEFORE creating QApplication
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create main controller
    main_controller = MainController()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()