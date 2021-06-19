from base_matrix import _BaseMatrix


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
