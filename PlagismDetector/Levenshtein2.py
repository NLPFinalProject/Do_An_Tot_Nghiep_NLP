# ----------------Thêm, xóa, thay thế chữ"----------------#


def String_insert(string, text, position):
    return string[:position] + text + string[position:]


def String_delete(string, position):
    return string[:position] + string[(position + 1) :]


def String_substitute(string, new_text, position):
    return string[:position] + new_text + string[(position + 1) :]


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

    case_1 = "insertion"
    case_2 = "deletion"
    case_3 = "substitution"
    case_4 = "0"

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
                backtrace_list.append(case_1 + "_" + str2[str2_char_index])
                r_NextCell = r_NextCell - 1
            else:
                if value == deletions:
                    backtrace_list.append(case_2 + "_" + str1[str1_char_index])
                    c_NextCell = c_NextCell - 1
                else:
                    if value == substitutions:
                        backtrace_list.append(case_3 + "_" + str2[str2_char_index])
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
    matrix = Create_Matrix(str1, str2)
    rows = len(matrix)
    cols = len(matrix[0])
    return matrix[rows - 1][cols - 1]


# Source: https://stackoverflow.com/questions/14260126/how-python-levenshtein-ratio-is-computed
# Tính tỉ lệ tương đồng giữa 2 chuỗi
# Input: 2 chuỗi (String)
#    + Str1 (String)
#    + Str2 (String)
# Output: Tỉ lệ tương đồng bao nhiêu % (Float)
def Matching_ratio(str1, str2):
    l = Levenshtein_distance(str1, str2)
    m = len(str1)
    if m < len(str2):
        m = len(str2)
    ratio = (1 - l / m) * 100

    return ratio


# Tính tỉ lệ tương đồng của từng câu trong mảng 1 với từng câu trong mảng 2
# Input:
#    + List_1 (String)
#    + List_2 (String)
# Output: List các giá trị tương đồng (Float)
def Matching_ratio_list(lst_1, lst_2):
    result = []

    for str1 in lst_1:
        for str2 in lst_2:
            ratio = Matching_ratio(str1, str2)
            result.append(ratio)

    return result


# Xuất kết quả
# Input:
#    + List các kết quả đã tính ở hàm Matching_ratio_list
#    + List_1 (String)
#    + List_2 (String)
# Output: Hiển thị theo format: "câu a - câu b: (tỉ lệ tương đồng) %"
# vd: 123456 - 3456: 66.666667 %
def Export(result_list, lst_1, lst_2):
    len_result = len(result_list)
    # len_2 = len(lst2)

    index = 0
    # tra ket qua ve list
    report_list = []
    for str1 in lst_1:
        for str2 in lst_2:
            string = str1 + " - " + str2 + ": " + str(result_list[index]) + " %"
            # print(string)
            report_list.append(string)
            index += 1
    return report_list


def main():
    lst1 = ["Python", "C-Sharp", "Java"]
    lst2 = ["JavaScript", "Swift", "C++", "Python"]

    result = Matching_ratio_list(lst1, lst2)
    Export(result, lst1, lst2)


if __name__ == "__main__":
    main()

# CHỈ CẦN CHẠY THÔI LÀ SẼ XUẤT KẾT QUẢ, KHÔNG CẦN CHỈNH SỬA GÌ.
