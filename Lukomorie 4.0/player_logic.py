# player_logic.py
import random

class PlayerLogic:
    def __init__(self, name="Игрок"):
        self.name = name
        self.position = 1
        self.bon = 0
        self.inventory = [None, None, None]
        self.skip_turn = False
        self.in_mini_game = False
        self.needs_extra_roll = False  # флаг: нужен доп. бросок?

    def roll_dice(self):
        return random.randint(1, 6)

    def move_forward(self, steps):
        """Переместиться вперёд на N клеток (макс. 13)"""
        self.position = min(13, self.position + steps)

    def handle_cell_after_move(self):
        """Обрабатывает клетку ПОСЛЕ перемещения"""
        cell = self.position

        # Обычные эффекты
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

        # Особые клетки: требуют доп. броска
        if cell in (2, 9, 10):
            self.needs_extra_roll = True
        else:
            self.needs_extra_roll = False

    def handle_extra_roll(self, dice_roll):
        """Обработка доп. броска на клетках 2, 9, 10"""
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
            self.position = 3
        elif dice_roll in (3, 4):
            self.position = 4
        else:
            self.position = 5

    def handle_crossroad(self, dice_roll):
        if dice_roll in (1, 2):
            self.position = 11
        elif dice_roll in (3, 4):
            self.position = 12
        else:
            self.position = 13

    def get_treasure(self):
        self.bon += self.roll_dice() + self.roll_dice()

    def get_big_treasure(self):
        self.bon += self.roll_dice() + self.roll_dice() + self.roll_dice()

    def handle_goose(self):
        self.position = random.randint(1, 13)

    def handle_repkа_question(self, answer: str = "7"):
        try:
            if int(answer.strip()) == 7:
                self.position = 7
                return True
            else:
                return False
        except ValueError:
            return False

    def handle_baba_yaga(self):
        if self.bon >= 20:
            self.inventory[0] = "Волшебный клубок"
            return True
        else:
            self.position = 3
            return False

    def start_mini_game(self, title):
        self.in_mini_game = True

    def exit_mini_game(self):
        self.in_mini_game = False