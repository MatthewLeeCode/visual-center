import visual_center

polygon = [
    [0, 0],
    [0, 100],
    [100, 100],
    [100, 0]
]

pole, distance = visual_center.find_pole(polygon)
print(pole)
print(distance)