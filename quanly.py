import tkinter as tk
from tkinter import messagebox
import csv
import os
import uuid

# Các lớp đã định nghĩa trước đó
class Person:
    def __init__(self, name, age, gender, contact_info):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact_info = contact_info

    def get_details(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact_info": self.contact_info
        }

class Player(Person):
    def __init__(self, name, age, gender, contact_info, player_number, player_position):
        super().__init__(name, age, gender, contact_info)
        self.player_number = player_number
        self.player_position = player_position

    def get_player_info(self):
        return {
            "name": self.name,
            "player_number": self.player_number,
            "player_position": self.player_position
        }

class Coach(Person):
    def __init__(self, name, age, gender, contact_info, coaching_experience, managed_team):
        super().__init__(name, age, gender, contact_info)
        self.coaching_experience = coaching_experience
        self.managed_team = managed_team

    def get_coach_info(self):
        return {
            "name": self.name,
            "coaching_experience": self.coaching_experience,
            "managed_team": self.managed_team
        }

class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.persons = []

    def add_person(self, person):
        if person not in self.persons:
            self.persons.append(person)
        else:
            print(f"{person.name} đã tồn tại trong đội {self.team_name}.")

    def remove_person(self, person):
        if person in self.persons:
            self.persons.remove(person)
        else:
            print(f"{person.name} không tồn tại trong đội {self.team_name}.")

class SportMatch:
    def __init__(self):
        self.team1 = None
        self.team2 = None
        self.match_date = None
        self.result = None

    def schedule_match(self, team1, team2, date):
        self.team1 = team1
        self.team2 = team2
        self.match_date = date

    def record_result(self, team1_score, team2_score):
        self.result = (team1_score, team2_score)

# Hàm kiểm tra xem file CSV đã có tiêu đề hay chưa
def check_and_add_header():
    if not os.path.exists('accounts.csv'):
        with open('accounts.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password', 'Role'])  # Thêm tiêu đề cột
    if not os.path.exists('matches.csv'):
        with open('matches.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Home Team', 'Away Team', 'Refree', 'Stadium', 'Date'])  # Thêm tiêu đề cột
    if not os.path.exists('referees.csv'):
        with open('referees.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Referee'])  # Thêm tiêu đề cột
    if not os.path.exists('stadiums.csv'):
        with open('stadiums.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Stadium'])  # Thêm tiêu đề cột
    if not os.path.exists('teams.csv'):
        with open('teams.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Team Name', 'Coach'])  # Thêm tiêu đề cột

# Hàm lưu thông tin đăng ký vào file CSV
def save_account_to_csv(username, password, role):
    check_and_add_header()  # Đảm bảo rằng file có tiêu đề trước khi ghi dữ liệu
    with open('accounts.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role])  # Lưu thông tin đăng ký

# Hàm kiểm tra tài khoản đăng nhập từ file CSV
def check_login(username, password, role):
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.DictReader(file)  # Đọc file với DictReader để tham chiếu theo tiêu đề cột
            for row in reader:
                if row['Username'] == username and row['Password'] == password and row['Role'] == role:
                    return True
    except FileNotFoundError:
        return False
    return False

# Hàm xử lý đăng ký
def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    role = role_var.get()  # Lấy vai trò từ menu thả xuống

    if username and password and confirm_password and role:
        if password == confirm_password:
            save_account_to_csv(username, password, role)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            login_screen()  # Quay lại màn hình đăng nhập sau khi đăng ký thành công
        else:
            messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp!")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

# Hàm xử lý đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()
    role = role_var.get()

    if check_login(username, password, role):
        messagebox.showinfo("Đăng nhập", f"Đăng nhập thành công với vai trò: {role}")
        if role == 'User':
            user_dashboard()  # Chuyển sang giao diện của User
        elif role == 'Coach':
            coach_dashboard()  # Chuyển sang giao diện của Coach
        elif role == 'Admin':
            admin_dashboard()  # Chuyển sang giao diện của Admin
    else:
        messagebox.showerror("Lỗi", "Tài khoản, mật khẩu hoặc vai trò không đúng!")

# Chuyển sang màn hình đăng ký
def register_screen():
    clear_screen()
    
    lbl_register = tk.Label(window, text="Đăng ký tài khoản", font=("Arial", 16))
    lbl_register.pack(pady=10)
    
    # Nhãn cho tài khoản
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username, entry_password, entry_confirm_password, role_var
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)
    
    # Nhãn cho mật khẩu
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)
    
    # Nhãn cho xác nhận mật khẩu
    lbl_confirm_password = tk.Label(window, text="Xác nhận mật khẩu:")
    lbl_confirm_password.pack()
    entry_confirm_password = tk.Entry(window, width=30, show='*')
    entry_confirm_password.pack(pady=5)

    # Nhãn cho vai trò
    lbl_role = tk.Label(window, text="Chọn vai trò:")
    lbl_role.pack(pady=5)
    role_var = tk.StringVar()
    role_var.set("User")  # Giá trị mặc định
    role_menu = tk.OptionMenu(window, role_var, "User", "Coach", "Admin")  # Thêm Admin vào menu
    role_menu.pack(pady=5)
    
    btn_register = tk.Button(window, text="Đăng ký", command=register)
    btn_register.pack(pady=5)
    
    btn_back = tk.Button(window, text="Quay lại", command=login_screen)
    btn_back.pack(pady=5)

