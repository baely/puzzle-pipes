//
// Created by Bailey on 30/09/2021.
//

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int x;
    int y;
} int_pair;

int count_bits(int);
int tile_rotate_clockwise(int);
void get_neighbours(int*, int, int);

int SHAPES[16] = {0, 1, 1, 2, 1, 3, 2, 4, 1, 2, 3, 4, 2, 4, 4};

/**
 * https://stackoverflow.com/a/26839647/1702816
 * @param ch
 * @return
 */
int hex2int(char ch)
{
    if (ch >= '0' && ch <= '9')
        return ch - '0';
    if (ch >= 'A' && ch <= 'F')
        return ch - 'A' + 10;
    if (ch >= 'a' && ch <= 'f')
        return ch - 'a' + 10;
    return -1;
}

int count_bits(int x) {
    if (x > 0) {
        return (x & 1) + count_bits(x >> 1);
    }

    return 0;
}

int tile_rotate_clockwise(int x) {
    return ((x << 3) | (x >> 1)) & 15;
}

int flip_int(int x) {
    return ((x << 2) | (x >> 2)) & 15;
}

int coord_to_pos(int size, int_pair x, int def) {
    if (x.x < 0 || x.x >= size || x.y < 0 || x.y >= size) {
        return def;
    }

    return x.x * size + x.y;
}

int_pair pos_to_coord(int size, int x) {
    int mod, rem;
    int_pair ret;
    mod = x % size;
    rem = x - mod;
    ret.x = rem;
    ret.y = mod;
    return ret;
}

int get_cell(int size, int* g, int x, int def) {
    if (x < 0 || x >= size * size) {
        return def;
    }

    return g[x];
}

void lock(int* g, int x) {
    g[x] = 1;
}

int is_neighbours(int size, int x, int y) {
    if (y < 0 || y >= size * size) {
        return 0;
    }
    int_pair p1, p2, p3, p4;
    p1 = p2 = p3 = p4 = pos_to_coord(size, x);
    p1.y++;
    p2.x--;
    p3.y--;
    p4.x++;

    return ((coord_to_pos(size, p1, -1) == y) ? 1 : 0) +
            ((coord_to_pos(size, p2, -1) == y) ? 2 : 0) +
            ((coord_to_pos(size, p3, -1) == y) ? 4 : 0) +
            ((coord_to_pos(size, p4, -1) == y) ? 8 : 0);
}

int is_connected(int size, int* g, int x, int y) {
    int dir;
    dir = is_neighbours(size, x, y);
    return (g[x] & dir) > 0 && (g[y] & flip_int(dir)) > 0;
}

int has_locked_neighbours(int size, int* g, int x) {
    int neighbours[4];
    int max, curr;
    max = 0;

    get_neighbours(neighbours, size, x);

    for (int i = 0; i < 4; i++) {
        curr = get_cell(size, g, neighbours[i], 2);
        if (curr > max) {
            max = curr;
        }
    }

    return max;
}

void get_neighbours(int* ret, int size, int x) {
    int_pair p1, p2, p3, p4;
    p1 = p2 = p3 = p4 = pos_to_coord(size, x);
    p1.y++;
    p2.x--;
    p3.y--;
    p4.x++;

    ret[0] = coord_to_pos(size, p1, -1);
    ret[1] = coord_to_pos(size, p2, -1);
    ret[2] = coord_to_pos(size, p3, -1);
    ret[3] = coord_to_pos(size, p4, -1);
}

int neighbours_locked(int size, int* g, int* c) {
    int ret;
    ret = get_cell(size, g, c[0], 1) +
            2 * get_cell(size, g, c[1], 1) +
            4 * get_cell(size, g, c[2], 1) +
            8 * get_cell(size, g, c[3], 1);
    return ret;
}

