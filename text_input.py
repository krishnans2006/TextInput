import pygame


class Cursor:
    def __init__(self, x, y, height):
        self.original_x = x
        self.x = self.original_x
        self.y = y
        self.height = height
        self.show = True
        self.cnt_since_change = 0
        self.change_frames = 15

    def move(self, loc):
        self.x = loc

    def update(self):
        self.cnt_since_change += 1
        if self.cnt_since_change > self.change_frames:
            self.show = not self.show
            self.cnt_since_change = 0

    def draw(self, win):
        if self.show:
            pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.x, self.y + self.height), 2)


class TextInput:
    def __init__(self, x, y, width, height, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = ""
        self.disp_text = self.text
        self.text_render = font.render(self.disp_text, 1, (0, 0, 0))
        self.cursor = Cursor(self.x + 5, self.y + 5, self.height - 10)
        self.shift_pressed = False

    def manage_key_press(self, event, font):
        key_name = pygame.key.name(event.key)
        if len(key_name) == 1:
            final_key = key_name
        elif key_name == "space":
            final_key = " "
        elif key_name == "return":
            text = self.text
            self.enter(font)
            return text
        elif key_name == "backspace":
            final_key = "back"
        elif key_name in ["right shift", "left shift"]:
            self.shift_pressed = True
            final_key = ""
        else:
            final_key = ""
        if final_key == "back":
            self.remove_key(font)
        else:
            self.add_key(final_key, font)

    def add_key(self, key, font):
        if self.shift_pressed:
            self.text += key.upper()
        else:
            self.text += key
        self.update_cursor_pos(font)

    def remove_key(self, font):
        self.text = self.text[:-1]
        self.update_cursor_pos(font)
    
    def enter(self, font):
        self.text = ""
        self.update_cursor_pos(font)

    def shift_unpressed(self):
        self.shift_pressed = False

    def update_cursor_pos(self, font):
        self.disp_text += self.text[-1]
        self.text_render = font.render(self.disp_text, 1, (0, 0, 0))
        if self.text_render.get_width() > self.width - 10:
            self.cursor.move(self.cursor.original_x + self.width - 10)
            self.disp_text = self.disp_text[1:]
        else:
            self.cursor.move(self.cursor.original_x + self.text_render.get_width())

    def update(self):
        self.cursor.update()

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)
        if self.text_render.get_width() > self.width - 10:
            win.blit(self.text_render, (self.x - (self.text_render.get_width() - self.width + 5), self.y + 5))
        else:
            win.blit(self.text_render, (self.x + 5, self.y + 5))
        self.cursor.draw(win)

    def __del__(self):
        del self.cursor
