from PPlay.window import *
from EatThis.enemy_spawn import *
from EatThis.Classes.rolling_text import *
from random import *


def can_purchase(save, shop_inventory, selection):
    upgrade_ceiling = {
        "speed": 5,
        "vul_res": 0.5,
        "grip_factor": 5,
        "bomb amount": 9,
        "bomb range": 9,
        "fireball ammo": 9,
        "fireball speed": 1.5,
        "teleport": 1,
        "poison pill": 1,
        "piggy_bank": 0.5,
        "bullet_time": 1,
        "reverse_states": 5,
        "fireball": 1,
        "bomb": 1,
        "shoes":1
    }

    attribute = shop_inventory[selection][0]
    max_values = upgrade_ceiling[attribute]

    if attribute == "speed":
        if save.speed_upgrade < max_values:
            return True
        else:
            return False

    if attribute == "vul_res":
        if save.vuln_res < max_values:
            return True
        else:
            return False

    if attribute == "grip_factor":
        if save.grip_factor < max_values:
            return True
        else:
            return False

    if attribute == "bomb amount":
        if save.max_bombs < max_values:
            return True
        else:
            return False

    if attribute == "bomb range":
        if save.bomb_range_upgrade < max_values:
            return True
        else:
            return False

    if attribute == "fireball ammo":
        if save.fireball_ammo < max_values:
            return True
        else:
            return False

    if attribute == "fireball speed":
        if save.fireball_mult_spd < max_values:
            return True
        else:
            return False

    if attribute == "teleport":
        if not save.has_teleport:
            return True
        else:
            return False

    if attribute == "poison pill":
        if not save.has_poison_pill:
            return True
        else:
            return False

    if attribute == "piggy_bank":
        if save.piggy_bank < max_values:
            return True
        else:
            return False

    if attribute == "bullet_time":
        if save.has_bullet_time < max_values:
            return True
        else:
            return False

    if attribute == "reverse_states":
        if save.reverse_state < max_values:
            return True
        else:
            return False

    if attribute == "fireball":
        if not save.has_fireball_ability:
            return True
        else:
            return False

    if attribute == "bomb":
        if not save.has_bomb_ability:
            return True
        else:
            return False

    if attribute == "shoes":
        if not save.has_shoes:
            return True
        else:
            return False



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
    elif name == "piggy_bank":
        save.piggy_bank += 0.1
    elif name == "bullet_time":
        save.has_bullet_time = 1
    elif name == "reverse_states":
        save.reverse_state += 1
    elif name == "fireball":
        save.has_fireball_ability = 1
    elif name == "bomb":
        save.has_bomb_ability = 1
    elif name == "shoes":
        save.has_shoes = 1


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
    set_upgrades = {"speed",
                    "vul_res",
                    "teleport",
                    "poison pill",
                    "piggy_bank",
                    "bullet_time",
                    "reverse_states",
                    "fireball",
                    "bomb",
                    "shoes"
                    }

    if save.has_bomb_ability:
        set_upgrades.update({"bomb amount", "bomb range"})
    if save.has_fireball_ability:
        set_upgrades.update({"fireball ammo", "fireball speed"})
    if save.has_shoes:
        set_upgrades.update({"grip_factor"})

    shopping_list = []
    for i in range(stock_size):
        random_upgrade = choices(list(set_upgrades))[0]
        set_upgrades = set_upgrades - {random_upgrade}
        shopping_list.append([random_upgrade])

    return shopping_list


def get_shop_inventory(save, stock_size):
    price_table = {
        "speed": 100,
        "vul_res": 10,
        "grip_factor": 10,
        "bomb amount": 10,
        "bomb range": 10,
        "fireball ammo": 10,
        "fireball speed": 10,
        "teleport": 10,
        "poison pill": 10,
        "piggy_bank":200,
        "bullet_time":100,
        "reverse_states": 300,
        "bomb": 500,
        "fireball": 500,
        "shoes": 500
    }
    offer_list = get_possible_upgrades(save, stock_size)
    for i in range(stock_size):
        offer_list[i].append(price_table[offer_list[i][0]])

    return offer_list


