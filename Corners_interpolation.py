import Graphs
import CIRCLE
import Spline
import math
import Work_with_files
import Path_length_calculator
import Trajectory_mapping
import Block_type
import Profile_generation

'CNC parameters'
BLU = 0.01 #mm
T = 0.01 #sec
V = 25 #mm/sec

'Corner parameters'
Lt = 1
n = 0.9

"""Исходные данные траектории"""
"Начальные и конечные точки"
st_point = [[0, 0, 0],
            [50, 50, 0]]
fn_point = [[50, 50, 0],
            [100, 0, 0]]

"Степень точности обработки углов"
tolerance_angle = [10, 10]
ratio = [0.95, 0.4]

"Определение углов между участками траектории"
print("Анализ углов участков траектории.")
angles = Trajectory_mapping.Trajectory_analisys(st_point, fn_point)
for i in range (len(angles)):
    print(Work_with_files.Write_log("Между участками " + str(i+1) + " и " + str (i+2) + " имеется угол в " + str(angles[i]) + " град."))

length_1 = CIRCLE.Length_linear(st_point[0], fn_point[0])
length_2 = CIRCLE.Length_linear(st_point[1], fn_point[1])

start = Spline.Point_find (st_point[0], fn_point[0], length_1, 0)
finish = Spline.Point_find (st_point[1], fn_point[1], length_2, 1)
spline_result = Spline.Spline6_interpolation(tolerance_angle[0], ratio[0], st_point[0], fn_point[0], st_point[1], fn_point[1], T, V)
spline_result_1 = Spline.Spline6_interpolation(tolerance_angle[1], ratio[1], st_point[0], fn_point[0], st_point[1], fn_point[1], T, V)
print('Острый угол')
print('Минимальная величина сегмента: ' + str(min(spline_result[9])))
print('Максимальная величина сегмента: ' + str(max(spline_result[9])))
print('Число сегментов: ' + str(len(spline_result[9])))
print('Минимальная ошибка: ' + str(min(spline_result[10])))
print('Максимальная ошибка: ' + str(max(spline_result[10])))

print('Тупой угол')
print('Минимальная величина сегмента: ' + str(min(spline_result_1[9])))
print('Максимальная величина сегмента: ' + str(max(spline_result_1[9])))
print('Число сегментов: ' + str(len(spline_result_1[9])))
print('Минимальная ошибка: ' + str(min(spline_result_1[10])))
print('Максимальная ошибка: ' + str(max(spline_result_1[10])))
#print('Контурная ошибка: ' + str(max(circle_test[3])))
#print('Контурная ошибка: ' + str(min(circle_test[3])))

#Graphs.Plotting_bw2(spline_result[0], spline_result[1], spline_result[3], spline_result[4], "X, mm", "Y, mm", "Corner smoothing example",
#                    "Curve", "Acute angle", "PIC_3")

Graphs.Plotting_bw3(spline_result[3], spline_result[4], spline_result[0], spline_result[1], spline_result_1[0], spline_result_1[1], "X, mm", "Y, mm",
                    "Corner smoothing example", "Input segment", "Rounding, n = 0.95", "Rounding, n = 0.4", "PIC_3")
