"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c
"""
import os,  inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import time
import subprocess
import pybullet as p
import pybullet_data
from pkg_resources import parse_version

logger = logging.getLogger(__name__)

class EnvOpenDogForwardSimple(gym.Env):
  metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second' : 50
  }

  def __init__(self, renders=True):
    # start the bullet physics server
    self._renders = renders
    if (renders):
	    p.connect(p.GUI)
    else:
    	p.connect(p.DIRECT)

    observation_high = np.array([
          np.finfo(np.float32).max,
          np.finfo(np.float32).max,
          np.finfo(np.float32).max,
          np.finfo(np.float32).max])
    #action_high = np.array([0.1])

    #self.action_space = spaces.Discrete(9)
    #self.observation_space = spaces.Box(-observation_high, observation_high)

    self.theta_threshold_radians = 1
    self.x_threshold = 2.4
    self._seed()
#    self.reset()
    self.viewer = None
    self._configure()

  def _configure(self, display=None):
    self.display = display

  def _seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]


  def computeState(self):
      bodyState = p.getLinkState(self.dog, 0)
      bodypos = bodyState[0]
      bodyquat = bodyState[1]
      pos, rot = p.getBasePositionAndOrientation(self.dog)
      rotmat = p.getMatrixFromQuaternion(rot)
      self.state = {"JointPosition": [ p.getJointState(self.dog, i)[0] for i in range(self.numJoints)],
                    "JointVelocity":  [p.getJointState(self.dog, i)[1] for i in range(self.numJoints)],
                    "bodyRot" : rotmat,
                    "bodyPos": bodypos,
                    "bodyquat": bodyquat}

  def _step(self, action):
    p.stepSimulation()
    self.currentSimTime += self.timeStep

    self.computeState()

    jp = self.state["JointPosition"]
    #jv = self.state["JointVelocity"]


    bodyx = self.state["bodyPos"][0]
    #print( bodypos[0] )
    #There are multiple possible choice of motor control, for the moment we settle on relative continuous position control
    #We chose this because it explores less so it should be faster to learn provided that we stay close to a path to the solution
    #jp[i]+
    for i in range(self.numJoints):
        p.setJointMotorControl2(self.dog, i, p.POSITION_CONTROL, targetPosition=action[i], force=500)
        #p.setJointMotorControl2(self.dog, i, p.VELOCITY_CONTROL, targetVelocity=jv[i]+deltav, force=500)

    hasFallen = self.state["bodyPos"][2] < 3.0
    #print( self.state["bodyPos"][2])
    pos, rot = p.getBasePositionAndOrientation(self.dog)

    rotmat = p.getMatrixFromQuaternion(rot)
    upv = np.array([rotmat[2],rotmat[5],rotmat[8] ]) #or the transpose : p.getMatrixFromQuaternion(rot)[6:9]
    hasFallenOrient = False
    # we compute the dot product of 0 0 1 with upv
    # the angle between the global z axis and the z axis of the base is the arccos of this dotproduct
    # 0.95 ~ cos( 18.5° )
    if( upv[2] < 0.8 ):
        hasFallenOrient = True


    done =  self.currentSimTime > 100.0 or hasFallen or hasFallenOrient or np.isnan(bodyx)

    reward = np.nan_to_num(pos[0]-self.previousPos[0])

    if hasFallen or hasFallenOrient:
        reward = reward - 5.0

    self.previousPos = pos
    return self.state, reward, done, {}

  def _reset(self):
#    print("-----------reset simulation---------------")
    p.resetSimulation()
    self.dog = p.loadURDF("opendog.urdf",[1,0,4],flags=p.URDF_USE_SELF_COLLISION)
    self.plane = p.loadURDF("myplane.urdf",[0,0,0])

    self.timeStep = 0.1
    self.currentSimTime = 0.0
    #p.setJointMotorControl2(self.cartpole, 1, p.VELOCITY_CONTROL, force=0)
    p.setGravity(0,0, -10)
    p.setTimeStep(self.timeStep)
    p.setRealTimeSimulation(0)
    pos, rot = p.getBasePositionAndOrientation(self.dog)
    self.previousPos = pos
    #initialCartPos = self.np_random.uniform(low=-0.5, high=0.5, size=(1,))
    #initialAngle = self.np_random.uniform(low=-0.5, high=0.5, size=(1,))
    #p.resetJointState(self.cartpole, 1, initialAngle)
    #p.resetJointState(self.cartpole, 0, initialCartPos)

    #self.state = p.getJointState(self.cartpole, 1)[0:2] + p.getJointState(self.cartpole, 0)[0:2]
    self.state = {}
    self.numJoints = p.getNumJoints(self.dog)
    self.computeState()

    return self.state

  def _render(self, mode='human', close=False):
      return

  if parse_version(gym.__version__)>=parse_version('0.9.6'):
    render = _render
    reset = _reset
    seed = _seed
    step = _step