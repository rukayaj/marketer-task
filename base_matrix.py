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
