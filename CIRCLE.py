import math
import Graphs
import Path_length_calculator
import sympy


def Length_linear(start, end):
    length = math.sqrt((math.pow((end[0]-start[0]), 2))+(math.pow((end[1]-start[1]), 2)))
    return length

"""Функция подсчета угла между участками траектории а и б.
На вход:
1. Стартовая точка траектории а в формате [x, y, z];
2. Конечная точка траектории а в формате [x, y, z];
2. Стартовая точка траектории б в формате [x, y, z];
3. Конечная точка траектории б в формате [x, y, z].
На выход: список из двух значений: угол в град., угол в радианах].
"""
def Angle_calc(start_p_1, finish_p_1, start_p_2, finish_p_2):
    if len(start_p_1) == 2:
        vector_1 = [finish_p_1[0] - start_p_1[0], finish_p_1[1] - start_p_1[1]]
    if len(start_p_2) == 2:
        vector_2 = [finish_p_2[0] - start_p_2[0], finish_p_2[1] - start_p_2[1]]
    cos = (vector_1[0]*vector_2[0]+vector_1[1]*vector_2[1])/(math.sqrt(vector_1[0]*vector_1[0]+vector_1[1]*vector_1[1])*
                                                             math.sqrt(vector_2[0]*vector_2[0]+vector_2[1]*vector_2[1]))
    angle_rad = math.acos(cos)
    angle_grad = math.degrees(math.acos(cos))
    return angle_grad, angle_rad

def Circle_interpolation (center_p, radius, BLU_CNC):
    point_1 = center_p
    s = 0
    x_axis = []
    y_axis = []
    section_1 = (math.pi*radius)/2
    section_12 = (math.pi*radius)
    while s < section_12:
        x_point = point_1[0] + radius*math.cos(s/radius)
        x_axis.append(x_point)
        y_point = point_1[1] + radius*math.sin(s/radius)
        y_axis.append(y_point)
        s += BLU_CNC
    return x_axis, y_axis

def Circle_parametric_interpolation (V, T, a, range_u):
    u = range_u[0]
    x_axis = []
    y_axis = []
    segment_len = []
    u_len = []
    error_len = []
    check = 0
    while u <= range_u[1]:
        x_p = a*math.sin(u)
        y_p = a*math.cos(u)
        x_axis.append(x_p)
        y_axis.append(y_p)
        u += V*T/a
        u_len.append(u)
        V += 0.5
        if check > 1:
            segment_len.append(Length_linear([x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]]))
            contour_e = contour_error_c (a, u_len[-2], u_len[-1], [x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]])
            error_len.append(contour_e)
        check += 1
    return x_axis, y_axis, segment_len, error_len

def contour_error_c (a, u_1, u_2, point_1, point_2):
    u = u_1 + (u_2-u_1)/2
    x_p = a*math.sin(u)
    y_p = a*math.cos(u)
    curve_middle = [x_p, y_p]
    base = Length_linear(point_1, point_2)
    side_left = Length_linear(point_1, curve_middle)
    side_right = Length_linear(curve_middle, point_2)
    p = 0.5*(base+side_left+side_right)
    error = 2*math.sqrt(p*(p-side_left)*(p-side_right)*(p-base))/base
    return error

def Curve_conventional_2D ():
    u = 0
    x_axis = []
    y_axis = []
    segment_len = []
    u_len = []
    error_len = []
    check = 0
    while u <= 1.001:
        #x_p = -140*math.pow(u,3)+90*math.pow(u,2)+90*u
        #y_p = -90*math.pow(u,2)+90*u
        #x_p = -90*(u**3)+5*(u**2)+70*u
        #y_p = -25*(u**2)+70*u
        x_p = -90*(u**3)+5*(u**2)+85*u
        y_p = 10*math.sin(u)
        x_axis.append(x_p)
        y_axis.append(y_p)
        u += 0.01
        u_len.append(u)
        if check > 1:
            segment_len.append(Length_linear([x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]]))
            error_c = contour_error (u_len[-2], u_len[-1], [x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]])
            error_len.append(error_c)
        check += 1
    return x_axis, y_axis, check, error_len, segment_len

def Curve_equal_s_2D (feedrate, t_sample):
    z = 0
    x_axis = []
    y_axis = []
    segment_len = []
    u_len = []
    error_len = []
    check = 0
    i = 0
    while z <= 1:
        u = z
        #x_p = -140*(u**3)+90*(u**2)+90*u
        #y_p = -90*(u**2)+90*u
        #x_p = -90*(u**3)+5*(u**2)+70*u
        #y_p = -25*(u**2)+70*u
        x_p = -90*(u**3)+5*(u**2)+85*u
        y_p = 10*math.sin(u)
        
        x_axis.append(x_p)
        y_axis.append(y_p)

        y_diff = 10*math.cos(u)
        u = sympy.Symbol('u')
        #x_p = -140*(u**3)+90*(u**2)+90*u
        #y_p = -90*(u**2)+90*u
        #x_p = -90*(u**3)+5*(u**2)+70*u
        #y_p = -25*(u**2)+70*u
        x_p = -90*(u**3)+5*(u**2)+85*u
        #y_p = 10*math.sin(u)
        
        x_dev = x_p.diff(u)
        #y_dev = y_p.diff(u)
        u = z
        x_diff = eval(str(x_dev))
        #y_diff = eval(str(y_dev))
        form = x_diff**2 + y_diff**2
        z = z + feedrate[i]*t_sample/(math.sqrt(form))
        u_len.append(z)
        if check > 1:
            segment_len.append(Length_linear([x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]]))
            error_c = contour_error (u_len[-2], u_len[-1], [x_axis[-2], y_axis[-2]], [x_axis[-1], y_axis[-1]])
            error_len.append(error_c)
        check += 1
        i += 1
    return x_axis, y_axis, check, error_len, segment_len, u_len

def contour_error (u_1, u_2, point_1, point_2):
    u = u_1 + (u_2-u_1)/2
    #x_p = -90*(u**3)+5*(u**2)+70*u
    #y_p = -25*(u**2)+70*u
    #x_p = -140*(u**3)+90*(u**2)+90*u
    #y_p = -90*(u**2)+90*u
    x_p = -90*(u**3)+5*(u**2)+85*u
    y_p = 10*math.sin(u)
    curve_middle = [x_p, y_p]
    base = Length_linear(point_1, point_2)
    side_left = Length_linear(point_1, curve_middle)
    side_right = Length_linear(curve_middle, point_2)
    p = 0.5*(base+side_left+side_right)
    error = 2*math.sqrt(p*(p-side_left)*(p-side_right)*(p-base))/base
    return error

    