# Chuyển sang màn hình đăng nhập
def login_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Hệ thống quản lý bóng đá", font=("Arial", 18), fg="blue")
    lbl_title.pack(pady=10)

    lbl_login = tk.Label(window, text="Đăng nhập", font=("Arial", 16))
    lbl_login.pack(pady=10)
    
    # Nhãn cho tài khoản
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username, entry_password
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)
    
    # Nhãn cho mật khẩu
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)

    # Nhãn cho vai trò
    lbl_role = tk.Label(window, text="Chọn vai trò:")
    lbl_role.pack(pady=5)
    global role_var
    role_var = tk.StringVar()
    role_var.set("User")  # Giá trị mặc định
    role_menu = tk.OptionMenu(window, role_var, "User", "Coach", "Admin")  # Thêm Admin vào menu
    role_menu.pack(pady=5)

    btn_login = tk.Button(window, text="Đăng nhập", command=login)
    btn_login.pack(pady=5)
    
    btn_register = tk.Button(window, text="Đăng ký", command=register_screen)
    btn_register.pack(pady=5)

# Giao diện quản lý User
def user_dashboard():
    clear_screen()
    lbl_user = tk.Label(window, text="Giao diện User", font=("Arial", 16))
    lbl_user.pack(pady=10)

    btn_view_teams = tk.Button(window, text="Xem đội bóng", command=view_teams)
    btn_view_teams.pack(pady=5)

    btn_view_schedule = tk.Button(window, text="Xem lịch thi đấu", command=view_schedule)
    btn_view_schedule.pack(pady=5)

    btn_view_results = tk.Button(window, text="Xem kết quả trận đấu", command=view_results)
    btn_view_results.pack(pady=5)
    
    btn_logout = tk.Button(window, text="Đăng xuất", command=login_screen)
    btn_logout.pack(pady=5)

# Giao diện quản lý Coach
def coach_dashboard():
    clear_screen()
    lbl_coach = tk.Label(window, text="Giao diện Coach", font=("Arial", 16))
    lbl_coach.pack(pady=10)

    btn_manage_team = tk.Button(window, text="Quản lý đội bóng", command=manage_teams)
    btn_manage_team.pack(pady=5)

    btn_view_schedule = tk.Button(window, text="Xem lịch thi đấu", command=view_schedule)
    btn_view_schedule.pack(pady=5)

    btn_view_results = tk.Button(window, text="Xem kết quả trận đấu", command=view_results)
    btn_view_results.pack(pady=5)


    btn_logout = tk.Button(window, text="Đăng xuất", command=login_screen)
    btn_logout.pack(pady=5)

def admin_dashboard():
    clear_screen()
    
    lbl_admin_dashboard = tk.Label(window, text="Bảng điều khiển Admin", font=("Arial", 16))
    lbl_admin_dashboard.pack(pady=10)

    btn_manage_teams = tk.Button(window, text="Quản lý đội bóng", command=manage_teams)
    btn_manage_teams.pack(pady=5)

    btn_manage_referees = tk.Button(window, text="Quản lý trọng tài", command=manage_referees)
    btn_manage_referees.pack(pady=5)

    btn_manage_stadiums = tk.Button(window, text="Quản lý sân thi đấu", command=manage_stadiums)
    btn_manage_stadiums.pack(pady=5)

    btn_manage_schedule = tk.Button(window, text="Quản lý lịch thi đấu", command=manage_schedule)
    btn_manage_schedule.pack(pady=5)

    lbl_manage_users = tk.Button(window, text="Quản lý người dùng", command=manage_users)
    lbl_manage_users.pack(pady=5)

    btn_update_result = tk.Button(window, text="Cập nhật kết quả", command=update_result_window)
    btn_update_result.pack(pady=5) 

    btn_logout = tk.Button(window, text="Đăng xuất", command=login_screen)
    btn_logout.pack(pady=5)



# Các hàm chức năng cho Admin
def manage_users():
    messagebox.showinfo("Quản lý người dùng", "Quản lý thông tin người dùng...")

