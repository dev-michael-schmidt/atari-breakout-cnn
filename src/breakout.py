###-----------------------------------------###
###          Breakout Main Loop             ###
###-----------------------------------------###

from DQNAgent import *
from ReplayMemory import *
from discrete_frames import *
from sliding_frames import *

import gymnasium as gym


def main():
    # start time of the program
    start_time = time.time()

    # pixel/frame data
    env = gym.make(hp['GAME'], render_mode='rgb_array')
    np.random.seed(0)

    # 4 actions
    # 0: no-op
    # 1: fire
    # 2: right
    # 3: left
    action_space = env.action_space.n - 1

    # create a new 3-dimensional space for a downscaled grayscale image
    agent_input_space = np.array([hp['HEIGHT'], hp['WIDTH'], hp['FRAME_BATCH_SIZE']])

    if hp['DISCRETE_FRAMING']:
        # create a new 3-dimensional space for a downscaled grayscale image, default: (64, 64, 4)
        # uses two discrete memory history frames
        memory_input_space = np.array([hp['HEIGHT'], hp['WIDTH'], hp['FRAME_BATCH_SIZE']])
    else:
        # create a new 3-dimensional space for a downscaled grayscale image, default: (64, 64, 5)
        # uses a sliding memory history frames
        memory_input_space = np.array([hp['HEIGHT'], hp['WIDTH'], hp['FRAME_BATCH_SIZE'] + 1])

    # print the initial state
    print('AGENT FRAME input:', agent_input_space.shape, 'DISCRETE FRAME SAVING:', hp['DISCRETE_FRAMING'],
          'MEMORY input:', memory_input_space.shape, 'ACTION output:', action_space)

    # performance
    stats = []

    # create a DQN Agent
    agent = DQNAgent(agent_input_space, action_space)

    # and a target DQN Agent
    target_agent = DQNAgent(agent_input_space, action_space)

    # to load weights
    if hp['LOAD_WEIGHTS']:
        agent.load_weights(hp['LOAD_WEIGHTS'])

    # create a memory for remembering and replay
    memory = ReplayMemory(hp['MEMORY_SIZE'], memory_input_space, action_space)

    """
    Run the main loop of the game
    """
    if hp['DISCRETE_FRAMING']:
        run_discrete(agent, target_agent, memory, env, stats, start_time)

    else:
        run_frame_sliding(agent, target_agent, memory, env, stats, start_time)

    # end time of the program
    end_time = time.time()

    # total time in seconds
    time_elapsed = end_time - start_time

    # print the final time elapsed
    print('finished training in', time_elapsed, 'seconds')

    # save and quit
    agent.quit(stats)


# execute main
if __name__ == "__main__":
    main()
