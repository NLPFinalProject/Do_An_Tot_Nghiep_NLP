import Levenshtein as L
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MailComponent import views as mail
import sys
import os
sys.path.insert(1, os.getcwd() + "/ExportResultComponent")
from ExportResultComponent.deep import ratio

# Create your views here.
@api_view(['POST'])
def ExportResult(request):
    data = request.data
    mail.sendExportMail(data)
    return Response(status=status.HTTP_200_OK)


# Xuất kết quả theo format: [thứ tự câu trong lst_1,
# số câu trùng với câu trong lst_1, [các câu trùng theo thứ tự]]
# Ví dụ: [5, 3, [1, 6, 7]]:
# Ứng với câu thứ 5 trong lst_1, có 3 câu trùng, các câu trùng là 1, 6, 7
# Input:
#    + Lst_1 (String)
#    + Lst_2 (String)
#    + Ratio (Float): Mức ratio chuẩn để xác định một câu
#    có trùng với câu kia hay không? (>= ratio được xem là trùng)
# Output: List của các các kết quả như ví dụ trên
# Ví dụ: [[5, 3, [1, 6, 7]], [6, 1, [6]] , [4, 0, []]]
def ExportOrder(lst_1, lst_2, ratio):
    result = []
    sum_ratio = 0
    for i in range(len(lst_1)):
        export = []
        similar_sent = []
        similar_ratio = []
        count = 0
        for j in range(len(lst_2)):
            CurrentRatio = L.ratio(lst_1[i], lst_2[j]) * 100
            if CurrentRatio >= ratio:
                count += 1
                similar_sent.append(j + 1)
                similar_ratio.append(CurrentRatio)
        export.append(i + 1)
        export.append(count)
        export.append(similar_sent)
        export.append(similar_ratio)
        result.append(export)
        if (len(similar_ratio) != 0):
            sum_ratio += max(similar_ratio)
    return result, sum_ratio / len(lst_1)


# ham tinh toan co sử dụgn deep learning
def ExportOrder2(lst_1, lst_2, ratio):
    pre = ratio.ratio(lst_1, lst_2)
    result = []
    sum_ratio = 0
    for i in range(len(lst_1)):
        export = []
        similar_sent = []
        similar_ratio = []
        count = 0
        for j in range(len(lst_2)):
            CurrentRatio = pre[i * len(lst_2) + j]
            if CurrentRatio >= ratio:
                count += 1
                similar_sent.append(j + 1)
                similar_ratio.append(CurrentRatio)
        export.append(i + 1)
        export.append(count)
        export.append(similar_sent)
        export.append(similar_ratio)
        result.append(export)
        if (len(similar_ratio) != 0):
            sum_ratio += max(similar_ratio)
    return result, sum_ratio / len(lst_1)