def manage_teams():
    messagebox.showinfo("Quản lý đội bóng", "Quản lý thông tin đội bóng...")

def manage_schedules():
    messagebox.showinfo("Quản lý lịch thi đấu", "Quản lý lịch thi đấu...")

def manage_referees():
    messagebox.showinfo("Quản lý trọng tài", "Quản lý trọng tài...")

def manage_stadiums():
    messagebox.showinfo("Quản lý sân thi đấu", "Quản lý sân thi đấu...")  

def update_result():
    messagebox.showinfo("Cập Nhật Kết Quả ", "Cập Nhật Kết Quả...")  

# Hàm để xóa màn hình
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()
# Giao diện quản lý trọng tài
def manage_referees():
    clear_screen()
    check_and_add_header()
    lbl_manage_referees = tk.Label(window, text="Quản lý trọng tài", font=("Arial", 16))
    lbl_manage_referees.pack(pady=10)

    btn_view_referees = tk.Button(window, text="Xem danh sách trọng tài", command=view_referees)
    btn_view_referees.pack(pady=5)

    btn_add_referee = tk.Button(window, text="Thêm trọng tài", command=add_referee)
    btn_add_referee.pack(pady=5)

    btn_delete_referee = tk.Button(window, text="Xóa trọng tài", command=delete_referee)
    btn_delete_referee.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

def view_referees():
    try:
        with open('referees.csv', 'r') as file:
            reader = csv.reader(file)
            referees = [row[0] for row in reader]
            referee_list = "\n".join(referees[1:])  # Bỏ qua tiêu đề
            messagebox.showinfo("Danh sách trọng tài", referee_list or "Không có trọng tài nào!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa trọng tài.")

def add_referee():
    clear_screen()
    
    lbl_add_referee = tk.Label(window, text="Thêm trọng tài mới", font=("Arial", 16))
    lbl_add_referee.pack(pady=10)
    
    lbl_referee_name = tk.Label(window, text="Tên trọng tài:")
    lbl_referee_name.pack()
    entry_new_referee_name = tk.Entry(window, width=30)
    entry_new_referee_name.pack(pady=5)

    btn_save_referee = tk.Button(window, text="Lưu trọng tài", command=lambda: save_new_referee(entry_new_referee_name.get()))
    btn_save_referee.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_referees)
    btn_back.pack(pady=5)

def save_new_referee(referee_name):
    if referee_name:
        with open('referees.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([referee_name])  # Lưu thông tin trọng tài
        messagebox.showinfo("Thành công", "Thêm trọng tài thành công!")
        manage_referees()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập tên trọng tài!")

def delete_referee():
    clear_screen()
    
    lbl_delete_referee = tk.Label(window, text="Xóa trọng tài", font=("Arial", 16))
    lbl_delete_referee.pack(pady=10)

    lbl_referee_name = tk.Label(window, text="Tên trọng tài cần xóa:")
    lbl_referee_name.pack()
    entry_delete_referee_name = tk.Entry(window, width=30)
    entry_delete_referee_name.pack(pady=5)

    btn_confirm_delete = tk.Button(window, text="Xóa trọng tài", command=lambda: confirm_delete_referee(entry_delete_referee_name.get()))
    btn_confirm_delete.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_referees)
    btn_back.pack(pady=5)

def confirm_delete_referee(referee_name):
    referees = []
    deleted = False
    try:
        with open('referees.csv', 'r') as file:
            reader = csv.reader(file)
            referees = [row[0] for row in reader]
            if referee_name in referees:
                referees.remove(referee_name)  # Xóa trọng tài
                deleted = True
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa trọng tài.")

    if deleted:
        with open('referees.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for referee in referees:
                writer.writerow([referee])  # Ghi lại danh sách trọng tài còn lại
        messagebox.showinfo("Thành công", "Xóa trọng tài thành công!")
    else:
        messagebox.showwarning("Lỗi", "Trọng tài không tồn tại!")

    manage_referees()
# Giao diện quản lý sân thi đấu
def manage_stadiums():
    clear_screen()
    check_and_add_header()
    lbl_manage_stadiums = tk.Label(window, text="Quản lý sân thi đấu", font=("Arial", 16))
    lbl_manage_stadiums.pack(pady=10)

    btn_view_stadiums = tk.Button(window, text="Xem danh sách sân", command=view_stadiums)
    btn_view_stadiums.pack(pady=5)

    btn_add_stadium = tk.Button(window, text="Thêm sân thi đấu", command=add_stadium)
    btn_add_stadium.pack(pady=5)

    btn_delete_stadium = tk.Button(window, text="Xóa sân thi đấu", command=delete_stadium)
    btn_delete_stadium.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

def view_stadiums():
    try:
        with open('stadiums.csv', 'r') as file:
            reader = csv.reader(file)
            stadiums = [row[0] for row in reader]
            stadium_list = "\n".join(stadiums[1:])  # Bỏ qua tiêu đề
            messagebox.showinfo("Danh sách sân thi đấu", stadium_list or "Không có sân nào!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa sân thi đấu.")

def add_stadium():
    clear_screen()
    
    lbl_add_stadium = tk.Label(window, text="Thêm sân thi đấu mới", font=("Arial", 16))
    lbl_add_stadium.pack(pady=10)
    
    lbl_stadium_name = tk.Label(window, text="Tên sân thi đấu:")
    lbl_stadium_name.pack()
    entry_new_stadium_name = tk.Entry(window, width=30)
    entry_new_stadium_name.pack(pady=5)

    btn_save_stadium = tk.Button(window, text="Lưu sân thi đấu", command=lambda: save_new_stadium(entry_new_stadium_name.get()))
    btn_save_stadium.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_stadiums)
    btn_back.pack(pady=5)

