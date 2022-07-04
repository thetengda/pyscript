from distutils.log import debug
from numpy import arange
import roslib
import rosbag
import rospy
import cv2

import sys

from cv_bridge import CvBridge,CvBridgeError

def debag_imu(file:str,topic:str,out:str):
    fout = open(out,'w')
    with rosbag.Bag(file,'r') as bag:
        for top,msg,t in bag.read_messages():
            if topic == top :
                acc_y = "%40.20f" % msg.linear_acceleration.y
                acc_x = "%40.20f" % msg.linear_acceleration.x
                acc_z = "%40.20f" % msg.linear_acceleration.z
                w_y = "%40.20f" % msg.angular_velocity.y
                w_x = "%40.20f" % msg.angular_velocity.x
                w_z = "%40.20f" % msg.angular_velocity.z
                timeimu = "%40.20f" %  msg.header.stamp.to_sec()
                fout.write(timeimu + " " + w_x + " " + w_y + " " + w_z + " " + acc_x + " " + acc_y + " " + acc_z+'\n')
    fout.close()
def debag_gnss(file:str,topic:str,out:str):
    fout = open(out,'w')
    with rosbag.Bag(file,'r') as bag:
        for top,msg,t in bag.read_messages():
            if topic == top :
                time = "%40.20f" %  msg.header.stamp.to_sec()
                lat = "%40.20f" % msg.status.latitude
                lon = "%40.20f" % msg.status.longitude
                hgt = "%40.20f" % msg.status.altitude
                timeimu = "%40.20f" %  msg.header.stamp.to_sec()
                fout.write(timeimu + " " + lat + " " + lon + " " + hgt +'\n')
    fout.close()
def main():
    if len(sys.argv) != 4: print('use: dabug <.bag> </topic> <.out>');exit(-1)
    _,file,topic,out = sys.argv
    debag_imu(file,topic,out)
main()