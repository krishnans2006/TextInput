import pygame
from text_input import TextInput


def setup(W, H):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((W, H))

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("timesnewroman", 20)
    music = pygame.mixer.music.load("jeopardy_music.mp3")

    return win, clock, font, music


win, clock, font, music = setup(800, 600)


def redraw(win, **kwargs):
    win.fill((50, 75, 200))
    for name, object in kwargs.items():
        object.draw()
    pygame.display.flip()


def main():
    test_text = TextInput(50, 50, 200, 30, font)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                manage_reply = test_text.manage_key_press(event, font)
                if manage_reply:
                    print(f"You said {manage_reply}.")
            if event.type == pygame.KEYUP and event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                test_text.shift_unpressed()
        test_text.update()
        redraw(win)
        clock.tick(30)


if __name__ == '__main__':
    main()