def save_new_stadium(stadium_name):
    if stadium_name:
        with open('stadiums.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([stadium_name])  # Lưu thông tin sân thi đấu
        messagebox.showinfo("Thành công", "Thêm sân thi đấu thành công!")
        manage_stadiums()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập tên sân thi đấu!")

def delete_stadium():
    clear_screen()
    
    lbl_delete_stadium = tk.Label(window, text="Xóa sân thi đấu", font=("Arial", 16))
    lbl_delete_stadium.pack(pady=10)

    lbl_stadium_name = tk.Label(window, text="Tên sân thi đấu cần xóa:")
    lbl_stadium_name.pack()
    entry_delete_stadium_name = tk.Entry(window, width=30)
    entry_delete_stadium_name.pack(pady=5)

    btn_confirm_delete = tk.Button(window, text="Xóa sân thi đấu", command=lambda: confirm_delete_stadium(entry_delete_stadium_name.get()))
    btn_confirm_delete.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_stadiums)
    btn_back.pack(pady=5)


def confirm_delete_stadium(stadium_name):
    stadiums = []
    deleted = False
    
    try:
        with open('stadiums.csv', 'r') as file:
            reader = csv.reader(file)
            stadiums = [row[0] for row in reader]
            if stadium_name in stadiums:
                stadiums.remove(stadium_name)  # Xóa sân
                deleted = True
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa sân thi đấu.")

    if deleted:
        # Ghi lại danh sách sân còn lại vào file CSV
        with open('stadiums.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for stadium in stadiums:
                writer.writerow([stadium])  # Ghi lại danh sách sân còn lại
        messagebox.showinfo("Thành công", "Xóa sân thi đấu thành công!")
    else:
        messagebox.showwarning("Lỗi", "Sân thi đấu không tồn tại!")

    manage_stadiums()  # Quay lại màn hình quản lý sân thi đấu




# Giao diện quản lý người dùng
def manage_users():
    clear_screen()
    check_and_add_header()
    lbl_manage_users = tk.Label(window, text="Quản lý người dùng", font=("Arial", 16))
    lbl_manage_users.pack(pady=10)

    btn_view_users = tk.Button(window, text="Xem danh sách người dùng", command=view_users)
    btn_view_users.pack(pady=5)

    btn_add_user = tk.Button(window, text="Thêm người dùng", command=add_user)
    btn_add_user.pack(pady=5)

    btn_edit_user = tk.Button(window, text="Chỉnh sửa người dùng", command=edit_user)
    btn_edit_user.pack(pady=5)

    btn_delete_user = tk.Button(window, text="Xóa người dùng", command=delete_user)
    btn_delete_user.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

# Hàm xem danh sách người dùng
def view_users():
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.DictReader(file)
            users = [f"{row['Username']} - {row['Role']}" for row in reader]
            user_list = "\n".join(users)
            messagebox.showinfo("Danh sách người dùng", user_list or "Không có người dùng nào!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa người dùng.")

# Hàm thêm người dùng
def add_user():
    # Tạo giao diện để thêm người dùng mới
    clear_screen()
    
    lbl_add_user = tk.Label(window, text="Thêm người dùng mới", font=("Arial", 16))
    lbl_add_user.pack(pady=10)
    
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    entry_new_username = tk.Entry(window, width=30)
    entry_new_username.pack(pady=5)

    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_new_password = tk.Entry(window, width=30, show='*')
    entry_new_password.pack(pady=5)

    lbl_role = tk.Label(window, text="Chọn vai trò:")
    lbl_role.pack(pady=5)
    new_role_var = tk.StringVar()
    new_role_var.set("User")  # Giá trị mặc định
    new_role_menu = tk.OptionMenu(window, new_role_var, "User", "Coach", "Admin")
    new_role_menu.pack(pady=5)

    btn_save = tk.Button(window, text="Lưu người dùng", command=lambda: save_new_user(entry_new_username.get(), entry_new_password.get(), new_role_var.get()))
    btn_save.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_users)
    btn_back.pack(pady=5)

