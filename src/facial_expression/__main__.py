from PyQt6.QtWidgets import QApplication
import sys
from .main import MainApplication


def main() -> None:
    """Launch the GUI application."""
    app = QApplication(sys.argv)
    main_window = MainApplication()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