def go_shopping(screen_width, screen_height, save):
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    offer_qty = 4 # stock size
    shop_inventory = get_shop_inventory(save, offer_qty)
    image_correspondence = {
        "speed": "speed_up.png",
        "vul_res": "vulnerability_res.png",
        "grip_factor": "boots_spiked_box.png",
        "bomb amount": "bomb_box.png",
        "bomb range": "bomb_upgrade_box.png",
        "fireball ammo": "fireball_box.png",
        "fireball speed": "fireball_speed_box.png",
        "teleport": "teleport.png",
        "poison pill": "Poison_Pill.png",
        "piggy_bank": "Piggy_Bank.png",
        "bullet_time": "bullet_time_box.png",
        "reverse_states": "reverse_states0.png",
        "bomb": "bomb_box.png",
        "fireball":"fireball_box.png",
        "shoes":"boots_box.png"
    }

    tempo = 0
    tic = 0
    print_char_count = 0
    text_speed = 50  # character per second
    base_speed = 300
    janela = Window(screen_width, screen_height)
    janela.set_title("Shop Time!")
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
    song_start = "Assets/Music/Shop_Start.ogg"
    bgm_start = Sound(song_start)
    bgm_start.set_volume(save.BGM_vol * save.Master_vol)
    bgm_start.set_repeat(False)
    bgm_start.play()
    song_loop = "Assets/Music/Shop_Loop.ogg"
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
                item_selected = shop_inventory[upgrade_selection][0]
                item_cost = shop_inventory[upgrade_selection][1]
                if item_cost <= save.credits and can_purchase(save, shop_inventory, upgrade_selection):
                    confirm_sound.play()
                    purchase_item(shop_inventory[upgrade_selection], save)
                else:
                    deny_sound.play()

                print(upgrade_selection)
                print(f"upgrade: {item_selected}, price: {item_cost}")
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
                upgrade_selection = (upgrade_selection + 1) % offer_qty

        # ==== In Dialogue Left
        if not teclado.key_pressed("left"):
            left_pressed = False

        if not left_pressed and teclado.key_pressed("left"):
            left_pressed = True
            # print(left_pressed)
            if chat_depth == 3:
                select_sound.play()
                upgrade_selection = (upgrade_selection - 1) % offer_qty

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

        # ==============================================================================================================
        # UPGRADE ICONS
        upgrade_draw_list = []

        if save.speed_upgrade > 0:
            speed_increase_icon = Sprite("Assets/Sprites/UI Icons/speed_up.png")
            speed_increase_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            speed_increase_level = Sprite("Assets/Sprites/UI Icons/amount_box_black_and_white_borders.png", 10)
            speed_increase_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            speed_increase_level.set_curr_frame(save.speed_upgrade)
            upgrade_draw_list.append(speed_increase_icon)
            upgrade_draw_list.append(speed_increase_level)

        if save.has_shoes:
            boots = Sprite("Assets/Sprites/UI Icons/boots_box.png")
            boots.set_position(370 + len(upgrade_draw_list) * 22, 670)
            upgrade_draw_list.append(boots)
            upgrade_draw_list.append(boots)

        if 1 < save.grip_factor < 99:
            grip_icon = Sprite("Assets/Sprites/UI Icons/boots_spiked_box.png")
            grip_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon = Sprite("Assets/Sprites/UI Icons/amount_box_up.png", 10)
            grip_level_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon.set_curr_frame((save.grip_factor - 1) // 0.5)
            upgrade_draw_list.append(grip_icon)
            upgrade_draw_list.append(grip_level_icon)
        elif save.grip_factor == 100:
            grip_icon = Sprite("Assets/Sprites/UI Icons/golden_boots_spiked_box.png")
            grip_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon = Sprite("Assets/Sprites/UI Icons/amount_box_max.png", 2)
            grip_level_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon.set_curr_frame(1)
            upgrade_draw_list.append(grip_icon)
            upgrade_draw_list.append(grip_level_icon)

        if save.has_bomb_ability:
            # bomb enable icon
            bomb_box = Sprite("Assets/Sprites/UI Icons/bomb_box.png")
            bomb_box.set_position(370 + len(upgrade_draw_list) * 22, 670)
            # bomb max quantity
            bomb_amount = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            bomb_amount.set_position(370 + len(upgrade_draw_list) * 22, 670)
            bomb_amount.set_curr_frame(save.max_bombs)
            upgrade_draw_list.append(bomb_box)
            upgrade_draw_list.append(bomb_amount)
            b_range = Sprite("Assets/Sprites/UI Icons/bomb_upgrade_box.png")
            b_range.set_position(370 + len(upgrade_draw_list) * 22, 670)
            b_range_level = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            b_range_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            b_range_level.set_curr_frame(save.bomb_range_upgrade + 1)
            upgrade_draw_list.append(b_range)
            upgrade_draw_list.append(b_range_level)

        if save.has_fireball_ability:
            fireball_icon = Sprite("Assets/Sprites/UI Icons/fireball_box.png")
            fireball_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_ammo = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            fireball_ammo.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_ammo.set_curr_frame(save.fireball_ammo)
            upgrade_draw_list.append(fireball_icon)
            upgrade_draw_list.append(fireball_ammo)

        if save.fireball_mult_spd > 1:
            fireball_spd_icon = Sprite("Assets/Sprites/UI Icons/fireball_speed_box.png")
            fireball_spd_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_spd_level = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            fireball_spd_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_spd_level.set_curr_frame((save.fireball_mult_spd - 1) // 0.1)
            upgrade_draw_list.append(fireball_spd_icon)
            upgrade_draw_list.append(fireball_spd_level)

        if save.vuln_res != 0:
            vulnerability_res = Sprite("Assets/Sprites/UI Icons/vulnerability_res2.png")
            vulnerability_res.set_position(370 + len(upgrade_draw_list) * 22, 670)
            resistance_level = Sprite("Assets/Sprites/UI Icons/amount_box_down.png", 10)
            resistance_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            resistance_level.set_curr_frame(save.vuln_res * 10)
            upgrade_draw_list.append(vulnerability_res)
            upgrade_draw_list.append(resistance_level)

        if save.has_poison_pill != 0:
            poison_pill = Sprite("Assets/Sprites/UI Icons/Poison_Pill.png")
            poison_pill.set_position(370 + len(upgrade_draw_list) * 22, 670)
            upgrade_draw_list.append(poison_pill)
            upgrade_draw_list.append(poison_pill)

        if save.has_teleport != 0:
            teleport_ability = Sprite("Assets/Sprites/UI Icons/teleport.png")
            teleport_ability.set_position(370 + len(upgrade_draw_list) * 22, 670)
            upgrade_draw_list.append(teleport_ability)
            upgrade_draw_list.append(teleport_ability)

        if save.piggy_bank != 0:
            piggy_bank_icon = Sprite("Assets/Sprites/UI Icons/Piggy_Bank.png")
            piggy_bank_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            piggy_bank_level = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            piggy_bank_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            piggy_bank_level.set_curr_frame(1 + save.piggy_bank // 0.1)
            upgrade_draw_list.append(piggy_bank_icon)
            upgrade_draw_list.append(piggy_bank_level)

        if save.has_bullet_time != 0:
            bullet_time_icon = Sprite("Assets/Sprites/UI Icons/bullet_time_box.png")
            bullet_time_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            upgrade_draw_list.append(bullet_time_icon)
            upgrade_draw_list.append(bullet_time_icon)

        if save.reverse_state != 0:
            reverse_icon = Sprite("Assets/Sprites/UI Icons/reverse_states0.png")
            reverse_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            reverse_amount_icon = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            reverse_amount_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            reverse_amount_icon.set_curr_frame(save.reverse_state)
            upgrade_draw_list.append(reverse_icon)
            upgrade_draw_list.append(reverse_amount_icon)
        # ==============================================================================================================

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

        # draw da lista de upgrades
        for item in upgrade_draw_list:
            item.draw()

        credits_string = f"credits: {save.credits}"
        credits_surface = font.render(credits_string, True, 'white')
        janela.screen.blit(credits_surface, (930, 680))
        item_descriptions = {
            "speed": "Aumento de velocidade.",
            "vul_res": "Reduz tempo de vulnerabildade.",
            "grip_factor": "Aumenta velocidade de meia-volta.",
            "bomb amount": "Aumenta quantia máxima de bombas ao mesmo tempo.",
            "bomb range": "Aumenta alcance das bombas.",
            "fireball ammo": "+1 para cargas de tiros.",
            "fireball speed": "Aumento de velocidade do tiro.",
            "teleport": "Habilidade de teletransporte",
            "poison pill": "Habilidade de pilula de veneno",
            "piggy_bank": "Habilidade permanente: Guarda uma parcela dos creditos ao morrer.",
            "bullet_time": "\"There is no spoon\"",
            "reverse_states": "Habilidade: Troca imediatamente estado de vulnerabilidade (com cargas).",
            "fireball": "Fireball Ability",
            "bomb": "Ability to plant bombs!",
            "shoes": "Get your shoes on!"
        }

        if in_dialogue and not text_box.is_playing():
            if chat_depth == 0:
                talk("Shopkeeper", greetings1, janela, text_box)
            elif chat_depth == 1:
                talk("Blinky", greetings2, janela, text_box)
            elif chat_depth == 2:
                talk("Shopkeeper", greetings3, janela, text_box)
            elif chat_depth == 3:
                # Shop Items
                for i in range(offer_qty):
                    price_str = f"{shop_inventory[i][1]} cred"
                    price_surface = font.render(price_str, True, 'white')
                    janela.screen.blit(price_surface, (310 + 600/(offer_qty-1) * i, 110))
                    item = Sprite(f"Assets/Sprites/UI Icons/{image_correspondence[shop_inventory[i][0]]}")
                    item.set_position(340 + 600/(offer_qty-1) * i, 155)
                    item.draw()

                # Shop Cursor
                shop_cursor.set_position(300 + 600/(offer_qty-1) * upgrade_selection, 150)
                shop_cursor.draw()
                shop_cursor.update()
                selection_name = f"{item_descriptions[shop_inventory[upgrade_selection][0]]}"
                surface_select_name = font.render(selection_name, True, 'white')
                janela.screen.blit(surface_select_name, ((janela.width - surface_select_name.get_width())/2, 220))

        janela.update()