# Hàm lưu người dùng mới vào file CSV
def save_new_user(username, password, role):
    if username and password:
        save_account_to_csv(username, password, role)
        messagebox.showinfo("Thành công", "Thêm người dùng thành công!")
        manage_users()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

# Hàm chỉnh sửa người dùng
def edit_user():
    # Tạo giao diện để chỉnh sửa thông tin người dùng
    clear_screen()
    
    lbl_edit_user = tk.Label(window, text="Chỉnh sửa người dùng", font=("Arial", 16))
    lbl_edit_user.pack(pady=10)
    
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    entry_edit_username = tk.Entry(window, width=30)
    entry_edit_username.pack(pady=5)

    lbl_new_password = tk.Label(window, text="Mật khẩu mới:")
    lbl_new_password.pack()
    entry_new_password = tk.Entry(window, width=30, show='*')
    entry_new_password.pack(pady=5)

    btn_save_changes = tk.Button(window, text="Lưu thay đổi", command=lambda: save_edited_user(entry_edit_username.get(), entry_new_password.get()))
    btn_save_changes.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_users)
    btn_back.pack(pady=5)

# Hàm lưu thông tin người dùng đã chỉnh sửa
def save_edited_user(username, new_password):
    # Đọc tất cả người dùng từ file CSV
    users = []
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    row['Password'] = new_password  # Cập nhật mật khẩu mới
                users.append(row)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa người dùng.")
        return

    # Ghi lại thông tin người dùng vào file CSV
    with open('accounts.csv', 'w', newline='') as file:
        fieldnames = ['Username', 'Password', 'Role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)
    
    messagebox.showinfo("Thành công", "Cập nhật thông tin người dùng thành công!")
    manage_users()

# Hàm xóa người dùng
def delete_user():
    # Tạo giao diện để xóa người dùng
    clear_screen()
    
    lbl_delete_user = tk.Label(window, text="Xóa người dùng", font=("Arial", 16))
    lbl_delete_user.pack(pady=10)

    lbl_username = tk.Label(window, text="Tài khoản cần xóa:")
    lbl_username.pack()
    entry_delete_username = tk.Entry(window, width=30)
    entry_delete_username.pack(pady=5)

    btn_confirm_delete = tk.Button(window, text="Xóa người dùng", command=lambda: confirm_delete(entry_delete_username.get()))
    btn_confirm_delete.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_users)
    btn_back.pack(pady=5)

# Hàm xác nhận xóa người dùng
def confirm_delete(username):
    users = []
    deleted = False
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    deleted = True  # Đánh dấu người dùng đã xóa
                else:
                    users.append(row)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa người dùng.")
        return

    # Ghi lại thông tin người dùng còn lại vào file CSV
    with open('accounts.csv', 'w', newline='') as file:
        fieldnames = ['Username', 'Password', 'Role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

    if deleted:
        messagebox.showinfo("Thành công", "Xóa người dùng thành công!")
    else:
        messagebox.showwarning("Lỗi", "Người dùng không tồn tại!")

    manage_users()



# Giao diện quản lý đội bóng
def manage_teams():
    clear_screen()
    check_and_add_header()
    lbl_manage_teams = tk.Label(window, text="Quản lý đội bóng", font=("Arial", 16))
    lbl_manage_teams.pack(pady=10)

    btn_view_teams = tk.Button(window, text="Xem danh sách đội bóng", command=view_teams)
    btn_view_teams.pack(pady=5)

    btn_add_team = tk.Button(window, text="Thêm đội bóng", command=add_team)
    btn_add_team.pack(pady=5)

    btn_edit_team = tk.Button(window, text="Chỉnh sửa đội bóng", command=edit_team)
    btn_edit_team.pack(pady=5)

    btn_delete_team = tk.Button(window, text="Xóa đội bóng", command=delete_team)
    btn_delete_team.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

# Hàm xem danh sách đội bóng
def view_teams():
    try:
        with open('teams.csv', 'r') as file:
            reader = csv.DictReader(file)
            teams = [f"{row['Team Name']} - {row['Coach']}" for row in reader]
            team_list = "\n".join(teams)
            messagebox.showinfo("Danh sách đội bóng", team_list or "Không có đội bóng nào!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa đội bóng.")
    except KeyError as e:
        messagebox.showerror("Lỗi", f"Khóa không hợp lệ: {str(e)}. Vui lòng kiểm tra file CSV.")

# Hàm thêm đội bóng
def add_team():
    clear_screen()
    
    lbl_add_team = tk.Label(window, text="Thêm đội bóng mới", font=("Arial", 16))
    lbl_add_team.pack(pady=10)
    
    lbl_team_name = tk.Label(window, text="Tên đội:")
    lbl_team_name.pack()
    entry_new_team_name = tk.Entry(window, width=30)
    entry_new_team_name.pack(pady=5)

    lbl_coach_name = tk.Label(window, text="Tên huấn luyện viên:")
    lbl_coach_name.pack()
    entry_coach_name = tk.Entry(window, width=30)
    entry_coach_name.pack(pady=5)

    btn_save_team = tk.Button(window, text="Lưu đội bóng", command=lambda: save_new_team(entry_new_team_name.get(), entry_coach_name.get()))
    btn_save_team.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_teams)
    btn_back.pack(pady=5)

