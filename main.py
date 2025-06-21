import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

class SudokuSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(400, 450)

        self.grid = QGridLayout()
        self.inputs = [[QLineEdit() for _ in range(9)] for _ in range(9)]

        font = QFont("Arial", 14)
        for i in range(9):
            for j in range(9):
                box = self.inputs[i][j]
                box.setFixedSize(40, 40)
                box.setFont(font)
                box.setMaxLength(1)
                box.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(box, i, j)

        self.solve_button = QPushButton("Resolver Sudoku")
        self.solve_button.clicked.connect(self.solve)

        layout = QVBoxLayout()
        layout.addLayout(self.grid)
        layout.addWidget(self.solve_button)
        self.setLayout(layout)

    def get_board(self):
        board = []
        for row in self.inputs:
            current_row = []
            for cell in row:
                text = cell.text()
                if text.isdigit():
                    current_row.append(int(text))
                else:
                    current_row.append(0)
            board.append(current_row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.inputs[i][j].setText(str(board[i][j]))

    def solve(self):
        board = self.get_board()
        if solve_sudoku(board):
            self.set_board(board)
        else:
            QMessageBox.warning(self, "Erro", "Sudoku não pode ser resolvido!")

if __name__ == "__main__":
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    window = SudokuSolver()
    window.show()
    sys.exit(app.exec_())
