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

types = []
rotations = []
locked = []
current = []


def count_bits(x: int) -> int:
    """
    Count 1 bits present in x
    :param x:
    :return:
    """
    return x & 1 + count_bits(x >> 1) if x else 0


def title_rotate_clockwise(x: int) -> int:
    """
    Circular bitshift right
    :param x:
    :return:
    """
    return ((x << 3) | (x >> 1)) & 0b1111


def flip_int(x: int) -> int:
    """
    Double rotate int
    :param x:
    :return:
    """
    return ((x << 2) | (x >> 2)) & 0b1111


def coord_to_pos(coord: tuple[int, int]) -> int:
    """
    Convert multidimensional coord to single dimensional position
    :param coord:
    :return:
    """
    if not 0 <= coord[0] < SIZE or not 0 <= coord[1] < SIZE:
        return -1
    return coord[0] * SIZE + coord[1]


def pos_to_coord(x: int) -> tuple[int, int]:
    """
    Convert single dimensional position to multidimensional coord
    :param x:
    :return:
    """
    return x // SIZE, x % SIZE


def get_cell(g: list[int], x: int) -> int:
    """
    Get value of a grid g at position x. Provides defaults for locked and current grid
    :param g:
    :param x:
    :return:
    """
    if 0 <= x < SIZE ** 2:
        return g[x]
    if g is locked:
        return 1
    if g is current:
        return 0


def lock(x: int) -> None:
    """
    Lock value at x
    :param x:
    :return:
    """
    locked[x] = 1


def is_neighbours(x: int, y: int) -> int:
    # TODO: Efficiency of algo
    """
    Determines if pos x and pos y are neighbours. Returns direction x -> y
    :param x: Pos 1
    :param y: Pos 2
    :return: Direction or 0
    """
    coord = pos_to_coord(x)
    return (coord_to_pos((coord[0], coord[1] + 1)) == y) * 1 + \
           (coord_to_pos((coord[0] - 1, coord[1])) == y) * 2 + \
           (coord_to_pos((coord[0], coord[1] - 1)) == y) * 4 + \
           (coord_to_pos((coord[0] + 1, coord[1])) == y) * 8


def is_connected(x: int, y: int) -> bool:
    """
    Determines if pos x and pos y are connected
    :param x:
    :param y:
    :return:
    """
    direction = is_neighbours(x, y)
    return bool(current[x] & direction and current[y] & flip_int(direction))


def has_locked_neighbour(x: int) -> int:
    """
    Return if pos x has a locked neighbour
    :param x:
    :return:
    """
    return max([get_cell(locked, y) for y in get_neighbours(x)])


def get_neighbours(x: int) -> set[int]:
    """
    Return the neighbouring positions to position x
    :param x:
    :return:
    """
    p = pos_to_coord(x)
    return {
        coord_to_pos((p[0], p[1] + 1)),
        coord_to_pos((p[0] - 1, p[1])),
        coord_to_pos((p[0], p[1] - 1)),
        coord_to_pos((p[0] + 1, p[1]))
    }


def neighbours_locked(*c: int) -> int:
    """
    Returns the locked int of locked neighbours surrounding x
    :param c:
    :return:
    """
    return get_cell(locked, c[0]) + \
           2 * get_cell(locked, c[1]) + \
           4 * get_cell(locked, c[2]) + \
           8 * get_cell(locked, c[3])


def neighbours_facing(*c: int) -> int:
    """
    Returns the facing int of facing neighbours surrounding x
    :param c:
    :return:
    """
    return ((get_cell(current, c[0]) & 4) >> 2) + \
           ((get_cell(current, c[1]) & 8) >> 2) + \
           ((get_cell(current, c[2]) & 1) << 2) + \
           ((get_cell(current, c[3]) & 2) << 2)


def locked_game() -> bool:
    """
    If whole board is locked
    :return:
    """
    return sum(locked) == SIZE ** 2


def rotate_cell(x: int) -> None:
    """
    Rotate the cell at position x
    :param x:
    :return:
    """
    rotations[x] = (rotations[x] + 3) % 4
    current[x] = title_rotate_clockwise(current[x])


def rotate_rule(x: int, ll: int, ff: int, nff: int) -> None:
    """
    Rotate the cell at position x until it fits with it's locked neighbours
    :param x: Position of cell
    :param ll: Locked neighbours
    :param ff: Facing neighbours
    :param nff: Not facing neighbours
    :return:
    """
    for _ in range(4):
        if not ((current[x] ^ ff) | (~current[x] ^ nff)) & ll:
            break
        rotate_cell(x)


def print_box(g: list[int] = None, pp: bool = True) -> list[list[str]]:
    """
    Prints the grid g or current state
    :param g: Grid
    :param pp: Print bool. (or only return)
    :return:
    """
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


def get_first_unlocked() -> int:
    """
    Return index of first unlocked pos
    :return:
    """
    return locked.index(0)


def contains_loops(x: int) -> (bool, set[int]):
    """
    Detect if loop exists anywhere starting from x
    :param x:
    :return:
    """
    loop = False
    checked = set()
    to_check = [x]
    prev = None
    while to_check:
        curr = to_check.pop()
        if curr in checked:
            continue
        for neighbour in get_neighbours(curr):
            if is_connected(curr, neighbour):
                to_check.append(neighbour)
                if neighbour is not prev:
                    loop = True
        checked.add(curr)
    return loop, checked


def retrieve_new_game() -> str:
    # Pull the page
    req = requests.get(f"https://www.puzzle-pipes.com/?size={p_size}")

    # Extract game
    # print(req.text[16650:])
    # task = [int(c, 16) for c in req.text[16650:16650 + SIZE ** 2]]

    param_index = req.text.index("\"param\"")
    param_sub = req.text[param_index + 15:param_index + 500]
    param_sub_index = param_sub.index("\"")
    param = param_sub[:param_sub_index]

    return req.text[16650:16650 + SIZE ** 2]


def create_new_game(task: str = None) -> None:
    global types
    global rotations
    global locked
    global current
    if task is None:
        task = retrieve_new_game()

    task = [int(c, 16) for c in task]
    types = [SHAPES[n] for n in task]
    rotations = [0 for _ in task]
    locked = [0 for _ in task]
    current = task.copy()


# Solve the game
li = True

while li:
    # Algorithm 1: Simple algorithm
    # For all cells, checked if the locked neighbours can determine current rotation

    li = False

    for i in range(SIZE ** 2):
        if not get_cell(locked, i) and has_locked_neighbour(i):
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
    # Algorithm 2: Complex
    print("Attempting complex algorithm")
    print(f"{sum(locked)}/{SIZE**2} locked tiles so far.")

    li = False

    for i in range(SIZE ** 2):
        if not get_cell(locked, i) and has_locked_neighbour(i):
            neighbours = get_neighbours(i)
            locked_neighbours = neighbours_locked(*neighbours)
            facing_neighbours = neighbours_facing(*neighbours)

            locked_facing = locked_neighbours & facing_neighbours
            locked_not_facing = locked_neighbours & ~facing_neighbours

            # Node

            # Bend:
            # - If any 1 side is locked. Opposite side must inverse

            # Bar

            # T


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
