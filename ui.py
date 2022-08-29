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
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.elements = []
        self.elements_dict = {}

        self.last_x = 0
        self.last_y = 0

        self.padding_x = 10
        self.padding_y = 10

        self.elements_overflow_screen = False
    def add_element(self, name, element, colour, extra_args=()):
        # extra args holds the extraneous arguments that do not belong to UIElement parent class
        if not self.elements_overflow_screen:
            ui = element(self.x + self.last_x + self.padding_x,
                         self.y + self.last_y + self.padding_y,
                         colour, *extra_args)
            ui.name = name
            self.elements.append(ui)
            self.elements_dict[name] = ui

            self.last_x += ui.width + self.padding_x

            if self.last_x + self.padding_x >= self.x + self.width:
                self.last_x = 0
                self.last_y += element.height + self.padding_y

            if self.last_y >= self.y + self.height:
                self.elements_overflow_screen = True

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)
