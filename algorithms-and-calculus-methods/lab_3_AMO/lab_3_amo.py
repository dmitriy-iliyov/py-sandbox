import logic_func as lf
import draw_func as df

number_line = [0, 4]
interpolation = lf.Interpolation(number_line)
start_data = interpolation.default_func()
interpolated_data = interpolation.interpolated_func()
d = interpolation.interpolation_error()
df.main_draw(start_data, interpolated_data, d)
