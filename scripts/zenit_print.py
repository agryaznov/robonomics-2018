import http.client
import rospy
from std_msgs.msg import String
from robonomics_liability.msg import Liability
from std_srvs.srv import Empty

def path(model):
	return {
		"model1": "monopoly/shaman/blue_shaman.gco",
		"model2": "monopoly/alllover.gco",
		"model3": "monopoly/eth/ether.gco"
	}[model]

def callback(data):
	rospy.loginfo("GOTCHA!")

	# ip6 of the printer is fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3
	conn = http.client.HTTPConnection("192.168.0.87")
	# conn = http.client.HTTPConnection("127.0.0.1:8081")
	# conn = http.client.HTTPConnection("http://[fced:97fd:da23:b15d:7897:4fa6:57b3:f2a3]")

	payload = "{\"command\":\"select\",\"print\":true}"

	headers = {
	    'X-Api-Key': "6580BFF7899C4CB88FD6ABD545E3854C",
	    'Content-Type': "application/json",
	    'Cache-Control': "no-cache",
	    'Postman-Token': "ca05c9ef-b6b0-4cef-b67a-115fcd92e840"
	    }

	model_path = path(data.data)

	conn.request("POST", "api/files/local/{}".format(model_path), payload, headers)

	res = conn.getresponse()
	data = res.read()

	rospy.loginfo(data.decode("utf-8"))

	rospy.wait_for_service("/liability/finish")
	fin = rospy.ServiceProxy("/liability/finish", Empty)
	rospy.loginfo("Finishing liability...")
	fin()

if __name__ == '__main__':
    rospy.init_node("zenit_print_node")
    
    # callback(String('model1'))
    rospy.Subscriber('task', String, callback)
    # rospy.Subscriber('/liability/current', Liability, callback)

    rospy.spin()

