test = "<color:(0, 0, 0)>hjsfjhskd<size: 20   >lfasdasdasda<size:23123;super_offset:3; italic:True>sdasdasda</>dasdhsj</>kdfhkls</aaa>"
tags = {""}

styles = {"int": ["size", "sub_offset", "super_offset", "word_spacing", "letter_spacing", "leading"], "bool": ["italic", "bold", "underline", "shadow", "super", "sub"], "intlist": ["color", "background", "shadow_offset", "shadow_color"], "string": ["font"]}

def process_style(style):
    temp = style.replace(" ", "")
    temp = temp.split(";")
    final = {}
    for x in temp:
        split_text = x.split(":")
        if split_text[0] in styles["int"]:
            final[split_text[0]] = int(split_text[1])
        elif split_text[0] in styles["bool"]:
            final[split_text[0]] = bool(split_text[1])
        elif split_text[0] in styles["string"]:
            final[split_text[0]] = split_text[1]
        elif split_text[0] in styles["intlist"]:
            final[split_text[0]] = [int(x) for x in split_text[1][1:-1].split(",")]
    return final

def append(levels, lst, item):
    temp = lst
    for level in levels:
        temp = temp[level]
    temp.append(item)
    return(len(temp))

style = []
text = []
final = []
current_index = 0
state = "between_tags"
close = False
levels = []

temp_final = []


for char in test:
    if state == "inside_tags":
        text.append(char)
        if char == ">":
            state = "between_tags"
            temp_final.append("".join(text))
            text = []
    elif state == "between_tags":
        if char == "<":
            state = "inside_tags"
            temp_final.append("".join(text))
            text = []
        text.append(char)
print(temp_final)




for char in test:
    if state == "inside_tags":
        if char == ">":
            state = "between_tags"
            final_style = process_style("".join(style))
            if final_style != {}:
                append(levels, final, final_style)
            style = []
        elif char == "/":
            try:
                levels.pop()
            except:
                pass
        else:
            style.append(char)
    elif state == "between_tags":
        if char == "<":
            state = "inside_tags"
            if text != []:
                append(levels, final, "".join(text))
            levels.append(append(levels, final, []) - 1)
            text = []
        else:
            text.append(char)
print(final)