int neighbours_facing(int size, int* g, int* c) {
    int ret;
    ret = ((get_cell(size, g, c[0], 0) & 4) >> 2) +
           ((get_cell(size, g, c[1], 0) & 8) >> 2) +
           ((get_cell(size, g, c[2], 0) & 1) << 2) +
           ((get_cell(size, g, c[3], 0) & 2) << 2);
    return ret;
}

int locked_game(int size, int* g) {
    for (int i = 0; i < (size * size); i++) {
        if (g[i] == 0) {
            return 0;
        }
    }

    return 1;
}

void rotate_cell(int* rg, int* cg, int x) {
    rg[x] = (rg[x] + 3) % 4;
    cg[x] = tile_rotate_clockwise(cg[x]);
    printf("Rotating pos: %d\n", x);
}

void rotate_rule(int* rg, int* cg, int x, int ll, int ff, int nff) {
    for (int i = 0; i < 4; i++) {
        if ((((cg[x] ^ ff) | (~cg[x] ^ nff)) & ll) == 0) {
            break;
        }
        rotate_cell(rg, cg, x);
    }
}

void create_new_game(int size, char* task_str, int* task, int* types, int* rotations, int* locked, int* current) {
    for (int i = 0; i < (size * size); i++) {
        char c;
        c = task_str[i];
        task[i] = hex2int(c);

//        printf("%c -> %d\n", task_str[i], task[i]);

        types[i] = SHAPES[i];
        rotations[i] = 0;
        locked[i] = 0;
        current[i] = task[i];
    }
}

void solve(int size, int* types, int* rotations, int* locked, int* current) {
    int li, locked_neighbours, facing_neighbours, locked_facing, locked_not_facing, neighbours[size * size];

    li = 1;

    while (li > 0) {
        li = 0;

        for (int i = 0; i < size * size; i ++) {
            printf("Checking pos: %d, current state: %d\n", i, current[i]);

            if (get_cell(size, locked, i, 1) == 0 && has_locked_neighbours(size, locked, i)) {
                get_neighbours(neighbours, size, i);
                locked_neighbours = neighbours_locked(size, locked, neighbours);
                facing_neighbours = neighbours_facing(size, locked, neighbours);

                locked_facing = locked_neighbours & facing_neighbours & 15;
                locked_not_facing = locked_neighbours & ~facing_neighbours & 15;

                if (locked_neighbours > 0) {
                    rotate_rule(rotations, current, i, locked_neighbours, locked_facing, locked_not_facing);

                    if (types[i] == 1) {
                        if (locked_facing > 0 || count_bits(locked_not_facing) == 3) {
                            lock(locked, i);
                            li = 1;
                            printf("Locked\n");
                        }
                    }

                    if (types[i] == 2) {
                        if (count_bits(locked_neighbours) > 2 || locked_neighbours % 3 == 0) {
                            lock(locked, i);
                            li = 1;
                            printf("Locked\n");
                        }
                    }

                    if (types[i] == 3) {
                        if (locked_facing > 0 || locked_not_facing > 0) {
                            lock(locked, i);
                            li = 1;
                            printf("Locked\n");
                        }
                    }

                    if (types[i] == 4) {
                        if (locked_not_facing > 0 || count_bits(locked_facing) == 3) {
                            lock(locked, i);
                            li = 1;
                            printf("Locked\n");
                        }
                    }
                }
            }
        }

        if (locked_game(size, locked) == 1) {
            break;
        }
    }
}

int* do_game(int size, char* task_str, int* task, int* current, int*rotations) {
    int types[size * size], locked[size * size];
    create_new_game(size, task_str, task, types, rotations, locked, current);
    solve(size, types, rotations, locked, current);
    return rotations;
}

int main(int argv, char* arg[]) {
    int task[16], current[16], rotations[16];
    char task_str[] = { 56, 49, 56, 54, 55, 100, 98, 54, 99, 49, 100, 54, 52, 53, 51, 56};
    do_game(4, task_str, task, current, rotations);
}
