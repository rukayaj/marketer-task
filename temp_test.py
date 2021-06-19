import unittest
from temp import make_df, scan, get_match_tolerance_threshold


class TestRadarScan(unittest.TestCase):
    @staticmethod
    def _strify(_list):
        return '\n'.join(_list)

    def test_get_match_tolerance_threshold_0(self):
        res = get_match_tolerance_threshold(500, 0)
        self.assertEqual(res, 500)

    def test_finds_invaders_simple(self):
        radar = make_df('\n'.join(['01',
                                   '00']))
        invader = make_df('\n'.join(['01',
                                     '00']))
        found = scan(radar, invader)
        top_left_corner = (-1, -1)
        middle = (0, 0)
        bottom_right_corner = (1, 1)
        self.assertEqual(found, {top_left_corner, middle, bottom_right_corner})

    def test_finds_invader_top_right(self):
        radar = make_df('\n'.join(['0001',
                                   '0001',
                                   '0000']))
        invader = make_df('\n'.join(['01',
                                     '01']))
        found = scan(radar, invader)
        self.assertEqual(found, {(2, -1), (2, 0), (3, 2)})

    def test_finds_invader_top_left(self):
        radar = make_df('\n'.join(['1000',
                                   '1000',
                                   '0000']))
        invader = make_df('10\n10')
        found = scan(radar, invader)
        self.assertEqual(found, {(0, -1), (0, 0), (-1, 2)})

    def test_finds_invader_bottom_right(self):
        radar = make_df('\n'.join(['0000',
                                   '0001',
                                   '0001']))
        invader = make_df('01\n01')
        found = scan(radar, invader)
        self.assertEqual(found, {(3, -1), (2, 1), (2, 2)})

    def test_finds_invader_bottom_left(self):
        radar = make_df('\n'.join(['0000',
                                   '1000',
                                   '1000']))
        invader = make_df('10\n10')
        found = scan(radar, invader)
        self.assertEqual(found, {(-1, -1), (0, 1), (0, 2)})

    def test_finds_invader_middle(self):
        radar = make_df('\n'.join(['0000',
                                   '0110',
                                   '0110',
                                   '0000']))
        invader = make_df('11\n11')
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1)})

    def test_finds_multiple_invaders(self):
        radar = make_df('\n'.join(['0000000',
                                   '0110110',
                                   '0110110',
                                   '0000000']))
        invader = make_df('\n'.join(['11', '11']))
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1), (4, 1)})

    def test_finds_overlapping_invaders(self):
        radar = make_df('\n'.join(['0000000',
                                   '0111110',
                                   '0111110',
                                   '0000110',
                                   '0000000']))
        invader = make_df('\n'.join(['11', '11']))
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1), (2, 1), (3, 1), (4, 1), (4, 2)})

    # With noise

    def finds_one_invader_with_noise_tolerance(self):
        radar = Radar('\n'.join(['01000',
                                 '11011',
                                 '11011',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = (alien.width - 1) / alien.width
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, {(0, 0), (3, 1)})

    def excludes_invader_with_too_much_noise(self):
        radar = Radar('\n'.join(['01000',
                                 '01011',
                                 '11011',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = (alien.width - 1) / alien.width
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, {(3, 1)})

    def finds_multiple_invaders_with_noise_tolerance(self):
        radar = Radar('\n'.join(['01000',
                                 '01010',
                                 '11011',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = ((alien.width - 1) / alien.width) * 2
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, {(0, 0), (3, 1)})

    def excludes_multiple_invaders_with_noise_tolerance(self):
        radar = Radar('\n'.join(['01000',
                                 '01010',
                                 '11010',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = (alien.width - 1) / alien.width
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, set())

    # Edges and corners - no tolerance

if __name__ == '__main__':
    unittest.main()
