import threading
import time


class BiddingManager:
    '''Bidding Manager class representing a BM as described by MANPro'''

    def __init__(self, resource_storage):
        self.manufacturing_resources = []
        self.manufacturing_resource_availabilities = []
        self.manufacturing_resource_availabilities_lock = threading.Lock()
        self.resource_storage = resource_storage

    
    def add_manufacturing_resource(self, manufacturing_resource):
        manufacturing_resource.index = len(self.manufacturing_resources)
        self.manufacturing_resources.append(manufacturing_resource)
        self.manufacturing_resource_availabilities.append(True)


    def set_manufacturing_resource_availability(self, index, value):
        self.manufacturing_resource_availabilities[index] = value


    def schedule_task(self, task):
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
    def __init__(self, compatible_tasks):
        self.in_negotiation = False
        self.in_negotiation_lock = threading.Lock()
        self.task_schedule = []
        self.task_schedule_lock = threading.Lock()
        self.run_loop = True
        self.index = 0
        self.compatible_tasks = compatible_tasks


    def run_update_loop(self):
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
        threading.Thread(target=self.run_update_loop).start()


    def stop(self):
        self.run_loop = False
    
    def add_task_to_schedule(self, task):
        with self.task_schedule_lock:
            self.task_schedule.append(task)


class RecursiveResourceAgent(ResourceAgent):
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
    def __init__(self, bidding_manager, task, available_resource_agents):
        self.bidding_manager = bidding_manager
        self.task = task
        self.available_resource_agents = available_resource_agents
    

    def run_update_loop(self):
        n_agent = NegotiationAgent(self.task, self.available_resource_agents)
        best_r_agent = n_agent.get_best_r_agent()
        best_r_agent.add_task_to_schedule(self.task)
        for r_agent in self.available_resource_agents:
            with self.bidding_manager.manufacturing_resource_availabilities_lock:
                self.bidding_manager.set_manufacturing_resource_availability(r_agent.index, True)


    def run(self):
        threading.Thread(target=self.run_update_loop).start()


class NegotiationAgent:
    def __init__(self, task, available_r_agents):
        self.task = task
        self.available_r_agents = available_r_agents


    def generate_bid(self, resource_agent):
        return 1.0 / (1 + len(resource_agent.task_schedule))


    def get_best_r_agent(self):
        max_bid = 0
        best_resource_resource = None
        for resource_agent in self.available_r_agents:
            bid = self.generate_bid(resource_agent)
            if bid > max_bid:
                max_bid = bid
                best_resource_resource = resource_agent
        return best_resource_resource