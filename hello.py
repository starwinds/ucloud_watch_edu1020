from flask import Flask
from ucloud_apis.Client import *
import pygal
from pygal.style import DarkSolarizedStyle

app = Flask(__name__)
api_key_input = "" 
secret_input = ""

@app.route('/rawdata')
def rawdata():
        input_args = dict()
        input_args["namespace"] = "ucloud/server"
        input_args["metricname"] = "CPUUtilization"
        input_args["starttime"] = "2016-10-13T10:00:00.000"
        input_args["endtime"] = "2016-10-13T11:00:00.000"
        input_args["period"] = "5"
        input_args["statistics.member.1"] = "Average"
        input_args["unit"] = "Percent"
        ucloud_client = Client(api_type='watch',api_key=api_key_input,secret=secret_input)
        response = ucloud_client.request(command='getMetricStatistics',args=input_args)
        dump_result = json.dumps(response)
        return '%s' %dump_result


@app.route('/graph')
def graph():

        input_args = dict()
        input_args["namespace"] = "ucloud/server"
        input_args["metricname"] = "CPUUtilization"
        input_args["starttime"] = "2016-10-13T10:00:00.000"
        input_args["endtime"] = "2016-10-13T11:00:00.000"
        input_args["period"] = "5"
        input_args["statistics.member.1"] = "Average"
        input_args["unit"] = "Percent"


        ucloud_client = Client(api_type='watch',api_key=api_key_input,secret=secret_input)
        response = ucloud_client.request(command='getMetricStatistics',args=input_args)
        print "response = %s" % (response)	

        #result data manipulation for drawing graph
        time_list = []
        data_list = []
        for i in range(0,len(response["metricstatistics"])):
        	time_list.append(response["metricstatistics"][i]["timestamp"])
        	data_list.append(response["metricstatistics"][i]["average"])
        
        #draw simple graph with pygal module
        title = "CPU Utilization Graph(From: %s, To: %s)" %(input_args["starttime"], input_args["endtime"])
        bar_chart = pygal.Bar(width=1200,height=600,explicit_size=True, title=title, style=DarkSolarizedStyle)
        bar_chart.x_labels = time_list
        bar_chart.add('CPU Average(Percent)',data_list)
        html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render())
        return html

@app.route('/')
def hello():
	return "hello world!"

if __name__ == "__main__":
	app.run(host='0.0.0.0')
