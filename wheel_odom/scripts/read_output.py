#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
import sys
import math

class discover:
	
	def __init__(self):
		self.gps_cov= 0.5
		self.gps_cov_large=20
		self.filtered_data = rospy.Subscriber("/odometry/gps", Odometry, self.callback, queue_size=1)
		self.pub_gps_cov = rospy.Publisher("/cov", Float32, queue_size=1)
		self.i=0;
		self.last_gps= [0,0];
		self.current_gps= [];
		self.differential_gps=[];
		self.linear_distance=0;
	
	def callback(self,msg):

		gps_x = msg.pose.pose.position.x
		gps_y = msg.pose.pose.position.y
		if self.i == 0:
			last_gps=[gps_x,gps_y];	
		self.current_gps= [gps_x,gps_y];
		self.differential_gps= [self.current_gps[0]-self.last_gps[0],self.current_gps[1]-self.last_gps[1]];
		linear_distance=math.hypot(self.differential_gps[0],self.differential_gps[1]);
		print linear_distance
		#print gps_x
		#print gps_y
		threshold_get = rospy.get_param("/gps_cov_threshold")
		threshold = threshold_get[0]; 
		if linear_distance <= threshold:
			self.pub_gps_cov.publish(self.gps_cov)
			print "small"
		else:
			self.pub_gps_cov.publish(self.gps_cov_large)
			print "large"
		self.i=self.i+1
		self.last_gps=self.current_gps

	def listener(self):
			rospy.spin()
	

if __name__ == '__main__':
	
	rospy.init_node('read_output', anonymous=True)
	readone = discover()
	
	readone.listener()
