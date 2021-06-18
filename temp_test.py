import unittest
from temp import Radar, Invader


class TestRadar(unittest.TestCase):
    def test_it_does_not_allow_empty_radars(self):
        self.assertRaises(ValueError, Radar(''))

    def test_it_does_not_allow_triangular_radars(self):
        self.assertRaises(ValueError, Radar('0\n00\n0'))


class TestRadarScan(unittest.TestCase):
    def test_finds_invader_same_size_as_radar(self):
        found = Radar('01\n00').scan(Invader('01\n00'))
        self.assertEqual(found, {(0, 0)})

    def test_finds_invader_in_bigger_radar(self):
        radar = Radar('\n'.join(['0000',
                                 '0001',
                                 '0000']))
        found = radar.scan(Invader('01\n00'))
        self.assertEqual(found, {(2, 1)})

    def test_finds_multiple_invaders(self):
        radar = Radar('\n'.join(['11000',
                                 '11011',
                                 '11011',
                                 '00011']))
        found = radar.scan(Invader('\n'.join(['11', '11', '11'])))
        self.assertEqual(found, {(0, 0), (3, 1)})

    # With noise

    def test_finds_one_invader_with_noise_tolerance(self):
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

    def test_finds_multiple_invaders_with_noise_tolerance(self):
        radar = Radar('\n'.join(['01000',
                                 '01010',
                                 '11011',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = ((alien.width - 1) / alien.width) * 2
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, {(0, 0), (3, 1)})

    def test_excludes_multiple_invaders_with_noise_tolerance(self):
        radar = Radar('\n'.join(['01000',
                                 '01010',
                                 '11010',
                                 '00011']))
        alien = Invader('\n'.join(['11', '11', '11']))
        tolerance = (alien.width - 1) / alien.width
        found = radar.scan(alien, tolerance)
        self.assertEqual(found, set())

    # Edges and corners - no tolerance

    def finds_invaders_over_bottom_edge_of_radar(self):
        radar = Radar('00\n01\n11')
        invader = ['01', '11', '11']
        self.assertEqual(radar.scan(invader), [(0, 1)])

    def finds_invaders_over_top_edge_of_radar(self):
        radar = Radar('11\n00\n00')
        invader = ['01', '11']

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


if __name__ == '__main__':
    unittest.main()
