import requests
from bs4 import BeautifulSoup
import sys

if len(sys.argv) > 1:
    p_size = int(sys.argv[1])
else:
    p_size = 1

SIZES = [4, 5, 7, 10, 15, 20, 25]
SIZE = SIZES[p_size]

# 1 Node
# 2 Bend
# 3 Bar
# 4 T
SHAPES = [0, 1, 1, 2, 1, 3, 2, 4, 1, 2, 3, 4, 2, 4, 4]

BOX_DRAWING = [" ", "╺", "╹", "┗", "╸", "━", "┛", "┻", "╻", "┏", "┃", "┣", "┓", "┳", "┫", "╋"]


def count_bits(x): return x & 1 + count_bits(x >> 1) if x else 0


def title_rotate_clockwise(x): return ((x << 3) | (x >> 1)) & 0b1111


def coord_to_pos(coord):
    if not 0 <= coord[0] < SIZE or not 0 <= coord[1] < SIZE:
        return -1
    return coord[0] * SIZE + coord[1]


def pos_to_coord(x): return x // SIZE, x % SIZE


def get_cell(g, x):
    if 0 <= x < SIZE ** 2:
        return g[x]
    if g is locked:
        return 1
    if g is current:
        return 0


def lock(x): locked[x] = 1


def get_neighbours(x):
    p = pos_to_coord(x)
    return [
        coord_to_pos((p[0], p[1] + 1)),
        coord_to_pos((p[0] - 1, p[1])),
        coord_to_pos((p[0], p[1] - 1)),
        coord_to_pos((p[0] + 1, p[1]))
    ]


def neighbours_locked(*c):
    return get_cell(locked, c[0]) + \
           2 * get_cell(locked, c[1]) + \
           4 * get_cell(locked, c[2]) + \
           8 * get_cell(locked, c[3])


def neighbours_facing(*c):
    return ((get_cell(current, c[0]) & 4) >> 2) + \
           ((get_cell(current, c[1]) & 8) >> 2) + \
           ((get_cell(current, c[2]) & 1) << 2) + \
           ((get_cell(current, c[3]) & 2) << 2)


def locked_game(): return sum(locked) == SIZE ** 2


def board_locked(): return locked


def rotate_cell(x):
    rotations[x] = (rotations[x] + 3) % 4
    current[x] = title_rotate_clockwise(current[x])


def rotate_rule(x, ll, ff, nff):
    for _ in range(4):
        if not ((current[x] ^ ff) | (~current[x] ^ nff)) & ll:
            break
        rotate_cell(x)


def print_box(g=None, pp=True):
    if g is None:
        g = current
    if pp:
        print("Current:")
    rows = []
    for index in range(0, SIZE ** 2, SIZE):
        new_row = [BOX_DRAWING[c] for c in g[index:index + SIZE]]
        rows.append(new_row)
        if pp:
            print("".join(new_row))
    if pp:
        print("")
    return rows


# Pull the page
req = requests.get(f"https://www.puzzle-pipes.com/?size={p_size}")

# Extract game
# print(req.text[16650:])
task = [int(c, 16) for c in req.text[16650:16650 + SIZE**2]]

param_index = req.text.index("\"param\"")
param_sub = req.text[param_index + 15:param_index + 500]
param_sub_index = param_sub.index("\"")
param = param_sub[:param_sub_index]

types = [SHAPES[n] for n in task]
rotations = [0 for _ in task]
locked = [0 for _ in task]
current = task.copy()


# Solve the game
li = True

while li:
    li = False

    for i in range(SIZE ** 2):
        if not get_cell(locked, i):
            neighbours = get_neighbours(i)
            locked_neighbours = neighbours_locked(*neighbours)
            facing_neighbours = neighbours_facing(*neighbours)

            locked_facing = locked_neighbours & facing_neighbours
            locked_not_facing = locked_neighbours & ~facing_neighbours

            if locked_neighbours:
                rotate_rule(i, locked_neighbours, locked_facing, locked_not_facing)

                # Node
                if types[i] == 1:
                    if locked_facing or count_bits(locked_not_facing) == 3:
                        lock(i)
                        li = True

                # Bend
                if types[i] == 2:
                    if count_bits(locked_neighbours) > 2 or locked_neighbours in (3, 6, 9, 12):
                        lock(i)
                        li = True

                # Bar
                if types[i] == 3:
                    if locked_facing or locked_not_facing:
                        lock(i)
                        li = True

                # T
                if types[i] == 4:
                    if locked_not_facing or count_bits(locked_facing) == 3:
                        lock(i)
                        li = True

    if locked_game():
        break
else:
    print("Failed.")

r = "".join([hex(c)[2:] for c in current])
# Submit

ans = ""
for i in range(SIZE):
    for j in range(SIZE):
        if 5 == task[coord_to_pos((i, j))] or 10 == task[coord_to_pos((i, j))]:
            if 2 == rotations[coord_to_pos((i, j))]:
                ans += "0"
            elif 3 == rotations[coord_to_pos((i, j))]:
                ans += "1"
            else:
                ans += str(rotations[coord_to_pos((i, j))])
        else:
            ans += str(rotations[coord_to_pos((i, j))])
ans += ":"
ans += "".join("0" for _ in range(SIZE ** 2))

obj = {
    "jstimer": "0", 
    "jsPersonalTimer": "",
    "jstimerPersonal": "0",
    "stopClock": "0", 
    "fromSolved": "0", 
    "robot": "1",
    "zoomslider": "0", 
    "jstimerShow": "00:00",
    "jstimerShowPersonal": "00:00",
    "b": "1", 
    "size": p_size,
    "param": param, 
    "w": SIZE,
    "h": SIZE,
    "ansH": ans,
    "ready": "   Done   "
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

req = requests.post("https://www.puzzle-pipes.com/", obj, headers=headers)

if "Congratulations" in req.text:
    i = req.text.index("Congratulations")
    print_box(task)
    print_box()
    print(f"{sum(rotations)} moves.", req.text[i:i + 56])

    soup = BeautifulSoup(req.text, features="html.parser")
    form = soup.find("form", {"action": "/hallsubmit.php"})
    solparams = form.find("input", {"name": "solparams"}).get("value")
    data = {
        "submitscore": 1,
        "solparams": solparams,
        "robot": 1,
        "email": "bailey_fun@live.com.au"
    }
    requests.post("https://www.puzzle-pipes.com/hallsubmit.php", data=data, headers=headers)
elif "Not there yet" not in req.text:
    print(req.text)
