import pandas as pd

class RadarMatrix(pd.DataFrame):

    @property
    def _constructor(self):
        return RadarMatrix

    def pad(self, y, x):
        y_padding = pd.DataFrame(columns=range(y - 1))
        padded = pd.concat([y_padding, self.data, y_padding], axis=1, ignore_index=True)
        x_padding = pd.DataFrame(columns=padded.columns, index=['*' for x in range(x - 1)])
        padded = pd.concat([x_padding, padded, x_padding], axis=0, ignore_index=True).fillna('*')
        return padded

    def crop(self, min_y, max_y, min_x, max_x):
        matrix = self.data.iloc[min_y:max_y, min_x:max_x]
        return matrix.reset_index(drop=True).T.reset_index(drop=True).T


class InvaderMatrix(pd.DataFrame):

    @property
    def _constructor(self):
        return InvaderMatrix
