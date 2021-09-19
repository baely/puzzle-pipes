import requests
from bs4 import BeautifulSoup

# 1 Node
# 2 Bend
# 3 Bar
# 4 T
t = [0, 1, 1, 2, 1, 3, 2, 4, 1, 2, 3, 4, 2, 4, 4]

box_drawing_chars = [" ", "╺", "╹", "┗", "╸", "━", "┛", "┻", "╻", "┏", "┃", "┣", "┓", "┳", "┫", "╋"]


def count_bits(x): return x & 1 + count_bits(x >> 1) if x else 0


def title_rotate_clockwise(x): return ((x << 3) | (x >> 1)) & 0b1111


def coord_to_pos(a): return a[0] * 4 + a[1]


def pos_to_coord(x): return x // 4, x % 4


def get_cell(g, x):
    if 0 <= x < 16:
        return g[x]
    if g is locked:
        return 1
    if g is current:
        return 0


def lock(x): locked[x] = 1


def get_neighbours(x): return [x + 1, x - 4, x - 1, x + 4]


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


def locked_game(): return sum(locked) == 16


def board_locked(): return locked


def rotate_cell(x):
    rotations[x] = (rotations[x] + 3) % 4
    current[x] = title_rotate_clockwise(current[x])


def rotate_rule(x, ll, ff, nff):
    for _ in range(4):
        if not ((current[x] ^ ff) | (~current[x] ^ nff)) & ll:
            break
        rotate_cell(x)


def print_box(g=None):
    if g is None:
        g = current
    print("Current:")
    print("".join([box_drawing_chars[c] for c in g[0:4]]))
    print("".join([box_drawing_chars[c] for c in g[4:8]]))
    print("".join([box_drawing_chars[c] for c in g[8:12]]))
    print("".join([box_drawing_chars[c] for c in g[12:16]]))
    print("")


# Pull the page
req = requests.get("https://www.puzzle-pipes.com/")

# Extract game
task = [int(c, 16) for c in req.text[16550:16566]]

param_index = req.text.index("\"param\"")
param = req.text[param_index + 15:param_index + 271]

types = [t[n] for n in task]
rotations = [0 for _ in task]
locked = [0 for _ in task]
current = task.copy()


# Solve the game
while not locked_game():
    li = 0

    for i in range(16):
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
                        li += 1

                # Bend
                if types[i] == 2:
                    if count_bits(locked_neighbours) > 2 or locked_neighbours in (3, 6, 9, 12):
                        lock(i)
                        li += 1

                # Bar
                if types[i] == 3:
                    if locked_facing or locked_not_facing:
                        lock(i)
                        li += 1

                # T
                if types[i] == 4:
                    if locked_not_facing or count_bits(locked_facing) == 3:
                        lock(i)
                        li += 1

    if not li:
        break

r = "".join([hex(c)[2:] for c in current])
# Submit

t = ""
for i in range(4):
    for j in range(4):
        if 5 == task[coord_to_pos((i, j))] or 10 == task[coord_to_pos((i, j))]:
            if 2 == rotations[coord_to_pos((i, j))]:
                t += "0"
            elif 3 == rotations[coord_to_pos((i, j))]:
                t += "1"
            else:
                t += str(rotations[coord_to_pos((i, j))])
        else:
            t += str(rotations[coord_to_pos((i, j))])
t += ":"
t += "".join("0" for _ in range(16))

obj = {
    "jstimer": "0", 
    "jsPersonalTimer": "1", 
    "jstimerPersonal": "", 
    "stopClock": "0", 
    "fromSolved": "0", 
    "robot": "1",
    "zoomslider": "0", 
    "jstimerShow": "00:00",
    "jstimerShowPersonal": "00:00",
    "b": "1", 
    "size": "0", 
    "param": param, 
    "w": "4", 
    "h": "4", 
    "ansH": t, 
    "ready": "   Done   "
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

req = requests.post("https://www.puzzle-pipes.com/", obj, headers=headers)

print_box(task)
print_box()

if "Congratulations" in req.text:
    i = req.text.index("Congratulations")
    print(req.text[i:i + 56])

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
