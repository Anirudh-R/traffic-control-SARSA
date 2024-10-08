# Implements Differential semi-gradient n-step Sarsa for estimating q = q*
# Implemented according to pseudo-code given in Sec 10.5 of Sutton & Bartos's RL book
# Takes as input No. of runs, n, alpha, beta, epsilon. Outputs the final weights after all the runs.

# Depends on: sim_environment.py



import numpy as np
import random
import sim_environment
import math

S_LEN = 15
A_LEN = 15


# Desc: Runs the Differential n-step Sarsa algorithm for estimating optimal action-value function using Linear
#       function approximation.
# Inputs - n: n-step bootstrapping
#          c: Step-size ratio; beta = c*alpha
#          epsilon: Initial exploration parameter for epsilon-greedy
#          Nruns: No. of runs
# Outputs - W: Trained weights after all runs
def sarsa_nstep_diff_train(n, c, epsilon, Nruns):
    print("Running nstep SARSA training")

    buff_len = n + 1
    weight = np.zeros([S_LEN * A_LEN + 1, 1])
    avg_reward = 0
    dl_counter = 0

    for run in range(Nruns):
        print("Run " + str(run + 1))

        r_arr = np.zeros(n, dtype=int)
        a_arr = np.zeros(buff_len, dtype=int)
        s_arr = []
        alpha = 0.1 / (run + 1)
        beta = c * alpha
        e = math.exp(-run)
        #Start new run
        sim_environment.start_new_run(run)
        curr_s = initial_state_generate()
        curr_a = random.randint(1, 4)

        a_arr[0] = curr_a
        s_arr.insert(0, curr_s)
        t = 0
        while True:
            next_intersection = (t + 1) % 4
            #signals corresponding to that intersection
            if next_intersection == 3:
                a_space = [13, 14, 15]
            else:
                a_space = [4 * next_intersection + 1, 4 * next_intersection + 2, 4 * next_intersection + 3,
                           4 * next_intersection + 4]
            #take action on intersection
            env_param = sim_environment.take_action(curr_a)
            #if all the traffic has left the simulation, sim_environment.py returns 1000 reward
            r = env_param['rwd']
            if r == 1000:
                print("End of simulation at t = " + str(t))
                break

            next_s = env_param['next_state']
            r_arr[t % n] = r
            #chose next action epsilon greedily
            next_a = epsilon_greedy_a(e, a_space, next_s, weight[:, 0])
            #store the next state and next action
            s_arr.insert((t + 1) % (n + 1), next_s)
            a_arr[(t + 1) % (n + 1)] = next_a

            tau = t - n + 1
            #n-step SARSA Algo from Richard S. Sutton's Reinforcement Learning book
            if tau >= 0:
                q_tau_n = q_est(s_arr[(tau + n) % (n + 1)], a_arr[(tau + n) % (n + 1)], weight[:, 0])
                q_tau = q_est(s_arr[tau % (n + 1)], a_arr[tau % (n + 1)], weight[:, 0])
                do_error = sum(r_arr) - n * avg_reward + q_tau_n - q_tau
                avg_reward = avg_reward + beta * do_error
                phi_s_a_tau = phi(s_arr[tau % (n + 1)], a_arr[tau % (n + 1)])
                weight[:, 0] = weight[:, 0] + alpha * do_error * np.transpose(phi_s_a_tau)
            curr_a = next_a
            t += 1

    W = weight[:, 0]
    return W


# Desc: Uses the previously trained weights by n-step Sarsa to pick optimal actions.
# Inputs - W: Trained weights using n-step Sarsa
#          Nruns: No. of runs
# Outputs - None
def sarsa_nstep_diff_live(W, Nruns):
    print("Running nstep SARSA live")

    for run in range(Nruns):
        print("Run " + str(run + 1))

        sim_environment.start_new_run(run)
        curr_s = initial_state_generate()

        t = 0
        while True:
            intersection = t % 4
            if intersection == 3:
                a_space = [13, 14, 15]
            else:
                a_space = [4 * intersection + 1, 4 * intersection + 2, 4 * intersection + 3,
                           4 * intersection + 4]

            a = epsilon_greedy_a(0, a_space, curr_s, W)

            env_param = sim_environment.take_action(a)
            next_s = env_param['next_state']
            r = env_param['rwd']
            if r == 1000:
                print("End of simulation at t = " + str(t))
                break

            curr_s = next_s
            t += 1
    return


# Desc: Computes the approximate action-value function q(s, a) using Linear function approximation.
# Inputs - s: 15-element array containing the no. of vehicles waiting at the intersections in state s
#          a: Action taken in state s, 1<=a<=15
#          w: 556-element weight vector, with the last element corresponding to bias
# Outputs - q_val: Calculated q(s, a) value
def q_est(s, a, w):
    q_val = np.dot(w, phi(s, a))
    return q_val


# Calculate state-action feature vector
def phi(s, a):
    arr = np.zeros([S_LEN * A_LEN + 1, 1])
    N1 = s[0]; N2 = s[1]; N3 = s[2]; N4 = s[3];
    N5 = s[4]; N6 = s[5]; N7 = s[6]; N8 = s[7];
    N9 = s[8]; N10 = s[9]; N11 = s[10]; N12 = s[11];
    N13 = s[12]; N14 = s[13]; N15 = s[14];

    for i in range(15):
        arr[i + S_LEN * (a - 1)] = s[i] / 100.0

    return arr


# Chooses an action from a_space epsilon-greedily
def epsilon_greedy_a(e, a_space, next_s, w):
    random_e = random.uniform(0, 1)
    if random_e < e:
        return np.random.choice(a_space)
    else:
        q_next = []
        for a_temp in a_space:
            q_next.append(q_est(next_s, a_temp, w))
        q_max = max(q_next)
        q_max_index = [i for i, j in enumerate(q_next) if j == q_max]
        rand_greedy_q = np.random.choice(q_max_index)
        return a_space[rand_greedy_q]


# Generate a random initial state for the simulation
def initial_state_generate():
    for j in range(np.random.choice([4, 8, 12, 16, 20])):
        env_dict = sim_environment.take_action(0)
    return env_dict['next_state']
