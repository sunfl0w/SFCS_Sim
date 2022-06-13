'''The main file of the SFCS simulation suit. This file contains all test scenarios and handles computing mean run times and standard deviations for each scenario'''

import time
import math
import matplotlib.pyplot as plt

from resource_storage import ResourceStorage
from sfcs import ResourceAgent, BiddingManager, RecursiveResourceAgent
from task import AssembleIronGearWheelTask, AssembleElectronicCircuitTask, AssembleCopperCableTask, AssembleAdvancedCircuitTask

def run_test_0(save_fig):
    '''Method to run test scenario 0. For more information about the scenario refer to the linked paper in the README.md'''
    resource_storage = ResourceStorage()
    resource_storage.resources = {
        'iron_plate': 200,
        'copper_plate': 50,
        'plastic_bar': 0,
        'iron_gear_wheel': 0,
        'copper_cable': 0,
        'electronic_circuit': 0,
        'advanced_circuit': 0,
    }

    bm = BiddingManager(resource_storage)

    total_task_time = 0.0
    num_assemblers = 10

    for _ in range (num_assemblers):
        r_agent = ResourceAgent(['IGW_Task', 'CC_Task'])
        r_agent.run()
        bm.add_manufacturing_resource(r_agent)

    data_iron_plate = []
    data_copper_plate = []
    data_iron_gear_wheel = []
    data_copper_cable = []
    delta = []
    run_time = 0
    goal_accomplished_time = 0
    start_time = time.perf_counter()

    add_extra_tasks = True

    for _ in range (100):
        task = AssembleIronGearWheelTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    while goal_accomplished_time == 0 or run_time <= goal_accomplished_time + 2.0:
        data_iron_plate.append(resource_storage.resources['iron_plate'])
        data_iron_gear_wheel.append(resource_storage.resources['iron_gear_wheel'])
        data_copper_plate.append(resource_storage.resources['copper_plate'])
        data_copper_cable.append(resource_storage.resources['copper_cable'])
        run_time = time.perf_counter() - start_time
        delta.append(run_time)

        if resource_storage.resources['iron_gear_wheel'] == 100 and resource_storage.resources['copper_cable'] == 100 and goal_accomplished_time == 0:
            goal_accomplished_time = run_time

        if add_extra_tasks and run_time > 2.5:
            for _ in range (50):
                task = AssembleCopperCableTask(resource_storage)
                total_task_time += task.time
                bm.schedule_task(task)
            add_extra_tasks = False

        time.sleep(0.01)

    resource_storage.stop_resource_access()

    for resource_agent in bm.manufacturing_resources:
        resource_agent.stop()

    print('Test run 0 took', goal_accomplished_time, 'seconds')
    print('Optimal run would take', total_task_time / num_assemblers, 'seconds')

    plt.figure()

    plt.plot(delta, data_iron_plate, label='Iron Plate')
    plt.plot(delta, data_iron_gear_wheel, label='Iron Gear Wheel')
    plt.plot(delta, data_copper_plate, label='Copper Plate')
    plt.plot(delta, data_copper_cable, label='Copper Cable')
    plt.axvline(x=goal_accomplished_time, color=(1.0, 0.0, 0.0), linestyle='--', linewidth=2.0)

    plt.xlabel('Time in s')
    plt.ylabel('Resources')
    plt.title('SFCS test run 0')
    plt.legend()

    if save_fig:
        plt.savefig('TestRun0.png')

    plt.close()
    return goal_accomplished_time


