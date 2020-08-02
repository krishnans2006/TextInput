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
        self.text_render = font.render(self.text, 1, (0, 0, 0))
        self.cursor = Cursor(self.x + 5, self.y + 5, self.height - 10)

    def add_key(self, key, font):
        self.text += key
        self.update_cursor_pos(font)

    def remove_key(self, font):
        self.text = self.text[:-1]
        self.update_cursor_pos(font)
    
    def enter(self, font):
        self.text = ""
        self.update_cursor_pos(font)

    def update_cursor_pos(self, font):
        self.text_render = font.render(self.text, 1, (0, 0, 0))
        self.cursor.move(self.cursor.original_x + self.text_render.get_width())

    def update(self):
        self.cursor.update()

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)
        win.blit(self.text_render, (self.x + 5, self.y + 5))
        self.cursor.draw(win)

    def __del__(self):
        del self.cursor
