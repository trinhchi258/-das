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
        self.save_results_to_csv()  # Lưu kết quả vào tệp CSV sau khi ghi

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
        self.persons = []  # Danh sách các thành viên của đội

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
        self.teams_listbox = tk.Listbox(self.admin_frame, width=50)
        self.teams_listbox.grid(row=3, columnspan=2)
        self.update_teams_listbox()  # Cập nhật danh sách đội

        # Nhập thông tin cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ:").grid(row=4, column=0)
        self.player_name_entry = tk.Entry(self.admin_frame)
        self.player_name_entry.grid(row=4, column=1)

        tk.Label(self.admin_frame, text="Tuổi:").grid(row=5, column=0)
        self.player_age_entry = tk.Entry(self.admin_frame)
        self.player_age_entry.grid(row=5, column=1)

        tk.Label(self.admin_frame, text="Giới Tính:").grid(row=6, column=0)
        self.player_gender_entry = tk.Entry(self.admin_frame)
        self.player_gender_entry.grid(row=6, column=1)

        tk.Label(self.admin_frame, text="Thông Tin Liên Hệ:").grid(row=7, column=0)
        self.player_contact_entry = tk.Entry(self.admin_frame)
        self.player_contact_entry.grid(row=7, column=1)

        tk.Label(self.admin_frame, text="Số Cầu Thủ:").grid(row=8, column=0)
        self.player_number_entry = tk.Entry(self.admin_frame)
        self.player_number_entry.grid(row=8, column=1)

        tk.Label(self.admin_frame, text="Vị Trí:").grid(row=9, column=0)
        self.player_position_entry = tk.Entry(self.admin_frame)
        self.player_position_entry.grid(row=9, column=1)

        self.add_player_button = tk.Button(self.admin_frame, text="Thêm Cầu Thủ", command=self.add_player)
        self.add_player_button.grid(row=10, columnspan=2)

        # Nhập thông tin trọng tài
        tk.Label(self.admin_frame, text="Tên Trọng Tài:").grid(row=11, column=0)
        self.referee_name_entry = tk.Entry(self.admin_frame)
        self.referee_name_entry.grid(row=11, column=1)

        tk.Label(self.admin_frame, text="Tuổi Trọng Tài:").grid(row=12, column=0)
        self.referee_age_entry = tk.Entry(self.admin_frame)
        self.referee_age_entry.grid(row=12, column=1)

        tk.Label(self.admin_frame, text="Giới Tính Trọng Tài:").grid(row=13, column=0)
        self.referee_gender_entry = tk.Entry(self.admin_frame)
        self.referee_gender_entry.grid(row=13, column=1)

        tk.Label(self.admin_frame, text="Thông Tin Liên Hệ Trọng Tài:").grid(row=14, column=0)
        self.referee_contact_entry = tk.Entry(self.admin_frame)
        self.referee_contact_entry.grid(row=14, column=1)

        tk.Label(self.admin_frame, text="Kinh Nghiệm (Năm):").grid(row=15, column=0)
        self.referee_experience_entry = tk.Entry(self.admin_frame)
        self.referee_experience_entry.grid(row=15, column=1)

        self.add_referee_button = tk.Button(self.admin_frame, text="Thêm Trọng Tài", command=self.add_referee)
        self.add_referee_button.grid(row=16, columnspan=2)

        # Lên lịch trận đấu
        tk.Label(self.admin_frame, text="Lên Lịch Trận Đấu", font=("Arial", 16)).grid(row=17, columnspan=2)

        tk.Label(self.admin_frame, text="ID Trận Đấu:").grid(row=18, column=0)
        self.match_id_entry = tk.Entry(self.admin_frame)
        self.match_id_entry.grid(row=18, column=1)

        tk.Label(self.admin_frame, text="Đội 1:").grid(row=19, column=0)
        self.match_team1_entry = tk.Entry(self.admin_frame)
        self.match_team1_entry.grid(row=19, column=1)

        tk.Label(self.admin_frame, text="Đội 2:").grid(row=20, column=0)
        self.match_team2_entry = tk.Entry(self.admin_frame)
        self.match_team2_entry.grid(row=20, column=1)

        self.schedule_match_button = tk.Button(self.admin_frame, text="Lên Lịch Trận Đấu", command=self.schedule_match)
        self.schedule_match_button.grid(row=21, columnspan=2)

        # Nhập kết quả trận đấu
        tk.Label(self.admin_frame, text="Nhập Kết Quả Trận Đấu", font=("Arial", 16)).grid(row=22, columnspan=2)

        tk.Label(self.admin_frame, text="ID Trận Đấu:").grid(row=23, column=0)
        self.result_match_id_entry = tk.Entry(self.admin_frame)
        self.result_match_id_entry.grid(row=23, column=1)

        tk.Label(self.admin_frame, text="Điểm Đội 1:").grid(row=24, column=0)
        self.result_team1_score_entry = tk.Entry(self.admin_frame)
        self.result_team1_score_entry.grid(row=24, column=1)

        tk.Label(self.admin_frame, text="Điểm Đội 2:").grid(row=25, column=0)
        self.result_team2_score_entry = tk.Entry(self.admin_frame)
        self.result_team2_score_entry.grid(row=25, column=1)

        self.record_result_button = tk.Button(self.admin_frame, text="Ghi Kết Quả", command=self.record_result)
        self.record_result_button.grid(row=26, columnspan=2)

    def add_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            self.sport_match.add_team(Team(team_name))
            self.update_teams_listbox()
            self.team_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh Báo", "Tên đội không được để trống.")

    def add_player(self):
        team_name = self.teams_listbox.get(tk.ACTIVE)
        if team_name:
            name = self.player_name_entry.get()
            age = self.player_age_entry.get()
            gender = self.player_gender_entry.get()
            contact_info = self.player_contact_entry.get()
            player_number = self.player_number_entry.get()
            player_position = self.player_position_entry.get()

            if name and age.isdigit() and player_number.isdigit() and player_position:
                player = Player(name, int(age), gender, contact_info, int(player_number), player_position)
                for team in self.sport_match.teams:
                    if team.team_name == team_name:
                        team.add_person(player)
                        break
                self.clear_player_entries()
            else:
                messagebox.showwarning("Cảnh Báo", "Vui lòng nhập thông tin hợp lệ cho cầu thủ.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng chọn một đội.")

    def add_referee(self):
        name = self.referee_name_entry.get()
        age = self.referee_age_entry.get()
        gender = self.referee_gender_entry.get()
        contact_info = self.referee_contact_entry.get()
        experience_years = self.referee_experience_entry.get()

        if name and age.isdigit() and experience_years.isdigit():
            referee = Referee(name, int(age), gender, contact_info, int(experience_years))
            # Giả định rằng trọng tài sẽ được lưu trữ theo cách khác hoặc cho phép thêm vào lớp khác
            self.clear_referee_entries()
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập thông tin hợp lệ cho trọng tài.")

    def schedule_match(self):
        match_id = self.match_id_entry.get()
        team1_name = self.match_team1_entry.get()
        team2_name = self.match_team2_entry.get()

        if match_id and team1_name and team2_name:
            team1 = next((team for team in self.sport_match.teams if team.team_name == team1_name), None)
            team2 = next((team for team in self.sport_match.teams if team.team_name == team2_name), None)

            if team1 and team2:
                match = Match(int(match_id), team1, team2, "Unknown", datetime.now())
                self.sport_match.schedule_match(match)
                messagebox.showinfo("Thông Báo", "Trận đấu đã được lên lịch.")
                self.clear_match_entries()
            else:
                messagebox.showwarning("Cảnh Báo", "Một trong hai đội không tồn tại.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin trận đấu.")

    def record_result(self):
        match_id = self.result_match_id_entry.get()
        team1_score = self.result_team1_score_entry.get()
        team2_score = self.result_team2_score_entry.get()

        if match_id and team1_score.isdigit() and team2_score.isdigit():
            match = next((match for match in self.sport_match.matches if match.match_id == int(match_id)), None)

            if match:
                self.sport_match.record_result(match, int(team1_score), int(team2_score))
                messagebox.showinfo("Thông Báo", "Kết quả đã được ghi.")
                self.clear_result_entries()
            else:
                messagebox.showwarning("Cảnh Báo", "Trận đấu không tồn tại.")
        else:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập đầy đủ thông tin kết quả.")

    def clear_player_entries(self):
        self.player_name_entry.delete(0, tk.END)
        self.player_age_entry.delete(0, tk.END)
        self.player_gender_entry.delete(0, tk.END)
        self.player_contact_entry.delete(0, tk.END)
        self.player_number_entry.delete(0, tk.END)
        self.player_position_entry.delete(0, tk.END)

    def clear_referee_entries(self):
        self.referee_name_entry.delete(0, tk.END)
        self.referee_age_entry.delete(0, tk.END)
        self.referee_gender_entry.delete(0, tk.END)
        self.referee_contact_entry.delete(0, tk.END)
        self.referee_experience_entry.delete(0, tk.END)

    def clear_match_entries(self):
        self.match_id_entry.delete(0, tk.END)
        self.match_team1_entry.delete(0, tk.END)
        self.match_team2_entry.delete(0, tk.END)

    def clear_result_entries(self):
        self.result_match_id_entry.delete(0, tk.END)
        self.result_team1_score_entry.delete(0, tk.END)
        self.result_team2_score_entry.delete(0, tk.END)

    def update_teams_listbox(self):
        self.teams_listbox.delete(0, tk.END)
        for team in self.sport_match.teams:
            self.teams_listbox.insert(tk.END, team.team_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = SportMatchApp(root)
    root.mainloop()
