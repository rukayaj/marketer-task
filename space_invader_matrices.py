import pandas as pd

def get_match_tolerance_threshold(total_chars, tolerance):
    return total_chars - (total_chars * tolerance)


class BaseMatrix(pd.DataFrame):
    @property
    def _constructor(self):
        return BaseMatrix

    def __init__(self, data=None, data_list=None, *args, **kwargs):
        if data_list:
            data = [list(x) for x in data_list]
        super(BaseMatrix, self).__init__(data, *args, **kwargs)


class RadarMatrix(BaseMatrix):
    @property
    def _constructor(self):
        return RadarMatrix

    def pad(self, y, x):
        y_padding = RadarMatrix(columns=range(y - 1))
        padded = pd.concat([y_padding, self, y_padding], axis=1, ignore_index=True)
        x_padding = RadarMatrix(columns=padded.columns, index=['*' for x in range(x - 1)])
        return pd.concat([x_padding, padded, x_padding], axis=0, ignore_index=True).fillna('*')

    def crop(self, min_y, max_y, min_x, max_x):
        matrix = self.iloc[min_y:max_y, min_x:max_x]
        return matrix.reset_index(drop=True).T.reset_index(drop=True).T

    def scan(self, invader, tolerance=0):  # A tolerance of 0 = must be perfect match, 0.2 = 80% match, etc
        i_length, i_width = invader.shape
        match_tolerance_threshold = get_match_tolerance_threshold(i_width * i_length, tolerance)
        print(f'threshold: {match_tolerance_threshold}')
        found = set()
        print(f'invader: {invader}')
        print('--------')
        print(f'radar: {self}')
        print('--------')
        radar = self.pad(i_length, i_width)
        print('--------')
        print(f'radar padded: {radar}')
        print('--------')
        r_length, r_width = radar.shape
        for x in range(r_width - i_width + 1):
            for y in range(r_length - i_length + 1):
                crop_radar = radar.crop(y, y + i_length, x, x + i_width)
                print(f'{y}:{y + i_length}, {x}:{x + i_width}')
                print(f'crop radar: {crop_radar}')
                print('----')
                masked_invader = invader.copy()
                for i, row in crop_radar.iteritems():
                    masked_invader[i] = ['*' if row[j] == '*' else x for j, x in enumerate(masked_invader[i])]
                number_of_matching_chars = masked_invader.isin(crop_radar).sum().sum()
                print(f'masked invader: {masked_invader}')
                print(f'matches: {number_of_matching_chars}')
                if number_of_matching_chars >= match_tolerance_threshold:
                    print(f'adding  {x - i_width + 1}, {y - i_length + 1}')
                    found.add((x - i_width + 1, y - i_length + 1))

        return found


class InvaderMatrix(BaseMatrix):
    @property
    def _constructor(self):
        return InvaderMatrix
