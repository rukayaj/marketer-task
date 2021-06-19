import unittest
from temp import _im, scan, get_match_tolerance_threshold


class TestRadarScan(unittest.TestCase):
    @staticmethod
    def _strify(_list):
        return '\n'.join(_list)

    def test_get_match_tolerance_threshold_0(self):
        res = get_match_tolerance_threshold(500, 0)
        self.assertEqual(res, 500)

    def test_finds_invaders_simple(self):
        radar = _im(['01', '00'])
        import pdb; pdb.set_trace()
        invader = _im(['01', '00'])
        found = scan(radar, invader)
        top_left_corner = (-1, -1)
        middle = (0, 0)
        bottom_right_corner = (1, 1)
        self.assertEqual(found, {top_left_corner, middle, bottom_right_corner})

    def test_finds_invader_top_right(self):
        radar = _im(['0001',
                     '0001',
                     '0000'])
        invader = _im(['01', '01'])
        found = scan(radar, invader)
        self.assertEqual(found, {(2, -1), (2, 0), (3, 2)})

    def test_finds_invader_top_left(self):
        radar = _im(['1000',
                                   '1000',
                                   '0000'])
        invader = _im(['10', '10'])
        found = scan(radar, invader)
        self.assertEqual(found, {(0, -1), (0, 0), (-1, 2)})

    def test_finds_invader_bottom_right(self):
        radar = _im(['0000',
                                   '0001',
                                   '0001'])
        invader = _im(['01', '01'])
        found = scan(radar, invader)
        self.assertEqual(found, {(3, -1), (2, 1), (2, 2)})

    def test_finds_invader_bottom_left(self):
        radar = _im(['0000',
                                   '1000',
                                   '1000'])
        invader = _im(['10', '10'])
        found = scan(radar, invader)
        self.assertEqual(found, {(-1, -1), (0, 1), (0, 2)})

    def test_finds_invader_middle(self):
        radar = _im(['0000',
                                   '0110',
                                   '0110',
                                   '0000'])
        invader = _im(['11', '11'])
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1)})

    def test_finds_multiple_invaders(self):
        radar = _im(['0000000',
                                   '0110110',
                                   '0110110',
                                   '0000000'])
        invader = _im(['11', '11'])
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1), (4, 1)})

    def test_finds_overlapping_invaders(self):
        radar = _im(['0000000',
                                   '0111110',
                                   '0111110',
                                   '0000110',
                                   '0000000'])
        invader = _im(['11', '11'])
        found = scan(radar, invader)
        self.assertEqual(found, {(1, 1), (2, 1), (3, 1), (4, 1), (4, 2)})

    # With noise

    def test_finds_invaders_with_noise_tolerance(self):
        radar = _im(['0000',
                                   '0010',
                                   '0110',
                                   '0000'])
        alien = _im(['11', '11'])
        found = scan(radar, alien, 0.25)
        self.assertEqual(found, {(-1, -1), (3, -1), (1, 1), (-1, 3), (3, 3)})

    def test_excludes_invader_with_too_much_noise(self):
        radar = _im(['0000',
                                   '0010',
                                   '0010',
                                   '0000'])
        alien = _im(['11', '11'])
        found = scan(radar, alien, 0.25)
        self.assertEqual(found, {(-1, -1), (3, -1), (-1, 3), (3, 3)})

if __name__ == '__main__':
    unittest.main()
