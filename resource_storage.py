'''The resource storage module defines a globally accessible resource storage for a SFCS to use.'''

import threading
import time


class ResourceStorage:
    '''Class representing global manufacturing resource storage.'''

    def __init__(self):
        self.resources = {}
        self.resource_access_lock = threading.Lock()
        self.stop_access = False


    def pop_resource(self, resource_name, amount):
        '''Removes an amount resources of resource_name from the storage.
        Only if the requested amount is available this method returns true.
        If the requested amount is unavailable the method loops until availability is established again.'''

        while not self.resource_available(resource_name, amount):
            if self.stop_access:
                return False
            time.sleep(0.01)
        with self.resource_access_lock:
            self.resources[resource_name] -= amount
            return True


    def push_resource(self, resource_name, amount):
        '''Adds an amount of resources of resource_name to the storage.'''
        with self.resource_access_lock:
            self.resources[resource_name] += amount


    def resource_available(self, resource_name, amount):
        '''Returns true if a given amount of resource_name is currently available in storage.'''
        return self.resources[resource_name] - amount >= 0


    def stop_resource_access(self):
        '''Method to stop resource access. This is used to halt looping pop_resource() method calls at the end of a simulation.'''
        self.stop_access = True
