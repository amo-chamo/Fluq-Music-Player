from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel

class MusicApp(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.North)       # Tabs on top
        self.setMovable(False)                      # Tabs not rearrangeable
        self.setTabsClosable(False)                 # Tabs not closable
        self.setDocumentMode(True)                  # Flat browser-like style

        # Add sections
        self.addTab(self.home_tab(), "Home")
        self.addTab(self.discover_tab(), "Discover")
        self.addTab(self.library_tab(), "Library")
        self.addTab(self.playlists_tab(), "Playlists")

    def home_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to Home"))
        tab.setLayout(layout)
        return tab

    def discover_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Discover new tracks"))
        tab.setLayout(layout)
        return tab

    def library_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Your Library"))
        tab.setLayout(layout)
        return tab

    def playlists_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Playlists"))
        tab.setLayout(layout)
        return tab

if __name__ == "__main__":
    app = QApplication([])
    window = MusicApp()
    window.setWindowTitle("My Music Player")
    window.resize(800, 600)
    window.show()
    app.exec_()
