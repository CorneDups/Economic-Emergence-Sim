# Import necessary libraries
import random

# Define the Agent class
class Agent:
    def __init__(self, agent_id, wealth, inventory):
        self.agent_id = agent_id
        self.wealth = wealth      # Money the agent has
        self.inventory = inventory  # Quantity of the commodity the agent has

    def decide_action(self, market_price):
        """
        Agents make a simple decision:
        - If they have money, they attempt to buy.
        - If they have inventory, they attempt to sell.
        - Otherwise, they hold.
        """
        if self.wealth >= market_price:
            return 'buy'
        elif self.inventory > 0:
            return 'sell'
        else:
            return 'hold'

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
            action = agent.decide_action(self.price)
            if action == 'buy':
                buyers.append(agent)
                self.total_demand += 1
            elif action == 'sell':
                sellers.append(agent)
                self.total_supply += 1
            # No action for 'hold'

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
