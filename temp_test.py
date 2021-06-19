import unittest
from temp import make_df, scan, get_match_tolerance_threshold


class TestRadarScan(unittest.TestCase):
    @staticmethod
    def _strify(_list):
        return '\n'.join(_list)

    def test_get_match_tolerance_threshold_0(self):
        res = get_match_tolerance_threshold(500, 0)
        self.assertEqual(res, 500)

    def test_finds_invader_same_size_as_radar(self):
        radar = make_df('01\n00')
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(0, 0)})

    def test_finds_invader_top_right(self):
        radar = make_df('\n'.join(['0001',
                                   '0000',
                                   '0000']))
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(2, 0)})

    def test_finds_invader_top_left(self):
        radar = make_df('\n'.join(['0100',
                                   '0000',
                                   '0000']))
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(0, 0)})

    def test_finds_invader_bottom_right(self):
        radar = make_df('\n'.join(['0000',
                                   '0001',
                                   '0000']))
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(2, 1)})

    def test_finds_invader_bottom_left(self):
        radar = make_df('\n'.join(['0000',
                                   '0001',
                                   '0000']))
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(2, 1)})

    def test_finds_invader_middle(self):
        radar = make_df('\n'.join(['0000',
                                   '0010',
                                   '0000',
                                   '0000']))
        invader = make_df('01\n00')
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1)})

    def test_finds_multiple_invaders(self):
        radar = make_df('\n'.join(['11000',
                                   '11011',
                                   '11011',
                                   '00011']))
        invader = make_df('\n'.join(['11', '11', '11']))
        found = scan(radar, invader)
        self.assertEqual(found, {(0, 0), (3, 1)})

    def test_finds_overlapping_invaders(self):
        radar = make_df('\n'.join(['0000000',
                                   '0111110',
                                   '0111110',
                                   '0000110',
                                   '0000000']))
        invader = make_df('\n'.join(['11', '11']))
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1), (2, 1), (3, 1), (4, 1), (4, 2)})

    # Edges and corners

    def test_finds_invader_over_bottom_edge(self):
        radar = make_df('000\n000\n010')
        invader = make_df('01\n11')
        found = scan(radar, invader)
        self.assertEqual(found, {(0, 2)})

    def test_finds_long_invader_over_bottom_edge(self):
        radar = make_df('000\n000\n001\n001')
        invader = make_df('01\n01\n11')
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 2), (1, 3)})

    def test_finds_overlapping_invaders_over_bottom_edge(self):
        radar = make_df('000\n111\n111')
        invader = make_df('11\n11\n11')
        found = scan(radar, invader)
        self.assertEqual(found, {(0, 1), (1, 1), (0, 2), (1, 2)})

    def test_finds_invader_over_top_edge(self):
        radar = make_df('011\n000\n000\n000')
        invader = make_df('01\n01\n11')
        found = scan(radar, invader)
        self.assertEqual(found, {(1, -2)})

    def finds_multiple_invaders_over_top_edge(self):
        radar = Radar('11\n11\n00')
        alien = Invader('\n'.join(['11', '11', '11']))
        found = radar.scan(alien)

    def finds_invaders_over_left_edge_of_radar(self):
        radar = Radar('00\n10\n10')
        invader = ['01', '11']

    def finds_invaders_over_right_edge_of_radar(self):
        radar = Radar('00\n10\n10')
        invader = ['01', '11']

    def finds_invaders_over_corners(self):
        radar = Radar('000\n000\n001')
        invader = ['11', '11']
        self.assertEqual(found, [(2, 2)])

        radar = Radar('000\n000\n100')
        invader = ['11', '11']
        self.assertEqual(found, [(-1, 2)])

        radar = Radar('001\n000\n000')
        invader = ['11', '11']
        self.assertEqual(found, [(2, 1)])
        radar = Radar('100\n000\n000')
        invader = ['11', '11']
        self.assertEqual(found, [(2, 1)])


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
