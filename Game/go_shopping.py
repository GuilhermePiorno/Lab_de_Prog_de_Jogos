from PPlay.window import *
from EatThis.enemy_spawn import *
from EatThis.Classes.rolling_text import *
from random import *


def purchase_item(item, save):
    name = item[0]
    cost = item[1]
    save.credits -= cost
    if name == "speed":
        save.speed_upgrade += 1
    elif name == "vul_res":
        save.vuln_res += 0.1
    elif name == "grip_factor":
        save.grip_factor += 0.5
    elif name == "bomb amount":
        save.max_bombs += 1
    elif name == "bomb range":
        save.bomb_range_upgrade += 1
    elif name == "fireball ammo":
        save.fireball_ammo += 1
    elif name == "fireball speed":
        save.fireball_mult_spd += 0.1
    elif name == "teleport":
        save.has_teleport = 1
    elif name == "poison pill":
        save.has_poison_pill = 1


def measure_longest_message(msg, font_name='Assets/Fonts/MinimalPixel v2.ttf', size=24):
    longest = 0
    font = pygame.font.Font(font_name, size)
    for i in range(len(msg)):
        snip = font.render(msg[i], True, 'white')
        if longest < snip.get_width():
            longest = snip.get_width()
    return longest


def talk(who, what, janela, text_box, font_name='Assets/Fonts/MinimalPixel v2.ttf', size=24):
    # Retrato de quem fala.
    if who.lower() == 'shopkeeper':
        speaker_portrait = Sprite('Assets/Sprites/Characters/Shopkeeper_Portrait_Simple_BIG.png', 1)
        what.insert(0, "Shopkeeper: ")
    else:
        what.insert(0, "Blinky: ")
        speaker_portrait = Sprite("Assets/Sprites/Characters/Blinky_Portrait_02_Simple_BIG.png", 1)
    speaker_portrait.set_position(60, 70)
    speaker_portrait.draw()

    # Transforma vetor de texto em vetor de superfícies.
    fonte = pygame.font.Font(font_name, size)
    for i in range(len(what)):
        what[i] = fonte.render(what[i], True, 'white')

    # posições das linhas.
    pos_linha = []
    for i in range(6):
        pos_linha.append(((janela.width - text_box.width) / 2 + 180, 80 + 30 * i))

    # Dá 'blit' nas linhas de texto.
    for i in range(len(what)):
        janela.screen.blit(what[i], pos_linha[i])


def get_possible_upgrades(save, stock_size):
    set_upgrades = {"speed", "vul_res", "grip_factor", "teleport", "poison pill"}
    # 2 upgrades + 1 persistent offer.
    if save.has_bomb_ability:
        set_upgrades.update({"bomb amount", "bomb range"})
    if save.has_fireball_ability:
        set_upgrades.update({"fireball ammo", "fireball speed"})

    shopping_list = []
    for i in range(stock_size):
        random_upgrade = choices(list(set_upgrades))[0]
        set_upgrades = set_upgrades - {random_upgrade}
        shopping_list.append([random_upgrade])

    return shopping_list


def get_shop_inventory(save):
    price_table = {
        "speed": 100,
        "vul_res": 1,
        "grip_factor": 1,
        "bomb amount": 1,
        "bomb range": 1,
        "fireball ammo": 1,
        "fireball speed": 1,
        "teleport": 1,
        "poison pill": 1
    }
    stock_size = 3  # alterar stocksize não está implementando, foi implementado para compatibilidade futura.
    offer_list = get_possible_upgrades(save, stock_size)
    for i in range(stock_size):
        offer_list[i].append(price_table[offer_list[i][0]])

    return offer_list


