import threading
import time


class ResourceStorage:
    '''Class representing global manufacturing resource storage'''

    def __init__(self):
        self.resources = {}
        self.resource_access_lock = threading.Lock()
        self.stop_access = False

    def pop_resource(self, resource_name, amount):
        '''Removes amount resources of resource_name from '''

        while not self.resource_available(resource_name, amount):
            if self.stop_access:
                return False
            time.sleep(0.01)
        with self.resource_access_lock:
            self.resources[resource_name] -= amount
            return True


    def push_resource(self, resource_name, amount):
        with self.resource_access_lock:
            self.resources[resource_name] += amount


    def resource_available(self, resource_name, amount):
        return self.resources[resource_name] - amount >= 0

    
    def stop_resource_access(self):
        self.stop_access = True