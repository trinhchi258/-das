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
        self.load_teams_from_csv()
        self.load_results_from_csv()

    def add_team(self, team):
        self.teams.append(team)
        self.save_teams_to_csv()

    def remove_team(self, team):
        self.teams.remove(team)
        self.save_teams_to_csv()

    def schedule_match(self, match):
        self.matches.append(match)

    def record_result(self, match, team1_score, team2_score):
        match.record_result(team1_score, team2_score)
        self.save_results_to_csv()  # Ghi kết quả vào CSV
        return match.result

    def save_teams_to_csv(self):
        with open('teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for team in self.teams:
                writer.writerow([team.team_name])

    def load_teams_from_csv(self):
        try:
            with open('teams.csv', 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                       team_name = row[0]
                       self.add_team(Team(team_name))
        except FileNotFoundError:
            print("Tệp teams.csv không tồn tại. Một tệp mới sẽ được tạo khi thêm đội.")

    def save_results_to_csv(self):
        with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Match ID', 'Team 1', 'Team 2', 'Score Team 1', 'Score Team 2'])
            for match in self.matches:
                if match.result:
                    writer.writerow([
                        match.match_id,
                        match.team1.team_name,
                        match.team2.team_name,
                        match.result['Score'][match.team1.team_name],
                        match.result['Score'][match.team2.team_name]
                    ])

    def load_results_from_csv(self):
        try:
            with open('results.csv', 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row:
                        match_id = int(row[0])
                        team1_name = row[1]
                        team2_name = row[2]
                        team1_score = int(row[3])
                        team2_score = int(row[4])
                        match = Match(match_id, Team(team1_name), Team(team2_name), "Unknown", datetime.now())
                        match.record_result(team1_score, team2_score)
                        self.matches.append(match)
        except FileNotFoundError:
            print("Tệp results.csv không tồn tại. Một tệp mới sẽ được tạo khi ghi kết quả.")

class Person:
    def __init__(self, name, age, gender, contact_info):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact_info = contact_info

    def get_details(self):
        return {
            'Name': self.name,
            'Age': self.age,
            'Gender': self.gender,
            'Contact Info': self.contact_info
        }


class Player(Person):
    def __init__(self, name, age, gender, contact_info, player_number, player_position):
        super().__init__(name, age, gender, contact_info)
        self.player_number = player_number
        self.player_position = player_position

    def get_player_info(self):
        return {
            **self.get_details(),
            'Player Number': self.player_number,
            'Position': self.player_position
        }


class Coach(Person):
    def __init__(self, name, age, gender, contact_info, coaching_experience, managed_team):
        super().__init__(name, age, gender, contact_info)
        self.coaching_experience = coaching_experience
        self.managed_team = managed_team

    def get_coach_info(self):
        return {
            **self.get_details(),
            'Coaching Experience': self.coaching_experience,
            'Managed Team': self.managed_team
        }


class Referee(Person):
    def __init__(self, name, age, gender, contact_info, experience_years):
        super().__init__(name, age, gender, contact_info)
        self.experience_years = experience_years

    def get_referee_info(self):
        return {
            **self.get_details(),
            'Experience Years': self.experience_years
        }


class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.persons = []

    def add_person(self, person):
        if person not in self.persons:
            self.persons.append(person)
        else:
            print(f"{person.name} is already in the team.")

    def remove_person(self, person):
        if person in self.persons:
            self.persons.remove(person)
        else:
            print(f"{person.name} is not in the team.")

    def get_team_members(self):
        return [person.get_details() for person in self.persons]


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

    def record_result(self, team1_score, team2_score):
        self.result = {
            'Team 1': self.team1.team_name,
            'Team 2': self.team2.team_name,
            'Score': {self.team1.team_name: team1_score, self.team2.team_name: team2_score}
        }


class SportMatchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Hệ Thống Quản Lý Thể Thao")

        self.users = [User("admin", "admin123"), User("referee1", "ref123")]
        self.sport_match = SportMatch()

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
        self.login_frame.pack_forget()

        self.admin_frame = tk.Frame(self.master)
        self.admin_frame.pack(pady=20)

        tk.Label(self.admin_frame, text="Quản Lý Đội Bóng", font=("Arial", 16)).grid(row=0, columnspan=2)

        # Nhập tên đội
        tk.Label(self.admin_frame, text="Tên Đội:").grid(row=1, column=0)
        self.team_name_entry = tk.Entry(self.admin_frame)
        self.team_name_entry.grid(row=1, column=1)

        self.add_team_button = tk.Button(self.admin_frame, text="Thêm Đội", command=self.add_team)
        self.add_team_button.grid(row=1, column=2)

        self.remove_team_button = tk.Button(self.admin_frame, text="Xóa Đội", command=self.remove_team)
        self.remove_team_button.grid(row=1, column=3)

        # Nhập thông tin cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ:").grid(row=2, column=0)
        self.player_name_entry = tk.Entry(self.admin_frame)
        self.player_name_entry.grid(row=2, column=1)

        tk.Label(self.admin_frame, text="Số Cầu Thủ:").grid(row=2, column=2)
        self.player_number_entry = tk.Entry(self.admin_frame)
        self.player_number_entry.grid(row=2, column=3)

        tk.Label(self.admin_frame, text="Vị Trí:").grid(row=2, column=4)
        self.player_position_entry = tk.Entry(self.admin_frame)
        self.player_position_entry.grid(row=2, column=5)

        self.add_player_button = tk.Button(self.admin_frame, text="Thêm Cầu Thủ", command=self.add_player)
        self.add_player_button.grid(row=2, column=6)

        # Nhập thông tin trận đấu
        tk.Label(self.admin_frame, text="Trận Đấu ID:").grid(row=3, column=0)
        self.match_id_entry = tk.Entry(self.admin_frame)
        self.match_id_entry.grid(row=3, column=1)

        tk.Label(self.admin_frame, text="Đội 1:").grid(row=3, column=2)
        self.team1_entry = tk.Entry(self.admin_frame)
        self.team1_entry.grid(row=3, column=3)

        tk.Label(self.admin_frame, text="Đội 2:").grid(row=3, column=4)
        self.team2_entry = tk.Entry(self.admin_frame)
        self.team2_entry.grid(row=3, column=5)

        tk.Label(self.admin_frame, text="Trọng Tài:").grid(row=3, column=6)
        self.referee_entry = tk.Entry(self.admin_frame)
        self.referee_entry.grid(row=3, column=7)

        tk.Label(self.admin_frame, text="Ngày Giờ:").grid(row=3, column=8)
        self.date_entry = tk.Entry(self.admin_frame)
        self.date_entry.grid(row=3, column=9)

        self.schedule_match_button = tk.Button(self.admin_frame, text="Lên Lịch Trận Đấu", command=self.schedule_match)
        self.schedule_match_button.grid(row=3, column=10)

        # Nhập kết quả trận đấu
        tk.Label(self.admin_frame, text="Kết Quả Đội 1:").grid(row=4, column=0)
        self.team1_score_entry = tk.Entry(self.admin_frame)
        self.team1_score_entry.grid(row=4, column=1)

        tk.Label(self.admin_frame, text="Kết Quả Đội 2:").grid(row=4, column=2)
        self.team2_score_entry = tk.Entry(self.admin_frame)
        self.team2_score_entry.grid(row=4, column=3)

        self.record_result_button = tk.Button(self.admin_frame, text="Ghi Kết Quả", command=self.record_result)
        self.record_result_button.grid(row=4, column=4)

    def add_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            self.sport_match.add_team(Team(team_name))
            messagebox.showinfo("Thông Báo", f"Đội '{team_name}' đã được thêm!")
            self.team_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def remove_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            team_to_remove = next((team for team in self.sport_match.teams if team.team_name == team_name), None)
            if team_to_remove:
                self.sport_match.remove_team(team_to_remove)
                messagebox.showinfo("Thông Báo", f"Đội '{team_name}' đã được xóa!")
                self.team_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Đội không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def add_player(self):
        player_name = self.player_name_entry.get()
        player_number = self.player_number_entry.get()
        player_position = self.player_position_entry.get()
        if player_name and player_number.isdigit() and player_position:
            player = Player(player_name, 18, "Unknown", "Unknown", int(player_number), player_position)  # Ví dụ đơn giản
            # Thêm cầu thủ vào đội hiện tại (cần chỉnh sửa để chọn đội cụ thể)
            team_name = self.team1_entry.get()  # Giả sử cầu thủ được thêm vào Đội 1
            team = next((t for t in self.sport_match.teams if t.team_name == team_name), None)
            if team:
                team.add_person(player)
                messagebox.showinfo("Thông Báo", f"Cầu thủ '{player_name}' đã được thêm vào đội '{team_name}'!")
                self.player_name_entry.delete(0, tk.END)
                self.player_number_entry.delete(0, tk.END)
                self.player_position_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Đội không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông tin cầu thủ hợp lệ.")

    def schedule_match(self):
        match_id = self.match_id_entry.get()
        team1_name = self.team1_entry.get()
        team2_name = self.team2_entry.get()
        referee_name = self.referee_entry.get()
        match_date = self.date_entry.get()

        if match_id.isdigit() and team1_name and team2_name and referee_name and match_date:
            match = Match(int(match_id), Team(team1_name), Team(team2_name), referee_name, match_date)
            self.sport_match.schedule_match(match)
            messagebox.showinfo("Thông Báo", f"Trận đấu '{match_id}' đã được lên lịch!")
            self.match_id_entry.delete(0, tk.END)
            self.team1_entry.delete(0, tk.END)
            self.team2_entry.delete(0, tk.END)
            self.referee_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông tin trận đấu hợp lệ.")

    def record_result(self):
        match_id = self.match_id_entry.get()
        team1_score = self.team1_score_entry.get()
        team2_score = self.team2_score_entry.get()

        if match_id.isdigit() and team1_score.isdigit() and team2_score.isdigit():
            match = next((m for m in self.sport_match.matches if m.match_id == int(match_id)), None)
            if match:
                result = self.sport_match.record_result(match, int(team1_score), int(team2_score))
                messagebox.showinfo("Kết Quả", f"Kết quả trận đấu '{match_id}': {result['Team 1']} {result['Score'][match.team1.team_name]} - {result['Score'][match.team2.team_name]} {result['Team 2']}")
                self.team1_score_entry.delete(0, tk.END)
                self.team2_score_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", "Trận đấu không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông tin kết quả hợp lệ.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SportMatchApp(root)
    root.mainloop()




