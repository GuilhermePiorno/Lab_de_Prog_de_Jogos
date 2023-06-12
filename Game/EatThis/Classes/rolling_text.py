

class RollingFont:
    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.print_index = 0

    def return_slice(self, index):
        self.print_index = index
        return self.text[:index]

def text2rolling(txt):
    if isinstance(txt, str):
        return RollingFont(txt)
    else:
        aux = []
        for element in txt:
            sub_aux = []
            if isinstance(element, str):
                aux.append(text2rolling(element))
            else:
                for subelement in element:
                    sub_aux.append(text2rolling(subelement))
                aux.append(sub_aux)
        return aux












