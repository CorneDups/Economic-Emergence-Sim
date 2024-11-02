# Economic-Emergence-Sim


# **Agent-Based Economic Simulation**

This repository contains a Python implementation of an agent-based economic simulation where agents interact in a market environment. Agents use reinforcement learning (specifically Q-learning) to make decisions on buying, selling, or holding a commodity based on market conditions and policies. The simulation incorporates dynamic tax policies that adjust based on economic indicators like wealth inequality.

---

## **Table of Contents**

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Simulation](#running-the-simulation)
  - [Simulation Parameters](#simulation-parameters)
- [Code Overview](#code-overview)
  - [Agent Class](#agent-class)
  - [MarketEnvironment Class](#marketenvironment-class)
- [Visualization](#visualization)
- [Extending the Simulation](#extending-the-simulation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## **Introduction**

This simulation models a simple economy where multiple agents interact by buying and selling a single commodity. Agents aim to maximize their wealth over time using reinforcement learning to adapt their strategies based on market conditions and policies. The market environment includes dynamic tax policies that adjust according to the wealth inequality among agents, measured by the Gini coefficient.

---

## **Features**

- **Agent-Based Modeling**: Simulates individual agents with their own wealth and inventory.
- **Reinforcement Learning**: Agents use Q-learning to make decisions and adapt over time.
- **Dynamic Policies**: Implements tax rates that adjust based on economic indicators like the Gini coefficient.
- **Policy Options**: Supports different tax redistribution policies:
  - Equal redistribution
  - Need-based redistribution (favoring less wealthy agents)
  - Wealth-based redistribution (favoring wealthier agents)
- **Visualization**: Generates plots to visualize agents' wealth, tax rates, Gini coefficients, inventory levels, and market dynamics over time.

---

## **Requirements**

- Python 3.x
- Libraries:
  - `matplotlib`
  - `collections` (standard library)
  - `random` (standard library)

---

## **Installation**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/agent-based-economic-simulation.git
   ```
2. **Navigate to the Directory**

   ```bash
   cd agent-based-economic-simulation
   ```
3. **Install Required Libraries**

   If you don't have `matplotlib` installed, you can install it using:

   ```bash
   pip install matplotlib
   ```

---

## **Usage**

### **Running the Simulation**

1. **Ensure Dependencies are Installed**

   Make sure you have all the required libraries installed.
2. **Run the Simulation Script**

   ```bash
   python simulation.py
   ```

   Replace `simulation.py` with the name of the Python file containing the simulation code.
3. **View Outputs**

   - The script will print the starting and ending values of each agent's wealth and inventory.
   - It will display plots showing:
     - Agents' wealth over time.
     - Tax rate over time.
     - Gini coefficient over time.
     - Agents' inventory over time.
     - Market price, demand, and supply over time.

### **Simulation Parameters**

You can customize the simulation by modifying parameters in the script.

- **Number of Agents**

  ```python
  num_agents = 9  # Adjust the number of agents
  ```
- **Time Steps**

  ```python
  time_steps = 10001  # Adjust the number of simulation steps
  ```
- **Initial Market Price**

  ```python
  initial_price = 10  # Set the initial market price
  ```
- **Tax Rate**

  The initial tax rate is set but will adjust dynamically during the simulation.

  ```python
  tax_rate = 0.05  # Initial tax rate
  ```
- **Redistribution Policy**

  Choose between `'equal'`, `'need-based'`, or `'wealth-based'`.

  ```python
  redistribution_policy = 'need-based'  # Set the redistribution policy
  ```
- **Adjusting Tax Rate Frequency**

  ```python
  # Adjust tax rate every 500 time steps
  if t % 500 == 0 and t != 0:
      market.adjust_tax_rate()
  ```
- **Tax Redistribution Frequency**

  ```python
  # Redistribute taxes every 1000 time steps
  if t % 1000 == 0 and t != 0:
      market.redistribute_taxes()
  ```

---

## **Code Overview**

### **Agent Class**

Represents individual agents participating in the market.

- **Attributes**:
  - `agent_id`: Unique identifier.
  - `wealth`: Current wealth of the agent.
  - `inventory`: Quantity of the commodity the agent holds.
  - `q_table`: Stores Q-values for state-action pairs.
- **Methods**:
  - `get_state()`: Constructs the agent's perception of the current state.
  - `select_action()`: Chooses an action based on an epsilon-greedy policy.
  - `update_q_value()`: Updates the Q-values using the Q-learning algorithm.
  - `perform_action()`: Executes the selected action and updates wealth and inventory.

### **MarketEnvironment Class**

Simulates the market where agents interact and policies are enforced.

- **Attributes**:
  - `price`: Current market price of the commodity.
  - `tax_rate`: Current tax rate, which may adjust dynamically.
  - `redistribution_policy`: Policy for redistributing collected taxes.
  - `agents`: List of agents in the market.
  - `government_funds`: Accumulated tax funds for redistribution.
- **Methods**:
  - `update_market()`: Processes agents' actions, updates the market, and collects taxes.
  - `calculate_reward()`: Calculates rewards for agents based on their actions.
  - `redistribute_taxes()`: Redistributes collected taxes according to the chosen policy.
  - `calculate_gini_coefficient()`: Computes the Gini coefficient to measure wealth inequality.
  - `adjust_tax_rate()`: Dynamically adjusts the tax rate based on the Gini coefficient.

---

## **Visualization**

The simulation generates several plots to help analyze the results:

- **Agents' Wealth Over Time**

  Visualizes how each agent's wealth changes throughout the simulation.
- **Tax Rate Over Time**

  Shows how the tax rate adjusts dynamically in response to wealth inequality.
- **Gini Coefficient Over Time**

  Illustrates changes in wealth inequality among agents.
- **Agents' Inventory Over Time**

  Tracks the inventory levels of agents over time.
- **Market Price, Demand, and Supply Over Time**

  Displays market dynamics, including price fluctuations and changes in demand and supply.

---

## **Extending the Simulation**

You can extend and customize the simulation in various ways:

- **Modify Agent Behavior**

  - Adjust learning parameters (`epsilon`, `alpha`, `gamma`).
  - Implement different learning algorithms.
  - Include policy awareness in agents by adding the current tax rate to their state.
- **Enhance Market Policies**

  - Introduce new dynamic policies based on other economic indicators.
  - Experiment with non-linear functions for tax rate adjustments.
- **Add Economic Shocks**

  - Simulate external events that impact the market or agents, such as sudden price changes.
- **Increase Complexity**

  - Introduce multiple commodities.
  - Implement more sophisticated market mechanisms.

---

## **Contributing**

Contributions are welcome! If you have ideas for improving the simulation or adding new features:

1. **Fork the Repository**
2. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
4. **Commit and Push**

   ```bash
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```
5. **Submit a Pull Request**

---

## **License**

This project is not licensed. You are free to use, modify, and distribute this software.

---

## **Contact**

For questions, suggestions, or collaborations:

- **Email**: jhcduplooy@gmail.com
- **GitHub Issues**: Feel free to open an issue on the repository.

---

**Enjoy exploring the dynamics of agent-based economic simulations!**
