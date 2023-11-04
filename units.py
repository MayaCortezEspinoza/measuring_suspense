import pygame
import time

from auxiliaries import *
from question_window import *
import numpy as np


class Unit:
    """
        a word unit in the application
    """
    # class properties shared by all instances:
    font = None
    color_1 = (0, 0, 0)
    color_2 = (0, 0, 0)
    number_of_lines = 0

    def __init__(self, text, number, properties):
        """
        Initializes a Unit object.
        """
        self.text = text
        self.number = number  # Unique identifier for the word (word index)
        self.properties = properties  # a dictionary of further properties
        self.width = 0  # the size of the word in the textbox
        self.height = 0  # the size of the word in the textbox
        self.position_x = 0  # the position - of the word in the textbox
        self.position_y = 0  # the position - of the word in the textbox
        self.cumulative_x = 0  # the position of the word in the textbox, if there were no line breaks
        self.cumulative_end = 0  # the end position of the word in the textbox if there were no line breaks
        self.cumulative_total = 0  # the end of the line if there were no line_breaks
        self.screen_width = 0
        self.screen_number = 0  # the number of the screen on which the word is shown
        self.paragraph = 0  # the paragraph
        self.line_number_on_screen = 0  # the number of the line on the screen on which the word is shown
        self.values = []  # these are the values that will be saved for all words
        self.times = []  # these are the times saved for each word
        self.checked = False  # set to true if suspense value for word is drawn
        self.mean_value = 0

    def set_font(self, my_font_name, text_height, number_of_lines):
        """
        try to render a word in pygame
        Find font size according to number of lines per screen

        Args:
        my_font_name (str): Name of the font.
        text_height (int): Height of the text area.
        number_of_lines (int): Number of lines per screen.
        """
        left, right = 1, 50  # Set appropriate font size range
        while left <= right:
            mid = (left + right) // 2
            chosen_font = pygame.font.SysFont(my_font_name, mid)
            img = chosen_font.render("Text I I II", True, self.color_1)
            rect = img.get_rect()
            h = rect.height
            if h > text_height / number_of_lines:
                right = mid - 1
            else:
                left = mid + 1
        Unit.font = pygame.font.SysFont(my_font_name, left - 1)
        Unit.number_of_lines = number_of_lines

    def set_color(self, color1, color2):
        Unit.color_1 = color1
        Unit.color_2 = color2

    def __repr__(self):
        s = f"(w: {self.text}| " \
            f"number: {self.number}| " \
            f"paragraph: {self.paragraph}| " \
            f"screen nr: " \
            f"{self.screen_number}| " \
            f"line on screen: {self.line_number_on_screen}| " \
            f"width: {self.width}" \
            f"| height: {self.height}| " \
            f"position x: {self.position_x}| " \
            f"position y: {self.position_y}| " \
            f"c: {self.cumulative_x}{self.cumulative_end}/{self.cumulative_total})"
        return s

    def show(self, surface):
        """show word on the screen in correct color:
        when the measure is drawn for the word, the color of the displayed word is different"""
        if self.checked:
            r = self.font.render(self.text, True, self.color_2)
        else:
            r = self.font.render(self.text, True, self.color_1)
        surface.blit(r, (self.position_x, self.position_y))

    def check(self, mouse):
        """This function checks for a word if there is already a suspense line for it.

        divides the end position of the word (as if all 10 lines were drawn in one line)
        by the full length of the text (as if drawn in one line)
        This gives the proportion of the word to the whole text.

        multiplies by screen width to convert proportion into drawing screen progress
        """
        progress_proportion = self.cumulative_end / self.cumulative_total
        max_x = self.screen_width * progress_proportion
        if 0 < mouse[0] >= max_x - 5:  # is the mouse past this word? (was this word drawn?)
            self.checked = True
        else:
            return False

    def uncheck(self):
        self.checked = False
        self.delete_values()

    def store_values(self, values, times, screen):
        """

        :param values: values drawn for this word
        :param times: time stamps of drawn values
        :param screen: at which screen this word was shown
        :return:
        """
        min_x = self.screen_width * self.cumulative_x / self.cumulative_total
        max_x = self.screen_width * self.cumulative_end / self.cumulative_total
        all_values = []
        for i in range(len(values)):  # values are tuples of (x,y)
            if min_x <= values[i][0] <= max_x:  # if x_coordinate within word start and end positions
                all_values.append(values[i][1])
                self.values.append(values[i][1])  # store heights
                self.times.append(times[i])  # store times at which points were drawn
        m = np.mean(all_values)
        if m > 0:
            if not screen.memorybox.training:
                screen.memorybox.update_values(int(m))

    def delete_values(self):
        self.values = []
        self.times = []

    def __eq__(self, other):
        return self == other

    def __str__(self):
        return self.__repr__()


