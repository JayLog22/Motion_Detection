from motion_detector import data_frame
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas


data_frame["Start_String"] = pandas.to_datetime(data_frame["Start"], format='%Y-%m-%d %H:%M:%S')
data_frame["End_String"] = pandas.to_datetime(data_frame["End"], format='%Y-%m-%d %H:%M:%S')

data_frame["Start_String"] = data_frame["Start_String"].dt.strftime('%Y-%m-%d %H:%M:%S')
data_frame["End_String"] = data_frame["End_String"].dt.strftime('%Y-%m-%d %H:%M:%S')

column_data_source = ColumnDataSource(data_frame)

plot = figure(x_axis_type = 'datetime', height = 300,
              width = 800, title = "Motion Graph")

plot.yaxis.minor_tick_line_color = None

hover = HoverTool(tooltips = [("Start", "@Start_String"), ("End", "@End_String")])
plot.add_tools(hover)

quad_graph = plot.quad(left = "Start", right = "End",
                       bottom = 0, top = 1, color = "red",
                       source = column_data_source)

output_file("Graph.html")
show(plot)

