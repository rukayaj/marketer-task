import pandas as pd


class _BaseMatrix(pd.DataFrame):
    @property
    def _constructor(self):
        return _BaseMatrix

    def __init__(self, data=None, data_list=None, *args, **kwargs):
        # TODO needs an exception raised if someone tries to make an empty radar or invader
        if data_list:
            data = [list(x) for x in data_list]
        super(_BaseMatrix, self).__init__(data, *args, **kwargs)


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

    def scan(self, invader, tolerance=0):  # A tolerance of 0 = must be perfect match, 0.2 = 80% match, etc
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
                if invader.matched_in(radar_subset, tolerance):
                    found.add((x - i_width + 1, y - i_length + 1))

        return found


class InvaderMatrix(_BaseMatrix):
    @property
    def _constructor(self):
        return InvaderMatrix

    def area(self):
        length, width = self.shape
        return length  *  width

    def get_tolerance_threshold(self, tolerance):
        total_chars = self.area()
        return total_chars - (total_chars *  tolerance)

    def count_non_matches(self, masker):
        masked_invader = self.copy()
        for i, row in masker.iteritems():
            masked_invader[i] = ['*' if row[j] == '*' else x for j, x in enumerate(masked_invader[i])]
        # The above should really be in a separate method
        return masked_invader.isin(masker).sum().sum()

    def matched_in(self, radar_subset, tolerance):
        number_of_matching_chars = self.count_non_matches(radar_subset)
        return number_of_matching_chars >= self.get_tolerance_threshold(tolerance)
