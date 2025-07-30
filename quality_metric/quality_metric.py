import json

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import KDTree
from scipy.spatial.distance import cdist


def chamfer_distance_optimized(a, b, save_as=""):
    """Optimized Chamfer distance calculation between two individual point clouds.

    Args:
        a: A numpy array of shape (num_points_a, 3) representing the first point cloud.
        b: A numpy array of shape (num_points_b, 3) representing the second point cloud.

    Returns:
        The Chamfer distance between the two point clouds.
    """

    assert a.shape[1] == b.shape[1] == 3, "Point clouds must have 3D coordinates"

    ca = np.average(a, axis=0)
    cb = np.average(b, axis=0)

    a = a - ca
    b = b - cb

    visualize_trajectories(a, b, save_as)

    a_tree = KDTree(a)
    b_tree = KDTree(b)

    a_nn_dists = a_tree.query(b)[0]
    b_nn_dists = b_tree.query(a)[0]

    a_nn_sq_dists = a_nn_dists ** 2
    b_nn_sq_dists = b_nn_dists ** 2

    # print(np.sqrt(np.mean(a_nn_sq_dists)))
    # print(np.sqrt(np.mean(b_nn_sq_dists)))

    rmse = np.sqrt(np.mean(a_nn_sq_dists))

    return rmse
    # return np.mean(a_nn_dists)/2 + np.mean(b_nn_dists)/2  # chamfer distance


def visualize_trajectories(trajectory_a, trajectory_b, save_as=""):
    fig = plt.figure(figsize=(4, 6))
    ax = fig.add_subplot(111)
    # ax = fig.add_subplot(111, projection='3d')
    xy1 = trajectory_a[:, [0, 2]]
    xy2 = trajectory_b[:, [0, 2]]
    ax.plot(*xy1.T, 'ro--', markersize=3)
    ax.plot(*xy2.T, 'bo--', markersize=3)
    ax.set_aspect('equal')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if save_as:
        pass
        plt.savefig(f"{save_as}.png", dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
    else:
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.show()


def load_vicon_trajectory(path, interval, scale=1/1000):
    with open(path, 'r') as f:
        json_data = json.load(f)

    frames = json_data['frames'][interval[0]: interval[1]]
    trajectory = []

    for frame in frames:
        trajectory.append(frame["tvec"])

    return np.array(trajectory) * scale


def load_writing_trajectory(path):
    with open(path, 'r') as f:
        json_data = json.load(f)

    segments = json_data['segments']
    trajectory = []

    for segment in segments:
        trajectory.extend(segment["path"])

    return np.array(trajectory)


if __name__ == "__main__":
    params = [
        (
            "E_vicon_09_38_11_07_25_2025.json",
            (965, 2433),  # 3894, 5056
            "/Users/hamed/Documents/Holodeck/fls_prototype/FLS/motion_planner/animation_data/E_2_0.4x0.6m_fps60_speed0.75_accel0.1.json",
            "E"
        ),
        (
            "O_vicon_09_40_08_07_25_2025.json",
            (975, 1363),  # 1747, 2140
            "/Users/hamed/Documents/Holodeck/fls_prototype/FLS/motion_planner/animation_data/O_0.4x0.6m_fps60_speed0.25.json",
            "O"
        ),
        (
            "S_vicon_09_42_15_07_25_2025.json",
            (963, 1399),  # 1866, 2246
            "/Users/hamed/Documents/Holodeck/fls_prototype/FLS/motion_planner/animation_data/S_0.4x0.6m_fps60_speed0.25.json",
            "S"
        ),
        (
            "N_vicon_10_06_30_07_25_2025.json",
            (951, 2105),  # 3322, 4188
            "/Users/hamed/Documents/Holodeck/fls_prototype/FLS/motion_planner/animation_data/N_0.4x0.6m_fps60_speed0.75_accel0.1.json",
            "N"
        )
    ]

    # FLS 2
    # E vicon_08_42_50_07_25_2025.json, vicon_08_46_16_07_25_2025.json, vicon_08_52_15_07_25_2025.json
    # O vicon_08_54_16_07_25_2025.json, vicon_08_55_35_07_25_2025.json
    # S vicon_08_57_05_07_25_2025.json, vicon_08_58_36_07_25_2025.json
    # N vicon_09_30_45_07_25_2025.json, vicon_09_33_09_07_25_2025.json

    # FLS 1
    # E vicon_09_38_11_07_25_2025.json
    # O vicon_09_40_08_07_25_2025.json
    # S vicon_09_42_15_07_25_2025.json
    # N vicon_10_13_16_07_25_2025.json, vicon_10_06_30_07_25_2025.json, vicon_09_44_19_07_25_2025.json (low bat), vicon_09_46_51_07_25_2025.json (low bat)


    for vicon_log, interval, trajectory, letter in params:
        vicon_trajectory = load_vicon_trajectory("fls1_vicon_2/" + vicon_log, interval)
        writing_trajectory = load_writing_trajectory(trajectory)

        cd = chamfer_distance_optimized(vicon_trajectory, writing_trajectory, save_as=letter)

        print(f"{letter}: {cd*1000:.1f} (mm)")
