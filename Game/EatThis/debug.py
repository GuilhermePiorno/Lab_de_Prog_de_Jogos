def var_toggle(var, input_string, teclado):
    if teclado.key_pressed(input_string):
        var = not var
    return var

def check_keys(teclado, *args):
    pressed = False
    for i in range(len(args)):
        if teclado.key_pressed(args[i]):
            pressed = True
    return pressed