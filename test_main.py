from unittest import TestCase

import main


class Test(TestCase):
    def test_count_bits(self):
        self.assertEqual(main.count_bits(0), 0)
        self.assertEqual(main.count_bits(1), 1)
        self.assertEqual(main.count_bits(2), 1)
        self.assertEqual(main.count_bits(3), 2)
        self.assertEqual(main.count_bits(4), 1)
        self.assertEqual(main.count_bits(5), 2)
        self.assertEqual(main.count_bits(6), 2)
        self.assertEqual(main.count_bits(7), 3)
        self.assertEqual(main.count_bits(8), 1)
        self.assertEqual(main.count_bits(9), 2)
        self.assertEqual(main.count_bits(10), 2)
        self.assertEqual(main.count_bits(11), 3)
        self.assertEqual(main.count_bits(12), 2)
        self.assertEqual(main.count_bits(13), 3)
        self.assertEqual(main.count_bits(14), 3)
        self.assertEqual(main.count_bits(15), 4)

    def test_title_rotate_clockwise(self):
        self.assertEqual(0, main.title_rotate_clockwise(0))
        self.assertEqual(8, main.title_rotate_clockwise(1))
        self.assertEqual(1, main.title_rotate_clockwise(2))
        self.assertEqual(9, main.title_rotate_clockwise(3))
        self.assertEqual(2, main.title_rotate_clockwise(4))
        self.assertEqual(10, main.title_rotate_clockwise(5))
        self.assertEqual(3, main.title_rotate_clockwise(6))
        self.assertEqual(11, main.title_rotate_clockwise(7))
        self.assertEqual(4, main.title_rotate_clockwise(8))
        self.assertEqual(12, main.title_rotate_clockwise(9))
        self.assertEqual(5, main.title_rotate_clockwise(10))
        self.assertEqual(13, main.title_rotate_clockwise(11))
        self.assertEqual(6, main.title_rotate_clockwise(12))
        self.assertEqual(14, main.title_rotate_clockwise(13))
        self.assertEqual(7, main.title_rotate_clockwise(14))
        self.assertEqual(15, main.title_rotate_clockwise(15))

    def test_flip_int(self):
        self.assertEqual(4, main.flip_int(1))
        self.assertEqual(8, main.flip_int(2))
        self.assertEqual(1, main.flip_int(4))
        self.assertEqual(2, main.flip_int(8))

    def test_coord_to_pos(self):
        self.assertEqual(0, main.coord_to_pos(4, (0, 0), -1))
        self.assertEqual(1, main.coord_to_pos(4, (0, 1), -1))
        self.assertEqual(2, main.coord_to_pos(4, (0, 2), -1))
        self.assertEqual(3, main.coord_to_pos(4, (0, 3), -1))
        self.assertEqual(4, main.coord_to_pos(4, (1, 0), -1))
        self.assertEqual(5, main.coord_to_pos(4, (1, 1), -1))
        self.assertEqual(6, main.coord_to_pos(4, (1, 2), -1))
        self.assertEqual(7, main.coord_to_pos(4, (1, 3), -1))
        self.assertEqual(8, main.coord_to_pos(4, (2, 0), -1))
        self.assertEqual(9, main.coord_to_pos(4, (2, 1), -1))
        self.assertEqual(10, main.coord_to_pos(4, (2, 2), -1))
        self.assertEqual(11, main.coord_to_pos(4, (2, 3), -1))
        self.assertEqual(12, main.coord_to_pos(4, (3, 0), -1))
        self.assertEqual(13, main.coord_to_pos(4, (3, 1), -1))
        self.assertEqual(14, main.coord_to_pos(4, (3, 2), -1))
        self.assertEqual(15, main.coord_to_pos(4, (3, 3), -1))

    def test_pos_to_coord(self):
        self.assertEqual((0, 0), main.pos_to_coord(4, 0))
        self.assertEqual((0, 1), main.pos_to_coord(4, 1))
        self.assertEqual((0, 2), main.pos_to_coord(4, 2))
        self.assertEqual((0, 3), main.pos_to_coord(4, 3))
        self.assertEqual((1, 0), main.pos_to_coord(4, 4))
        self.assertEqual((1, 1), main.pos_to_coord(4, 5))
        self.assertEqual((1, 2), main.pos_to_coord(4, 6))
        self.assertEqual((1, 3), main.pos_to_coord(4, 7))
        self.assertEqual((2, 0), main.pos_to_coord(4, 8))
        self.assertEqual((2, 1), main.pos_to_coord(4, 9))
        self.assertEqual((2, 2), main.pos_to_coord(4, 10))
        self.assertEqual((2, 3), main.pos_to_coord(4, 11))
        self.assertEqual((3, 0), main.pos_to_coord(4, 12))
        self.assertEqual((3, 1), main.pos_to_coord(4, 13))
        self.assertEqual((3, 2), main.pos_to_coord(4, 14))
        self.assertEqual((3, 3), main.pos_to_coord(4, 15))

    def test_get_cell(self):
        self.assertEqual(1, main.get_cell(2, [1, 2, 3, 4], 0, 0))
        self.assertEqual(2, main.get_cell(2, [1, 2, 3, 4], 1, 0))
        self.assertEqual(3, main.get_cell(2, [1, 2, 3, 4], 2, 0))
        self.assertEqual(4, main.get_cell(2, [1, 2, 3, 4], 3, 0))
        self.assertEqual(0, main.get_cell(2, [1, 2, 3, 4], 4, 0))
        self.assertEqual(0, main.get_cell(2, [1, 2, 3, 4], -1, 0))
        self.assertEqual(1, main.get_cell(2, [1, 2, 3, 4], -1, 1))

    def test_is_neighbours(self):
        self.assertEqual(1, main.is_neighbours(4, 0, 1))
        self.assertEqual(0, main.is_neighbours(4, 0, -4))
        self.assertEqual(0, main.is_neighbours(4, 0, -1))
        self.assertEqual(8, main.is_neighbours(4, 0, 4))
        self.assertEqual(1, main.is_neighbours(4, 5, 6))
        self.assertEqual(2, main.is_neighbours(4, 5, 1))
        self.assertEqual(4, main.is_neighbours(4, 5, 4))
        self.assertEqual(8, main.is_neighbours(4, 5, 9))
        self.assertEqual(1, main.is_neighbours(4, 13, 14))
        self.assertEqual(2, main.is_neighbours(4, 13, 9))
        self.assertEqual(4, main.is_neighbours(4, 13, 12))
        self.assertEqual(0, main.is_neighbours(4, 13, 17))

    def test_is_connected(self):
        self.assertEqual(True, main.is_connected(2, [1, 4, 5, 5], 0, 1))
        self.assertEqual(True, main.is_connected(2, [9, 4, 3, 4], 0, 1))
        self.assertEqual(False, main.is_connected(2, [8, 8, 3, 6], 0, 1))
        self.assertEqual(False, main.is_connected(2, [1, 1, 1, 1], 0, 1))
        self.assertEqual(False, main.is_connected(2, [9, 12, 3, 6], 0, 3))
        self.assertEqual(True, main.is_connected(2, [9, 0, 2, 0], 0, 2))

    def test_has_locked_neighbour(self):
        self.assertEqual(2, main.has_locked_neighbour(2, [0, 0, 0, 0], 0))
        self.assertEqual(2, main.has_locked_neighbour(2, [0, 1, 0, 0], 0))
        self.assertEqual(0, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 0, 0, 0, 0], 4))
        self.assertEqual(0, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 0, 0, 0, 1], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 0, 0, 1, 0], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 0, 0, 1, 1], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 1, 0, 0, 0], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 1, 0, 0, 1], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 1, 0, 1, 0], 4))
        self.assertEqual(1, main.has_locked_neighbour(3, [0, 0, 0, 0, 0, 1, 0, 1, 1], 4))

    def test_get_neighbours(self):
        self.assertEqual([1, -1, -1, 4], main.get_neighbours(4, 0))
        self.assertEqual([2, -1, 0, 5], main.get_neighbours(4, 1))
        self.assertEqual([3, -1, 1, 6], main.get_neighbours(4, 2))
        self.assertEqual([-1, -1, 2, 7], main.get_neighbours(4, 3))
        self.assertEqual([46, 35, 44, 55], main.get_neighbours(10, 45))
        self.assertEqual([-1, 79, 88, 99], main.get_neighbours(10, 89))
        self.assertEqual([101, 75, -1, 125], main.get_neighbours(25, 100))
        self.assertEqual([1, -1, -1, 25], main.get_neighbours(25, 0))

    def test_neighbours_locked(self):
        self.assertEqual(6, main.neighbours_locked(2, [0, 0, 0, 0], *[1, -1, -1, 2]))
        self.assertEqual(14, main.neighbours_locked(2, [0, 0, 1, 0], *[1, -1, -1, 2]))
        self.assertEqual(15, main.neighbours_locked(2, [0, 1, 1, 1], *[1, -1, -1, 2]))

    def test_neighbours_facing(self):
        pass

    def test_locked_game(self):
        self.assertEqual(True, main.locked_game(4, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
        self.assertEqual(True, main.locked_game(2, [1, 1, 1, 1]))
        self.assertEqual(False, main.locked_game(2, [1, 1, 1, 0]))
        self.assertEqual(False, main.locked_game(2, [1, 0, 0, 0]))

    def test_rotate_cell(self):
        # self.assertEqual()
        pass

    def test_rotate_rule(self):
        # self.fail()
        pass

    def test_print_box(self):
        pass

    def test_get_first_unlocked(self):
        self.assertEqual(0, main.get_first_unlocked([0, 1, 1, 0]))
        self.assertEqual(1, main.get_first_unlocked([1, 0, 0, 1]))
        self.assertEqual(2, main.get_first_unlocked([1, 1, 0, 1]))
        self.assertEqual(3, main.get_first_unlocked([1, 1, 1, 0]))
        self.assertEqual(-1, main.get_first_unlocked([1, 1, 1, 1]))

    def test_contains_loops(self):
        pass
