import os


def compute_class_weight(folder):
    weights = []
    total = 0
    for i, cls in enumerate(os.listdir(folder)):
        num_files = len(os.listdir(os.path.join(folder, cls)))
        weights.append(num_files)
        total += num_files
    for i in range(len(weights)):
        weights[i] = total / (len(weights) * weights[i])
    return weights
