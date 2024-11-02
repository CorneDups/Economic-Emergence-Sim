# Import necessary libraries
import random
import numpy as np
from collections import deque
import matplotlib.pyplot as plt  # Import matplotlib for plotting

random.seed(2) # Set random seed for reproducibility

class Agent:
    def __init__(self, agent_id, wealth, inventory, action_space, state_space):
        self.agent_id = agent_id
        self.wealth = wealth
        self.inventory = inventory
        self.action_space = action_space  # ['buy', 'sell', 'hold']
        self.state_space = state_space
        self.epsilon = 0.1  # Exploration rate
        self.alpha = 0.5    # Learning rate
        self.gamma = 0.9    # Discount factor
        self.q_table = {}   # Q-table initialized as empty dictionary

    def get_state(self, market_price, price_trend):
        # Discretize market price and price trend
        price_state = int(market_price / 5)  # Assuming price buckets of size 5
        trend_state = int(price_trend)       # Trend can be -1, 0, 1

        # Agent's own state
        wealth_state = int(self.wealth / 10)    # Wealth buckets of size 10
        inventory_state = self.inventory        # Assuming inventory is an integer

        # Combine into a tuple to represent the state
        state = (price_state, trend_state, wealth_state, inventory_state)
        return state

    def select_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Explore: select a random action
            action = random.choice(self.action_space)
        else:
            # Exploit: select the action with max Q-value for the current state
            q_values = [self.q_table.get((state, a), 0) for a in self.action_space]
            max_q = max(q_values)
            # In case of multiple actions with same max Q-value, randomly choose one
            max_actions = [a for a, q in zip(self.action_space, q_values) if q == max_q]
            action = random.choice(max_actions)
        return action

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        # Get max Q-value for next state
        next_q_values = [self.q_table.get((next_state, a), 0) for a in self.action_space]
        max_next_q = max(next_q_values)
        # Q-learning update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def perform_action(self, action, market_price):
        if action == 'buy' and self.wealth >= market_price:
            self.wealth -= market_price
            self.inventory += 1
        elif action == 'sell' and self.inventory > 0:
            self.wealth += market_price
            self.inventory -= 1
        # 'hold' action does nothing

    def __str__(self):
        return f"Agent {self.agent_id}: Wealth = {self.wealth}, Inventory = {self.inventory}"

class MarketEnvironment:
    def __init__(self, initial_price):
        self.price = initial_price
        self.agents = []
        self.total_demand = 0
        self.total_supply = 0

        # Market history
        self.price_history = deque(maxlen=5)
        self.price_history.append(self.price)

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_price_trend(self):
        if len(self.price_history) < 2:
            return 0  # No trend if insufficient data
        else:
            delta = self.price_history[-1] - self.price_history[-2]
            if delta > 0:
                return 1
            elif delta < 0:
                return -1
            else:
                return 0

    def update_market(self):
        self.total_demand = 0
        self.total_supply = 0

        # Keep track of state-action-reward-next_state for each agent
        agent_experiences = []

        # Agents observe the state and select actions
        price_trend = self.get_price_trend()
        current_price = self.price

        # Agents' actions and their initial states
        agent_actions = {}
        agent_states = {}
        for agent in self.agents:
            state = agent.get_state(current_price, price_trend)
            action = agent.select_action(state)
            agent_states[agent.agent_id] = state
            agent_actions[agent.agent_id] = action

        # Execute actions and collect experiences
        buyers = []
        sellers = []
        for agent in self.agents:
            action = agent_actions[agent.agent_id]
            if action == 'buy' and agent.wealth >= current_price:
                buyers.append(agent)
                self.total_demand += 1
            elif action == 'sell' and agent.inventory > 0:
                sellers.append(agent)
                self.total_supply += 1
            # 'hold' action does not affect demand/supply

        # Process transactions
        num_transactions = min(len(buyers), len(sellers))
        random.shuffle(buyers)
        random.shuffle(sellers)
        for i in range(num_transactions):
            buyer = buyers[i]
            seller = sellers[i]
            # Execute transaction
            buyer.perform_action('buy', current_price)
            seller.perform_action('sell', current_price)

        # Update market price based on supply and demand
        if self.total_demand > self.total_supply:
            self.price += 1  # Price increases if demand exceeds supply
        elif self.total_demand < self.total_supply:
            self.price -= 1  # Price decreases if supply exceeds demand

        # Ensure price doesn't go negative
        if self.price < 1:
            self.price = 1

        # Update price history
        self.price_history.append(self.price)

        # Agents observe new state and receive rewards
        new_price_trend = self.get_price_trend()
        new_price = self.price

        for agent in self.agents:
            state = agent_states[agent.agent_id]
            action = agent_actions[agent.agent_id]
            next_state = agent.get_state(new_price, new_price_trend)
            # Calculate reward
            reward = self.calculate_reward(agent, action, current_price, new_price)
            # Update Q-value
            agent.update_q_value(state, action, reward, next_state)

    def calculate_reward(self, agent, action, current_price, new_price):
        if action == 'buy':
            # Reward is the change in price (future price - purchase price)
            reward = new_price - current_price
        elif action == 'sell':
            # Reward is the sale price minus future price
            reward = current_price - new_price
        else:
            # 'hold' action reward could be zero or based on opportunity cost
            reward = 0
        return reward

    def __str__(self):
        return f"Market Price: {self.price}, Total Demand: {self.total_demand}, Total Supply: {self.total_supply}"

