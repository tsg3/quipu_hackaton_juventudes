def even_sort(arr_1, arr_2):
    length_1 = len(arr_1)
    length_2 = len(arr_2)
    total_length = length_1 + length_2

    i_arr_1 = 0
    i_arr_2 = 0

    res = []

    # Same size 

    if length_1 == length_2:
        n = total_length >> 1
        while i_arr_1 < n:
            res.append(arr_1[i_arr_1])
            res.append(arr_2[i_arr_1])

            i_arr_1 += 1

    # arr_1 0

    elif length_1 == 0:
        return arr_2

    # arr_2 0

    elif length_2 == 0:
        return arr_1

    # 1+ | 1-

    elif abs(length_1 - length_2) == 1:
        n = total_length >> 1

        if length_1 > length_2:
            res.append(arr_1[n])

            while i_arr_1 < n:
                res.append(arr_2[i_arr_1])
                res.append(arr_1[i_arr_1])

                i_arr_1 += 1

        else:
            res.append(arr_2[n])

            while i_arr_1 < n:
                res.append(arr_1[i_arr_1])
                res.append(arr_2[i_arr_1])

                i_arr_1 += 1
    
    else:
        unit_arr_1_percent = 100 / length_1
        unit_arr_2_percent = 100 / length_2

        i_total = 0
        arr_1_percent_total = 0
        arr_2_percent_total = 0

        while i_total < total_length:
            if arr_1_percent_total <= arr_2_percent_total:
                res.append(arr_1[i_arr_1])
                i_arr_1 += 1
                arr_1_percent_total += unit_arr_1_percent
            else:
                res.append(arr_2[i_arr_2])
                i_arr_2 += 1
                arr_2_percent_total += unit_arr_2_percent
            i_total += 1

    return res