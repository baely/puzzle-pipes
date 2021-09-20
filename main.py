import requests
from bs4 import BeautifulSoup
import sys


SIZES = [4, 5, 7, 10, 15, 20, 25]

# 1 Node, 2 Bend, 3 Bar, 4 T
SHAPES = [0, 1, 1, 2, 1, 3, 2, 4, 1, 2, 3, 4, 2, 4, 4]

BOX_DRAWING = [" ", "╺", "╹", "┗", "╸", "━", "┛", "┻", "╻", "┏", "┃", "┣", "┓", "┳", "┫", "╋"]


def count_bits(x: int) -> int:
    """
    Count 1 bits present in x
    :param x:
    :return:
    """
    return (x & 1) + count_bits(x >> 1) if x else 0


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


def coord_to_pos(size: int, coord: tuple[int, int]) -> int:
    """
    Convert multidimensional coord to single dimensional position
    :param size:
    :param coord:
    :return:
    """
    if not 0 <= coord[0] < size or not 0 <= coord[1] < size:
        return -1
    return coord[0] * size + coord[1]


def pos_to_coord(size: int, x: int) -> tuple[int, int]:
    """
    Convert single dimensional position to multidimensional coord
    :param size:
    :param x:
    :return:
    """
    return x // size, x % size


def get_cell(size: int, g: list[int], x: int, default: int) -> int:
    """
    Get value of a grid g at position x. Provides defaults for locked and current grid
    :param size:
    :param g:
    :param x:
    :param default:
    :return:
    """
    if 0 <= x < size ** 2:
        return g[x]
    return default


def lock(g: list[int], x: int) -> None:
    """
    Lock value at x
    :param g:
    :param x:
    :return:
    """
    g[x] = 1


def is_neighbours(size: int, x: int, y: int) -> int:
    # TODO: Efficiency of algo
    """
    Determines if pos x and pos y are neighbours. Returns direction x -> y
    :param size:
    :param x: Pos 1
    :param y: Pos 2
    :return: Direction or 0
    """
    coord = pos_to_coord(size, x)
    return (coord_to_pos(size, (coord[0], coord[1] + 1)) == y) * 1 + \
           (coord_to_pos(size, (coord[0] - 1, coord[1])) == y) * 2 + \
           (coord_to_pos(size, (coord[0], coord[1] - 1)) == y) * 4 + \
           (coord_to_pos(size, (coord[0] + 1, coord[1])) == y) * 8


def is_connected(size: int, g: list[int], x: int, y: int) -> bool:
    """
    Determines if pos x and pos y are connected
    :param size:
    :param g:
    :param x:
    :param y:
    :return:
    """
    direction = is_neighbours(size, x, y)
    return bool(g[x] & direction and g[y] & flip_int(direction))


def has_locked_neighbour(size: int, g: list[int], x: int) -> int:
    """
    Return if pos x has a locked neighbour
    :param size:
    :param g:
    :param x:
    :return:
    """
    return max([get_cell(size, g, y, 1) for y in get_neighbours(size, x)])


def get_neighbours(size: int, x: int) -> list[int]:
    """
    Return the neighbouring positions to position x
    :param size:
    :param x:
    :return:
    """
    p = pos_to_coord(size, x)
    return [
        coord_to_pos(size, (p[0], p[1] + 1)),
        coord_to_pos(size, (p[0] - 1, p[1])),
        coord_to_pos(size, (p[0], p[1] - 1)),
        coord_to_pos(size, (p[0] + 1, p[1]))
    ]


def neighbours_locked(size: int, g: list[int], *c: int) -> int:
    """
    Returns the locked int of locked neighbours surrounding x
    :param size:
    :param g:
    :param c:
    :return:
    """
    return get_cell(size, g, c[0], 1) + 2 * get_cell(size, g, c[1], 1) + 4 * get_cell(size, g, c[2], 1) + 8 * get_cell(
        size, g, c[3], 1)


def neighbours_facing(size: int, g: list[int], *c: int) -> int:
    """
    Returns the facing int of facing neighbours surrounding x
    :param size:
    :param g:
    :param c:
    :return:
    """
    return ((get_cell(size, g, c[0], 0) & 4) >> 2) + \
           ((get_cell(size, g, c[1], 0) & 8) >> 2) + \
           ((get_cell(size, g, c[2], 0) & 1) << 2) + \
           ((get_cell(size, g, c[3], 0) & 2) << 2)


def locked_game(size: int, g: list[int]) -> bool:
    """
    If whole board is locked
    :param size:
    :param g:
    :return:
    """
    return sum(g) == size ** 2


def rotate_cell(rg: list[int], cg: list[int], x: int) -> None:
    """
    Rotate the cell at position x
    :param cg:
    :param rg:
    :param x:
    :return:
    """
    rg[x] = (rg[x] + 3) % 4
    cg[x] = title_rotate_clockwise(cg[x])


def rotate_rule(rg: list[int], cg: list[int], x: int, ll: int, ff: int, nff: int) -> None:
    """
    Rotate the cell at position x until it fits with it's locked neighbours
    :param cg:
    :param rg:
    :param x: Position of cell
    :param ll: Locked neighbours
    :param ff: Facing neighbours
    :param nff: Not facing neighbours
    :return:
    """
    for _ in range(4):
        if not ((cg[x] ^ ff) | (~cg[x] ^ nff)) & ll:
            break
        rotate_cell(rg, cg, x)


def print_box(size: int, g: list[int], pp: bool = True) -> list[list[str]]:
    """
    Prints the grid g or current state
    :param size:
    :param g: Grid
    :param pp: Print bool. (or only return)
    :return:
    """
    if pp:
        print("Current:")
    rows = []
    for index in range(0, size ** 2, size):
        new_row = [BOX_DRAWING[c] for c in g[index:index + size]]
        rows.append(new_row)
        if pp:
            print("".join(new_row))
    if pp:
        print("")
    return rows


