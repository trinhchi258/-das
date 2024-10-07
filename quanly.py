import tkinter as tk
from tkinter import messagebox, simpledialog
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
        self.save_results_to_csv()  # Lưu kết quả vào tệp CSV khi thêm trận đấu

    def record_result(self, match, team1_score, team2_score):
        match.record_result(team1_score, team2_score)
        self.save_results_to_csv()  # Lưu kết quả vào tệp CSV khi ghi kết quả
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

        tk.Label(self.admin_frame, text="Quản Lý Đội Bóng", font=("Arial", 16)).grid(row=0, columnspan=4)

        # Nhập tên đội
        tk.Label(self.admin_frame, text="Tên Đội:").grid(row=1, column=0)
        self.team_name_entry = tk.Entry(self.admin_frame)
        self.team_name_entry.grid(row=1, column=1)

        # Nhập tên cầu thủ
        tk.Label(self.admin_frame, text="Tên Cầu Thủ:").grid(row=1, column=2)
        self.player_name_entry = tk.Entry(self.admin_frame)
        self.player_name_entry.grid(row=1, column=3)

        self.add_team_button = tk.Button(self.admin_frame, text="Thêm Đội", command=self.add_team)
        self.add_team_button.grid(row=2, column=0)

        self.remove_team_button = tk.Button(self.admin_frame, text="Xóa Đội", command=self.remove_team)
        self.remove_team_button.grid(row=2, column=1)

        self.add_player_button = tk.Button(self.admin_frame, text="Thêm Cầu Thủ", command=self.add_player)
        self.add_player_button.grid(row=2, column=2)

        self.remove_player_button = tk.Button(self.admin_frame, text="Xóa Cầu Thủ", command=self.remove_player)
        self.remove_player_button.grid(row=2, column=3)

        self.schedule_match_button = tk.Button(self.admin_frame, text="Lên Lịch Trận Đấu", command=self.schedule_match)
        self.schedule_match_button.grid(row=3, column=0, columnspan=4)

        self.view_results_button = tk.Button(self.admin_frame, text="Xem Kết Quả", command=self.view_results)
        self.view_results_button.grid(row=4, column=0, columnspan=4)

        # Tạo một danh sách các trận đấu
        self.matches_listbox = tk.Listbox(self.admin_frame, width=80)
        self.matches_listbox.grid(row=5, columnspan=4)

        self.update_matches_listbox()

    def add_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            team = Team(team_name)
            self.sport_match.add_team(team)
            messagebox.showinfo("Thành Công", f"Đội {team_name} đã được thêm thành công!")
            self.team_name_entry.delete(0, tk.END)
            self.update_matches_listbox()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def remove_team(self):
        team_name = self.team_name_entry.get()
        if team_name:
            team_to_remove = next((team for team in self.sport_match.teams if team.team_name == team_name), None)
            if team_to_remove:
                self.sport_match.remove_team(team_to_remove)
                messagebox.showinfo("Thành Công", f"Đội {team_name} đã được xóa thành công!")
                self.team_name_entry.delete(0, tk.END)
                self.update_matches_listbox()
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đội.")

    def add_player(self):
        player_name = self.player_name_entry.get()
        team_name = self.team_name_entry.get()
        
        if player_name and team_name:
            team = next((team for team in self.sport_match.teams if team.team_name == team_name), None)
            if team:
                # Nhập thông tin cầu thủ
                player_age = simpledialog.askinteger("Nhập Tuổi", "Tuổi của cầu thủ:")
                player_gender = simpledialog.askstring("Nhập Giới Tính", "Giới tính của cầu thủ (Nam/Nữ):")
                player_contact = simpledialog.askstring("Nhập Thông Tin Liên Hệ", "Thông tin liên hệ của cầu thủ:")
                player_number = simpledialog.askinteger("Nhập Số Áo", "Số áo của cầu thủ:")
                player_position = simpledialog.askstring("Nhập Vị Trí", "Vị trí cầu thủ:")
                
                player = Player(player_name, player_age, player_gender, player_contact, player_number, player_position)
                team.add_person(player)
                messagebox.showinfo("Thành Công", f"Cầu thủ {player_name} đã được thêm vào đội {team_name}.")
                self.player_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên cầu thủ và tên đội.")

    def remove_player(self):
        player_name = self.player_name_entry.get()
        team_name = self.team_name_entry.get()
        
        if player_name and team_name:
            team = next((team for team in self.sport_match.teams if team.team_name == team_name), None)
            if team:
                player_to_remove = next((player for player in team.persons if player.name == player_name), None)
                if player_to_remove:
                    team.remove_person(player_to_remove)
                    messagebox.showinfo("Thành Công", f"Cầu thủ {player_name} đã được xóa khỏi đội {team_name}.")
                    self.player_name_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Lỗi", f"Cầu thủ {player_name} không tồn tại trong đội {team_name}.")
            else:
                messagebox.showerror("Lỗi", f"Đội {team_name} không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên cầu thủ và tên đội.")

    def schedule_match(self):
        team1_name = self.team_name_entry.get()
        team2_name = simpledialog.askstring("Nhập Tên Đội 2", "Tên Đội 2:")
        
        if team1_name and team2_name:
            team1 = next((team for team in self.sport_match.teams if team.team_name == team1_name), None)
            team2 = next((team for team in self.sport_match.teams if team.team_name == team2_name), None)

            if team1 and team2:
                match_id = len(self.sport_match.matches) + 1  # Tạo ID cho trận đấu
                referee_name = simpledialog.askstring("Nhập Tên Trọng Tài", "Tên Trọng Tài:")
                match = Match(match_id, team1, team2, referee_name, datetime.now())
                self.sport_match.schedule_match(match)
                messagebox.showinfo("Thành Công", f"Đã lên lịch trận đấu giữa {team1_name} và {team2_name}.")
                self.update_matches_listbox()
            else:
                messagebox.showerror("Lỗi", "Một trong các đội không tồn tại.")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên cả hai đội.")

    def view_results(self):
        results = []
        for match in self.sport_match.matches:
            if match.result:
                results.append(f"Trận {match.match_id}: {match.team1.team_name} {match.result['Score'][match.team1.team_name]} - {match.result['Score'][match.team2.team_name]} {match.team2.team_name}")
        
        if results:
            result_string = "\n".join(results)
            messagebox.showinfo("Kết Quả Trận Đấu", result_string)
        else:
            messagebox.showinfo("Kết Quả Trận Đấu", "Chưa có kết quả nào.")

    def update_matches_listbox(self):
        self.matches_listbox.delete(0, tk.END)  # Xóa danh sách hiện tại
        for match in self.sport_match.matches:
            if match.result:
                self.matches_listbox.insert(tk.END, f"Trận {match.match_id}: {match.team1.team_name} vs {match.team2.team_name}, Kết quả: {match.result['Score'][match.team1.team_name]} - {match.result['Score'][match.team2.team_name]}")
            else:
                self.matches_listbox.insert(tk.END, f"Trận {match.match_id}: {match.team1.team_name} vs {match.team2.team_name}, Chưa có kết quả.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SportMatchApp(root)
    root.mainloop()

