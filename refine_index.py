def refine_index(est_index, mouse_pos, size_list):
    if est_index <= 0:
        est_index = 0
        direction = "right"
    elif est_index >= len(size_list) - 1:
        est_index = len(size_list) - 1
        direction = "left"
    elif size_list[est_index] == mouse_pos:
        return est_index
    else:
        if size_list[est_index] - mouse_pos < 0:
            direction = "right"
        else:
            direction = "left"
    if direction == "right":
        for x in range(est_index, len(size_list)):
            if x == len(size_list) - 1:
                return x
            elif abs(size_list[x] - mouse_pos) < abs(size_list[x + 1] - mouse_pos):
                return x
    else:
        for x in range(est_index, -1, -1):
            if abs(size_list[x] - mouse_pos) < abs(size_list[x - 1] - mouse_pos):
                return x
