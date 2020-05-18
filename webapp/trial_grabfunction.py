import cmath, math

def get_largest_angle(center, peripheral):
    peripheral_radius = [complex(z[0]-center[0], z[1]-center[1]) for z in peripheral]
    peripheral_angle = [cmath.phase(z) for z in peripheral_radius]                     #in radians [-pi to pi]

    i = 0
    while i < len(peripheral_angle):
        if peripheral_angle[i] < 0:
            peripheral_angle[i] = peripheral_angle[i] + 2*(math.pi)
        peripheral_angle[i] = math.degrees(peripheral_angle[i])
        i += 1

    peripheral_angle.sort()
    # getting difference between adjacent angles
    diff_adjacent = []
    i = 0
    while i < len(peripheral_angle):
        if i == len(peripheral_angle) - 1:
            adj_diff = 360 - peripheral_angle[i] + peripheral_angle[0]
        else:
            adj_diff = peripheral_angle[i+1] - peripheral_angle[i]
        diff_adjacent.append(adj_diff)
        i += 1

    print(peripheral_angle)
    print(diff_adjacent)
    max_angle = 360 - max(diff_adjacent)

    return max_angle           #in degrees

center = (0,0)
peripheral = [(1,2),(3,4),(0,-0.1)]
print(get_largest_angle(center, peripheral))
