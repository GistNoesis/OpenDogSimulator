import gym
import numpy as np
from EnvOpenDogStand import EnvOpenDogStand
from EnvOpenDogForward import EnvOpenDogForward
import time
from es import CMAES
import tensorflow as tf
import gc
import pickle
from tensorforce.agents import PPOAgent


render = False
env = EnvOpenDogForward(renders=render)
ENV_NAME = "ForwardPPO"

env.seed(0)



'''
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
'''

class ForwardActor:
    def __init__(self):

        actions = {}
        for i in range(12):
            actions[str(i)] = {'type': 'float'}# 'num_actions': 10

        network_spec = [
            dict(type='dense', size=100, activation='relu'),
            dict(type='dense', size=100, activation='relu')
        ]

        self.agent = PPOAgent(
            states=dict(type='float', shape=(12,)),
            actions=actions,
            batching_capacity=2000,
            network=network_spec,
            step_optimizer=dict(
                type='adam',
                learning_rate=1e-4
            ),
        )


    def act(self, state):
        jp = np.expand_dims( np.nan_to_num( np.array(state["JointPosition"] ) ),axis=0)
        jv = np.expand_dims(np.array(state["JointVelocity"]), axis=0)

        #actiondict = self.agent.act( np.concatenate([jp,jv],axis=1))
        actiondict = self.agent.act(jp)

        action = np.zeros(12)
        for i in range(12):
            action[i] = actiondict[str(i)][0]
        action = np.nan_to_num(action)
        #print(action)
        return np.clip( 0.3*action,-1.0,1.0)

    def observe(self, reward, terminal):
        self.agent.observe(reward=reward,terminal=terminal)

    def save(self,directory):
        self.agent.save_model(directory=directory)

    def restore(self,directory):
        self.agent.restore_model(directory=directory)


agent = ForwardActor()



def runEpisode( ):
    ob = env.reset()
    while True:
        action = agent.act(ob)
        # Add experience, agent automatically updates model according to batch size

        ob, reward, done, _ = env.step(action)
        agent.observe(reward=reward, terminal=done)
        #time.sleep(0.01)
        if done:
            #print("episode done")
            #print(reward)
            gc.collect()
            # Only return last reward
            return reward

MY_REQUIRED_REWARD = 300.0

try:
    agent.restore("./ForwardPPO/")
except:
    print("No file found starting from scratch")

bestScore = - np.Infinity
ep = 0
while True:
  # ask the ES to give us a set of candidate solutions
  if( ep % 100 == 0) :
      agent.save("./ForwardPPO/")
  score = runEpisode()
  if( score > bestScore):
      bestScore = score
  # get best parameter, reward from ES

  print("Episode " + str(ep))
  print( "score : ")
  print( score )
  print("current Best : ")
  print( bestScore)
  ep = ep+1



# Close the env and write monitor result info to disk
env.close()