import tkinter as tk
from tkinter import messagebox
import pandas as pd

class AOVPickTool:
    def __init__(self, counter_file_path):
        self.counter_df = pd.read_excel(counter_file_path)
        self.blue_team = []
        self.red_team = []
        self.banned_heroes = []
        self.my_team = None  # Sẽ được thiết lập sau

    def set_my_team(self, team):
        self.my_team = team.lower()

    def get_counter(self, hero, exclude_list):
        hero_data = self.counter_df[self.counter_df['Hero'] == hero]
        if not hero_data.empty:
            for counter_col in ['Counter 3', 'Counter 2', 'Counter 1']:
                counter_hero = hero_data[counter_col].values[0].split(')')[1]
                if counter_hero not in exclude_list:
                    return counter_hero
        return "Không có tướng counter khả dụng."

    def ban_hero(self, hero, team):
        if hero in self.blue_team or hero in self.red_team or hero in self.banned_heroes:
            messagebox.showerror("Lỗi", "Tướng này đã được chọn hoặc bị cấm!")
            return False
        self.banned_heroes.append(hero)
        return True

    def pick_hero(self, hero, team):
        if hero in self.blue_team or hero in self.red_team or hero in self.banned_heroes:
            messagebox.showerror("Lỗi", "Tướng này đã được chọn hoặc bị cấm!")
            return False
        if team == 'blue':
            self.blue_team.append(hero)
        else:
            self.red_team.append(hero)

        exclude_list = self.blue_team + self.red_team + self.banned_heroes
        # Đề xuất tướng counter cho đội đối thủ
        if team != self.my_team:
            counter_hero = self.get_counter(hero, exclude_list)
            return counter_hero
        return None

def create_interface():
    tool = AOVPickTool(counter_file_path='Counter.xlsx')

    def set_team():
        team = my_team_entry.get()
        if team.lower() not in ['blue', 'red']:
            messagebox.showerror("Lỗi", "Vui lòng nhập 'Blue' hoặc 'Red'.")
            return
        tool.set_my_team(team)
        update_display()

    def ban_hero():
        hero = ban_entry.get()
        team = team_var.get().lower()
        if hero and tool.ban_hero(hero, team):
            update_display()

    def pick_hero():
        hero = hero_entry.get()
        team = team_var.get().lower()
        if hero:
            counter_hero = tool.pick_hero(hero, team)
            if counter_hero:
                counter_label.config(text=f"Gợi ý tướng counter: {counter_hero}")
            update_display()

    def update_display():
        blue_picks_label.config(text="Tướng đội Xanh: " + ", ".join(tool.blue_team))
        red_picks_label.config(text="Tướng đội Đỏ: " + ", ".join(tool.red_team))
        bans_label.config(text="Tướng bị cấm: " + ", ".join(tool.banned_heroes))

    # Thiết lập cửa sổ tkinter
    window = tk.Tk()
    window.title("Công Cụ Chọn Tướng AOV")

    # Nhập đội của người chơi
    tk.Label(window, text="Nhập đội của bạn (Blue/Red):").grid(row=0, column=0, padx=10, pady=10)
    my_team_entry = tk.Entry(window)
    my_team_entry.grid(row=0, column=1, columnspan=2)
    tk.Button(window, text="Xác nhận đội", command=set_team).grid(row=0, column=3, padx=10, pady=10)

    # Chọn đội cho việc cấm và chọn tướng
    team_var = tk.StringVar(value='Red')
    tk.Label(window, text="Chọn đội để cấm/chọn tướng:").grid(row=1, column=0, padx=10, pady=10)
    tk.Radiobutton(window, text="Xanh", variable=team_var, value="Blue").grid(row=1, column=1)
    tk.Radiobutton(window, text="Đỏ", variable=team_var, value="Red").grid(row=1, column=2)

    # Nhập tướng để cấm
    tk.Label(window, text="Nhập tướng để cấm:").grid(row=2, column=0, padx=10, pady=10)
    ban_entry = tk.Entry(window)
    ban_entry.grid(row=2, column=1, columnspan=2)
    tk.Button(window, text="Cấm tướng", command=ban_hero).grid(row=2, column=3, padx=10, pady=10)

    # Nhập tướng đối thủ đã chọn
    tk.Label(window, text="Nhập tướng để chọn:").grid(row=3, column=0, padx=10, pady=10)
    hero_entry = tk.Entry(window)
    hero_entry.grid(row=3, column=1, columnspan=2)
    tk.Button(window, text="Chọn tướng", command=pick_hero).grid(row=3, column=3, padx=10, pady=10)

    # Hiển thị thông tin
    blue_picks_label = tk.Label(window, text="Tướng đội Xanh: ")
    blue_picks_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    red_picks_label = tk.Label(window, text="Tướng đội Đỏ: ")
    red_picks_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    bans_label = tk.Label(window, text="Tướng bị cấm: ")
    bans_label.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

    # Hiển thị gợi ý counter
    counter_label = tk.Label(window, text="Gợi ý tướng counter: ")
    counter_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    # Khởi động vòng lặp tkinter
    window.mainloop()

if __name__ == "__main__":
    create_interface()
