import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class SportMatch:
    def __init__(self):
        self.teams = []
        self.matches = []
        self.load_teams_from_csv()  # Tải đội từ tệp CSV khi khởi tạo

    def add_team(self, team):
        self.teams.append(team)
        self.save_teams_to_csv()  # Lưu đội vào tệp CSV khi thêm

    def remove_team(self, team):
        self.teams.remove(team)
        self.save_teams_to_csv()  # Cập nhật tệp CSV khi xóa

    def schedule_match(self, match):
        self.matches.append(match)

    def save_teams_to_csv(self):
        with open('teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for team in self.teams:
                writer.writerow([team.team_name])  # Ghi tên đội với định dạng UTF-8

    def load_teams_from_csv(self):
        try:
            with open('teams.csv', 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:  # Kiểm tra hàng không rỗng
                        team_name = row[0]
                        self.add_team(Team(team_name))  # Thêm đội vào danh sách
        except FileNotFoundError:
            print("Tệp teams.csv không tồn tại. Một tệp mới sẽ được tạo khi thêm đội.")


class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def get_details(self):
        return {
            'Name': self.name,
            'Age': self.age,
            'Gender': self.gender
        }


class Player(Person):
    def __init__(self, name, age, gender, player_number, player_position):
        super().__init__(name, age, gender)
        self.player_number = player_number
        self.player_position = player_position

    def get_player_info(self):
        return {
            **self.get_details(),
            'Player Number': self.player_number,
            'Position': self.player_position
        }


class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
        else:
            print(f"{player.name} is already in the team.")

    def remove_player(self, player_name):
        player_to_remove = next((player for player in self.players if player.name == player_name), None)
        if player_to_remove:
            self.players.remove(player_to_remove)
            print(f"Player {player_name} removed from the team.")
        else:
            print(f"Player {player_name} not found in the team.")

    def get_team_members(self):
        return [player.get_player_info() for player in self.players]


class Match:
    def __init__(self, match_id, team1, team2, referee, match_date):
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.referee = referee
        self.match_date = match_date
        self.result = None

    def schedule_match(self):
        return f"Match scheduled between {self.team1.team_name} and {self.team2.team_name} on {self.match_date}."


class SportMatchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hệ Thống Quản Lý Thể Thao")

        # Tạo danh sách người dùng
        self.users = [User("admin", "admin123"), User("referee1", "ref123")]
        self.sport_match = SportMatch()  # Khởi tạo lớp SportMatch

        # Giao diện đăng nhập
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Tên Người Dùng:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Mật Khẩu:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Đăng Nhập", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.admin_frame = None

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user in self.users:
            if user.username == username and user.password == password:
                messagebox.showinfo("Đăng Nhập Thành Công", f"Chào mừng, {username}!")
                self.show_admin_interface()
                return
        messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng.")

    def show_admin_interface(self):
        # Xóa giao diện đăng nhập
        self.login_frame.pack_forget()

        self.admin_frame = tk.Frame(self.master)
        self.admin_frame.pack(pady=20)

        tk.Label(self.admin_frame, text="Quản Lý Đội Bóng", font=("Arial", 16)).grid(row=0, columnspan=2)

        tk.Label(self.admin_frame, text="Tên Đội:").grid(row=1, column=0)
        self.team_entry = tk.Entry(self.admin_frame)
        self.team_entry.grid(row=1, column=1)

        self.add_team_button = tk.Button(self.admin_frame, text="Thêm Đội", command=self.add_team)
        self.add_team_button.grid(row=1, column=2)

        self.remove_team_button = tk.Button(self.admin_frame, text="Xóa Đội", command=self.remove_team)
        self.remove_team_button.grid(row=1, column=3)

        # Thêm cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ:").grid(row=2, column=0)
        self.player_name_entry = tk.Entry(self.admin_frame)
        self.player_name_entry.grid(row=2, column=1)

        tk.Label(self.admin_frame, text="Tuổi Cầu Thủ:").grid(row=3, column=0)
        self.player_age_entry = tk.Entry(self.admin_frame)
        self.player_age_entry.grid(row=3, column=1)

        tk.Label(self.admin_frame, text="Giới Tính:").grid(row=4, column=0)
        self.player_gender_entry = tk.Entry(self.admin_frame)
        self.player_gender_entry.grid(row=4, column=1)

        tk.Label(self.admin_frame, text="Số Áo:").grid(row=5, column=0)
        self.player_number_entry = tk.Entry(self.admin_frame)
        self.player_number_entry.grid(row=5, column=1)

        tk.Label(self.admin_frame, text="Vị Trí:").grid(row=6, column=0)
        self.player_position_entry = tk.Entry(self.admin_frame)
        self.player_position_entry.grid(row=6, column=1)

        self.add_player_button = tk.Button(self.admin_frame, text="Thêm Cầu Thủ", command=self.add_player)
        self.add_player_button.grid(row=7, column=1)

        # Xóa cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ Cần Xóa:").grid(row=8, column=0)
        self.remove_player_entry = tk.Entry(self.admin_frame)
        self.remove_player_entry.grid(row=8, column=1)

        self.remove_player_button = tk.Button(self.admin_frame, text="Xóa Cầu Thủ", command=self.remove_player)
        self.remove_player_button.grid(row=9, column=1)

    def add_team(self):
        team_name = self.team_entry.get()
        if team_name:
            self.sport_match.add_team(Team(team_name))
            messagebox.showinfo("Thành Công", f"Đội {team_name} đã được thêm.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def remove_team(self):
        team_name = self.team_entry.get()
        if team_name:
            team = next((t for t in self.sport_match.teams if t.team_name == team_name), None)
            if team:
                self.sport_match.remove_team(team)
                messagebox.showinfo("Thành Công", f"Đội {team_name} đã được xóa.")
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def add_player(self):
        team_name = self.team_entry.get()
        player_name = self.player_name_entry.get()
        player_age = self.player_age_entry.get()
        player_gender = self.player_gender_entry.get()
        player_number = self.player_number_entry.get()
        player_position = self.player_position_entry.get()

        if team_name and player_name and player_age.isdigit() and player_number.isdigit():
            team = next((t for t in self.sport_match.teams if t.team_name == team_name), None)
            if team:
                player = Player(player_name, int(player_age), player_gender, int(player_number), player_position)
                team.add_player(player)
                messagebox.showinfo("Thành Công", f"Cầu thủ {player_name} đã được thêm vào đội {team_name}.")
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng thông tin cầu thủ.")

    def remove_player(self):
        team_name = self.team_entry.get()
        player_name = self.remove_player_entry.get()

        if team_name and player_name:
            team = next((t for t in self.sport_match.teams if t.team_name == team_name), None)
            if team:
                team.remove_player(player_name)
                messagebox.showinfo("Thành Công", f"Cầu thủ {player_name} đã bị xóa khỏi đội {team_name}.")
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng thông tin.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportMatchApp(root)
    root.mainloop()



