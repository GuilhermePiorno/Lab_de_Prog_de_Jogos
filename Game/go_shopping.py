from PPlay.window import *
from EatThis.enemy_spawn import *
from EatThis.Classes.rolling_text import *


def measure_longest_message(msg, font_name='Assets/Fonts/MinimalPixel v2.ttf', size=24):
    longest = 0
    font = pygame.font.Font(font_name, size)
    for i in range(len(msg)):
        snip = font.render(msg[i], True, 'white')
        if longest < snip.get_width():
            longest = snip.get_width()
    return longest




def go_shopping(screen_width, screen_height, save):
    tempo = 0
    tic = 0
    print_char_count = 0
    text_speed = 50   # character per second
    base_speed = 300
    is_done_printing = False
    janela = Window(screen_width, screen_height)
    janela.set_title("Shop Time!")
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    active_message = 0
    messages = [
        ["The quick brown fox jumps over the lazy dog.", "The slow black dog bows before the regal fox.", "Get it?."],
        ["I'm the shopkeeper. I sell stuff.", "You buy stuff.", "Simple as that.", "I'm not a very good shopkeeper."],
        ["Why do programmers always mix up Halloween and Christmas?", "Because Oct 31 == Dec 25."],
        ["To understand what recursion is, you must first understand recursion."]
    ]
    test_length = "loooooooooooooooooooooooooooooooooooooooooooooooooooooooooongest message"
    sample_text = ["Shopkeeper: ", "Hi, I'm the shopkeeper!", "Well, I actually work at the ship's warehouse, but I can sell you stuff."]
    teclado = janela.get_keyboard()
    in_dialogue_area = False
    in_dialogue = False
    enter_released = False


    #============layer 0=================SPACE==========================================================================
    # Background
    background = Sprite("Assets/Sprites/Shop/Background_Sky.png", 2)
    background.set_sequence_time(0, 2, 1000, True)
    background.set_curr_frame(0)
    # ============layer 1================3D WALLS========================================================================
    # Background Walls
    bg_walls = Sprite("Assets/Sprites/Shop/Background_Walls.png", 2)
    bg_walls.set_sequence_time(0, 2, 1000, True)
    bg_walls.set_curr_frame(0)
    # ============layer 2================================================================================================
    # Rightside Portal
    portal_r = Sprite("Assets/Sprites/Shop/Portal_R.png", 4)
    portal_r.set_sequence_time(0, 4, 200, True)
    portal_r.set_position(1156, 475)

    # Leftside Portal
    portal_l = Sprite("Assets/Sprites/Shop/Portal_L.png", 4)
    portal_l.set_sequence_time(0, 4, 200, True)
    portal_l.set_position(50, 475)

    # Shopkeeper
    shopkeeper = Sprite("Assets/Sprites/Characters/Shopkeeper.png", 3)
    shopkeeper.set_sequence_time(0, 3, 1000, True)
    shopkeeper.set_position(640, 525)

    # Chat Bubble
    chat_bubble = Sprite("Assets/Sprites/Shop/chat2.png", 2)
    chat_bubble.set_sequence_time(0, 2, 1000, True)
    chat_bubble.set_position(630, 500)

    # JukeBox
    jukebox = Sprite("Assets/Sprites/Shop/Jukebox.png", 1)
    jukebox.set_position(850, 400)

    # Bookshelf
    bookshelf = Sprite("Assets/Sprites/Shop/Bookshelf.png", 1)
    bookshelf.set_position(700, 450)

    # Locker
    locker = Sprite("Assets/Sprites/Shop/Locker.png", 1)
    locker.set_position(250, 420)
    # ============layer 3================================================================================================
    # Broom
    broom = Sprite("Assets/Sprites/Shop/Broom.png", 1)
    broom.set_position(350, 500)

    # Rightside Half Portal
    portal_r_half = Sprite("Assets/Sprites/Shop/Portal_R_Half.png", 4)
    portal_r_half.set_sequence_time(0, 4, 200, True)
    portal_r_half.set_position(1156, 475)

    # Leftside Half Portal
    portal_l_half = Sprite("Assets/Sprites/Shop/Portal_L_Half.png", 4)
    portal_l_half.set_sequence_time(0, 4, 200, True)
    portal_l_half.set_position(50, 475)

    # Shop Counter
    shop_counter = Sprite("Assets/Sprites/Shop/ShopCounter.png", 1)
    shop_counter.set_position(503, 575)
    # ============layer 4================================================================================================
    # Rightside Shop Door
    shop_door_r = Sprite("Assets/Sprites/Shop/ShopDoor_R.png", 1)
    shop_door_r.set_position(1056, 400)
    shop_door_r.set_curr_frame(0)

    # Leftside Shop Door
    shop_door_l = Sprite("Assets/Sprites/Shop/ShopDoor_L.png", 1)
    shop_door_l.set_position(-2, 400)
    shop_door_l.set_curr_frame(0)

    # Shop Counter Item 1
    shop_counter_item_1 = Sprite("Assets/Sprites/Shop/ShopCounterItems.png", 1)
    shop_counter_item_1.set_position(515, 500)
    # ============layer 5================================================================================================
    # Rightside Shop Door Front
    shop_door_r_front = Sprite("Assets/Sprites/Shop/ShopDoorFront_R.png", 1)
    shop_door_r_front.set_position(1056, 400)
    shop_door_r_front.set_curr_frame(0)

    # Leftside Shop Door Front
    shop_door_l_front = Sprite("Assets/Sprites/Shop/ShopDoorFront_L.png", 1)
    shop_door_l_front.set_position(-2, 400)
    shop_door_l_front.set_curr_frame(0)

    # Caixa de texto
    text_box = Sprite("Assets/Sprites/Shop/Text_Box_Sprites_Transparency.png", 13)
    text_box.set_position((janela.width - text_box.width)/2, 50)
    text_box.set_sequence_time(0, 7, 50, False)
    text_box.stop()

    # Shopkeeper Portrait
    shopkeeper_portrait = Sprite("Assets/Sprites/Characters/Shopkeeper_Portrait_Simple_BIG.png", 1)
    shopkeeper_portrait.set_position((janela.width - text_box.width)/2 + 20, 70)

    # Blinky Portrait
    blinky_portrait = Sprite("Assets/Sprites/Characters/Blinky_Portrait_02_Simple.png", 1)
    blinky_portrait.set_position((janela.width - text_box.width) / 2, 50)

    blinky = Sprite("Assets/Sprites/Characters/Blinky_Shop.png", 12)
    blinky.set_position(50, 625)
    blinky.set_sequence_time(0, 12, 100, True)
    blinky.set_sequence(0, 1, True)
    blinky_speed = 0
    facing = "afk"


    while True:
        dt = janela.delta_time()
        if dt > 0.1:
            dt = 0
        tempo += dt

        if not teclado.key_pressed("enter"):
            enter_released = False




        if not in_dialogue:
            if teclado.key_pressed("right"):
                blinky_speed = base_speed
            if teclado.key_pressed("left"):
                blinky_speed = -base_speed

        if not teclado.key_pressed("right") and not teclado.key_pressed("left"):
            blinky_speed = 0

        if not in_dialogue:
            if blinky_speed < 0 and facing != 'L':
                facing = 'L'
                blinky.set_sequence(2, 4, True)
            if blinky_speed > 0 and facing != 'R':
                facing = 'R'
                blinky.set_sequence(0, 2, True)
            if facing != 'UR' and facing == 'R' and teclado.key_pressed("up"):
                facing = 'UR'
                blinky.set_sequence(4, 6, True)
            if facing != 'UL' and facing == 'L' and teclado.key_pressed("up"):
                facing = 'UL'
                blinky.set_sequence(6, 8, True)
            if facing == 'UR' and not teclado.key_pressed("up"):
                facing = 'R'
                blinky.set_sequence(0, 2, True)
            if facing == 'UL' and not teclado.key_pressed("up"):
                facing = 'L'
                blinky.set_sequence(2, 4, True)


        # Resolve in_dialogue_area switch
        if 575 < blinky.x < 720 and not in_dialogue_area:
            in_dialogue_area = True
        if  (575 > blinky.x or blinky.x > 720) and in_dialogue_area:
            in_dialogue_area = False

        # Shows bubble when in dialogue area
        if in_dialogue_area and not in_dialogue:
            chat_bubble.unhide()
        else:
            chat_bubble.hide()

        # Detecta Enter.
        if enter_released == False and teclado.key_pressed("enter"):
            enter_released = True
            print(enter_released)

        # Animação de olhar para o Shopkeeper
        if in_dialogue_area and teclado.key_pressed("up") and not in_dialogue:
            text_box.set_sequence_time(0, 7, 50, False)
            text_box.play()
            in_dialogue = True                      # Updates in_dialogue variable
            if blinky.x < 640:
                blinky.set_sequence(4, 6, True)         # Sets blinky's sequence to up-right look
            else:
                blinky.set_sequence(6, 8, True)         # Sets blinky's sequence to up-left look


        if teclado.key_pressed("esc"):
            text_box.set_sequence_time(7, 13, 50, False)
            text_box.play()
            in_dialogue = False

        snip0 = font.render("Shopkeeper: ", True, "white")
        snip = font.render(test_length, True, "white")




        time_after_last_char_print = tempo - tic
        if in_dialogue and time_after_last_char_print > (1 / text_speed):
            tic = tempo                 # reseta referencial.
            print_char_count += 1


        list_page_lenghts = []
        for page in messages:
            chars_in_page = 0
            for line in page:
                chars_in_page += len(line)
            list_page_lenghts.append(chars_in_page)


        # snip = font.render(messages[active_message][0:print_char_count], True, 'white')





        # # Dialogue
        # if in_dialogue_area and teclado.key_pressed("up") and not in_dialogue:
        #     in_dialogue = True                      # Updates in_dialogue variable
        #     if blinky.x < 640:
        #         blinky.set_sequence(4, 6, True)         # Sets blinky's sequence to up-right look
        #     else:
        #         blinky.set_sequence(6, 8, True)         # Sets blinky's sequence to up-left look
        #
        #
        # # resets print_char_count, active_message, and is_done_printing after "enter" is pressed.
        # if enter_released and in_dialogue and is_done_printing and active_message < len(messages) -1:
        #     print_char_count = 0
        #     active_message += 1
        #     is_done_printing = False
        #
        #
        #
        # tempo_por_char = tempo - tic
        # if in_dialogue and tempo_por_char > (1 / text_speed) and print_char_count < len(messages[active_message]):
        #     tic = tempo             # reseta marcador de tempo.
        #     print_char_count += 1   # Avança um caractere para impressão.
        # elif print_char_count >= len(messages[active_message]) and not is_done_printing:
        #     is_done_printing = True
        #
        # snip = font.render(messages[active_message][0:print_char_count], True, 'white')
        #
        #
        # if is_done_printing and in_dialogue and enter_released and active_message == len(messages) - 1:
        #     in_dialogue = False
        #
        # if teclado.key_pressed("esc"):
        #     in_dialogue = False



























        # Set Screen Boundries
        if blinky.x <= 0:
            blinky.x = 0

        if blinky.x >= 1215:
            save.stage_no += 1
            return ["play", save]


        # Background
        background.draw()
        # Background Walls
        bg_walls.draw()
        # Rightside Portal
        portal_r.draw()
        portal_r.update()
        # Leftside Portal
        portal_l.draw()
        portal_l.update()
        # Shopkeeper
        shopkeeper.draw()
        shopkeeper.update()
        # Dialogue Bubble
        chat_bubble.draw()
        chat_bubble.update()
        # JukeBox
        jukebox.draw()
        # Bookshelf
        bookshelf.draw()
        # Shop Counter
        shop_counter.draw()
        # Shop Locker
        locker.draw()
        # Broom
        broom.draw()


        # Rightside Shop Door
        shop_door_r.draw()
        # Leftside Shop Door
        shop_door_l.draw()
        # Shop Counter Item 1
        shop_counter_item_1.draw()


        # Blinky
        blinky.x += blinky_speed * dt
        blinky.update()
        blinky.draw()


        # Rightside Shop Door Front
        shop_door_r_front.draw()

        # Leftside Shop Door Front
        shop_door_l_front.draw()

        # caixa de texto
        text_box.update()
        text_box.draw()



        # longest_msg = measure_longest_message(messages)
        # janela.screen.blit(snip, ((janela.width - longest_msg)/2, 360))



        if in_dialogue and not text_box.is_playing():
            shopkeeper_portrait.draw()
            teste = [snip0, snip, snip, snip, snip0, snip]
            for i in range(len(teste)):
                if snip.get_width() > 1000:
                    print(f"Text {i} is too long ({snip.get_width()}")
                janela.screen.blit(teste[i], ((janela.width - text_box.width) / 2 + 180, 80 + 30*i))





        janela.update()