def get_first_unlocked(g: list[int]) -> int:
    """
    Return index of first unlocked pos
    :param g:
    :return:
    """
    return g.index(0)


def contains_loops(size: int, g: list[int], x: int) -> (bool, set[int]):
    """
    Detect if loop exists anywhere starting from x
    :param size:
    :param g:
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
        for neighbour in get_neighbours(size, curr):
            if is_connected(size, g, curr, neighbour):
                to_check.append(neighbour)
                if neighbour is not prev:
                    loop = True
        checked.add(curr)
    return loop, checked


def retrieve_new_game(size: int, p_size: int) -> (str, dict):
    # Pull the page
    req = requests.get(f"https://www.puzzle-pipes.com/?size={p_size}")

    # Extract game
    # print(req.text[16650:])
    # task = [int(c, 16) for c in req.text[16650:16650 + SIZE ** 2]]

    param_index = req.text.index("\"param\"")
    param_sub = req.text[param_index + 15:param_index + 500]
    param_sub_index = param_sub.index("\"")
    param = param_sub[:param_sub_index]

    return req.text[16650:16650 + size ** 2], param


def create_new_game(
        size: int,
        p_size: int,
        task_str: str = None
) -> (list[int], list[int], list[int], list[int], list[int], dict):
    # global task
    # global types
    # global rotations
    # global locked
    # global current
    param = {}
    if task_str is None:
        task_str, param = retrieve_new_game(size, p_size)

    task = [int(c, 16) for c in task_str]
    types = [SHAPES[n] for n in task]
    rotations = [0 for _ in task]
    locked = [0 for _ in task]
    current = task.copy()

    return task, types, rotations, locked, current, param


def solve(size: int, types: list[int], rotations: list[int], locked: list[int], current: list[int]) -> None:
    # Solve the game
    li = True

    while li:
        # Algorithm 1: Simple algorithm
        # For all cells, checked if the locked neighbours can determine current rotation

        li = False

        for i in range(size ** 2):
            if not get_cell(size, locked, i, 1) and has_locked_neighbour(size, locked, i):
                neighbours = get_neighbours(size, i)
                locked_neighbours = neighbours_locked(size, locked, *neighbours)
                facing_neighbours = neighbours_facing(size, current, *neighbours)

                locked_facing = locked_neighbours & facing_neighbours
                locked_not_facing = locked_neighbours & ~facing_neighbours

                if locked_neighbours:
                    rotate_rule(rotations, current, i, locked_neighbours, locked_facing, locked_not_facing)

                    # Node
                    if types[i] == 1:
                        if locked_facing or count_bits(locked_not_facing) == 3:
                            lock(locked, i)
                            li = True

                    # Bend
                    if types[i] == 2:
                        if count_bits(locked_neighbours) > 2 or locked_neighbours in (3, 6, 9, 12):
                            lock(locked, i)
                            li = True

                    # Bar
                    if types[i] == 3:
                        if locked_facing or locked_not_facing:
                            lock(locked, i)
                            li = True

                    # T
                    if types[i] == 4:
                        if locked_not_facing or count_bits(locked_facing) == 3:
                            lock(locked, i)
                            li = True

        if locked_game(size, locked):
            break
    else:
        # Algorithm 2: Complex
        print("Attempting complex algorithm")
        print(f"{sum(locked)}/{size ** 2} locked tiles so far.")
        #
        # li = False
        #
        # for i in range(SIZE ** 2):
        #     if not get_cell(locked, i) and has_locked_neighbour(i):
        #         neighbours = get_neighbours(i)
        #         locked_neighbours = neighbours_locked(*neighbours)
        #         facing_neighbours = neighbours_facing(*neighbours)
        #
        #         locked_facing = locked_neighbours & facing_neighbours
        #         locked_not_facing = locked_neighbours & ~facing_neighbours
        #
        #         # Node
        #
        #         # Bend:
        #         # - If any 1 side is locked. Opposite side must inverse
        #
        #         # Bar
        #
        #         # T


def submit(size: int, p_size: int, task: list[int], current: list[int], rotations: list[int], param: dict) -> None:
    # r = "".join([hex(c)[2:] for c in current])

    ans = ""
    for i in range(size):
        for j in range(size):
            if 5 == task[coord_to_pos(size, (i, j))] or 10 == task[coord_to_pos(size, (i, j))]:
                if 2 == rotations[coord_to_pos(size, (i, j))]:
                    ans += "0"
                elif 3 == rotations[coord_to_pos(size, (i, j))]:
                    ans += "1"
                else:
                    ans += str(rotations[coord_to_pos(size, (i, j))])
            else:
                ans += str(rotations[coord_to_pos(size, (i, j))])
    ans += ":"
    ans += "".join("0" for _ in range(size ** 2))

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
        "w": size,
        "h": size,
        "ansH": ans,
        "ready": "   Done   "
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    req = requests.post("https://www.puzzle-pipes.com/", obj, headers=headers)

    if "Congratulations" in req.text:
        i = req.text.index("Congratulations")
        print_box(size, task)
        print_box(size, current)
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


def main() -> None:
    try:
        p_size = int(sys.argv[1])
    except (IndexError, ValueError):
        p_size = 1

    size = SIZES[p_size]

    task, types, rotations, locked, current, param = create_new_game(size, p_size)
    solve(size, types, rotations, locked, current)
    submit(size, p_size, task, current, rotations, param)


if __name__ == '__main__':
    main()
