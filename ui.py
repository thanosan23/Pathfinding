import pygame

class UIElement:
    def __init__(self, x, y, width, height, colour, clickable):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.clickable = clickable

        self.name = None
        def clicked(mouse_x, mouse_y):
            return (mouse_x >= self.x and
                    mouse_y >= self.y and
                    mouse_x <= self.x + self.width and
                    mouse_y <= self.y + self.height)

        if self.clickable is True:
            setattr(self, "clicked", clicked)


class Text(UIElement):
    def __init__(self, x, y, colour, font, text):
        self.font = font
        self.text = text
        width, height = self.font.size(self.text)
        super().__init__(x, y, width, height, colour, False)

    def draw(self, screen):
        surf = self.font.render(self.text, True, self.colour)
        screen.blit(surf, ((self.x), (self.y)))

    def update_text(self, text):
        self.text = text

class Button(UIElement):
    def __init__(self, x, y, colour, font, text):
        self.font = font
        self.text = text
        width, height = self.font.size(self.text)
        super().__init__(x, y, width * 2, height * 2, colour, True)

        self.transparency = 255

    def draw(self, screen):
        rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect.fill((*self.colour, self.transparency))
        screen.blit(rect, (self.x, self.y))

        surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(surf, ((self.x + (self.width // 4)),
                           (self.y + (self.height // 4))))

class HUD:
    def __init__(self, x, y, width, height, padding=(10, 10)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.elements = []
        self.elements_dict = {}

        self.last_x = 0
        self.last_y = 0

        self.padding = padding

        self.elements_overflow_screen = False

    def add_element(self, name, element, colour, extra_args=()):
        # extra args holds the extraneous arguments that do not belong to UIElement parent class
        if not self.elements_overflow_screen:
            # elements cannot have the same name
            assert name not in self.elements_dict.keys()

            ui = element(self.x + self.last_x + self.padding[0],
                         self.y + self.last_y + self.padding[1],
                         colour, *extra_args)
            ui.name = name
            if self.x + self.last_x + self.padding[0] + ui.width <= self.x + self.width:
                self.elements.append(ui)
                self.elements_dict[name] = ui
                self.last_x += ui.width + self.padding[0]
            else:
                self.last_x = 0
                self.last_y += ui.height + self.padding[1]

            if self.y + self.last_y + self.padding[1] + ui.height >= self.y + self.height:
                self.elements_overflow_screen = True

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)
