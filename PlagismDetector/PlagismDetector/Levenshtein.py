# Input: 2 chuoi bat ky
# Output: Khoang cach Levenshtein giua 2 chuoi


def String_insert(string, text, position):
    return string[:position] + text + string[position:]

def String_delete(string, position):
    return string[:position] + string[(position + 1):]

def String_substitute(string, new_text, position):
    return string[:position] + new_text + string[(position + 1):]

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

def Print_Process(str1, backtrace_list):
    
    case_1 = 'insertion'
    case_2 = 'deletion'
    case_3 = 'substitution'
    case_4 = '0'
    
    backtrace_list_index = 0
    str1_temp = str1
    string_index = len(str1_temp) - 1
    print(str1)

    while backtrace_list_index < len(backtrace_list):
        if backtrace_list[backtrace_list_index] != case_4:
            object_len = len(backtrace_list[backtrace_list_index])
            text = backtrace_list[backtrace_list_index][object_len - 1]
        
            if case_1 in backtrace_list[backtrace_list_index]:       
                str1_temp = String_insert(str1_temp, text, string_index + 1)
                string_index += 1
                print(str1_temp)

            if case_2 in backtrace_list[backtrace_list_index]:
                str1_temp = String_delete(str1_temp, string_index)
                print(str1_temp)
        
            if case_3 in backtrace_list[backtrace_list_index]:
                str1_temp = String_substitute(str1_temp, text, string_index)
                print(str1_temp)

        backtrace_list_index += 1
        string_index -= 1
    
def Levenshtein_distance(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return matrix[rows - 1][cols - 1]

def main():   
    print('Input 1: ')
    str1 = input()
    print('Input 2: ')
    str2 = input()

    matrix = Create_Matrix(str1,str2)

    print('\n')
    print('String 1: ', str1)
    print('String 2: ', str2)

    distance = 'Levenshtein distance: ' + str(Levenshtein_distance(matrix))
    print('\n')
    print(distance)

if __name__ == "__main__":
    main()