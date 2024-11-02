# Import necessary libraries
import random
from collections import deque

# Define the Agent class with enhanced decision-making
class Agent:
    def __init__(self, agent_id, wealth, inventory):
        self.agent_id = agent_id
        self.wealth = wealth
        self.inventory = inventory

    def calculate_reward(self, action, market_price, expected_price_change):
        """
        Calculate the immediate reward for a given action.
        """
        if action == 'buy':
            if self.wealth >= market_price:
                # Potential gain is the expected increase in price
                potential_gain = expected_price_change
                return potential_gain
            else:
                return float('-inf')  # Cannot afford to buy
        elif action == 'sell':
            if self.inventory > 0:
                # Potential gain is the expected decrease in price
                potential_gain = -expected_price_change
                return potential_gain
            else:
                return float('-inf')  # Nothing to sell
        elif action == 'hold':
            # No immediate reward or cost
            return 0
        else:
            return 0

    def expected_price_change(self, price_history, demand_history, supply_history):
        """
        Agents predict future price changes based on historical data.
        For simplicity, we'll use a linear regression on recent prices.
        """
        # Ensure there is enough history
        if len(price_history) < 2:
            return 0  # No expectation if insufficient data

        # Calculate average price change
        recent_price_changes = [price_history[i+1] - price_history[i] for i in range(len(price_history)-1)]
        avg_price_change = sum(recent_price_changes) / len(recent_price_changes)

        # Consider recent demand and supply changes
        recent_demand_changes = [demand_history[i+1] - demand_history[i] for i in range(len(demand_history)-1)]
        avg_demand_change = sum(recent_demand_changes) / len(recent_demand_changes)

        recent_supply_changes = [supply_history[i+1] - supply_history[i] for i in range(len(supply_history)-1)]
        avg_supply_change = sum(recent_supply_changes) / len(recent_supply_changes)

        # Simple model: price expected to increase if demand is rising or supply is falling
        expected_price_change = avg_price_change + 0.5 * (avg_demand_change - avg_supply_change)

        return expected_price_change

    def decide_action(self, market_price, price_history, demand_history, supply_history):
        """
        Agents evaluate possible actions and choose the one with the highest expected immediate reward.
        """
        actions = ['buy', 'sell', 'hold']
        action_rewards = {}

        # Calculate expected price change
        expected_change = self.expected_price_change(price_history, demand_history, supply_history)

        for action in actions:
            reward = self.calculate_reward(action, market_price, expected_change)
            action_rewards[action] = reward

        # Filter out actions with negative expected rewards
        feasible_actions = {action: reward for action, reward in action_rewards.items() if reward >= 0}

        if feasible_actions:
            # Choose the action with the highest reward
            best_action = max(feasible_actions, key=feasible_actions.get)
        else:
            # If all rewards are negative, choose 'hold'
            best_action = 'hold'

        return best_action

    def buy(self, market_price):
        self.wealth -= market_price
        self.inventory += 1

    def sell(self, market_price):
        self.wealth += market_price
        self.inventory -= 1

    def __str__(self):
        return f"Agent {self.agent_id}: Wealth = {self.wealth}, Inventory = {self.inventory}"

# Define the Market Environment class
class MarketEnvironment:
    def __init__(self, initial_price):
        self.price = initial_price
        self.agents = []
        self.total_demand = 0
        self.total_supply = 0

        # Market history
        self.price_history = deque(maxlen=5)
        self.demand_history = deque(maxlen=5)
        self.supply_history = deque(maxlen=5)

        # Initialize history with initial values
        self.price_history.append(self.price)
        self.demand_history.append(0)
        self.supply_history.append(0)

    def add_agent(self, agent):
        self.agents.append(agent)

    def update_market(self):
        """
        Update the market based on agents' actions.
        """
        self.total_demand = 0
        self.total_supply = 0

        # Lists to hold buyers and sellers
        buyers = []
        sellers = []

        # Agents decide their actions
        for agent in self.agents:
            action = agent.decide_action(
                self.price,
                list(self.price_history),
                list(self.demand_history),
                list(self.supply_history)
            )
            if action == 'buy':
                if agent.wealth >= self.price:
                    buyers.append(agent)
                    self.total_demand += 1
            elif action == 'sell':
                if agent.inventory > 0:
                    sellers.append(agent)
                    self.total_supply += 1
            # 'hold' action does nothing

        # Process transactions
        num_transactions = min(len(buyers), len(sellers))
        random.shuffle(buyers)
        random.shuffle(sellers)
        for i in range(num_transactions):
            buyer = buyers[i]
            seller = sellers[i]
            # Execute transaction
            buyer.buy(self.price)
            seller.sell(self.price)

        # Simple price adjustment based on supply and demand
        if self.total_demand > self.total_supply:
            self.price += 1  # Increase price if demand exceeds supply
        elif self.total_demand < self.total_supply:
            self.price -= 1  # Decrease price if supply exceeds demand

        # Ensure price doesn't go negative
        if self.price < 1:
            self.price = 1

        # Update market history
        self.price_history.append(self.price)
        self.demand_history.append(self.total_demand)
        self.supply_history.append(self.total_supply)

    def __str__(self):
        return f"Market Price: {self.price}, Total Demand: {self.total_demand}, Total Supply: {self.total_supply}"

# Initialize the market environment
market = MarketEnvironment(initial_price=10)

# Create agents
num_agents = 10
for i in range(num_agents):
    # Assign random wealth and inventory to agents
    wealth = random.randint(5, 15)
    inventory = random.randint(0, 5)
    agent = Agent(agent_id=i, wealth=wealth, inventory=inventory)
    market.add_agent(agent)

# Run the simulation for a number of time steps
time_steps = 10
for t in range(time_steps):
    print(f"\nTime Step {t+1}")
    market.update_market()
    print(market)
    for agent in market.agents:
        print(agent)