# Initialize the market environment
market = MarketEnvironment(initial_price=10)
initial_market_price = market.price

# Define action space and state space (for simplicity, state space is not explicitly defined)
action_space = ['buy', 'sell', 'hold']

# Initialize data structures to store agents' initial wealth and inventory
initial_wealth = {}
initial_inventory = {}

# Create agents
num_agents = 9  # Adjusted to 9 agents as per your request
agents = []
for i in range(num_agents):
    # Assign random wealth and inventory to agents
    wealth = random.randint(50, 100)  # Increased wealth for longer simulations
    inventory = random.randint(5, 15)
    agent = Agent(agent_id=i, wealth=wealth, inventory=inventory, action_space=action_space, state_space=None)
    market.add_agent(agent)
    agents.append(agent)

    # Store initial values
    initial_wealth[agent.agent_id] = agent.wealth
    initial_inventory[agent.agent_id] = agent.inventory

# Initialize data structures to store agents' wealth and inventory over time
agent_wealth_history = {agent.agent_id: [] for agent in agents}
agent_inventory_history = {agent.agent_id: [] for agent in agents}
time_steps = 10000

# Initialize lists to store market data over time
market_prices = []
total_demands = []
total_supplies = []

# Run the simulation
for t in range(time_steps):
    market.update_market()
    
    # Record market data
    market_prices.append(market.price)
    total_demands.append(market.total_demand)
    total_supplies.append(market.total_supply)
    
    # Record agents' wealth and inventory
    for agent in agents:
        agent_wealth_history[agent.agent_id].append(agent.wealth)
        agent_inventory_history[agent.agent_id].append(agent.inventory)


# After the simulation, output the starting and ending values
print("\nStarting and Ending Values:")
print("Agent ID | Initial Wealth | Final Wealth | Initial Inventory | Final Inventory")
for agent in agents:
    print(f"{agent.agent_id:^8} | {initial_wealth[agent.agent_id]:^14} | {agent.wealth:^12} | {initial_inventory[agent.agent_id]:^17} | {agent.inventory:^15}")

print(f"\nMarket Price Start: {initial_market_price}")
print(f"Market Price End: {market.price}")


# Visualization of Wealth Over Time
plt.figure(figsize=(12, 6))
for agent_id, wealth_history in agent_wealth_history.items():
    plt.plot(range(time_steps), wealth_history, label=f'Agent {agent_id}')
plt.title('Agents\' Wealth Over Time')
plt.xlabel('Time Steps')
plt.ylabel('Wealth')
plt.legend()
plt.grid(True)
plt.show()

# Visualization of Inventory Over Time
plt.figure(figsize=(12, 6))
for agent_id, inventory_history in agent_inventory_history.items():
    plt.plot(range(time_steps), inventory_history, label=f'Agent {agent_id}')
plt.title('Agents\' Inventory Over Time')
plt.xlabel('Time Steps')
plt.ylabel('Inventory')
plt.legend()
plt.grid(True)
plt.show()

# Visualization of Market Price, Supply, and Demand Over Time
plt.figure(figsize=(12, 6))
plt.plot(range(time_steps), market_prices, label='Market Price', color='blue')
plt.plot(range(time_steps), total_demands, label='Total Demand', color='green')
plt.plot(range(time_steps), total_supplies, label='Total Supply', color='red')
plt.title('Market Price, Demand, and Supply Over Time')
plt.xlabel('Time Steps')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.show()

