import rospy
from robonomics_lighthouse.msg import Ask, Bid
# from std_msgs.msg import String

def callback(data): 
    if data.model != "QmdFh1HPVe7H4LrDio899mxA7NindgxqiNUM9BNnBD7ryA":
        return

    signing_bid = rospy.Publisher('/liability/infochan/signing/bid', Bid, queue_size=128)
    # signing_task = rospy.Publisher('/task', String, queue_size=128)

    rospy.loginfo("Got an Ask:")
    msg = Bid()
    msg.model = data.model
    msg.objective   = data.objective
    rospy.loginfo(data)
    msg.token = data.token
    msg.cost = data.cost
    msg.lighthouseFee = 0
    msg.deadline = data.deadline

    rospy.loginfo("Publishing...")
    signing_bid.publish(msg)
    rospy.loginfo("Published Bid")
    # signing_task.publish(':)')

if __name__ == '__main__':
    rospy.init_node("zenit_pub_node")

    rospy.Subscriber('/liability/infochan/incoming/ask', Ask, callback)

    rospy.spin()