# Hàm lưu đội bóng mới vào file CSV
def save_new_team(team_name, coach_name):
    if team_name and coach_name:
        file_exists = os.path.isfile('teams.csv')  # Kiểm tra xem file đã tồn tại chưa
        with open('teams.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Team Name', 'Coach'])  # Ghi tiêu đề vào file nếu chưa tồn tại
            writer.writerow([team_name, coach_name])  # Lưu thông tin đội bóng
        messagebox.showinfo("Thành công", "Thêm đội bóng thành công!")
        manage_teams()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

# Hàm chỉnh sửa đội bóng
def edit_team():
    clear_screen()
    
    lbl_edit_team = tk.Label(window, text="Chỉnh sửa đội bóng", font=("Arial", 16))
    lbl_edit_team.pack(pady=10)
    
    lbl_team_name = tk.Label(window, text="Tên đội cần chỉnh sửa:")
    lbl_team_name.pack()
    entry_edit_team_name = tk.Entry(window, width=30)
    entry_edit_team_name.pack(pady=5)

    lbl_new_coach_name = tk.Label(window, text="Tên huấn luyện viên mới:")
    lbl_new_coach_name.pack()
    entry_new_coach_name = tk.Entry(window, width=30)
    entry_new_coach_name.pack(pady=5)

    btn_save_changes = tk.Button(window, text="Lưu thay đổi", command=lambda: save_edited_team(entry_edit_team_name.get(), entry_new_coach_name.get()))
    btn_save_changes.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_teams)
    btn_back.pack(pady=5)

# Hàm lưu thông tin đội bóng đã chỉnh sửa
def save_edited_team(team_name, new_coach_name):
    teams = []
    try:
        with open('teams.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Team Name'] == team_name:
                    row['Coach'] = new_coach_name  # Cập nhật tên huấn luyện viên mới
                teams.append(row)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa đội bóng.")
        return

    # Ghi lại thông tin đội bóng vào file CSV
    with open('teams.csv', 'w', newline='') as file:
        fieldnames = ['Team Name', 'Coach']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Ghi tiêu đề vào file
        writer.writerows(teams)
    
    messagebox.showinfo("Thành công", "Cập nhật thông tin đội bóng thành công!")
    manage_teams()

# Hàm xóa đội bóng
def delete_team():
    clear_screen()
    
    lbl_delete_team = tk.Label(window, text="Xóa đội bóng", font=("Arial", 16))
    lbl_delete_team.pack(pady=10)

    lbl_team_name = tk.Label(window, text="Tên đội cần xóa:")
    lbl_team_name.pack()
    entry_delete_team_name = tk.Entry(window, width=30)
    entry_delete_team_name.pack(pady=5)

    btn_confirm_delete = tk.Button(window, text="Xóa đội bóng", command=lambda: confirm_delete_team(entry_delete_team_name.get()))
    btn_confirm_delete.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_teams)
    btn_back.pack(pady=5)

# Hàm xác nhận xóa đội bóng
def confirm_delete_team(team_name):
    teams = []
    team_found = False  # Biến để kiểm tra xem đội bóng có tồn tại hay không
    try:
        with open('teams.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Team Name'] != team_name:
                    teams.append(row)
                else:
                    team_found = True  # Đánh dấu là tìm thấy đội bóng
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa đội bóng.")
        return

    if team_found:
        # Ghi lại thông tin đội bóng vào file CSV
        with open('teams.csv', 'w', newline='') as file:
            fieldnames = ['Team Name', 'Coach']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Ghi tiêu đề vào file
            writer.writerows(teams)
        
        messagebox.showinfo("Thành công", "Đã xóa đội bóng thành công!")
    else:
        messagebox.showwarning("Lỗi", "Đội bóng không tồn tại trong danh sách.")

    manage_teams()
# Hàm xóa màn hình
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()