class Screen:
    textbox_height = 0  # the box in which the text is displayed
    textbox_width = 0
    textbox_y = 0
    textbox_x = 0
    drawbox_height = 0  # the drawing box
    drawbox_width = 0
    drawbox_y = 0
    drawbox_x = 0
    draw_box_background = (0, 0, 0)
    draw_box_text = (0, 0, 0)
    draw_box_line = (0, 0, 0)
    text_background = (0, 0, 0)
    memorybox_height = 0  # the box where previously drawn bits of suspense arc are shown
    memorybox_width = 0
    memorybox_y = 0
    memorybox_x = 0

    def set_geometric_indices(self, SCR_HEIGHT, TXT_HEIGHT, SCR_WIDTH, TXT_WIDTH, TXT_Y, TXT_X, SUSPENSE_HEIGHT,
                              SUSPENSE_SPACE, MEMORY):
        # turn all relative indices into absolute numbers
        Screen.textbox_height = int(SCR_HEIGHT * TXT_HEIGHT / 100)
        Screen.textbox_width = int(SCR_WIDTH * TXT_WIDTH / 100)
        Screen.textbox_y = int(SCR_HEIGHT * TXT_Y / 100)
        Screen.textbox_x = int(SCR_WIDTH * TXT_X / 100)
        Screen.drawbox_height = int(SCR_HEIGHT * SUSPENSE_HEIGHT / 100)
        Screen.drawbox_width = self.textbox_width
        Screen.drawbox_y = int(self.textbox_y - (SCR_HEIGHT * SUSPENSE_SPACE / 100) - self.drawbox_height)
        Screen.drawbox_x = self.textbox_x
        Unit.screen_width = Screen.textbox_width
        Screen.memorybox_height = int(SCR_HEIGHT * MEMORY / 100)
        Screen.memorybox_width = self.textbox_width
        Screen.memorybox_y = int(self.textbox_y + self.textbox_height + 5)
        Screen.memorybox_x = self.textbox_x

    def __init__(self, SCR_HEIGHT=None, TXT_HEIGHT=None, SCR_WIDTH=None, TXT_WIDTH=None, TXT_Y=None, TXT_X=None,
                 SUSPENSE_HEIGHT=None, SUSPENSE_SPACE=None,
                 drawbox=None, number=None, words=None, drawbox_background=None, drawbox_text=None, drawbox_line=None,
                 textbackground=None, memory_size=None, memorybox=None):
        if SCR_HEIGHT is not None:
            self.set_geometric_indices(SCR_HEIGHT, TXT_HEIGHT, SCR_WIDTH, TXT_WIDTH, TXT_Y, TXT_X, SUSPENSE_HEIGHT,
                                       SUSPENSE_SPACE, memory_size)
        if drawbox is not None:
            self.drawbox = drawbox
        else:
            self.drawbox = None
        if memorybox is not None:
            self.memorybox = memorybox
        else:
            self.memorybox = None
        if number is None:
            self.number = 0
        else:
            self.number = number
        if words is not None:
            self.words = words
        else:
            self.words = None
        if drawbox_background is not None:
            Screen.draw_box_background = drawbox_background
        if drawbox_text is not None:
            Screen.draw_box_text = drawbox_text
        if drawbox_line is not None:
            Screen.draw_box_line = drawbox_line
        if textbackground is not None:
            Screen.text_background = textbackground
        self.allowed_keys = []  # between training vs. main phase different keys are allowed
        self.next_screen = None
        self.previous_screen = None
        self.checked = False
        self.shown = False
        self.last_mouse_position_absolute = (self.drawbox_x, self.drawbox_y + self.drawbox_height)  # lower left corner
        self.last_mouse_position_relative = (0, self.drawbox_height)  # set to lower left corner
        self.last_mouse_position_value = 0  # "suspense value"
        self.allow_mouse = True  # is moving the mouse allowed? (in some training screens, it may not)

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return self.__repr__()

    def get_mouse(self):
        return self.last_mouse_position_relative[0], max(0, self.last_mouse_position_relative[1])

    def set_mouse(self):
        return self.last_mouse_position_absolute[0], max(self.drawbox_y, self.last_mouse_position_absolute[1])

    def change_last_mouse(self, new_mouse):
        # new_mouse is a relative value screen.change_last_mouse(screen.get_mouse())
        self.last_mouse_position_relative = new_mouse
        self.last_mouse_position_absolute = (new_mouse[0] + self.drawbox_x, new_mouse[1] + self.drawbox_y)

    def set_allowed_key(self, key):
        self.allowed_keys.append(key)

    def get_checked(self):
        if self.checked:  # for screens which are checked by default
            return True
        else:
            for word in self.words:  # only checked screens allow to move forward!
                if not word.checked:
                    return False
        return True

    def check_words(self):
        for w in self.words:
            w.check(self.last_mouse_position_relative)

    def set_value_mouse(self):
        """
        this method transforms mouse height value to fit a new screen
        """
        y = self.drawbox.height - self.last_mouse_position_relative[1]
        new_y = y * DrawBox.current_max_y / DrawBox.height
        self.last_mouse_position_value = new_y

    def get_mouse_from_value(self):
        """
        transforms relative drawn height to an absolute mouse position
        """
        y = self.last_mouse_position_value
        new_y = DrawBox.height - (y * DrawBox.height / DrawBox.current_max_y)
        self.last_mouse_position_relative = (self.last_mouse_position_relative[0], new_y)
        self.last_mouse_position_absolute = (
            self.last_mouse_position_relative[0] + self.drawbox_x, self.drawbox_y + new_y)

    def action(self, action):  # what happens when an allowed key is pressed
        if action == "forward":
            if self.next_screen is not None:  # if this is not the last screen
                if self.next_screen.last_mouse_position_value != 0:  # if the next screen already has values
                    self.next_screen.get_mouse_from_value()
                if self.allow_mouse:  # if drawing was possible, store all values for this screen
                    if self.get_checked():
                        self.drawbox.map_from_pixel()
                        for w in self.words:
                            w.store_values(self.drawbox.values, self.drawbox.times, self)
                        MemoryBox.tobeshown = True
                        self.next_screen.last_mouse_position_relative = 0, self.last_mouse_position_relative[1]
                        self.next_screen.last_mouse_position_absolute = self.drawbox_x, self.last_mouse_position_absolute[1]
                        return self.next_screen
                    else:
                        return "play_error"  # drawing not done but participants want to move forward: play error sound
                else:
                    self.shown = False
                    self.next_screen.shown = False
                    return self.next_screen
            else:
                return "no next screen found"
        elif action == "backward":  # if people move to previous screen
            if self.previous_screen is not None:  # not first screen
                self.set_value_mouse()
                if self.allow_mouse:
                    self.drawbox.map_from_pixel()  # if drawing was allowed: store drawn values
                self.shown = False
                self.previous_screen.shown = False
                self.previous_screen.allow_mouse = False
                return self.previous_screen
            else:
                return "play_error"
        elif action == "delete":
            if self.allow_mouse:  # if drawing is allowed: start again from x = zero, y = last y from last screen
                if self.previous_screen is not None:
                    self.last_mouse_position_relative = (0, self.previous_screen.last_mouse_position_relative[1])
                    self.last_mouse_position_absolute = (
                        self.drawbox_x, self.previous_screen.last_mouse_position_absolute[1])
                else:  # if very first screen is deleted, go back to (0,0)- coordinate
                    self.last_mouse_position_absolute = (self.drawbox_x, self.drawbox_y + self.drawbox_height)
                    self.last_mouse_position_relative = (0, self.drawbox_height)
                self.drawbox.delete_values()
                self.shown = False
                for w in self.words:
                    w.uncheck()
                return self
            else:
                return "play_error"  # if no drawing is allowed, deleting results in error sound
        elif action == "in":  # zooming: double the suspense max (if suspense gets too high to fit on current zooming)
            if DrawBox.current_max_y < DrawBox.max_y:
                self.set_value_mouse()
                DrawBox.current_max_y = DrawBox.current_max_y * 2
                if DrawBox.current_max_y > MemoryBox.current_max_y and False:
                    MemoryBox.current_max_y = DrawBox.current_max_y
                self.drawbox.map_to_pixel()
                self.get_mouse_from_value()
                self.shown = False
            return self
        elif action == "out":  # zooming: halve the suspense max (if suspense gets smaller)
            if DrawBox.current_max_y > DrawBox.min_y:
                self.set_value_mouse()
                DrawBox.current_max_y = DrawBox.current_max_y / 2
                self.drawbox.map_to_pixel()
                self.get_mouse_from_value()
                self.shown = False
            return self
        elif action == "getout":
            return "getout"

    def plot_words(self):
        textsurface = pygame.Surface(size=(self.textbox_width, self.textbox_height))
        textsurface.fill(self.text_background)
        for w in self.words:
            w.show(textsurface)
        return textsurface

    def show(self, pysurface):
        """
        Displays the screen elements on the provided Pygame surface.

        Args:
            pysurface (pygame.Surface): The Pygame surface on which the screen elements will be displayed.

        Returns:
            None
        """
        assert isinstance(pysurface, pygame.Surface)

        # Blit the drawing box on the surface at the specified position
        pysurface.blit(self.drawbox.show(), (self.drawbox_x, self.drawbox_y))

        # Check if the memory box should be displayed
        if self.memorybox.tobeshown:
            # Update the maximum y-coordinate value based on MemoryBox values
            MemoryBox.current_max_y = max([x[1] for x in MemoryBox.values])
            # Blit the memory box on the surface at the specified position
            pysurface.blit(self.memorybox.show(), (self.memorybox_x, self.memorybox_y))
            # Mark MemoryBox as shown and reset the flag
            MemoryBox.tobeshown = False

        # Draw arrows at the edges of the drawing box
        arrow(pysurface, self.draw_box_line, self.draw_box_line,
              (self.drawbox_x, self.drawbox_height + self.drawbox_y),
              (self.drawbox_x - 0, self.drawbox_y), 10)
        arrow(pysurface, self.draw_box_line, self.draw_box_line,
              (self.drawbox_x, self.drawbox_height + self.drawbox_y),
              (self.drawbox_x + self.drawbox_width, self.drawbox_height + self.drawbox_y), 10)

        # Check the words on the screen for user interactions
        self.check_words()

        # Render and blit text elements on the surface at the specified position
        pysurface.blit(self.plot_words(), (self.textbox_x, self.textbox_y))

        # Update the display to show the changes
        pygame.display.update()

        # Mark the screen as shown
        self.shown = True

    def __repr__(self):
        s = f"\n(screen:{self.number}| " \
            f"textbox size:{self.textbox_width}, {self.textbox_height}|" \
            f"drawbox coordinates: {self.textbox_x}, {self.textbox_y}|" \
            f"drawbox size:{self.drawbox_width}, {self.drawbox_height}" \
            f"drawbox coordinates{self.drawbox_x}, {self.drawbox_y}| " \
            f"screen words:\n{self.words}\n)"
        return s

    def restart_memorybox(self):
        # set all previous suspense values to -1:
        for d in MemoryBox.values:
            d[1] = -1
        self.memorybox.tobeshown = True


