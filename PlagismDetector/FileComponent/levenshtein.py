import Levenshtein as L


def String_insert(string, text, position):
    return string[:position] + text + string[position:]


def String_delete(string, position):
    return string[:position] + string[(position + 1):]


def String_substitute(string, new_text, position):
    return string[:position] + new_text + string[(position + 1):]


# ---------------Thuật toán tính khoảng cách Levenshtein----------------#

def Create_Matrix(str1, str2):
    matrix = []

    # Create matrix
    row = []
    for i in range(len(str2) + 1):
        row = []
        if i == 0:
            for j in range(len(str1) + 1):
                row.append(j)
        else:
            row.append(i)

        matrix.append(row)

    # Find minimum edit distance
    previous_row = 0
    for i, c1 in enumerate(str2):
        row = []
        current_row = previous_row + 1
        for j, c2 in enumerate(str1):
            value = 0

            if c2 == c1:
                value = matrix[previous_row][j]
            else:
                substitutions = matrix[previous_row][j]
                deletions = matrix[previous_row + 1][j]
                insertions = matrix[previous_row][j + 1]
                value = min(substitutions, deletions, insertions) + 1

            matrix[current_row].append(value)

        previous_row += 1

    return matrix


def Create_Backtrace_List(str1, str2, matrix):
    backtrace_list = []

    case_1 = 'insertion'
    case_2 = 'deletion'
    case_3 = 'substitution'
    case_4 = '0'

    rows = len(matrix)
    cols = len(matrix[0])

    c_NextCell = cols - 1
    r_NextCell = rows - 1

    while r_NextCell > 0:
        str1_char_index = c_NextCell - 1
        str2_char_index = r_NextCell - 1

        if str1[str1_char_index] == str2[str2_char_index]:
            backtrace_list.append(case_4)
            c_NextCell = c_NextCell - 1
            r_NextCell = r_NextCell - 1

        else:
            substitutions = matrix[r_NextCell - 1][c_NextCell - 1]
            deletions = matrix[r_NextCell][c_NextCell - 1]
            insertions = matrix[r_NextCell - 1][c_NextCell]

            value = min(substitutions, deletions, insertions)

            if value == insertions:
                backtrace_list.append(case_1 + '_' + str2[str2_char_index])
                r_NextCell = r_NextCell - 1
            else:
                if value == deletions:
                    backtrace_list.append(case_2 + '_' + str1[str1_char_index])
                    c_NextCell = c_NextCell - 1
                else:
                    if value == substitutions:
                        backtrace_list.append(case_3 + '_' + str2[str2_char_index])
                        c_NextCell = c_NextCell - 1
                        r_NextCell = r_NextCell - 1

    return backtrace_list


# --------------------------------Phần trên là thuật toán, bắt đầu từ đây thôi-----------------------------------------#

# Khoảng cách Levenshtein giữa 2 chuỗi
# Input: 2 chuỗi (String)
#    + Str1 (String)
#    + Str2 (String)
# Output: Khoảng cách Levenshtein (kiểu Int)
def Levenshtein_distance(str1, str2):
    # time3=time.time()
    matrix = Create_Matrix(str1, str2)
    # print("line 315 create matrix mất %s seconds ---" % (time.time() - time3))
    rows = len(matrix)
    cols = len(matrix[0])
    return matrix[rows - 1][cols - 1]


# Source: https://stackoverflow.com/questions/14260126/how-python-levenshtein-ratio-is-computed
# Tính tỉ lệ tương đồng giữa 2 chuỗi
# Input: 2 chuỗi (String)
#    + Str1 (String)
#    + Str2 (String)
# Output: Tỉ lệ tương đồng bao nhiêu % (Float): Ví dụ 40%, 30%, 99.521%
def Matching_ratio(str1, str2):
    l = Levenshtein_distance(str1, str2)
    lensum = len(str1) + len(str2)
    return round((100 * (lensum - l) / lensum), 3)

    # m = len(str1)
    # if m < len(str2):
    #     m = len(str2)
    # return (1 - l/m) * 100


# Tính tỉ lệ tương đồng của từng câu trong mảng 1 với từng câu trong mảng 2
# Input: 
#    + Lst_1 (String)
#    + Lst_2 (String)
# Output: List của các dictionary. Với mỗi dictionary có format:
#    + 'senA': <câu A>
#    + 'senB': <câu B>
#    + 'ratio': <tỉ lệ tương đồng (ratio)> [kiểu float]
def Matching_ratio_dict(lst_1, lst_2):
    result = []

    key_1 = "senA"
    key_2 = "senB"
    key_3 = "ratio"

    for str1 in lst_1:
        for str2 in lst_2:
            dic = {}
            dic[key_1] = str1
            dic[key_2] = str2
            dic[key_3] = Matching_ratio(str1, str2)
            result.append(dic)

    return result


# Xuất kết quả theo format: [thứ tự câu trong lst_1, số câu trùng với câu trong lst_1, [các câu trùng theo thứ tự]]
# Ví dụ: [5, 3, [1, 6, 7]]: Ứng với câu thứ 5 trong lst_1, có 3 câu trùng, các câu trùng là 1, 6, 7
# Input: 
#    + Lst_1 (String)
#    + Lst_2 (String)
#    + Ratio (Float): Mức ratio chuẩn để xác định một câu có trùng với câu kia hay không? (>= ratio được xem là trùng)
# Output: List của các các kết quả như ví dụ trên
# Ví dụ: [[5, 3, [1, 6, 7]], [6, 1, [6]] , [4, 0, []]]

# them ham exportorder3 vao levenshtein
def ExportOrder(lst1, lst2, ratio):
    result = []
    length = 0
    sumRatio = 0
    for i in range(len(lst1)):
        export = []
        similarSen = []
        similarRatio = []
        count = 0
        for j in range(len(lst2)):
            CurrentRatio = L.ratio(lst1[i], lst2[j]) * 100
            if CurrentRatio >= ratio:
                count += 1
                similarSen.append(j + 1)
                similarRatio.append(CurrentRatio)
        if count != 0:
            length += 1
        export.append(i + 1)
        export.append(count)
        export.append(similarSen)
        export.append(similarRatio)
        result.append(export)
        if (len(similarRatio) != 0):
            sumRatio += max(similarRatio)
        return result, sumRatio / len(lst1)


# ham tinh toan co sử dụgn deep learning
def ExportOrder2(lst1, lst2, ratio):
    pre = ratio.ratio(lst1, lst2)
    result = []
    length = 0
    sumRatio = 0
    for i in range(len(lst1)):
        export = []
        similarSen = []
        similarRatio = []
        count = 0
        for j in range(len(lst2)):
            CurrentRatio = pre[i * len(lst2) + j]
            if CurrentRatio >= ratio:
                count += 1
                similarSen.append(j + 1)
                similarRatio.append(CurrentRatio)
        if count != 0:
            length += 1
        export.append(i + 1)
        export.append(count)
        export.append(similarSen)
        export.append(similarRatio)
        result.append(export)
        if (len(similarRatio) != 0):
            sumRatio += max(similarRatio)
        return result, sumRatio / len(lst1)
