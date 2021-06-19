import pandas as pd
from base_matrix import _BaseMatrix

class RadarMatrix(_BaseMatrix):
    @property
    def _constructor(self):
        return RadarMatrix

    def pad(self, y, x):  # TODO double check that pad isn't already a pd.df method
        y_padding = RadarMatrix(columns=range(y))
        padded = pd.concat([y_padding, self, y_padding], axis=1, ignore_index=True)
        x_padding = RadarMatrix(columns=padded.columns, index=['*' for x in range(x)])
        return pd.concat([x_padding, padded, x_padding], axis=0, ignore_index=True).fillna('*')

    def crop(self, min_y, max_y, min_x, max_x):
        matrix = self.iloc[min_y:max_y, min_x:max_x]
        return matrix.reset_index(drop=True).T.reset_index(drop=True).T

    def scan(self, invader, tolerance=0):
        """
        Note that tolerance of 0 = must be a perfect match,  0.2 = 80% match, etc
        Returns upper left coordinates of each found invader
        """
        i_length, i_width = invader.shape
        radar = self.pad(i_length - 1, i_width - 1)
        r_length, r_width = radar.shape
        # TODO raise exception if radar is smaller than invader
        found = set()
        # Maybe the nested for loops here should be an iterator which yields radar_subsets, then can do e.g.:
        # for subset in self.subsets(width, length): if invader.matched_in(subset, tolerance) ....
        for x in range(r_width - i_width + 1):
            for y in range(r_length - i_length + 1):
                radar_subset = radar.crop(y, y + i_length, x, x + i_width)
                # Ideally here we should get a matching score, not just a boolean and then return in order of likeliness
                if invader.matched_in(radar_subset, tolerance):
                    found.add((x - i_width + 1, y - i_length + 1))

        return found
