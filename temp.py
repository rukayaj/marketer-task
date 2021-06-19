import pandas as pd

def make_df(s):
    s = s.split('\n')
    return pd.DataFrame([list(x) for x in s])

def get_match_tolerance_threshold(total_chars, tolerance):
    return total_chars - (total_chars * tolerance)

def crop(matrix, min_y, max_y, min_x, max_x):
    matrix = matrix.iloc[min_y:max_y, min_x:max_x]
    return matrix.reset_index(drop=True).T.reset_index(drop=True).T

def scan(radar, invader, tolerance=0):  # A tolerance of 0 = must be perfect match, 0.2 = 80% match, etc
    i_length, i_width = invader.shape
    match_tolerance_threshold = get_match_tolerance_threshold(i_width * i_length, tolerance)
    print(f'threshold: {match_tolerance_threshold}')
    found = set()
    print(f'invader: {invader}')
    print('--------')
    print(radar)
    print('--------')
    y_padding = pd.DataFrame(columns=range(i_length - 1))
    padded = pd.concat([y_padding, radar, y_padding], axis=1, ignore_index=True)
    x_padding = pd.DataFrame(columns=padded.columns, index=['*' for x in range(i_width - 1)])
    padded = pd.concat([x_padding, padded, x_padding], axis=0, ignore_index=True).fillna('*')
    r_length, r_width = padded.shape
    for x in range(r_width - i_width + 1):
        for y in range(r_length - i_length + 1):
            crop_radar = crop(padded, y, y + i_length, x, x + i_width)
            print(f'{y}:{y + i_length}, {x}:{x + i_width}')
            print(crop_radar)
            print('----')
            number_of_matching_chars = invader.isin(crop_radar).sum().sum()
            print(f'matches: {number_of_matching_chars}')
            if number_of_matching_chars >= match_tolerance_threshold:
                print(f'adding  {y}, {x}')
                import pdb; pdb.set_trace()
                found.add((x - i_width, y - i_length))

    return found
    found = set()

    # bottom edge
    for il in range(i_length - 1, 0, -1):
        invader_crop = crop(invader, 0, il, 0, i_width)
        print(f'invader_crop: {invader_crop}')
        ic_length, ic_width = invader_crop.shape
        new_t = get_match_tolerance_threshold(ic_width * ic_length, tolerance)
        min_y  = r_length - ic_length
        for x in range(r_width - ic_width + 1):
            radar_crop = crop(radar, min_y, r_length, x, x + ic_width)
            number_of_matching_chars = invader_crop.isin(radar_crop).sum().sum()
            print(f'radar_crop: {radar_crop}')
            import pdb; pdb.set_trace()
            if number_of_matching_chars >= new_t:
                found.add((x, min_y))
    #return found
    found = set()

    # top edge
    print(f'invader: {invader}')
    for il in range(i_length - 1, 0, -1):
        invader_crop = crop(invader, il, i_length, 0, i_width)
        print(f'invader_crop: {invader_crop}')
        ic_length, ic_width = invader_crop.shape
        max_y = ic_length
        new_t = get_match_tolerance_threshold(ic_width * ic_length, tolerance)
        for x in range(r_width - ic_width + 1):
            radar_crop = crop(radar, 0, max_y, x, x + ic_width)
            print(f'radar_crop: {radar_crop}')
            number_of_matching_chars = invader_crop.isin(radar_crop).sum().sum()
            import pdb; pdb.set_trace()
            if number_of_matching_chars >= new_t:
                found.add((x, ic_length - i_length))


    print(found)
    return found


    for y in range(r_length):
        for x in range(r_width):
            crop_y = min(y + i_length, r_length)
            crop_x = min(x + i_width, r_width)
            crop_radar = radar.iloc[y:crop_y, x:crop_x]
            crop_invader = invader.iloc[0:crop_y, 0:crop_x]
            print(f'radar crop: [{y}:{crop_y}, {x}: {crop_x}]')
            print(crop_radar)
            print(f'invader crop: [{y}:{crop_y}, {x}: {crop_x}]')
            print(crop_invader)
            number_of_matching_chars = crop_invader.isin(crop_radar).sum().sum()
            if number_of_matching_chars > tolerance:
                found.add((y, x))
            import pdb; pdb.set_trace()

def get_number_of_matching_chars(radar, invader):
    return invader.isin(radar).sum().sum()


"""
    for radar_y, line in enumerate(self.body):
        top_overflow = invader.length - radar_y
        if top_overflow > 0:
            for i in range(top_overflow):


        if radar_y < invader.length):
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



def scan_top(radar, invader, tolerance=0):
    invader_width = invader.shape[0]
    invader_length = invader.shape[1]
    for y in range(invader_length):
        for x in range(invader_width):
            radar_crop = radar[0:y + 1][0:x + 1]
            print('radar: ')
            print(f'[0:{y + 1}][0:{x + 1}]')
            print(radar_crop)

            invader_crop = invader[y + 1:][x + 1:]
            print('invader: ')
            print(f'[{y + 1}:][{x + 1}:]')
            print(invader_crop)

            temp = radar_crop.isin(invader_crop)
            print(temp)


        def scan_overflow_y(radar, invader, tolerance=0):
        for radar_y, line in enumerate(self.body):
"""


