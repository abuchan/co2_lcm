#!/usr/bin/env python

import rospy

# LCM library and message definitions
import lcm
from fearing import co2

from std_msgs.msg import Int16

lcm_addr = rospy.get_param('lcm_addr', 'udpm://239.255.76.67:7667?ttl=1')
lcm_robot_id = rospy.get_param('lcm_robot_id','/999')
lcm_topic = lcm_robot_id + '/co2'

co2_val = -1

def lcm_callback(chan, data):
  global co2_val
  co2_val = int(co2.decode(data).value)
  if not rospy.is_shutdown():
    rospy.loginfo('Read %d from LCM:%s at %s' % (co2_val, lcm_topic, rospy.get_time()))

def ros_publish():
  lc = None
  while lc is None:
      try:
          lc = lcm.LCM(lcm_addr)
      except RuntimeError as e:
          print("couldn't create LCM:" + str(e))
          time.sleep(1)
  print("LCM connected properly!")
  print("LCM running...")
  
  lc.subscribe(lcm_topic, lcm_callback)

  pub = rospy.Publisher('co2', Int16, queue_size=10)
  
  rospy.init_node('co2_lcm_pub')
  r = rospy.Rate(2)

  while not rospy.is_shutdown():
    lc.handle()
    rospy.loginfo('Pub %d on ROS:co2 at %s' % (co2_val, rospy.get_time()))
    pub.publish(co2_val)
    r.sleep()

if __name__ == '__main__':
  try:
    ros_publish()
  except rospy.ROSInterruptException: pass
