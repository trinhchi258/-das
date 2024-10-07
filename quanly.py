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
        self.load_results_from_csv()  # Tải kết quả từ tệp CSV khi khởi tạo

    def add_team(self, team):
        self.teams.append(team)
        self.save_teams_to_csv()  # Lưu đội vào tệp CSV khi thêm

    def remove_team(self, team):
        self.teams.remove(team)
        self.save_teams_to_csv()  # Cập nhật tệp CSV khi xóa

    def schedule_match(self, match):
        self.matches.append(match)

    def record_result(self, match, team1_score, team2_score):
        match.record_result(team1_score, team2_score)
        self.save_results_to_csv()  # Lưu kết quả vào CSV
        return match.result

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

    def save_results_to_csv(self):
        with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Match ID', 'Team 1', 'Team 2', 'Score Team 1', 'Score Team 2'])
            for match in self.matches:
                if match.result:  # Kiểm tra xem kết quả đã được ghi
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
                next(reader)  # Bỏ qua hàng tiêu đề
                for row in reader:
                    if row:  # Kiểm tra hàng không rỗng
                        match_id = int(row[0])
                        team1_name = row[1]
                        team2_name = row[2]
                        team1_score = int(row[3])
                        team2_score = int(row[4])
                        # Tạo một trận đấu và thêm vào danh sách matches
                        match = Match(match_id, Team(team1_name), Team(team2_name), "Unknown", datetime.now())  # Trọng tài tạm thời là "Unknown"
                        match.record_result(team1_score, team2_score)  # Ghi kết quả cho trận đấu
                        self.matches.append(match)
        except FileNotFoundError:
            print("Tệp results.csv không tồn tại. Một tệp mới sẽ được tạo khi ghi kết quả.")


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


class Coach(Person):
    def __init__(self, name, age, gender, coaching_experience, managed_team):
        super().__init__(name, age, gender)
        self.coaching_experience = coaching_experience
        self.managed_team = managed_team

    def get_coach_info(self):
        return {
            **self.get_details(),
            'Coaching Experience': self.coaching_experience,
            'Managed Team': self.managed_team
        }


