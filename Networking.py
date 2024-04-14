import os.path
import random
from datetime import datetime
from tkinter import messagebox, Tk, Button
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "13XgVTsOJLVnDSg7McTIOrwClt76vmHcKRbSzDHxPeAQ"
SAMPLE_RANGE_NAME = "Sheet1!A1:C1"


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board_buttons = []
        self.current_winner = None
        self.turn = 'X'
        self.game_over = False
        self.create_board()
        self.db_name = "match_results.db"
        self.adapter = DataAdapter(self.db_name)
        self.start_date = datetime(2024, 4, 10)
        self.end_date = datetime(2024, 4, 11)
        self.creds = None
        self.authenticate_google_sheets()

    def authenticate_google_sheets(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = Button(self.master, text=' ', font=('Arial', 20), width=8, height=4,
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")
                self.board_buttons.append(button)

    def on_button_click(self, row, col):
        if self.game_over:
            return
        if self.board_buttons[row * 3 + col]['text'] == ' ':
            self.board_buttons[row * 3 + col]['text'] = self.turn
            if self.check_winner(row, col):
                self.current_winner = self.turn
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {self.current_winner} wins!")
                self.save_match_result_to_sheet()
            elif self.check_tie():
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a tie!")
                self.save_match_result_to_sheet()
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                if self.turn == 'O':
                    self.ai_make_move()

    def check_winner(self, row, col):
        # Check row
        if self.board_buttons[row * 3]['text'] == self.board_buttons[row * 3 + 1]['text'] == self.board_buttons[row * 3 + 2]['text'] == self.turn:
            return True
        # Check column
        if self.board_buttons[col]['text'] == self.board_buttons[col + 3]['text'] == self.board_buttons[col + 6]['text'] == self.turn:
            return True
        # Check diagonals
        if row == col:
            if self.board_buttons[0]['text'] == self.board_buttons[4]['text'] == self.board_buttons[8]['text'] == self.turn:
                return True
        if row + col == 2:
            if self.board_buttons[2]['text'] == self.board_buttons[4]['text'] == self.board_buttons[6]['text'] == self.turn:
                return True
        return False

    def check_tie(self):
        for button in self.board_buttons:
            if button['text'] == ' ':
                return False
        return True

    def ai_make_move(self):
        empty_squares = [i for i, button in enumerate(self.board_buttons) if button['text'] == ' ']
        if empty_squares:
            square = random.choice(empty_squares)
            self.board_buttons[square]['text'] = 'O'
            if self.check_winner(square // 3, square % 3):
                self.current_winner = 'O'
                self.game_over = True
                messagebox.showinfo("Game Over", f"Player {self.current_winner} wins!")
            elif self.check_tie():
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a tie!")

    def save_match_result_to_sheet(self):
        service = build("sheets", "v4", credentials=self.creds)
        match_time = generate_random_date(self.start_date, self.end_date).strftime("%d/%m/%Y %I:%M %p")
        if self.current_winner:
            winner = f"Player {self.current_winner}"
            loser = f"Player {'O' if self.current_winner == 'X' else 'X'}"
        else:
            winner = loser = "Tie"
        values = [[match_time, winner, loser]]
        body = {"values": values}
        service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()


def generate_random_date(start_date, end_date):
    start_timestamp = datetime.timestamp(start_date)
    end_timestamp = datetime.timestamp(end_date)
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)


def main():
    root = Tk()
    game = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