def go_shopping(screen_width, screen_height, save):
    save.credits += 99
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    credits_string = f"credits: {save.credits}"
    credits_surface = font.render(credits_string, True, 'white')
    shop_inventory = get_shop_inventory(save)
    image_correspondence = {
        "speed": "speed_up.png",
        "vul_res": "vulnerability_res.png",
        "grip_factor": "boots_spiked_box.png",
        "bomb amount": "bomb_box.png",
        "bomb range": "bomb_upgrade_box.png",
        "fireball ammo": "fireball_box.png",
        "fireball speed": "fireball_speed_box.png",
        "teleport": "teleport.png",
        "poison pill": "Poison_Pill.png"
    }

    tempo = 0
    tic = 0
    print_char_count = 0
    text_speed = 50  # character per second
    base_speed = 300
    is_done_printing = False
    janela = Window(screen_width, screen_height)
    janela.set_title("Shop Time!")
    active_message = 0
    messages = [
        ["The quick brown fox jumps over the lazy dog.", "The slow black dog bows before the regal fox.", "Get it?."],
        ["I'm the shopkeeper. I sell stuff.", "You buy stuff.", "Simple as that.", "I'm not a very good shopkeeper."],
        ["Why do programmers always mix up Halloween and Christmas?", "Because Oct 31 == Dec 25."],
        ["To understand what recursion is, you must first understand recursion."]
    ]

    teclado = janela.get_keyboard()
    in_dialogue_area = False
    in_dialogue = False
    esc_pressed = False
    enter_pressed = False
    right_pressed = False
    left_pressed = False
    song_start = "Assets/Music/Shop_Start.mp3"
    bgm_start = Sound(song_start)
    bgm_start.set_volume(save.BGM_vol * save.Master_vol)
    bgm_start.set_repeat(False)
    bgm_start.play()
    song_loop = "Assets/Music/Shop_Loop.mp3"
    bgm_loop = Sound(song_loop)
    bgm_loop.set_volume(save.BGM_vol * save.Master_vol)
    bgm_loop.set_repeat(True)

    select_sound = Sound("Assets/SFX/Shop_Select.ogg")
    select_sound.set_volume(save.SFX_vol * save.Master_vol)
    select_sound.set_repeat(False)

    confirm_sound = Sound("Assets/SFX/Shop_Confirm_Echo.ogg")
    confirm_sound.set_volume(save.SFX_vol * save.Master_vol)
    confirm_sound.set_repeat(False)

    deny_sound = Sound("Assets/SFX/Shop_Deny_Echo.ogg")
    deny_sound.set_volume(save.SFX_vol * save.Master_vol)
    deny_sound.set_repeat(False)

    # ============layer 0=================SPACE=========================================================================
    # Background
    background = Sprite("Assets/Sprites/Shop/Background_Sky.png", 2)
    background.set_sequence_time(0, 2, 1000, True)
    background.set_curr_frame(0)
    # ============layer 1================3D WALLS=======================================================================
    # Background Walls
    bg_walls = Sprite("Assets/Sprites/Shop/Background_Walls.png", 2)
    bg_walls.set_sequence_time(0, 2, 1000, True)
    bg_walls.set_curr_frame(0)
    # ============layer 2===============================================================================================
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
    # ============layer 3===============================================================================================
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
    # ============layer 4===============================================================================================
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
    # ============layer 5===============================================================================================
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
    text_box.set_position((janela.width - text_box.width) / 2, 50)
    text_box.set_sequence_time(0, 7, 50, False)
    text_box.stop()

    # Shopkeeper Portrait
    shopkeeper_portrait = Sprite("Assets/Sprites/Characters/Shopkeeper_Portrait_Simple_BIG.png", 1)
    shopkeeper_portrait.set_position((janela.width - text_box.width) / 2 + 20, 70)

    # Blinky Portrait
    blinky_portrait = Sprite("Assets/Sprites/Characters/Blinky_Portrait_02_Simple.png", 1)
    blinky_portrait.set_position((janela.width - text_box.width) / 2, 50)

    # Blinky's Sprite
    blinky = Sprite("Assets/Sprites/Characters/Blinky_Shop.png", 12)
    blinky.set_position(50, 625)
    blinky.set_sequence_time(0, 12, 100, True)
    blinky.set_sequence(0, 1, True)
    blinky_speed = 0
    facing = "afk"

    # Shop Cursor
    shop_cursor = Sprite("Assets/Sprites/Shop/Shop_Cursor_BIG2.png", 3)
    shop_cursor.set_sequence_time(0, 3, 700, True)

    upgrade_selection = 0
    num_options = 3

    chat_depth = 0
    while True:
        greetings1 = ["Hi there little one!"]
        greetings2 = ["..."]
        greetings3 = ["Anyway... can I help you with something?"]

        if tempo >= 58 and not bgm_loop.is_playing():
            bgm_loop.play()

        dt = janela.delta_time()
        if dt > 0.1:
            dt = 0
        tempo += dt

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
        if 500 < blinky.x < 720 and not in_dialogue_area:
            in_dialogue_area = True
        if (500 > blinky.x or blinky.x > 720) and in_dialogue_area:
            in_dialogue_area = False

        # Shows bubble when in dialogue area
        if in_dialogue_area and not in_dialogue:
            chat_bubble.unhide()
        else:
            chat_bubble.hide()

        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_input management/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
        # /_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # ===================Manages "Esc" keypress
        if not teclado.key_pressed("esc"):
            esc_pressed = False

        if teclado.key_pressed("esc") and not esc_pressed and in_dialogue:
            esc_pressed = True
            upgrade_selection = 0
            if chat_depth == 3:
                text_box.set_sequence_time(7, 13, 50, False)
                text_box.play()
                in_dialogue = False
                chat_depth = 0
            else:
                chat_depth = 3

        # ===================Manages "Enter" keypress
        if not teclado.key_pressed("enter"):
            enter_pressed = False

        if teclado.key_pressed("enter") and not enter_pressed:
            enter_pressed = True
            if in_dialogue and chat_depth == 3:
                item_purchased = shop_inventory[upgrade_selection][0]
                item_cost = shop_inventory[upgrade_selection][1]
                if item_cost <= save.credits:
                    confirm_sound.play()
                    purchase_item(shop_inventory[upgrade_selection], save)
                else:
                    deny_sound.play()

                print(upgrade_selection)
                print(f"upgrade: {item_purchased}, price: {item_cost}")
            if in_dialogue and chat_depth < 3:  # Limita o "Enter" de navegar o chat a partir até as escolhas de upgrade
                chat_depth += 1

        # ===================Manages "Side Arrows" keypress
        if not in_dialogue:
            if teclado.key_pressed("right"):
                blinky_speed = base_speed
            if teclado.key_pressed("left"):
                blinky_speed = -base_speed

        # ==== In Dialogue Right
        if not teclado.key_pressed("right"):
            right_pressed = False

        if not right_pressed and teclado.key_pressed("right"):
            right_pressed = True
            # print(right_pressed)
            if chat_depth == 3:
                select_sound.play()
                upgrade_selection = (upgrade_selection + 1) % 3

        # ==== In Dialogue Left
        if not teclado.key_pressed("left"):
            left_pressed = False

        if not left_pressed and teclado.key_pressed("left"):
            left_pressed = True
            # print(left_pressed)
            if chat_depth == 3:
                select_sound.play()
                upgrade_selection = (upgrade_selection - 1) % 3

        # ===================Manages "Up Arrows" keypress
        # Animação de olhar para o Shopkeeper
        if in_dialogue_area and teclado.key_pressed("up") and not in_dialogue:
            text_box.set_sequence_time(0, 7, 50, False)
            text_box.play()
            in_dialogue = True  # Updates in_dialogue variable
            if blinky.x < 640:
                blinky.set_sequence(4, 6, True)  # Sets blinky's sequence to up-right look
            else:
                blinky.set_sequence(6, 8, True)  # Sets blinky's sequence to up-left look

        time_after_last_char_print = tempo - tic
        if in_dialogue and time_after_last_char_print > (1 / text_speed):
            tic = tempo  # reseta referencial.
            print_char_count += 1

        # Set Screen Boundries
        if blinky.x <= 0:
            blinky.x = 0

        if blinky.x >= 1215:
            bgm_start.stop()
            bgm_start.pause()
            bgm_loop.stop()
            bgm_loop.pause()
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

        credits_string = f"credits: {save.credits}"
        credits_surface = font.render(credits_string, True, 'white')
        janela.screen.blit(credits_surface, (930, 680))

        if in_dialogue and not text_box.is_playing():
            if chat_depth == 0:
                talk("Shopkeeper", greetings1, janela, text_box)
            elif chat_depth == 1:
                talk("Blinky", greetings2, janela, text_box)
            elif chat_depth == 2:
                talk("Shopkeeper", greetings3, janela, text_box)
            elif chat_depth == 3:
                # Shop Items
                for i in range(3):
                    price_str = f"{shop_inventory[i][1]} cred"
                    price_surface = font.render(price_str, True, 'white')
                    janela.screen.blit(price_surface, (310 + 300 * i, 110))
                    item = Sprite(f"Assets/Sprites/UI Icons/{image_correspondence[shop_inventory[i][0]]}")
                    item.set_position(340 + 300 * i, 155)
                    item.draw()

                # Shop Cursor
                shop_cursor.set_position(300 + 300 * upgrade_selection, 150)
                shop_cursor.draw()
                shop_cursor.update()

        janela.update()
