import lib
import copy

baseDice = lib.parse_svg("test/baseDice.svg", 3)

dice_pass = [
    ["middle"],
    ["bottomleft", "topright"],
    ["bottomleft", "middle", "topright"],
    ["bottomleft", "bottomright", "topleft", "topright"],
    ["bottomleft", "bottomright", "topleft", "topright", "middle"],
    ["bottomleft", "bottomright", "topleft", "topright", "centerleft", "centerright"]
]


def clean_dice(x):
    if (x.type=="circle" and (x.data["id"] not in current_dice_pass)):
        return []
    elif x.data["id"]=="help-lines":
        return []
    else:
        return [copy.deepcopy(x)]



for i in range(0, 6):
    base_copy = copy.deepcopy(baseDice)
    current_dice_pass = dice_pass[i]

    new_dice = base_copy.modify(pre_fun=clean_dice)

    file = open(f"test/allDices/dice{i+1}.svg", "w")
    new_dice.print_to_file(file)
    file.close()
