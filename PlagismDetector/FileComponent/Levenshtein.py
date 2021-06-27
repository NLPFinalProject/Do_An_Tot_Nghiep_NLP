import time
import Levenshtein as L
from FileComponent.deep import *

def String_insert(string, text, position):
    return string[:position] + text + string[position:]


def String_delete(string, position):
    return string[:position] + string[(position + 1):]


def String_substitute(string, new_text, position):
    return string[:position] + new_text + string[(position + 1):]


#---------------Thuật toán tính khoảng cách Levenshtein----------------#

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
    #time3=time.time()
    matrix = Create_Matrix(str1, str2)
    #print("line 315 create matrix mất %s seconds ---" % (time.time() - time3))
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
def ExportOrder(lst_1, lst_2, ratio):
    result = []
    time1=time.time()
    #print("độ dài 2 lst là: ",len(lst_1),len(lst_2))
    for i in range(len(lst_1)):
        export = []
        similar_sent = []
        similar_ratio = []
        count = 0
        for j in range(len(lst_2)):
            #time2 = time.time()
            #CurrentRatio = Matching_ratio(lst_1[i], lst_2[j])
            CurrentRatio = L.ratio(lst_1[i], lst_2[j])*100
            #print("line 384 mất %s seconds ---" % (time.time() - time2))
            if CurrentRatio >= ratio:
                count += 1
                similar_sent.append(j + 1)
                similar_ratio.append(CurrentRatio)
        export.append(i + 1)
        export.append(count)
        export.append(similar_sent)
        export.append(similar_ratio)
        result.append(export)
    #print("line 395 export mất %s seconds ---" % (time.time() - time1))
    return result

def ExportOrder2(lst_1, lst_2, ratio):
    result = []

    for i in range(len(lst_1)):
        export = {}
        similar_sent = []
        count = 0
        for j in range(len(lst_2)):
            if L.ratio(lst_1[i], lst_2[j])*100 >= ratio:
                count += 1
                similar_sent.append(j + 1)

        export['line'] = i + 1
        export['count'] =count
        export['lst'] =similar_sent
        result.append(export)
    
    return result
def ExportOrder3(lst_1, lst_2, ratio):
    result = []

    for i in range(len(lst_1)):
        export = {}
        similar_sent = []
        similar_ratio =[]
        count = 0
        for j in range(len(lst_2)):
            CurrentRatio = L.ratio(lst_1[i], lst_2[j])*100
            if CurrentRatio >= ratio:
                count += 1
                similar_sent.append(j + 1)
                similar_ratio.append(CurrentRatio)
        export['line'] = i + 1
        export['count'] =count
        export['lst'] =similar_sent
        export['ratio']=similar_ratio
        result.append(export)
    
    return result

# them ham exportorder3 vao levenshtein
def ExportOrder4(lst_1, lst_2, ratio):
    #print("độ dài 2 list là: ",len(lst_1),len(lst_2))
    result = []
    length = 0
    for i in range(len(lst_1)):
        export = []
        similar_sent = []
        similar_ratio = []
        count = 0
        for j in range(len(lst_2)):
            CurrentRatio = L.ratio(lst_1[i], lst_2[j])*100
            if CurrentRatio >= ratio:
                count += 1
                similar_sent.append(j + 1)
                similar_ratio.append(CurrentRatio)
        if count != 0:
            length += 1
        export.append(i + 1)
        export.append(count)
        export.append(similar_sent)
        export.append(similar_ratio)
        result.append(export)
        sum_ratio=sum(similar_ratio)/(100*len(lst_1))
    return result, length*sum_ratio/len(lst_1)*100



def main():
    lst1 = ['Hồ chủ tịch vĩ đại']
    lst2 = ['Không có kính vì xe không có kính']

    result = ExportOrder4(lst1, lst2,50)
    print(result)




if __name__ == "__main__":
    main()

