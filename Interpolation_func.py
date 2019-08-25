import math
import Graphs

"""Определение организации входных данных
Input_data = [
            inter_type, //Тип G-кода (0: G00, 1: G01, 3: G02)
            P_start,    //Стартовая точка блока ([X, Y, Z])
            P_finish,   //Конечная точка блока ([X, Y, Z])
            Vel_list,   //Список скоростей для каждого времени интерполяции [V1, V2, ..., Vn]
            T_list,     //Список периодов интерполяции [T1, T2, ..., Tn]
            ]
"""

def Interfunc_Type(trajectory_data):
    if trajectory_data[0] == 1:
        #1 - G00 - линейная интерполяция
        result_data = Interfunc_Linear(trajectory_data)
    elif trajectory_data[0] == 2:
        #2 - G01 - линейная интепроляция
        result_data = ["0"]
    elif trajectory_data[0] == 3:
        #3 - G02 - круговая интерполяция
        result_data = ["0"]
    else:
        result_data = ["Не указан тип интерполяции."]
    return result_data

def Length_linear(start, end):
    length = math.sqrt((math.pow((end[0]-start[0]), 2))+(math.pow((end[1]-start[1]), 2)))
    return length

def Interfunc_Linear(trajectory_data):
    #Определение длины пути
    length_hole = Length_linear(trajectory_data[1], trajectory_data[2])
    S = 0
    Tipo = 0.005
    x_list = []
    y_list = []
    x_list.append(trajectory_data[1][0])
    y_list.append(trajectory_data[1][1])
    x_tmp = trajectory_data[1][0]
    y_tmp = trajectory_data[1][1]
    for i in range (200):
        if i == 0:
            Si = Tipo*10
            delta_x = Si*((trajectory_data[2][0]-trajectory_data[1][0])/length_hole)
            delta_y = Si*((trajectory_data[2][1]-trajectory_data[1][1])/length_hole)
            x_tmp += delta_x
            y_tmp += delta_y
            x_list.append(x_tmp)
            y_list.append(y_tmp)
            S += Si
            #Si = Tipo*(trajectory_data[3][i]+0)
        elif i > 0:
            Si = Tipo*10
            delta_x = Si*((trajectory_data[2][0]-trajectory_data[1][0])/length_hole)
            delta_y = Si*((trajectory_data[2][1]-trajectory_data[1][1])/length_hole)
            x_tmp += delta_x
            y_tmp += delta_y
            x_list.append(x_tmp)
            y_list.append(y_tmp)
            S += Si
            #Si = Tipo*(trajectory_data[3][i]+trajectory_data[3][i-1])
    return S, length_hole, x_list, y_list


"""vel_profile = Profile_generation.Velocity_profile(15, 15, time_periods[0], time_periods[1],
                                                  time_periods[2], time_interpolation, vel_start, feedrate_list[i])"""

inter_result = Interfunc_Type([1, [0, 0], [10, 10], [10, 10, 10, 10, 10, 10]])
print(inter_result[0])

Graphs.Plotting_01(inter_result[2], inter_result[3], 'da', 'da', 'da', 'da', 'da')


