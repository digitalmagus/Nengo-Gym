import nengo
import numpy as np
import gym

 
 
env = gym.make('CartPole-v0')
env.reset()

print("Environment Action Space: ",env.action_space)
print("Enviornment Observation Space: ",env.observation_space)
print("Enviornment Observation High: ",env.observation_space.high)
print("Enviornment Observation Low: ",env.observation_space.low)

def run_episode(env, parameters):  
    observation = env.reset()
    totalreward = 0
    for _ in range(200):
        actions = np.zeros(2)
        action0 = np.matmul(parameters[0],observation)
        action1 = np.matmul(parameters[1],observation)
        
        if action0 > action1:
            action = 0
        else:
            action = 1
        
                        
        observation, reward, done, info = env.step(action)
        #env.render()
        totalreward += reward
        if done:
            break
    return totalreward

##------------ Hill Climb Search Strategy -------------        
        
noise_scaling = 1 

bestreward = -9999
episodes_per_update = 10
steps = 0
run_total = 0

acts = 2
obs = 4

parameters = np.random.random((acts,obs)) * 2 - 1  

for i in range(10000):  
    
      
    newparams = np.zeros((acts,obs))
    noiseparams = (np.random.random(obs) * 2 - 1)*noise_scaling
    newparams[0] = parameters[0] + noiseparams[0] 
    newparams[1] = parameters[1] + noiseparams[1]
    
    reward = 0  
    
    for _ in range(episodes_per_update):  
        run = run_episode(env,newparams)
        reward += run
        
    steps += 1
    
    if reward > bestreward:
        print("Steps: ",steps,"Reward: ", reward)
        print("New params at step: ",steps)
        print("params0: ", parameters[0])
        print("params1: ", parameters[1])

        
        bestreward = reward
        parameters = newparams
        
        if reward/episodes_per_update >= 200:
            print()
            break  
        
    if(i%20 == 0): #after 20 steps lower noise (settle).
        noise_scaling -= 0.1
        
    if(i%200 == 0): #after 200 steps reset base params.
        parameters = np.random.random((acts,obs)) * 2 - 1
        noise_scaling = 1