import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from std_msgs.msg import Float32 
yaw=0
def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    print yaw
 
rospy.init_node('my_quaternion_to_euler')
 
sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
pub = rospy.Publisher ('/euler',Float32,queue_size=1)
r = rospy.Rate(10)
while not rospy.is_shutdown():
    pub.publish(yaw)
    r.sleep()
