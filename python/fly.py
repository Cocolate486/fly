#!/usr/bin/env python3
import rospy
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from geometry_msgs.msg import PoseStamped
import time

current_state = State()

def state_cb(msg):
    global current_state
    current_state = msg

def publish_pose(pub, x, y, z, duration):
    pose = PoseStamped()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    rate = rospy.Rate(20)
    for _ in range(int(duration * 20)):
        pub.publish(pose)
        rate.sleep()

def main():
    rospy.init_node("uav_mission_node")
    state_sub = rospy.Subscriber("/mavros/state", State, state_cb)
    local_pos_pub = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)

    rospy.wait_for_service("/mavros/cmd/arming")
    rospy.wait_for_service("/mavros/set_mode")
    arming_client = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
    set_mode_client = rospy.ServiceProxy("/mavros/set_mode", SetMode)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown() and not current_state.connected:
        rate.sleep()

    # 初始位置 setpoint（必須先送一段時間才能進入 OFFBOARD）
    for _ in range(100):
        local_pos_pub.publish(PoseStamped())
        rate.sleep()

    # 切換模式 & 解鎖
    set_mode_client(base_mode=0, custom_mode="OFFBOARD")
    arming_client(True)

    rospy.loginfo("起飛中...")
    publish_pose(local_pos_pub, 0, 0, 3, 5)  # 起飛到 3 公尺

    rospy.loginfo("向前飛 10 公尺...")
    publish_pose(local_pos_pub, 10, 0, 3, 5)  # 向前飛 10 公尺

    rospy.loginfo("降落中...")
    publish_pose(local_pos_pub, 10, 0, 0, 5)  # 降落到地面

    rospy.loginfo("任務完成")

if __name__ == "__main__":
    main()
