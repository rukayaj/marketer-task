from scipy.spatial.distance import hamming

def hamming_str(a, b):
    return hamming(list(a), list(b))


class Invader:
    def __init__(self, s):
        self.body = s.split('\n')
        self.width = len(self.body[0])
        self.length = len(self.body)


class Radar:
    def __init__(self, s):
        self.body = s.split('\n')
        self.width = len(self.body[0])
        self.length = len(self.body)
        if not self.width or not self.length:
            raise ValueError('Must have a height and width')
        if not all(len(x) == self.width for x in self.body):
            raise ValueError('Must be rectangular or square in shape')

    def scan(self, invader, tolerance=0):
        found = set()

        for radar_y, line in enumerate(self.body):
            if (radar_y + invader.length) > self.length:
                break
            for radar_x in range(self.width):
                if (radar_x + invader.width) > self.width:
                    break
                cumulative_diff = 0
                for i in range(invader.length):
                    next_radar_line = self.body[radar_y + i]
                    radar_line_subset = next_radar_line[radar_x:radar_x + invader.width]
                    cumulative_diff += hamming_str(radar_line_subset, invader.body[i])
                    if cumulative_diff > tolerance:
                        break
                    if i == invader.length - 1:
                        found.add((radar_x, radar_y))

        return found




