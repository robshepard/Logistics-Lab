#!/bin/python3
import math

def load_machine_positions(file):
    machines = []
    with open(file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            id, x, y = map(int, line.strip().split(';'))
            machines.append({'id': id, 'x': x, 'y': y})
    return machines

def load_orders(machines, file):
    n = len(machines)
    matrix = [[0] * n for _ in range(n)]
    for line in open(file).readlines()[1:]:
        start, dest, number = map(int, line.strip().split(';'))
        matrix[start - 1][dest - 1] = number
    return matrix

def calculate_distances(machines):
    n = len(machines)
    dists = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dists[i][j] = math.sqrt((machines[i]['x'] - machines[j]['x']) ** 2 + (machines[i]['y'] - machines[j]['y']) ** 2)
    return dists

def write_solution(solution, file):
    with open(file, "w") as file:
        for line in sorted(solution, key = lambda l: l[0]):
            file.write(';'.join(map(str, line)) + '\n')


def solve(orders, dists, n_vehicles):
    
    solution = []
    vehicles = [[i, i, 0, 0] for i in range(n_vehicles)] # (vehicle_id, next_pos, has_cargo, dist_to_go)
    
    while any(map(any, orders)):

        # select vehicle with least distance to its target
        vehicle_id, curr_pos, has_cargo, dist_to_go = vehicles.pop(0)
        for v in vehicles: v[3] -= dist_to_go

        # if current machine has pending orders
        if any(orders[curr_pos]):
            
            # we know that we pick up cargo, so write last move
            solution.append((vehicle_id + 1, curr_pos + 1, has_cargo, 1))
            has_cargo = 1

            # find machine with most orders from current machine
            next_pos = orders[curr_pos].index(max(orders[curr_pos]))
            orders[curr_pos][next_pos] -= 1
        
        else:
            # we know that we dont pick up cargo, so write last move
            solution.append((vehicle_id + 1, curr_pos + 1, has_cargo, 0))
            has_cargo = 0

            # drive to nearest machine that still has pending orders
            next_pos = next(machine for machine, dist in sorted(enumerate(dists[curr_pos]), key = lambda x: x[1]) if any(orders[machine]))
            

        vehicles.append([vehicle_id, next_pos, has_cargo, dists[curr_pos][next_pos]])
        vehicles.sort(key = lambda v: v[3])

    for vehicle_id, curr_pos, has_cargo, dist_to_go in vehicles:
        solution.append((vehicle_id + 1, curr_pos + 1, has_cargo, 0))

    return solution



machines = load_machine_positions("machine_positions.txt")
dists = calculate_distances(machines)

for n in [1, 5, 10]:
    order_matrix = load_orders(machines, "transport_demand.txt")
    solution = solve(order_matrix, dists, n)
    write_solution(solution, "greedy_" + str(n) + "_schedule.txt")




# 10
# Valid solution; Score for greedy_5_schedule.txt: 3620.6408

# 5
# Valid solution; Score for greedy_10_schedule.txt: 1819.8366

# 1
# Valid solution; Score for greedy_1_schedule.txt: 18112.595