def run_test_1(save_fig):
    '''Method to run test scenario 1. For more information about the scenario refer to the linked paper in the README.md'''
    resource_storage = ResourceStorage()
    resource_storage.resources = {
        'iron_plate': 40,
        'copper_plate': 100,
        'plastic_bar': 40,
        'iron_gear_wheel': 0,
        'copper_cable': 0,
        'electronic_circuit': 0,
        'advanced_circuit': 0,
    }

    bm = BiddingManager(resource_storage)

    total_task_time = 0.0
    num_assemblers = 10

    for i in range (num_assemblers):
        r_agent = ResourceAgent(['EC_Task', 'AC_Task', 'CC_Task'])
        r_agent.run()
        bm.add_manufacturing_resource(r_agent)

    data_iron_plate = []
    data_copper_plate = []
    data_iron_gear_wheel = []
    data_copper_cable = []
    data_plastic_bar = []
    data_electronic_circuit = []
    data_advanced_circuit = []
    delta = []
    run_time = 0
    goal_accomplished_time = 0
    start_time = time.perf_counter()

    for _ in range (100):
        task = AssembleCopperCableTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    for _ in range (40):
        task = AssembleElectronicCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)
    
    for _ in range (20):
        task = AssembleAdvancedCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    while goal_accomplished_time == 0 or run_time <= goal_accomplished_time + 2.0:
        data_iron_plate.append(resource_storage.resources['iron_plate'])
        data_iron_gear_wheel.append(resource_storage.resources['iron_gear_wheel'])
        data_copper_plate.append(resource_storage.resources['copper_plate'])
        data_copper_cable.append(resource_storage.resources['copper_cable'])
        data_plastic_bar.append(resource_storage.resources['plastic_bar'])
        data_electronic_circuit.append(resource_storage.resources['electronic_circuit'])
        data_advanced_circuit.append(resource_storage.resources['advanced_circuit'])
        run_time = time.perf_counter() - start_time
        delta.append(run_time)

        if resource_storage.resources['advanced_circuit'] == 20 and goal_accomplished_time == 0:
            goal_accomplished_time = run_time

        time.sleep(0.01)

    resource_storage.stop_resource_access()

    for resource_agent in bm.manufacturing_resources:
        resource_agent.stop()

    print('Test run 1 took', goal_accomplished_time, 'seconds')
    print('Optimal run would take', total_task_time / num_assemblers, 'seconds')

    plt.figure()

    plt.plot(delta, data_iron_plate, label='Iron Plate')
    plt.plot(delta, data_iron_gear_wheel, label='Iron Gear Wheel')
    plt.plot(delta, data_copper_plate, label='Copper Plate')
    plt.plot(delta, data_copper_cable, label='Copper Cable')
    plt.plot(delta, data_plastic_bar, label='Plastic Bar')
    plt.plot(delta, data_electronic_circuit, label='Electronic Circuit')
    plt.plot(delta, data_advanced_circuit, label='Advanced Circuit')
    plt.axvline(x=goal_accomplished_time, color=(1.0, 0.0, 0.0), linestyle='--', linewidth=2.0)

    plt.xlabel('Time in s')
    plt.ylabel('Resources')
    plt.title('SFCS test run 1')
    plt.legend()

    if save_fig:
        plt.savefig('TestRun1.png')

    plt.close()
    return goal_accomplished_time


def run_test_2(save_fig):
    '''Method to run test scenario 2. For more information about the scenario refer to the linked paper in the README.md'''
    resource_storage = ResourceStorage()
    resource_storage.resources = {
        'iron_plate': 40,
        'copper_plate': 100,
        'plastic_bar': 40,
        'iron_gear_wheel': 0,
        'copper_cable': 0,
        'electronic_circuit': 0,
        'advanced_circuit': 0,
    }

    bm = BiddingManager(resource_storage)

    total_task_time = 0.0
    num_assemblers = 10

    for i in range (num_assemblers):
        r_agent = ResourceAgent(['EC_Task', 'AC_Task', 'CC_Task'])
        r_agent.run()
        bm.add_manufacturing_resource(r_agent)

    data_iron_plate = []
    data_copper_plate = []
    data_iron_gear_wheel = []
    data_copper_cable = []
    data_plastic_bar = []
    data_electronic_circuit = []
    data_advanced_circuit = []
    delta = []
    run_time = 0
    goal_accomplished_time = 0
    start_time = time.perf_counter()

    for _ in range (100):
        task = AssembleCopperCableTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    for _ in range (20):
        task = AssembleAdvancedCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    for _ in range (40):
        task = AssembleElectronicCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    while run_time <= total_task_time / num_assemblers * 3.0:
        data_iron_plate.append(resource_storage.resources['iron_plate'])
        data_iron_gear_wheel.append(resource_storage.resources['iron_gear_wheel'])
        data_copper_plate.append(resource_storage.resources['copper_plate'])
        data_copper_cable.append(resource_storage.resources['copper_cable'])
        data_plastic_bar.append(resource_storage.resources['plastic_bar'])
        data_electronic_circuit.append(resource_storage.resources['electronic_circuit'])
        data_advanced_circuit.append(resource_storage.resources['advanced_circuit'])
        run_time = time.perf_counter() - start_time
        delta.append(run_time)

        if resource_storage.resources['advanced_circuit'] == 20 and goal_accomplished_time == 0:
            goal_accomplished_time = run_time

        time.sleep(0.01)

    resource_storage.stop_resource_access()

    for resource_agent in bm.manufacturing_resources:
        resource_agent.stop()

    print('Test run 2 took', goal_accomplished_time, 'seconds')
    print('Optimal run would take', total_task_time / num_assemblers, 'seconds')

    plt.figure()

    plt.plot(delta, data_iron_plate, label='Iron Plate')
    plt.plot(delta, data_iron_gear_wheel, label='Iron Gear Wheel')
    plt.plot(delta, data_copper_plate, label='Copper Plate')
    plt.plot(delta, data_copper_cable, label='Copper Cable')
    plt.plot(delta, data_plastic_bar, label='Plastic Bar')
    plt.plot(delta, data_electronic_circuit, label='Electronic Circuit')
    plt.plot(delta, data_advanced_circuit, label='Advanced Circuit')

    plt.xlabel('Time in s')
    plt.ylabel('Resources')
    plt.title('SFCS test run 2')
    plt.legend()

    if save_fig:
        plt.savefig('TestRun2.png')

    plt.close()
    return goal_accomplished_time