# Giao diện quản lý lịch thi đấu
def manage_schedule():
    clear_screen()
    check_and_add_header()
    lbl_manage_schedule = tk.Label(window, text="Quản lý lịch thi đấu", font=("Arial", 16))
    lbl_manage_schedule.pack(pady=10)

    btn_view_schedule = tk.Button(window, text="Xem lịch thi đấu", command=view_schedule)
    btn_view_schedule.pack(pady=5)

    btn_add_match = tk.Button(window, text="Thêm trận đấu", command=add_match)
    btn_add_match.pack(pady=5)

    btn_delete_match = tk.Button(window, text="Xóa trận đấu", command=delete_match)
    btn_delete_match.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

# Hàm xem lịch thi đấu
def view_schedule():
    try:
        with open('matches.csv', 'r') as file:
            reader = csv.DictReader(file)
            matches = [f"ID: {row['Match ID']} - {row['Date']} - {row['Home Team']} vs {row['Away Team']}\nTrọng tài: {row['Referee']} - Sân: {row['Stadium']}\nTỷ số: {row['Team 1 Score']} - {row['Team 2 Score']}" for row in reader]
            match_list = "\n\n".join(matches)
            messagebox.showinfo("Danh sách trận đấu", match_list or "Không có trận đấu nào!")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa lịch thi đấu.")


def add_match():
    clear_screen()
    
    lbl_add_match = tk.Label(window, text="Thêm trận đấu", font=("Arial", 16))
    lbl_add_match.pack(pady=10)

    lbl_team1 = tk.Label(window, text="Chọn đội 1:")
    lbl_team1.pack()
    # Giả sử bạn có một hàm get_team_names() để lấy danh sách đội bóng
    team1_var = tk.StringVar()
    team1_dropdown = tk.OptionMenu(window, team1_var, *get_team_names())
    team1_dropdown.pack(pady=5)

    lbl_team2 = tk.Label(window, text="Chọn đội 2:")
    lbl_team2.pack()
    team2_var = tk.StringVar()
    team2_dropdown = tk.OptionMenu(window, team2_var, *get_team_names())
    team2_dropdown.pack(pady=5)

    lbl_referee = tk.Label(window, text="Chọn trọng tài:")
    lbl_referee.pack()
    referee_var = tk.StringVar()
    referee_dropdown = tk.OptionMenu(window, referee_var, *get_referee_names())  # Hàm lấy danh sách trọng tài
    referee_dropdown.pack(pady=5)

    lbl_stadium = tk.Label(window, text="Chọn sân thi đấu:")
    lbl_stadium.pack()
    stadium_var = tk.StringVar()
    stadium_dropdown = tk.OptionMenu(window, stadium_var, *get_stadium_names())  # Hàm lấy danh sách sân thi đấu
    stadium_dropdown.pack(pady=5)

    lbl_date_time = tk.Label(window, text="Ngày và giờ thi đấu:")
    lbl_date_time.pack()
    entry_date_time = tk.Entry(window, width=30)
    entry_date_time.pack(pady=5)

    btn_save_match = tk.Button(window, text="Lưu trận đấu", command=lambda: save_new_match(team1_var.get(), team2_var.get(), referee_var.get(), stadium_var.get(), entry_date_time.get()))
    btn_save_match.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_schedule)  # Quay lại quản lý lịch thi đấu
    btn_back.pack(pady=5)

def generate_match_id():
    try:
        with open('matches.csv', 'r') as file:
            reader = csv.reader(file)
            ids = [int(row[0]) for row in reader if row[0].isdigit()]  # Lấy danh sách các ID trận đấu
            return max(ids) + 1 if ids else 1  # Trả về ID tiếp theo, hoặc 1 nếu không có trận đấu nào
    except FileNotFoundError:
        return 1  # Trả về 1 nếu file chưa tồn tại

