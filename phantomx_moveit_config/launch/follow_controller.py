#!/usr/bin/env python
import roslib; 
#roslib.load_manifest('trajectory_control_tutorial')
import rospy, actionlib, yaml, sys

from control_msgs.msg import *

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "usage: traj_yaml.py YAML_FILE TRAJECTORY_NAME"
    print "  where TRAJECTORY is a dictionary defined in YAML_FILE"
    sys.exit(1)
  traj_yaml = yaml.load(file(sys.argv[1], 'r'))
  traj_name = sys.argv[2]
  if not traj_name in traj_yaml:
    print "unable to find trajectory %s in %s" % (traj_name, sys.argv[1])
    sys.exit(1)
  traj_len = len(traj_yaml[traj_name])
  rospy.init_node('traj')
  traj_client = actionlib.SimpleActionClient( \
                                 '/drc_controller/follow_joint_trajectory', \
                                 FollowJointTrajectoryAction)
  traj_client.wait_for_server()
  # now, build the trajectory-action goal message from the YAML snippet
  goal = FollowJointTrajectoryGoal()
  goal.trajectory.joint_names = ['l_leg_uhz', 'l_leg_mhx', 'l_leg_lhy',
                                 'l_leg_kny', 'l_leg_uay', 'l_leg_lax',
                                 'r_leg_uhz', 'r_leg_mhx', 'r_leg_lhy',
                                 'r_leg_kny', 'r_leg_uay', 'r_leg_lax',
                                 'l_arm_usy', 'l_arm_shx', 'l_arm_ely',
                                 'l_arm_elx', 'l_arm_uwy', 'l_arm_mwx',
                                 'r_arm_usy', 'r_arm_shx', 'r_arm_ely',
                                 'r_arm_elx', 'r_arm_uwy', 'r_arm_mwx',
                                 'neck_ay', 
                                 'back_lbz', 'back_mby', 'back_ubx']
  goal.trajectory.points = [ trajectory_msgs.msg.JointTrajectoryPoint() \
                             for x in xrange(0, traj_len) ]
  t = 0.0
  for i in xrange(0, traj_len):
    y = traj_yaml[traj_name][i]
    goal_pt = goal.trajectory.points[i]
    t += float(y[0])
    goal_pt.time_from_start = rospy.Duration.from_sec(t)
    goal_pt.velocities = [0] * 28
    goal_pt.positions = [ float(x) for x in y[1].split() ]
  traj_client.send_goal(goal)
  traj_client.wait_for_result(rospy.Duration.from_sec(t + 3))
