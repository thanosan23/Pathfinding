def find_by_key(dictionary, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

# linear interpolation
def lerp(value, target, t):
    return value + (target - value) * t