def save_new_match(team1, team2, referee, stadium, date_time):
    if team1 and team2 and referee and stadium and date_time:
        match_id = generate_match_id()  # Gọi hàm để tạo ID ngắn

        with open('matches.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([match_id, team1, team2, referee, stadium, date_time, "", ""])  # Kết quả ban đầu để trống
        messagebox.showinfo("Thành công", f"Thêm trận đấu thành công! ID trận đấu: {match_id}")
        manage_schedule()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

def get_team_names():
    teams = []
    try:
        with open('teams.csv', 'r') as file:
            reader = csv.reader(file)
            teams = [row[0] for row in reader]
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa đội bóng.")
    return teams[1:]  # Bỏ qua tiêu đề

def get_referee_names():
    referees = []
    try:
        with open('referees.csv', 'r') as file:
            reader = csv.reader(file)
            referees = [row[0] for row in reader]
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa trọng tài.")
    return referees[1:]  # Bỏ qua tiêu đề

def get_stadium_names():
    stadiums = []
    try:
        with open('stadiums.csv', 'r') as file:
            reader = csv.reader(file)
            stadiums = [row[0] for row in reader]
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa sân thi đấu.")
    return stadiums[1:]  # Bỏ qua tiêu đề


# Hàm xóa trận đấu
def delete_match():
    clear_screen()
    
    lbl_delete_match = tk.Label(window, text="Xóa trận đấu", font=("Arial", 16))
    lbl_delete_match.pack(pady=10)

    lbl_match_info = tk.Label(window, text="Nhập thông tin trận đấu (ngày, đội nhà vs đội khách):")
    lbl_match_info.pack()

    entry_match_info = tk.Entry(window, width=30)
    entry_match_info.pack(pady=5)

    btn_confirm_delete = tk.Button(window, text="Xóa trận đấu", command=lambda: confirm_delete_match(entry_match_info.get()))
    btn_confirm_delete.pack(pady=5)

    btn_back = tk.Button(window, text="Quay lại", command=manage_schedule)
    btn_back.pack(pady=5)

# Hàm xác nhận xóa trận đấu
def confirm_delete_match(match_info):
    date, teams = match_info.split(" - ")
    home_team, away_team = teams.split(" vs ")

    matches = []
    match_found = False
    try:
        with open('matches.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'] == date and row['Home Team'] == home_team and row['Away Team'] == away_team:
                    match_found = True  # Đánh dấu là tìm thấy trận đấu
                else:
                    matches.append(row)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa lịch thi đấu.")
        return

    if match_found:
        # Ghi lại thông tin trận đấu vào file CSV
        with open('matches.csv', 'w', newline='') as file:
            fieldnames = ['Date', 'Home Team', 'Away Team']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Ghi tiêu đề vào file
            writer.writerows(matches)
        
        messagebox.showinfo("Thành công", "Đã xóa trận đấu thành công!")
    else:
        messagebox.showwarning("Lỗi", "Trận đấu không tồn tại trong danh sách.")

    manage_schedule()

# Giao diện để cập nhật kết quả trận đấu
def update_result_window():
    clear_screen()

    lbl_update_result = tk.Label(window, text="Cập nhật kết quả trận đấu", font=("Arial", 16))
    lbl_update_result.pack(pady=10)

    lbl_match_id = tk.Label(window, text="Nhập ID trận đấu:")
    lbl_match_id.pack()

    entry_match_id = tk.Entry(window, width=30)
    entry_match_id.pack(pady=5)

    lbl_team1_score = tk.Label(window, text="Tỷ số đội nhà:")
    lbl_team1_score.pack()
    entry_team1_score = tk.Entry(window, width=10)
    entry_team1_score.pack(pady=5)

    lbl_team2_score = tk.Label(window, text="Tỷ số đội khách:")
    lbl_team2_score.pack()
    entry_team2_score = tk.Entry(window, width=10)
    entry_team2_score.pack(pady=5)

    btn_update_result = tk.Button(window, text="Cập nhật kết quả", command=lambda: save_match_result(entry_match_id.get(), entry_team1_score.get(), entry_team2_score.get()))
    btn_update_result.pack(pady=10)

    btn_back = tk.Button(window, text="Quay lại", command=admin_dashboard)
    btn_back.pack(pady=5)

# Hàm lưu kết quả vào file CSV dựa trên ID
def save_match_result(match_id, team1_score, team2_score):
    if not match_id or not team1_score or not team2_score:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    matches = []
    match_found = False

    # Đọc thông tin từ file CSV và tìm trận đấu cần cập nhật dựa trên ID ngắn
    try:
        with open('matches.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Match ID'] == match_id:  # So khớp ID trận đấu
                    row['Team 1 Score'] = team1_score
                    row['Team 2 Score'] = team2_score
                    match_found = True  # Đánh dấu là đã tìm thấy và cập nhật kết quả
                matches.append(row)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file chứa lịch thi đấu.")
        return

    if match_found:
        # Ghi lại tất cả các trận đấu vào file CSV (bao gồm trận đã cập nhật)
        with open('matches.csv', 'w', newline='') as file:
            fieldnames = ['Match ID', 'Home Team', 'Away Team', 'Referee', 'Stadium', 'Date', 'Team 1 Score', 'Team 2 Score']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matches)
        
        messagebox.showinfo("Thành công", "Kết quả trận đấu đã được cập nhật!")
    else:
        messagebox.showwarning("Lỗi", "Không tìm thấy trận đấu với ID này.")

    manage_schedule()



# Khởi tạo giao diện chính
window = tk.Tk()
window.title("Hệ thống quản lý bóng đá")
window.geometry("300x400")

# Hiển thị màn hình đăng nhập đầu tiên
login_screen()

window.mainloop()



