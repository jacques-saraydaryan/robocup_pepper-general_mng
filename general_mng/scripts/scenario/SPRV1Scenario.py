__author__ = 'Jacques Saraydaryan'
from abc import ABCMeta, abstractmethod
import rospy
import uuid
import time
import random
import actionlib

from AbstractScenarioBus import AbstractScenarioBus
from AbstractScenarioAction import AbstractScenarioAction
from AbstractScenario import AbstractScenario


from map_manager.srv import getitP_service
from robocup_msgs.msg import gm_bus_msg

from navigation_manager.msg import NavMngGoal, NavMngAction
from tts_hri.msg import TtsHriGoal, TtsHriAction
from pepper_pose_for_nav.srv import MoveHeadAtPosition





class SPRV1Scenario(AbstractScenario,AbstractScenarioBus,AbstractScenarioAction):

    _severalActionPending={}
    _oneActionPending=None
    HEAD_PITCH_FOR_PEOPLE_DETECTION=-0.3
    HEAD_YAW_FOR_PEOPLE_DETECTION=0.0
    #DEFAULT_OBJ_LABEL=[]
    #DEFAULT_OBJECT_MEMORY_LOCATION="Robocup/objects"

    def __init__(self,config):
        AbstractScenarioBus.__init__(self,config)
        AbstractScenarioAction.__init__(self,config)
        self._getPoint_service = rospy.ServiceProxy('get_InterestPoint', getitP_service)

        #try:
        #    self.obj_labels=config['labels']
        #except Exception as e:
        #    rospy.logwarn("no config value for obj_label use default:"+str(self.DEFAULT_OBJ_LABEL))
        #    self.obj_labels=self.DEFAULT_OBJ_LABEL
#
        #try:
        #    self.object_memory_location=config['object_memory_location']
        #except Exception as e:
        #    rospy.logwarn("no config value for object_memory_location use default:"+str(self.DEFAULT_OBJECT_MEMORY_LOCATION))
        #    self.object_memory_location=self.DEFAULT_OBJECT_MEMORY_LOCATION

            


        try:
            rospy.wait_for_service('/move_head_pose_srv',5)
            rospy.loginfo("end service move_head_pose_srv wait time")
            self._moveHeadPose = rospy.ServiceProxy('move_head_pose_srv', MoveHeadAtPosition)
        except Exception as e:
            rospy.logerr("Service move_head_pose_srv call failed: %s" % e)
            return


    def startScenario(self):
        rospy.loginfo("")
        rospy.loginfo("######################################")
        rospy.loginfo("Starting the SPRV1 Scenario...")
        rospy.loginfo("######################################")
     
        #TOO make the logic of the scenario

        #turn of 180 degre before detecting people
        #TODO 

        # set the head position for detecting people
        self.moveheadPose(self.HEAD_PITCH_FOR_PEOPLE_DETECTION,self.HEAD_YAW_FOR_PEOPLE_DETECTION,True)
        rospy.sleep(2.0)
       
        orderState0,result0=self.detectMetaPeople(30)
        rospy.loginfo(result0)

        #process people attribute to save elts to ALMEMORY
        #TODO
        #TODO




    def gmBusListener(self,msg): 
        if self._status == self.WAIT_ACTION_STATUS:
           self.checkActionStatus(msg)


    def initScenario(self):
        
        self._enableNavAction=True
        self._enableTtsAction=False
        self._enableDialogueAction=False
        self._enableAddInMemoryAction=False
        self._enableObjectMngAction=False
        self._enableMultiplePeopleDetectionAction=True
        
        AbstractScenarioAction.configure_intern(self)

    def moveheadPose(self,pitch_value,yaw_value,track):
        try:
            self._moveHeadPose = rospy.ServiceProxy('move_head_pose_srv', MoveHeadAtPosition)
            result=self._moveHeadPose(pitch_value,yaw_value,track)
        except Exception as e:
            rospy.logerr("Service move_head_pose_srv call failed: %s" % e)
            return
        