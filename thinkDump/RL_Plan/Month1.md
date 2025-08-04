# Month 1: Reinforcement Learning Foundations
**Goal:** Understand basic RL concepts & implement first algorithms (multi-armed bandits).  
**Time:** ~5–10 hrs/week

---

## Week 1: Setting the Stage
- [ ] **Set up your environment**
  - [ ] Install Python 3.10+ and create a virtual environment.
  - [ ] Install libraries:  
    ```bash
    pip install gymnasium[all] stable-baselines3 torch numpy matplotlib
    ```
- [ ] **Read/Watch:**  
  - [ ] [Sutton & Barto – Ch. 1: Introduction](http://incompleteideas.net/book/RLbook2020.pdf)
  - [ ] [David Silver’s RL Lecture 1](https://www.youtube.com/watch?v=2pWv7GOvuf0)
- [ ] **Play with an environment:**  
  - [ ] Run **CartPole** in `gymnasium` with random actions ([Docs](https://gymnasium.farama.org/environments/classic_control/cart_pole/)).
  - [ ] Print observations, rewards, and done flags.

---

## Week 2: Multi-Armed Bandits (Epsilon-Greedy)
- [ ] **Read:**  
  - [ ] Sutton & Barto Ch. 2 (Bandits)
- [ ] **Implement from scratch:**  
  - [ ] Multi-armed bandit with **ε-greedy strategy** in Python.
  - [ ] Plot average reward over time.
- [ ] **Experiment:**  
  - [ ] Try different ε values (0.01, 0.1, 0.5).
  - [ ] Observe how exploration affects performance.
- [ ] **Helpful:** [Lil’Log blog – Bandits explained](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/)

---

## Week 3: Upper Confidence Bound (UCB)
- [ ] **Read:**  
  - [ ] UCB section in Sutton & Barto Ch. 2.
- [ ] **Implement from scratch:**  
  - [ ] UCB for the multi-armed bandit.
  - [ ] Compare UCB vs ε-greedy (plot results).
- [ ] **Helpful:** [Multi-Armed Bandits in Python](https://towardsdatascience.com/bandit-algorithms-explained-b2d3e6173a1f)

---

## Week 4: Mini-Project – Bandit Recommender
- [ ] **Simulate a simple recommendation system**
  - [ ] Create 5–10 “arms” with different reward probabilities (e.g., news articles or products).
  - [ ] Use **ε-greedy** and **UCB** to maximize simulated clicks.
- [ ] **Visualize:**  
  - [ ] Cumulative reward over time for each algorithm.
- [ ] **Document:**  
  - [ ] Write a short **notebook/blog** explaining the experiment and insights.

---

## Optional / Extra
- [ ] Join RL communities:
  - [OpenAI Discord](https://discord.gg/openai)
  - [Hugging Face forums](https://discuss.huggingface.co/)
- [ ] Skim [OpenAI Spinning Up: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)

---

**By the end of Month 1, you’ll:**  
- Understand core RL terms (agent, environment, reward, policy).  
- Implement **two algorithms from scratch** (ε-greedy & UCB).  
- Build your first **bandit-based recommender system**.  
