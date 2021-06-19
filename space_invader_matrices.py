import pandas as pd

class RadarMatrix(pd.DataFrame):
    @property
    def _constructor(self):
        return RadarMatrix

    def __init__(self, data=None, data_string=None, data_list=None, *args, **kwargs):
        if data_string:
            data = [list(x) for x in data_string.split('\n')]
        if data_list:
            data = [list(x) for x in data_list]
        super(RadarMatrix, self).__init__(data, *args, **kwargs)

    def pad(self, y, x):
        y_padding = RadarMatrix(columns=range(y - 1))
        padded = pd.concat([y_padding, self, y_padding], axis=1, ignore_index=True)
        x_padding = RadarMatrix(columns=padded.columns, index=['*' for x in range(x - 1)])
        return pd.concat([x_padding, padded, x_padding], axis=0, ignore_index=True).fillna('*')

    def crop(self, min_y, max_y, min_x, max_x):
        matrix = self.iloc[min_y:max_y, min_x:max_x]
        return matrix.reset_index(drop=True).T.reset_index(drop=True).T
