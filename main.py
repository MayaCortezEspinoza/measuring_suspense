from units import *
from auxiliaries import *
from question_window import *

# global parameters - mess with these even if you do not know what you are doing and you will be happy.
CSV_NAME = "dummy_text.csv"  # csv file must have at least one column named "text"
training_csv = "training_texts_english.csv"  # csv for training phase
training_phase = True  # set to false if you want to skip training
questionaire = True  # set to true if you want to show the questionnaire
try_it = False  # set to true if you want only a short passage to try out the program
SCR_WIDTH = 1920
SCR_HEIGHT = 1080
count_round = 1  # one as this version of the experiment has just one text

# screen proportions
TXT_HEIGHT = 35  # percent of screen height
TXT_WIDTH = 80  # percent of screen width
TXT_Y = 45  # position of upper end of text on the screen
TXT_X = 10  # position of left end of text on the screen
SUSPENSE_HEIGHT = 35  # height of box where things can be drawn
SUSPENSE_SPACE = 5  # the space between the drawing and the text
MEMORY_HEIGHT = 15  # percent of the screen

# Color settings
TEXT_COLOR_1 = (100, 100, 0)
TEXT_COLOR_2 = (100, 0, 100)
SUSPENSE_COLOR = (108, 25, 25)
PAST_SUSPENSE_COLOR = (131, 110, 110)
BACKGROUND_COLOR = (228, 221, 221)
SUSPENSE_BACKGROUND_COLOR = (210, 207, 200)
TEXT_BACKGROUND_COLOR = (228, 238, 238)
SUSPENSE_RANGE_COLOR = (0, 0, 0)

# keys
next_line = pygame.K_s  # press button s to move to next screen
previous_line = pygame.K_a  # press button a to go back to previous screen
zoom_in = pygame.K_d  # press d to zoom in (maximal value gets smaller)
zoom_out = pygame.K_e  # press e to zoom out (maximal value gets bigger)
delete_line = pygame.K_ESCAPE  # press ESC to delete the current picture
exit_key = pygame.K_q  # press q to exit the game at any moment

key_map = {next_line: "forward", previous_line: "backward", zoom_out: "out", zoom_in: "in", delete_line: "delete",
           exit_key: "getout"}

# program initializing starts!

pygame.init()
pygame.mixer.init()
error_sound = pygame.mixer.Sound("printer_sound.wav")
font_name = pygame.font.get_fonts()[0]  # change this if you do not like the font!!
my_screen = Screen(SCR_HEIGHT, TXT_HEIGHT, SCR_WIDTH, TXT_WIDTH, TXT_Y, TXT_X, SUSPENSE_HEIGHT, SUSPENSE_SPACE,
                   drawbox_background=BACKGROUND_COLOR, drawbox_text=SUSPENSE_RANGE_COLOR, drawbox_line=SUSPENSE_COLOR,
                   textbackground=TEXT_BACKGROUND_COLOR, memory_size=MEMORY_HEIGHT)
my_data = import_csv(CSV_NAME)
my_words = get_words(my_data)
my_words[0].set_color(TEXT_COLOR_1, TEXT_COLOR_2)
my_words[0].set_font(font_name, my_screen.textbox_height, 10)
compute_size_words(my_words)
my_screens, my_words = initialize(my_words, my_screen)
line_save(my_words, "line_file_cats.csv")
# print(my_screens)
# initialize Training screens in a similar way!

training_data = import_csv(training_csv)
training_words = get_words(training_data)
training_words[0].set_color(TEXT_COLOR_1, TEXT_COLOR_2)
training_words[0].set_font(font_name, my_screen.textbox_height, 10)
compute_size_words(training_words)
training_screens, training_words = initialize(training_words, my_screen, training=True)
# print(training_screens)

my_screens[0].memorybox.init_values(my_words)

# initialize allowed keys for the main session
for screen in my_screens:
    for key in [next_line, previous_line, zoom_in, zoom_out, delete_line, exit_key]:
        screen.set_allowed_key(key)
        screen.allow_mouse = True


for screen in training_screens:  # for the training, different keys are allowed on different training stages
    for key in [next_line, previous_line]:
        screen.set_allowed_key(key)
        screen.allow_mouse = False
    screen.memorybox.training = True

