#.\venv\Scripts\Activate
import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import pyqtgraph as pg

df = pd.DataFrame({"diena": ["P", "O", "T", "C", "Pk"], "vertiba": [12, 18, 9, 22, 15]})

app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle("Digitālais informācijas panelis")

layout = QVBoxLayout()
layout.addWidget(QLabel("Kopsavilkums:"))

# Tabula
table = QTableWidget(df.shape[0], df.shape[1])
table.setHorizontalHeaderLabels(df.columns.tolist())
for r in range(df.shape[0]):
    for c in range(df.shape[1]):
        table.setItem(r, c, QTableWidgetItem(str(df.iat[r, c])))
layout.addWidget(table)

# Grafiks
plot = pg.PlotWidget()
plot.plot(df["vertiba"].tolist())
layout.addWidget(plot)

w.setLayout(layout)
w.resize(700, 500)
w.show()
sys.exit(app.exec())