class MemoryBox:
    """
    display previously drawn bits of suspense arc

    Attributes:
        values (list): A list to store suspense arc values as tuples (x, y).
        drawn_values (list): A list to store drawn suspense arc values as tuples (x, y).
        current_max_y (float): The current maximum suspense value being displayed.
        training (bool): A flag indicating whether the memory box is used for training.
        background_color (tuple): RGB color tuple
        line_color (tuple): RGB color tuple for the line color of the drawn suspense arc.
        text_color (tuple): RGB color tuple for the text color.
        font (pygame.font.Font): The font used for rendering text on the memory box.
        tobeshown (bool): A flag indicating whether the memory box should be displayed.
    """

    values = []
    drawn_values = []
    current_max_y = 0
    height = 0
    width = 0
    training = False
    background_color = (0, 0, 0)
    line_color = (0, 0, 0)
    text_color = (0, 0, 0)
    font = None
    tobeshown = False

    def __init__(self, current_mx, height, width, background_color, text_color, line_color, font):
        """
        Initializes the MemoryBox with specified attributes.

        Args:
            current_mx (float): The current maximum suspense value being displayed.
            height (int): The height of the memory box.
            width (int): The width of the memory box.
            background_color (tuple): RGB color tuple for the background color.
            text_color (tuple): RGB color tuple for the text color.
            line_color (tuple): RGB color tuple for the line color.
            font (pygame.font.Font): The font used for rendering text.

        Returns:
            None
        """
        MemoryBox.current_max_y = current_mx
        MemoryBox.height = height
        MemoryBox.width = width
        MemoryBox.background_color = background_color
        MemoryBox.line_color = line_color
        MemoryBox.text_color = text_color
        MemoryBox.font = font

    def update_values(self, n):
        """
        Updates suspense arc values with a new suspense value.

        Args:
            n (float): The new suspense value to update the values with
            (all values start with height 1: the first occurrence of -1 is replaced with the new value

        Returns:
            None
        """
        i = 0
        done = False
        while not done:
            if self.values[i][1] == -1:
                self.values[i][1] = n
                done = True
            i += 1

    def map_from_pixel(self):
        """
        Maps drawn pixel heights to absolute suspense heights and updates self.values.

        Returns:
            None
        """
        self.values = []
        for (x, y) in self.drawn_values:
            new_x = x
            y = self.height - y
            new_y = y * self.current_max_y / self.height
            self.values.append((new_x, new_y))

    def init_values(self, words):
        """
        Initializes values based on the number of words in the suspense arc.

        Args:
            words (list): List of Unit objects representing words or text segments.

        Returns:
            None
        """
        n = len(words)
        for i in range(len(words)):
            self.values.append([(i * self.width) // n, -1])

    def map_to_pixel(self):
        """
        Maps absolute suspense coordinates to pixel coordinates and updates self.drawn_values.

        Returns:
            None
        """
        self.drawn_values = []
        for (x, y) in self.values:
            new_x = x
            if self.current_max_y != 0:
                new_y = self.height - (y * self.height / self.current_max_y)
            else:
                new_y = self.height - (y * self.height / 1)
            if new_x not in [x[0] for x in self.drawn_values]:
                self.drawn_values.append((new_x, new_y))

    def rezoom(self, x):
        """
        Adjusts the current maximum suspense value being displayed.

        Args:
            x (float): The new maximum suspense value.

        Returns:
            None
        """
        self.current_max_y = x

    def show(self):
        """
        Renders and returns the memory box as a Pygame surface.

        Returns:
            pygame.Surface: The memory box rendered as a Pygame surface.
        """
        surface = pygame.Surface(size=(self.width, self.height))
        surface.fill(self.background_color)
        y_text_oben = self.font.render(str(self.current_max_y), True, self.text_color)
        y_text_unten = self.font.render(str(0), True, self.text_color)
        if not self.training:
            if self.values:
                self.map_to_pixel()
            surface.blit(y_text_oben, (0, 0))
            surface.blit(y_text_unten, (0, self.height - y_text_unten.get_rect().height))
            for coord in self.drawn_values:
                pygame.draw.circle(surface, self.line_color, (coord[0], coord[1]), 5)

        return surface


class DrawBox:
    # suspense boxes are the canvasses on which suspense lines can be drawn.
    max_y = 0
    min_y = 0
    current_max_y = 0
    height = 0
    width = 0
    background_color = (0, 0, 0)
    line_color = (0, 0, 0)
    text_color = (0, 0, 0)
    font = None

    def __init__(self, current_mx, mx, mn, height, width, background_color, text_color, line_color, font):
        DrawBox.max_y = mx  # the biggest max - the maximal max
        DrawBox.min_y = mn  # the smallest possible zoom - the smallest max
        DrawBox.current_max_y = current_mx  # the max that is being shown right now
        DrawBox.height = height  # the number of pixels in the graphical realization = height of the box!
        DrawBox.width = width  # the width of the drawbox
        self.values = []  # pairs of (x,y) for each dot given in the suspense lines, coordinates will be saved
        self.times = []  # time at which a value was drawn
        self.starting_time = 0
        self.drawn_values = []
        DrawBox.background_color = background_color
        DrawBox.line_color = line_color
        DrawBox.text_color = text_color
        DrawBox.font = font

    def set_starting_time(self, starting_time):
        if self.starting_time == 0:  # starting time has not been set yet, this screen has never been seen
            self.starting_time = starting_time

    def map_from_pixel(self):
        # we convert values from drawn heights into absolute suspense heights, we save heights and times into the object
        self.values = []
        for (x, y) in self.drawn_values:
            new_x = x
            y = self.height - y
            new_y = y * self.current_max_y / self.height
            self.values.append((new_x, new_y))

    def map_to_pixel(self):
        # map each actual coordinate to a position on the screen
        # these values are not saved into the suspense boxes
        self.drawn_values = []
        for (x, y) in self.values:
            new_x = x
            new_y = self.height - (y * self.height / self.current_max_y)
            self.drawn_values.append((new_x, new_y))

    def rezoom(self, x):
        self.current_max_y = x

    def __repr__(self):
        s = "[box:" + str(self.values) + str(self.times) + str(self.drawn_values) + "]"
        return s

    def delete_values(self):
        self.values = []
        self.drawn_values = []
        self.times = []
        print(f" values are deleted ")

    def record_mouse(self, old, new):
        old_x, old_y = old
        new_x, new_y = new
        if old not in self.drawn_values:
            self.drawn_values.append(old)
            self.times.append(time.time())
        if old_x + 1 == new_x:
            self.drawn_values.append(new)
            self.times.append(time.time())
        else:
            # if values are drawn too fast, all values between the caught mouse points are linearly interpolated
            if new_x != old_x:
                a = (new_y - old_y) / (new_x - old_x)
                b = (new_x * old_y - new_y * old_x) / (new_x - old_x)
                for x in range(old_x, new_x):
                    self.drawn_values.append((x, a * x + b))
                    self.times.append(time.time())
        self.map_from_pixel()

    def show(self):
        surface = pygame.Surface(size=(self.width, self.height))
        surface.fill(self.background_color)
        y_text_upper = self.font.render(str(self.current_max_y), True, self.text_color)  # margin numbers displayed
        y_text_lower = self.font.render(str(0), True, self.text_color)
        surface.blit(y_text_upper, (0, 0))
        surface.blit(y_text_lower, (0, self.height - y_text_lower.get_rect().height))
        if self.values:
            self.map_to_pixel()
        for coord in self.drawn_values:
            pygame.draw.circle(surface, self.line_color, (coord[0], coord[1]), 5)

        return surface


def get_words(data, unit_delimiter=" "):
    # split all text from data into individual words
    # for all words, we keep all the further data from each line
    all_words_split = []
    number = 0
    paragraph = 0
    for line in data:
        paragraph += 1
        text = line["text"]
        assert (isinstance(text, str))
        t = text.split(unit_delimiter)
        for w in t:
            number += 1
            properties = {}
            for word_property in line:
                if word_property != "text":
                    properties[word_property] = line[word_property]  # line properties transferred as word properties
            unit = Unit(w, number, properties)  # initialize word class
            unit.paragraph = paragraph
            all_words_split.append(unit)
    return all_words_split


def initialize(words, my_screen, training=False):
    """
        Organizes the input words into screens based on screen width and paragraph breaks.

        Args:
            words (list of Unit): List of Unit objects representing individual words or text segments.
            my_screen (Screen): The Screen object used for layout calculations.
            training (bool, optional): Indicates whether the initialization is for training purposes. Defaults to False.

        Returns:
            list of Screens, list of Units: A list of Screen objects and a modified list of Unit objects with screen details.
        """
    assert isinstance(my_screen, Screen)
    font = words[0].font
    space = font.render(" ", True, (0, 0, 0)).get_rect().width
    done = False  # this variable will be true if there are no more words to be split into lines
    index = 0  # this index will be reset for every line, it counts up until the max nr of words for the line is reached
    current_paragraph = 1  # paragraph number from the input csv
    current_screen_line = 1  # number of lines shown in one screen
    current_screen = 1  # index of screen shown in the experiment
    current_x = 0  # the x position the word is shown on on the screen
    total_x = 0  # the position of the word if the length of the whole screen was plotted into one line,
    n_lines = words[0].number_of_lines
    max_paragraph = max([x.paragraph for x in words])
    # needed for the navigation on the drawing screen
    while not done:
        word = words[index]
        assert isinstance(word, Unit)
        if word.paragraph > current_paragraph:  # new paragraph started!
            current_paragraph += 1
            if training or max_paragraph == current_paragraph:  # for training: open a new screen for each paragraph
                current_screen += 1
                current_screen_line = 1
                for w in [x for x in words if x.screen_number == current_screen - 1]:
                    w.cumulative_total = total_x
                total_x = word.width + space
                word.position_x = 0
            else:  # not in training
                current_screen_line += 1  # for normal screens, new paragraph: new line!
                if current_screen_line == n_lines + 1:  # if 10th line is full, change to new screen
                    current_screen_line = 1
                    current_screen += 1
                    word.cumulative_x = 0
                    word.cumulative_end = word.cumulative_x + word.width
                    for w in [x for x in words if x.screen_number == current_screen - 1]:
                        w.cumulative_total = total_x
                    total_x = word.width + space
                else:  # there are lines left on the same screen!
                    word.cumulative_x = total_x
                    word.cumulative_end = word.cumulative_x + word.width
                    total_x = total_x + word.width + space
                word.position_x = 0
            current_x = word.width + space
        else:  # no new paragraph
            if current_x + word.width + space < my_screen.textbox_width:  # does the word fit in this line?
                # yes: change nothing but the x position, no: change line number
                word.position_x = current_x
                word.cumulative_x = total_x
                word.cumulative_end = word.cumulative_x + word.width
                current_x = current_x + word.width + space
                total_x = total_x + word.width + space
            else:  # new line needed
                current_screen_line += 1
                if current_screen_line == n_lines + 1:  # if 10th line is full, change to new screen
                    current_screen_line = 1
                    current_screen += 1
                    word.cumulative_x = 0
                    word.cumulative_end = word.cumulative_x + word.width
                    for w in [x for x in words if x.screen_number == current_screen - 1]:
                        w.cumulative_total = total_x
                    total_x = word.width + space
                else:  # screen has room for new line
                    word.cumulative_x = total_x
                    word.cumulative_end = word.cumulative_x + word.width
                    total_x = total_x + word.width + space
                word.position_x = 0
                current_x = word.width + space
        word.position_y = my_screen.textbox_height / n_lines * (current_screen_line - 1)
        word.screen_number = current_screen
        word.line_number_on_screen = current_screen_line
        index = index + 1
        if index == len(words):
            done = True
    for w in [x for x in words if x.screen_number == current_screen]:
        w.cumulative_total = total_x
    # print(words)
    screens = []
    current_screen = 1
    for w in words:
        assert isinstance(w, Unit)
        if current_screen == w.screen_number:
            draw_box = DrawBox(current_mx=10, mn=0.1, mx=1000, height=my_screen.drawbox_height,
                               width=my_screen.drawbox_width, font=w.font,
                               background_color=my_screen.draw_box_background, line_color=my_screen.draw_box_line,
                               text_color=my_screen.draw_box_text)
            memory_box = MemoryBox(current_mx=10, height=my_screen.memorybox_height,
                                   width=my_screen.drawbox_width, font=w.font,
                                   background_color=my_screen.draw_box_background, line_color=my_screen.draw_box_line,
                                   text_color=my_screen.draw_box_text)
            add = [x for x in words if x.screen_number == current_screen]
            for x in add:
                x.screen_width = draw_box.width
            screens.append(Screen(drawbox=draw_box, words=add, memorybox=memory_box))
            current_screen += 1
    for j in range(0, len(screens)):
        screens[j].number = j
        if j != 0:
            screens[j].previous_screen = screens[j - 1]
        if j != len(screens) - 1:
            screens[j].next_screen = screens[j + 1]
    # print(f' this is the number of screens {len(screens)}')
    return screens, words


def compute_size_words(words):
    # compute the actual size of words in pixels - height stays the same for all words, length differs
    for word in words:
        rect = word.font.render(word.text, True, (0, 0, 0)).get_rect()
        word.width = rect.width
        word.height = rect.height
    return words


def calculate_additional_properties(words):
    for word in words:
        if word.values:
            screen_words = [w for w in words if w.screen_number == word.screen_number]
            screen_starting_time = round(min([t for word in screen_words for t in word.times], default=99999), 4)
            screen_ending_time = round(max([t for word in screen_words for t in word.times], default=99999), 4)
            screen_values = [v for word in screen_words for v in word.values]
            setattr(word, "mean_screen_value", round(np.mean(screen_values), 3))
            screen_drawing_time = screen_ending_time - screen_starting_time  # calculate time needed to draw line
            setattr(word, "screen_drawing_time", round(screen_drawing_time, 4))
            setattr(word, "screen_starting_time", screen_starting_time)
    all_starting_times = sorted(list(set([w.screen_starting_time for w in words if w.values])))
    for word in words:
        if word.values:
            word.mean_value = round(np.mean(word.values), 3)
            try:
                next_starting_time = all_starting_times[all_starting_times.index(word.screen_starting_time) + 1]
                setattr(word, "time_until_next_screen", round(next_starting_time - word.screen_starting_time, 4))
            except IndexError:
                setattr(word, "time_until_next_screen", 99999)
    all_screen_times = sorted(list(set([w.screen_drawing_time for w in words if w.values])))
    for w in words:
        setattr(w, "mean_screen_time", round(np.mean(all_screen_times), 4))  # calculate mean reading time for screens
        setattr(w, "min_screen_time", round(min(all_screen_times, default=99999), 4))  # calculate shortest screen time
        setattr(w, "max_screen_time", round(max(all_screen_times, default=99999), 4))  # calculate longest screen time
        setattr(w, "drawing_time_word", round(max(w.times, default=99999) - min(w.times, default=99999), 4))
    for w in words:
        setattr(w, "average_word_time", round(np.mean([word.drawing_time_word for word in words if word.values]), 4))


def fancy_save(words, c_round, resultfile):
    calculate_additional_properties(words)
    new_words = []
    for word in words:
        assert isinstance(word, Unit)
        for key, value in word.properties.items():
            setattr(word, key, value)
        for i in range(len(word.values)):
            new_word = word.__dict__.copy()
            new_word["values"] = round(word.values[i], 3)
            new_word["times"] = round(word.times[i], 4)
            new_word["text_number_in_experiment"] = c_round
            new_word.pop("properties")
            new_words.append(new_word)
    my_keys = new_words[0].keys()
    with open(resultfile, 'a', newline='') as r_file:
        dict_writer = csv.DictWriter(r_file, my_keys, dialect="excel", delimiter=";")
        dict_writer.writeheader()
        for w in new_words:
            dict_writer.writerow(w)


def save_and_compress(words, c_round, resultfile):
    calculate_additional_properties(words)
    new_words = []
    for word in words:
        assert isinstance(word, Unit)
        for key, value in word.properties.items():
            setattr(word, key, value)
        for i in range(len(word.values)):
            new_word = word.__dict__.copy()
            new_word["values"] = round(word.values[i], 3)
            new_word["times"] = round(word.times[i], 4)
            new_word["text_number_in_experiment"] = c_round
            new_word.pop("properties")
            new_word.pop("width")
            new_word.pop("height")
            new_word.pop("position_y")
            new_word.pop("cumulative_end")
            new_word.pop("cumulative_total")
            new_word.pop("screen_width")
            new_word.pop("checked")
            new_word.pop("times")
            new_word.pop("values")
            new_words.append(new_word)
    my_words = []
    for i in new_words:
        if i not in my_words:
            my_words.append(i)
    dataframe = compress_data(my_words)
    dataframe.to_csv(resultfile, mode="a", header=True)


def line_save(words, result_file):
    all_screens = max([y.screen_number for y in words])
    line_list = []
    line_nr = 0
    for y in range(1, all_screens + 1):
        screen_words = [z for z in words if z.screen_number == y]
        line_count = max([z.line_number_on_screen for z in screen_words])
        for z in range(1, line_count + 1):
            line = {"line_nr": line_nr, "screen_nr": y, "line_nr_on_screen": z}
            line_text = " ".join([w.text for w in screen_words if w.line_number_on_screen == z])
            line["text"] = line_text
            line_list.append(line)
            line_nr += 1
    my_keys = line_list[0].keys()
    with open(result_file, 'w', newline='') as r_file:
        dict_writer = csv.DictWriter(r_file, my_keys, dialect="excel", delimiter=";")
        dict_writer.writeheader()
        for w in line_list:
            dict_writer.writerow(w)


def set_meta_data(meta_data_dict):
    my_keys = meta_data_dict.keys()
    with open("participants.csv", "a") as p_file:
        dict_writer = csv.DictWriter(p_file, my_keys, dialect="excel", delimiter=";")
        dict_writer.writeheader()
        dict_writer.writerow(meta_data_dict)


def get_meta_data(meta_data_dict):
    p_id = meta_data_dict["Teilnahme-ID"]
    with open('participants.csv', mode="r") as p_file:
        csv_reader = csv.DictReader(p_file, delimiter=';')
        participant = [row for row in csv_reader if row["Teilnahme-ID"] == p_id][0]
        for key, value in meta_data_dict.items():
            participant[key] = value
        return participant
