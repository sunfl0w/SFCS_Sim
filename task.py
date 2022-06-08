import time


class Task():
    time = 0.0
    name = None
    resource_storage = None
    
    def execute(self):
        pass


class AssembleIronGearWheelTask(Task):
    def __init__(self, resource_storage):
        self.time = 0.5
        self.name = 'IGW_Task'
        self.resource_storage = resource_storage

    def execute(self):
        if self.resource_storage.pop_resource('iron_plate', 2):
            time.sleep(0.5)
            self.resource_storage.push_resource('iron_gear_wheel', 1)


class AssembleCopperCableTask(Task):
    def __init__(self, resource_storage):
        self.time = 0.5
        self.name = 'CC_Task'
        self.resource_storage = resource_storage

    def execute(self):
        if self.resource_storage.pop_resource('copper_plate', 1):
            time.sleep(0.5)
            self.resource_storage.push_resource('copper_cable', 2)


class AssembleElectronicCircuitTask(Task):
    def __init__(self, resource_storage):
        self.time = 0.5
        self.name = 'EC_Task'
        self.resource_storage = resource_storage

    def execute(self):
        if self.resource_storage.pop_resource('iron_plate', 1):
            if self.resource_storage.pop_resource('copper_cable', 3):
                time.sleep(0.5)
                self.resource_storage.push_resource('electronic_circuit', 1)
            else:
                self.resource_storage.push_resource('iron_plate', 1)


class AssembleAdvancedCircuitTask(Task):
    def __init__(self, resource_storage):
        self.time = 6.0
        self.name = 'AC_Task'
        self.resource_storage = resource_storage

    def execute(self):
        if self.resource_storage.pop_resource('plastic_bar', 2):
            if self.resource_storage.pop_resource('copper_cable', 4):
                if self.resource_storage.pop_resource('electronic_circuit', 2):
                    time.sleep(6.0)
                    self.resource_storage.push_resource('advanced_circuit', 1)
                else:
                    self.resource_storage.push_resource('plastic_bar', 2)
                    self.resource_storage.push_resource('copper_cable', 4)
            else:
                self.resource_storage.push_resource('plastic_bar', 2)