class Referee(Person):
    def __init__(self, name, age, gender, experience_years):
        super().__init__(name, age, gender)
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

        # Nhập tên đội
        tk.Label(self.admin_frame, text="Tên Đội:").grid(row=1, column=0)
        self.team_name_entry = tk.Entry(self.admin_frame)
        self.team_name_entry.grid(row=1, column=1)

        self.add_team_button = tk.Button(self.admin_frame, text="Thêm Đội", command=self.add_team)
        self.add_team_button.grid(row=2, columnspan=2)

        # Danh sách đội
        tk.Label(self.admin_frame, text="Danh Sách Đội:").grid(row=3, column=0)
        self.team_listbox = tk.Listbox(self.admin_frame)
        self.team_listbox.grid(row=3, column=1)

        self.refresh_team_list()

        # Nhập tên cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ:").grid(row=4, column=0)
        self.player_name_entry = tk.Entry(self.admin_frame)
        self.player_name_entry.grid(row=4, column=1)

        tk.Label(self.admin_frame, text="Tuổi:").grid(row=5, column=0)
        self.player_age_entry = tk.Entry(self.admin_frame)
        self.player_age_entry.grid(row=5, column=1)

        tk.Label(self.admin_frame, text="Giới Tính:").grid(row=6, column=0)
        self.player_gender_entry = tk.Entry(self.admin_frame)
        self.player_gender_entry.grid(row=6, column=1)

        tk.Label(self.admin_frame, text="Số Cầu Thủ:").grid(row=7, column=0)
        self.player_number_entry = tk.Entry(self.admin_frame)
        self.player_number_entry.grid(row=7, column=1)

        tk.Label(self.admin_frame, text="Vị Trí:").grid(row=8, column=0)
        self.player_position_entry = tk.Entry(self.admin_frame)
        self.player_position_entry.grid(row=8, column=1)

        self.add_player_button = tk.Button(self.admin_frame, text="Thêm Cầu Thủ", command=self.add_player_to_team)
        self.add_player_button.grid(row=9, columnspan=2)

        # Xóa cầu thủ
        self.remove_player_button = tk.Button(self.admin_frame, text="Xóa Cầu Thủ", command=self.remove_player_from_team)
        self.remove_player_button.grid(row=10, columnspan=2)

        # Lịch thi đấu
        tk.Label(self.admin_frame, text="Lịch Thi Đấu", font=("Arial", 16)).grid(row=11, columnspan=2)

        tk.Label(self.admin_frame, text="Đội 1:").grid(row=12, column=0)
        self.team1_entry = tk.Entry(self.admin_frame)
        self.team1_entry.grid(row=12, column=1)

        tk.Label(self.admin_frame, text="Đội 2:").grid(row=13, column=0)
        self.team2_entry = tk.Entry(self.admin_frame)
        self.team2_entry.grid(row=13, column=1)

        tk.Label(self.admin_frame, text="Trọng Tài:").grid(row=14, column=0)
        self.referee_entry = tk.Entry(self.admin_frame)
        self.referee_entry.grid(row=14, column=1)

        tk.Label(self.admin_frame, text="Ngày Trận Đấu:").grid(row=15, column=0)
        self.match_date_entry = tk.Entry(self.admin_frame)
        self.match_date_entry.grid(row=15, column=1)

        self.schedule_match_button = tk.Button(self.admin_frame, text="Lên Lịch Trận Đấu", command=self.schedule_match)
        self.schedule_match_button.grid(row=16, columnspan=2)

        # Ghi kết quả
        tk.Label(self.admin_frame, text="Ghi Kết Quả", font=("Arial", 16)).grid(row=17, columnspan=2)

        tk.Label(self.admin_frame, text="Điểm Đội 1:").grid(row=18, column=0)
        self.team1_score_entry = tk.Entry(self.admin_frame)
        self.team1_score_entry.grid(row=18, column=1)

        tk.Label(self.admin_frame, text="Điểm Đội 2:").grid(row=19, column=0)
        self.team2_score_entry = tk.Entry(self.admin_frame)
        self.team2_score_entry.grid(row=19, column=1)

        self.record_result_button = tk.Button(self.admin_frame, text="Ghi Kết Quả", command=self.record_result)
        self.record_result_button.grid(row=20, columnspan=2)

    def add_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            team = Team(team_name)
            self.sport_match.add_team(team)
            messagebox.showinfo("Thông Báo", f"Đội {team_name} đã được thêm thành công.")
            self.refresh_team_list()
            self.team_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập tên đội.")

    def refresh_team_list(self):
        self.team_listbox.delete(0, tk.END)
        for team in self.sport_match.teams:
            self.team_listbox.insert(tk.END, team.team_name)

    def add_player_to_team(self):
        team_name = self.team_listbox.get(tk.ACTIVE)
        if not team_name:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn đội để thêm cầu thủ.")
            return

        name = self.player_name_entry.get()
        age = self.player_age_entry.get()
        gender = self.player_gender_entry.get()
        player_number = self.player_number_entry.get()
        position = self.player_position_entry.get()

        if name and age.isdigit() and player_number.isdigit() and position:
            age = int(age)
            player_number = int(player_number)
            player = Player(name, age, gender, player_number, position)
            for team in self.sport_match.teams:
                if team.team_name == team_name:
                    team.add_person(player)
                    messagebox.showinfo("Thông Báo", f"Cầu thủ {name} đã được thêm vào đội {team_name}.")
                    self.player_name_entry.delete(0, tk.END)
                    self.player_age_entry.delete(0, tk.END)
                    self.player_gender_entry.delete(0, tk.END)
                    self.player_number_entry.delete(0, tk.END)
                    self.player_position_entry.delete(0, tk.END)
                    return
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng điền đầy đủ thông tin cầu thủ.")

    def remove_player_from_team(self):
        team_name = self.team_listbox.get(tk.ACTIVE)
        if not team_name:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn đội để xóa cầu thủ.")
            return

        name = self.player_name_entry.get()
        if name:
            for team in self.sport_match.teams:
                if team.team_name == team_name:
                    for player in team.persons:
                        if player.name == name:
                            team.remove_person(player)
                            messagebox.showinfo("Thông Báo", f"Cầu thủ {name} đã được xóa khỏi đội {team_name}.")
                            self.player_name_entry.delete(0, tk.END)
                            return
            messagebox.showwarning("Cảnh Báo", f"Cầu thủ {name} không tồn tại trong đội {team_name}.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập tên cầu thủ cần xóa.")

    def schedule_match(self):
        team1_name = self.team1_entry.get()
        team2_name = self.team2_entry.get()
        referee_name = self.referee_entry.get()
        match_date = self.match_date_entry.get()

        if team1_name and team2_name and referee_name and match_date:
            match = Match(len(self.sport_match.matches) + 1, Team(team1_name), Team(team2_name), referee_name, match_date)
            self.sport_match.schedule_match(match)
            messagebox.showinfo("Thông Báo", f"Trận đấu giữa {team1_name} và {team2_name} đã được lên lịch.")
            self.team1_entry.delete(0, tk.END)
            self.team2_entry.delete(0, tk.END)
            self.referee_entry.delete(0, tk.END)
            self.match_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng điền đầy đủ thông tin lịch thi đấu.")

    def record_result(self):
        team1_score = self.team1_score_entry.get()
        team2_score = self.team2_score_entry.get()

        if team1_score.isdigit() and team2_score.isdigit():
            team1_score = int(team1_score)
            team2_score = int(team2_score)

            # Giả sử bạn sẽ ghi kết quả cho trận đấu gần nhất
            if self.sport_match.matches:
                match = self.sport_match.matches[-1]  # Trận đấu gần nhất
                result = self.sport_match.record_result(match, team1_score, team2_score)
                messagebox.showinfo("Thông Báo", f"Kết quả trận đấu: {result['Team 1']} {result['Score'][result['Team 1']]} - {result['Score'][result['Team 2']]} {result['Team 2']}")
                self.team1_score_entry.delete(0, tk.END)
                self.team2_score_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Cảnh Báo", "Chưa có trận đấu nào được lên lịch.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập điểm hợp lệ.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportMatchApp(root)
    root.mainloop()
