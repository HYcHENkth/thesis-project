#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
import sys


gps_cov = 0.5
i=0

def callback1(msg):
	global i
	global gps_cov	
	gps_cov= msg.data
	i=1

def callback2(msg):
	global i
	global gps_cov
	while i==1:
		break
	temp = msg
	temp.header.frame_id = 'trimble'
	temp.position_covariance = [gps_cov, 0.0, 0.0, 0.0, gps_cov, 0.0, 0.0, 0.0, gps_cov]
	print gps_cov	
	if gps_cov == 20:
		print "///////////////////////////////////////////////////////////////////"
	temp.position_covariance_type = 3
	pub_gps.publish(temp)
	i=0

if __name__ == '__main__':
	
	rospy.init_node("trimble_gps_convert", anonymous=True)
	# new_topic_name = rospy.get_param("/new_gps_topic_name")
	# print "--- new name"
	# print new_topic_name 
	sub_gps = rospy.Subscriber("/cov", Float32, callback1, queue_size=1)
	sub_gps = rospy.Subscriber("/fix", NavSatFix, callback2, queue_size=1)
	pub_gps = rospy.Publisher("/trimble_gps_fix", NavSatFix, queue_size=1)
	rospy.spin()
