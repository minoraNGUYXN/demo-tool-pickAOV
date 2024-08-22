import pandas as pd

class AOVPickTool:
    def __init__(self, counter_file_path, my_team='blue'):
        self.counter_df = pd.read_excel(counter_file_path)
        self.blue_team = []
        self.red_team = []
        self.my_team = my_team.lower()

    def get_counter(self, hero, exclude_list):
        hero_data = self.counter_df[self.counter_df['Hero'] == hero] # Lấy cột tướng
        if not hero_data.empty:
            for counter_col in ['Counter 3', 'Counter 2', 'Counter 1']: # Thứ tự ưu tiên counter
                counter_hero = hero_data[counter_col].values[0].split(')')[1]
                if counter_hero not in exclude_list: #Ktra tướng đó có trong list BAN hay được PICK ko
                    return counter_hero
        return None

    def ban_hero(self, hero, team):
        if hero in self.blue_team or hero in self.red_team:
            print("Tướng này đã được pick hoặc ban. Hãy chọn tướng khác.")
            return False
        if team == 'blue':
            self.blue_team.append(hero)
        else:
            self.red_team.append(hero)
        return True

    def pick_hero(self, hero, team):
        if hero in self.blue_team or hero in self.red_team:
            print("Tướng này đã được chọn. Hãy chọn tướng khác.")
            return False
        if team == 'blue':
            self.blue_team.append(hero)
        else:
            self.red_team.append(hero)

        exclude_list = self.blue_team + self.red_team #Tướng đã bị ban hoặc pick
        if team != self.my_team:  # Nếu đối thủ pick, gợi ý counter cho đội của người chơi
            counter_hero = self.get_counter(hero, exclude_list)
            print(f"Đội {team} chọn {hero}. Suggested counter: {counter_hero}")
        return True

    def execute(self):
        # BAN phase 1: Mỗi đội ban 2 tướng
        for i in range(1, 3):
            while True:
                if self.my_team == 'blue':
                    ban_hero = input(f"Nhập tướng Ban {i} (đội xanh): ")
                    if self.ban_hero(ban_hero, 'blue'):
                        break
                else:
                    ban_hero = input(f"Nhập tướng Ban {i} (đội đỏ): ")
                    if self.ban_hero(ban_hero, 'red'):
                        break

            while True:
                if self.my_team == 'blue':
                    ban_hero = input(f"Nhập tướng Ban {i} (đội đỏ): ")
                    if self.ban_hero(ban_hero, 'red'):
                        break
                else:
                    ban_hero = input(f"Nhập tướng Ban {i} (đội xanh): ")
                    if self.ban_hero(ban_hero, 'blue'):
                        break

        # PICK phase 1: xanh – đỏ - đỏ - xanh – xanh – đỏ
        pick_sequence = ['blue', 'red', 'red', 'blue', 'blue', 'red']
        for i, team in enumerate(pick_sequence):
            while True:
                hero = input(f"Nhập tướng Pick {i+1} (đội {team}): ")
                if self.pick_hero(hero, team):
                    break

        # BAN phase 2: Mỗi đội tiếp tục ban 2 tướng
        for i in range(3, 5):
            while True:
                if self.my_team == 'blue':
                    ban_hero = input(f"Nhập tướng Ban {i} (đội xanh): ")
                    if self.ban_hero(ban_hero, 'blue'):
                        break
                else:
                    ban_hero = input(f"Nhập tướng Ban {i} (đội đỏ): ")
                    if self.ban_hero(ban_hero, 'red'):
                        break

            while True:
                if self.my_team == 'blue':
                    ban_hero = input(f"Nhập tướng Ban {i} (đội đỏ): ")
                    if self.ban_hero(ban_hero, 'red'):
                        break
                else:
                    ban_hero = input(f"Nhập tướng Ban {i} (đội xanh): ")
                    if self.ban_hero(ban_hero, 'blue'):
                        break

        # PICK phase 2: đỏ - xanh – xanh – đỏ
        pick_sequence = ['red', 'blue', 'blue', 'red']
        for i, team in enumerate(pick_sequence):
            while True:
                hero = input(f"Nhập tướng Pick {i+1} (đội {team}): ")
                if self.pick_hero(hero, team):
                    break

        print("Hoàn thành quá trình BAN/PICK.")

# Đường dẫn đến file counter của bạn
counter_file_path = 'E:\\HocTap\\LTPython\\PickAOV\\demo-tool-pickAOV\\Counter.xlsx'

# Nhập đội của người dùng từ bàn phím
my_team = input("Nhập đội của bạn (red/blue): ").strip().lower()
while my_team not in ['red', 'blue']:
    print("Đội không hợp lệ. Vui lòng nhập lại (red/blue).")
    my_team = input("Nhập đội của bạn (red/blue): ").strip().lower()

# Tạo một instance của tool với đội được nhập từ bàn phím
pick_tool = AOVPickTool(counter_file_path, my_team=my_team)

# Bắt đầu quá trình BAN/PICK
pick_tool.execute()
