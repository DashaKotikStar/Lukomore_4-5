# player_logic.py
import random

class PlayerLogic:
    def __init__(self, name="Игрок"):
        self.name = name
        self.position = 1  # текущая клетка (1–13), None если между
        self.bon = 0
        self.inventory = [None, None, None]
        self.skip_turn = False
        self.in_mini_game = False
        self.needs_extra_roll = False
        self.current_path_index = 0  # индекс текущего белого кружка
        self.path_points = []        # [(x, y, cell_num), ...]
        self.load_path_points()

    def load_path_points(self):
        """Загружает путь из файла path_points.txt"""
        try:
            with open("path_points.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    x = int(parts[0])
                    y = int(parts[1])
                    cell_num = int(parts[2]) if len(parts) > 2 else None
                    self.path_points.append((x, y, cell_num))
            # Найдём начальную позицию (клетка 1)
            for i, (_, _, cell) in enumerate(self.path_points):
                if cell == 1:
                    self.current_path_index = i
                    break
        except FileNotFoundError:
            print("⚠️ path_points.txt не найден. Используется тестовый путь.")
            # Простой тестовый путь
            for i in range(50):
                cell = 1 if i == 0 else (2 if i == 5 else (3 if i == 10 else None))
                self.path_points.append((100 + i*20, 150 + i*5, cell))

    def roll_dice(self):
        return random.randint(1, 6)

    def move_by_steps(self, steps):
        """Переместиться на N шагов по белым кружкам"""
        if not self.path_points:
            return
        new_index = min(len(self.path_points) - 1, self.current_path_index + steps)
        self.current_path_index = new_index
        _, _, cell_num = self.path_points[new_index]
        if cell_num is not None:
            self.position = cell_num
        # иначе сохраняем предыдущую клетку (или можно None — но у тебя клетки везде важны)

    def handle_cell_after_move(self):
        cell = self.position
        if cell == 3:
            self.start_mini_game("Кот Учёный")
        elif cell == 5:
            self.start_mini_game("Царевна Лягушка")
            self.skip_turn = False
        elif cell == 6:
            self.skip_turn = True
        elif cell == 7:
            self.get_big_treasure()
        elif cell == 8:
            self.skip_turn = True
        elif cell == 11:
            self.handle_goose()
        elif cell == 12:
            self.handle_repkа_question()
        elif cell == 13:
            self.handle_baba_yaga()
        elif cell == 4:
            self.get_treasure()

        if cell in (2, 9, 10):
            self.needs_extra_roll = True
        else:
            self.needs_extra_roll = False

    def handle_extra_roll(self, dice_roll):
        cell = self.position
        if cell == 2:
            self.handle_waystone(dice_roll)
        elif cell == 9:
            loss = dice_roll
            self.bon = max(0, self.bon - loss)
            self.skip_turn = True
        elif cell == 10:
            self.handle_crossroad(dice_roll)
        self.needs_extra_roll = False

    def handle_waystone(self, dice_roll):
        if dice_roll in (1, 2):
            self._jump_to_cell(3)
        elif dice_roll in (3, 4):
            self._jump_to_cell(4)
        else:
            self._jump_to_cell(5)

    def handle_crossroad(self, dice_roll):
        if dice_roll in (1, 2):
            self._jump_to_cell(11)
        elif dice_roll in (3, 4):
            self._jump_to_cell(12)
        else:
            self._jump_to_cell(13)

    def _jump_to_cell(self, target_cell):
        """Найти первую точку с номером target_cell и перейти туда"""
        for i, (_, _, cell) in enumerate(self.path_points):
            if cell == target_cell:
                self.current_path_index = i
                self.position = target_cell
                break

    def get_treasure(self):
        self.bon += self.roll_dice() + self.roll_dice()

    def get_big_treasure(self):
        self.bon += self.roll_dice() + self.roll_dice() + self.roll_dice()

    def handle_goose(self):
        target = random.randint(1, 13)
        self._jump_to_cell(target)

    def handle_repkа_question(self, answer: str = "7"):
        try:
            if int(answer.strip()) == 7:
                self._jump_to_cell(7)
                return True
            return False
        except ValueError:
            return False

    def handle_baba_yaga(self):
        if self.bon >= 20:
            self.inventory[0] = "Волшебный клубок"
            return True
        else:
            self._jump_to_cell(3)
            return False

    def start_mini_game(self, title):
        self.in_mini_game = True

    def exit_mini_game(self):
        self.in_mini_game = False