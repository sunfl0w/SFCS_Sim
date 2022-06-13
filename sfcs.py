'''The SFCS module defines all classes needed to represent the organizational structure of the proposed SFCS.
The classes are mostly based on the modules defined by MANPro.'''

import threading
import time


class BiddingManager:
    '''Bidding Manager class representing a BM as described by MANPro.'''

    def __init__(self, resource_storage):
        self.manufacturing_resources = []
        self.manufacturing_resource_availabilities = []
        self.manufacturing_resource_availabilities_lock = threading.Lock()
        self.resource_storage = resource_storage

    
    def add_manufacturing_resource(self, manufacturing_resource):
        '''Adds a R-Agent to the bidding manager to manage'''
        manufacturing_resource.index = len(self.manufacturing_resources)
        self.manufacturing_resources.append(manufacturing_resource)
        self.manufacturing_resource_availabilities.append(True)


    def set_manufacturing_resource_availability(self, index, value):
        '''Used internally to specify if a given manufacturing resource is currently available for negotiations.'''
        self.manufacturing_resource_availabilities[index] = value


    def schedule_task(self, task):
        '''Schedules a given task to be performed by the bidding manager.
        The task will be awarded to a resource agent according to the negotiation process described by MANPro.'''
        candidate_manufacturing_resources = []
        while len(candidate_manufacturing_resources) == 0:
            for manufacturing_resource in self.manufacturing_resources:
                with self.manufacturing_resource_availabilities_lock:
                    if self.manufacturing_resource_availabilities[manufacturing_resource.index] and task.name in manufacturing_resource.compatible_tasks:
                        self.set_manufacturing_resource_availability(manufacturing_resource.index, False)
                        candidate_manufacturing_resources.append(manufacturing_resource)

        t_agent = TaskAgent(self, task, candidate_manufacturing_resources)
        t_agent.run()


class ResourceAgent:
    '''Resource agent class representing a R-Agent as described by MANPro.
    Compatible tasks is a list of names of tasks this agent is able to perform.'''
    def __init__(self, compatible_tasks):
        self.in_negotiation = False
        self.in_negotiation_lock = threading.Lock()
        self.task_schedule = []
        self.task_schedule_lock = threading.Lock()
        self.run_loop = True
        self.index = 0
        self.compatible_tasks = compatible_tasks


    def run_update_loop(self):
        '''Update loop used internally to run an resource agent's logic in another thread.'''
        while self.run_loop:
            task = None
            # Look for next task in the task schedule. If a task is found perform that task until completion
            with self.task_schedule_lock:
                if len(self.task_schedule) > 0:
                    task = self.task_schedule[0]
                    self.task_schedule.pop(0)
            if task:
                task.execute()
            else:
                time.sleep(0.001)


    def run(self):
        '''Starts the resource agent. After executing this method the agent is able to perform tasks.'''
        threading.Thread(target=self.run_update_loop).start()


    def stop(self):
        '''Stops a resource agent.'''
        self.run_loop = False


    def add_task_to_schedule(self, task):
        '''Adds a task to the agent's task schedule. This is used when the agent was awarded a task after negotiation.'''
        with self.task_schedule_lock:
            self.task_schedule.append(task)


class RecursiveResourceAgent(ResourceAgent):
    '''Recursive resource agent class representing a R-Agent as described by MANPro.
    This type of resource agent is different as it requires a unique bidding manager to simulate a nested holonic organizational structure.
    Compatible tasks is a list of names of tasks this agent is able to perform.'''
    def __init__(self, bidding_manager, compatible_tasks):
        ResourceAgent.__init__(self, compatible_tasks)
        self.bidding_manager = bidding_manager


    def run_update_loop(self):
        while self.run_loop:
            task = None
            # Look for next task in the task schedule. If a task is found perform that task until completion
            with self.task_schedule_lock:
                if len(self.task_schedule) > 0:
                    task = self.task_schedule[0]
                    self.task_schedule.pop(0)
            if task:
                self.bidding_manager.schedule_task(task)
            else:
                time.sleep(0.001)


class TaskAgent:
    '''Task Agent class representing a T-Agent as described by MANPro'''
    def __init__(self, bidding_manager, task, available_resource_agents):
        self.bidding_manager = bidding_manager
        self.task = task
        self.available_resource_agents = available_resource_agents


    def run_update_loop(self):
        '''Update loop used internally to run an task agent's logic in another thread.'''
        # Find best available manufacturing resource and award task
        n_agent = NegotiationAgent(self.task, self.available_resource_agents)
        best_r_agent = n_agent.get_best_r_agent()
        best_r_agent.add_task_to_schedule(self.task)
        for r_agent in self.available_resource_agents:
            with self.bidding_manager.manufacturing_resource_availabilities_lock:
                self.bidding_manager.set_manufacturing_resource_availability(r_agent.index, True)


    def run(self):
        '''Starts the task agent.'''
        threading.Thread(target=self.run_update_loop).start()


class NegotiationAgent:
    '''Negotiation Agent class representing a N-Agent as described by MANPro'''
    def __init__(self, task, available_r_agents):
        self.task = task
        self.available_r_agents = available_r_agents


    def generate_bid(self, resource_agent):
        '''Generates a bid for a given resource agent according to the method given in the paper.'''
        return 1.0 / (1 + len(resource_agent.task_schedule))


    def get_best_r_agent(self):
        '''Returns the best resource agent according to the generated bids. This is used later in the awarding stage by the task agent.'''
        max_bid = 0
        best_resource_agent = None
        for resource_agent in self.available_r_agents:
            bid = self.generate_bid(resource_agent)
            if bid > max_bid:
                max_bid = bid
                best_resource_agent = resource_agent
        return best_resource_agent