mouse_training = [1, 3, 4, 5, 6, 7]  # in these screens, the mouse can (and must) be moved.
for m in mouse_training:
    training_screens[m].allow_mouse = True

# individual handling of training screens, this defines which additional keys are allowed on various training screens
training_screens[4].set_allowed_key(zoom_in)
training_screens[5].set_allowed_key(zoom_out)
training_screens[6].set_allowed_key(delete_line)

data_list = meta_data_to_dict("cat", count_round)
meta = QuestionWindow("Deine Metadaten", data_list)
meta.display_questions()
meta.window.attributes("-topmost", True)
meta.window.mainloop()

for w in my_words:
    for i in range(len(meta.question_list)):
        w.properties[meta.question_list[i]["text"]] = meta.question_list[i]["result"]

display_surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
display_surface.fill(BACKGROUND_COLOR)

# implementing program parameters
if training_phase:
    current_screen = training_screens[0]
    run = 0
elif try_it:
    current_screen = my_screens[-3]  # set this to "training_screens[0] to start at the beginning"
    run = 1
else:
    current_screen = my_screens[0]
    run = 1

while run < 2:
    should_stop = False  # this turns true if the last screen is met or the game is quit. It helps escape the loop.
    # print("next screen", current_screen.next_screen)
    assert isinstance(current_screen, Screen)
    mouse_old_x, mouse_old_y = pygame.mouse.get_pos()
    while not should_stop:
        if not current_screen.shown:
            current_screen.show(display_surface)
            pygame.mouse.set_pos(current_screen.set_mouse())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in current_screen.allowed_keys:
                    next = current_screen.action(key_map[event.key])
                    if next == "play_error":
                        error_sound.play()
                    elif next == "no next screen found" or next == "getout":
                        run += 1
                        if run == 1:
                            DrawBox.current_max_y = 10
                            current_screen = my_screens[0]
                            current_screen.last_mouse_position_absolute = (current_screen.drawbox_x,
                                                                           current_screen.drawbox_y +
                                                                           current_screen.drawbox_height)
                            current_screen.last_mouse_position_relative = (0, current_screen.drawbox_height)
                            current_screen.last_mouse_position_value = 0
                            if current_screen.memorybox.training:
                                current_screen.restart_memorybox()
                        else:
                            pygame.quit()
                            should_stop = True
                        break
                    else:
                        current_screen = next
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # quit the program.
                    should_stop = True
                    break
            if pygame.mouse.get_pos() != (mouse_old_x, mouse_old_y):  # did the mouse move?
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # first check if the mouse is in the box
                    if current_screen.drawbox_x <= mouse_x <= current_screen.drawbox_width + current_screen.drawbox_x and \
                            current_screen.drawbox_y <= mouse_y <= current_screen.drawbox_height + current_screen.drawbox_y:
                        mouse_x = mouse_x - current_screen.drawbox_x
                        mouse_y = mouse_y - current_screen.drawbox_y
                        if mouse_x >= current_screen.get_mouse()[0]:
                            if current_screen.allow_mouse:
                                current_screen.drawbox.record_mouse(current_screen.get_mouse(), (mouse_x, mouse_y))
                                current_screen.change_last_mouse((mouse_x, mouse_y))
                                current_screen.shown = False
                                mouse_old_x, mouse_old_y = pygame.mouse.get_pos()
                        else:
                            pygame.mouse.set_pos(current_screen.set_mouse())
                else:
                    pygame.mouse.set_pos(current_screen.set_mouse())

questions = read_in_questions("questionaire2")
qu_1 = QuestionWindow("Fragebogen Teil 1", questions[0])
qu_1.display_questions()
qu_1.window.mainloop()
qu_2 = QuestionWindow("Fragebogen Teil 2", questions[1])
qu_2.display_questions(multiline=True)
qu_2.window.mainloop()
for w in my_words:
    for i in range(len(qu_1.question_list)):
        w.properties[qu_1.question_list[i]["text"]] = qu_1.question_list[i]["result"]
    for i in range(len(qu_2.question_list)):
        w.properties[qu_2.question_list[i]["text"]] = qu_2.question_list[i]["result"]
init_thanks()
save_and_compress(my_words, count_round, "cat_results.csv")
pygame.time.wait(100)
exit()