def run_test_3(save_fig):
    '''Method to run test scenario 3. For more information about the scenario refer to the linked paper in the README.md'''
    resource_storage = ResourceStorage()
    resource_storage.resources = {
        'iron_plate': 40,
        'copper_plate': 100,
        'plastic_bar': 40,
        'iron_gear_wheel': 0,
        'copper_cable': 0,
        'electronic_circuit': 0,
        'advanced_circuit': 0,
    }

    bm = BiddingManager(resource_storage)
    sub_bm = BiddingManager(resource_storage)

    total_task_time = 0.0
    num_assemblers = 20

    for i in range (19):
        r_agent = ResourceAgent(['EC_Task', 'AC_Task'])
        r_agent.run()
        bm.add_manufacturing_resource(r_agent)

    for i in range (1):
        r_agent = ResourceAgent(['CC_Task'])
        r_agent.run()
        sub_bm.add_manufacturing_resource(r_agent)

    rec_r_agent = RecursiveResourceAgent(sub_bm, ['CC_Task'])
    rec_r_agent.run()
    bm.add_manufacturing_resource(rec_r_agent)

    data_iron_plate = []
    data_copper_plate = []
    data_iron_gear_wheel = []
    data_copper_cable = []
    data_plastic_bar = []
    data_electronic_circuit = []
    data_advanced_circuit = []
    delta = []
    run_time = 0
    goal_accomplished_time = 0
    start_time = time.perf_counter()

    for _ in range (100):
        task = AssembleCopperCableTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    for _ in range (40):
        task = AssembleElectronicCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)
    
    for _ in range (20):
        task = AssembleAdvancedCircuitTask(resource_storage)
        total_task_time += task.time
        bm.schedule_task(task)

    while goal_accomplished_time == 0 or run_time <= goal_accomplished_time + 2.0:
        data_iron_plate.append(resource_storage.resources['iron_plate'])
        data_iron_gear_wheel.append(resource_storage.resources['iron_gear_wheel'])
        data_copper_plate.append(resource_storage.resources['copper_plate'])
        data_copper_cable.append(resource_storage.resources['copper_cable'])
        data_plastic_bar.append(resource_storage.resources['plastic_bar'])
        data_electronic_circuit.append(resource_storage.resources['electronic_circuit'])
        data_advanced_circuit.append(resource_storage.resources['advanced_circuit'])
        run_time = time.perf_counter() - start_time
        delta.append(run_time)

        if resource_storage.resources['advanced_circuit'] == 20 and goal_accomplished_time == 0:
            goal_accomplished_time = run_time

        time.sleep(0.01)

    resource_storage.stop_resource_access()

    for resource_agent in bm.manufacturing_resources:
        resource_agent.stop()

    for resource_agent in sub_bm.manufacturing_resources:
        resource_agent.stop()

    print('Test run 3 took', goal_accomplished_time, 'seconds')
    print('Optimal run would take', total_task_time / num_assemblers, 'seconds')

    plt.figure()

    plt.plot(delta, data_iron_plate, label='Iron Plate')
    plt.plot(delta, data_iron_gear_wheel, label='Iron Gear Wheel')
    plt.plot(delta, data_copper_plate, label='Copper Plate')
    plt.plot(delta, data_copper_cable, label='Copper Cable')
    plt.plot(delta, data_plastic_bar, label='Plastic Bar')
    plt.plot(delta, data_electronic_circuit, label='Electronic Circuit')
    plt.plot(delta, data_advanced_circuit, label='Advanced Circuit')
    plt.axvline(x=goal_accomplished_time, color=(1.0, 0.0, 0.0), linestyle='--', linewidth=2.0)

    plt.xlabel('Time in s')
    plt.ylabel('Resources')
    plt.title('SFCS test run 3')
    plt.legend()

    if save_fig:
        plt.savefig('TestRun3.png')

    plt.close()
    return goal_accomplished_time


def main():
    '''Main method. Run this to perform simulations'''
    num_runs = 30 # Change this to perform a different amount of iterations. Note that one iteration takes more than two minutes

    total_time_test = [[], [], [], []]

    # Testing each scenario in num_runs iterations and collecting the times to achieve a predefined manufacturing goal
    for i in range(num_runs):
        print("----")
        print("Test Iteration", i)
        total_time_test[0].append(run_test_0(i == 0))
        total_time_test[1].append(run_test_1(i == 0))
        total_time_test[2].append(run_test_2(i == 0))
        total_time_test[3].append(run_test_3(i == 0))
        print("----")

    # Calculating the mean time and standard deviation for each test scenario
    for i in range(4):
        mean = 0.0

        for j in range(num_runs):
            mean += total_time_test[i][j]
        mean /= num_runs

        sd = 0.0
        for j in range(num_runs):
            sd += pow(total_time_test[i][j] - mean, 2.0)
        sd /= num_runs
        sd = math.sqrt(sd)

        print("Test", i, "mean is:", mean)
        print("Test", i, "sd is:", sd)


if __name__ == '__main__':
    main()