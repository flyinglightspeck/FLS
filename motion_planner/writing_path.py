import json
import os.path
from enum import Enum

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from scipy.interpolate import splprep, splev, interp1d
from scipy.integrate import quad, cumtrapz

matplotlib.use("macosx")


class SegmentState(Enum):
    LIT = 1
    DARK = 2
    RETURN = 3

    def __str__(self):
        return str(self.name)


state_color = {
    SegmentState.LIT: '#FFA500',
    SegmentState.DARK: '#555555',
    SegmentState.RETURN: '#00BFFF'
}

strokes = {
    'A': [
        # Left diagonal up
        [(0, 0, 0), (0.5, 2, 0)],
        # Right diagonal down
        [(0.5, 2, 0), (1, 0, 0)],
        # Horizontal bar
        [(0.25, 1, 0), (0.75, 1, 0)]
    ],
    'B': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Top curve
        [(0, 2, 0), (0.5, 2, 0), (0.6, 1.5, 0), (0.5, 1, 0), (0, 1, 0)],
        # Bottom curve
        [(0, 1, 0), (0.6, 1, 0), (0.8, 0.5, 0), (0.6, 0, 0), (0, 0, 0)]
    ],
    'C': [
        # Arc from top to bottom
        [(0.8, 1.7, 0), (0.4, 2, 0), (0, 1.5, 0), (0, 0.5, 0), (0.4, 0, 0), (0.8, 0.3, 0)]
    ],
    'D': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Curved right side
        [(0, 2, 0), (0.5, 2, 0), (0.8, 1.7, 0), (0.8, 0.3, 0), (0.5, 0, 0), (0, 0, 0)]
    ],
    'E': [
        # Top horizontal
        [(0.8, 2, 0), (0, 2, 0)],
        # Vertical line
        [(0, 2, 0), (0, 0, 0)],
        # Bottom horizontal
        [(0, 0, 0), (0.8, 0, 0)],
        # Middle horizontal
        [(0, 1, 0), (0.6, 1, 0)]
    ],
    'F': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Top horizontal
        [(0, 2, 0), (0.8, 2, 0)],
        # Middle horizontal
        [(0, 1, 0), (0.6, 1, 0)]
    ],
    'G': [
        # Arc from top around
        [(0.8, 1.5, 0), (0.3, 2, 0), (0, 1.5, 0), (0, 0.5, 0), (0.3, 0, 0), (0.8, 0.3, 0)],
        # Horizontal line in
        [(0.8, 0.3, 0), (0.8, 1, 0)],
        # Short horizontal
        [(0.8, 1, 0), (0.5, 1, 0)]
    ],
    'H': [
        # Left vertical
        [(0, 0, 0), (0, 2, 0)],
        # Right vertical
        [(0.8, 0, 0), (0.8, 2, 0)],
        # Horizontal bar
        [(0, 1, 0), (0.8, 1, 0)]
    ],
    'I': [
        # Top horizontal
        [(0, 2, 0), (0.6, 2, 0)],
        # Vertical line
        [(0.3, 2, 0), (0.3, 0, 0)],
        # Bottom horizontal
        [(0, 0, 0), (0.6, 0, 0)]
    ],
    'J': [
        # Top horizontal
        [(0.4, 2, 0), (0.8, 2, 0)],
        # Vertical down and curve
        [(0.6, 2, 0), (0.6, 0.4, 0), (0.4, 0, 0), (0.2, 0.1, 0)]
    ],
    'K': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Upper diagonal
        [(0.8, 2, 0), (0, 1, 0)],
        # Lower diagonal
        [(0, 1, 0), (0.8, 0, 0)]
    ],
    'L': [
        # Vertical line
        [(0, 2, 0), (0, 0, 0)],
        # Horizontal line
        [(0, 0, 0), (0.8, 0, 0)]
    ],
    'M': [
        # Left vertical
        [(0, 0, 0), (0, 2, 0)],
        # Left diagonal down
        [(0, 2, 0), (0.4, 1, 0)],
        # Right diagonal up
        [(0.4, 1, 0), (0.8, 2, 0)],
        # Right vertical down
        [(0.8, 2, 0), (0.8, 0, 0)]
    ],
    'N': [
        # Left vertical
        [(0, 0, 0), (0, 2, 0)],
        # Diagonal
        [(0, 2, 0), (0.8, 0, 0)],
        # Right vertical
        [(0.8, 0, 0), (0.8, 2, 0)]
    ],
    'O': [
        # Circular motion starting from top
        [(0.4, 2, 0), (0.7, 1.75, 0), (0.8, 1, 0), (0.7, 0.25, 0),
         (0.4, 0, 0), (0.1, 0.25, 0), (0, 1, 0), (0.1, 1.75, 0), (0.4, 2, 0)]
    ],
    'P': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Top curve
        [(0, 2, 0), (0.5, 2, 0), (0.7, 1.7, 0), (0.7, 1.3, 0), (0.5, 1, 0), (0, 1, 0)]
    ],
    'Q': [
        # Circle like O
        [(0.4, 2, 0), (0.7, 1.7, 0), (0.8, 1, 0), (0.7, 0.3, 0),
         (0.4, 0, 0), (0.1, 0.3, 0), (0, 1, 0), (0.1, 1.7, 0), (0.4, 2, 0)],
        # Tail
        [(0.6, 0.4, 0), (0.9, -0.1, 0)]
    ],
    'R': [
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Top curve
        [(0, 2, 0), (0.5, 2, 0), (0.7, 1.7, 0), (0.7, 1.3, 0), (0.5, 1, 0), (0, 1, 0)],
        # Diagonal leg
        [(0.5, 1, 0), (0.8, 0, 0)]
    ],
    'S': [
        # S curve
        [(0.7, 1.6, 0), (0.5, 1.95, 0), (0.18, 1.95, 0), (0, 1.6, 0), (0.12, 1.15, 0), (0.35, 1, 0),
         (0.58, .85, 0), (0.7, 0.4, 0), (0.52, 0.05, 0), (0.2, 0.05, 0), (0, 0.4, 0)]
    ],
    'T': [
        # Top horizontal
        [(0, 2, 0), (0.8, 2, 0)],
        # Vertical line
        [(0.4, 2, 0), (0.4, 0, 0)]
    ],
    'U': [
        # Left down and curve
        [(0, 2, 0), (0, 0.3, 0), (0.1, 0, 0), (0.4, 0, 0)],
        # Right up
        [(0.4, 0, 0), (0.7, 0, 0), (0.8, 0.3, 0), (0.8, 2, 0)]
    ],
    'V': [
        # Left diagonal down
        [(0, 2, 0), (0.4, 0, 0)],
        # Right diagonal up
        [(0.4, 0, 0), (0.8, 2, 0)]
    ],
    'W': [
        # Left diagonal down
        [(0, 2, 0), (0.2, 0, 0)],
        # Up to middle
        [(0.2, 0, 0), (0.4, 1.8, 0)],
        # Down to right
        [(0.4, 1.8, 0), (0.6, 0, 0)],
        # Up to end
        [(0.6, 0, 0), (0.8, 2, 0)]
    ],
    'X': [
        # Left diagonal
        [(0, 2, 0), (0.8, 0, 0)],
        # Right diagonal
        [(0.8, 2, 0), (0, 0, 0)]
    ],
    'Y': [
        # Left diagonal to center
        [(0, 2, 0), (0.4, 1, 0)],
        # Right diagonal to center
        [(0.8, 2, 0), (0.4, 1, 0)],
        # Vertical down
        [(0.4, 1, 0), (0.4, 0, 0)]
    ],
    'Z': [
        # Top horizontal
        [(0, 2, 0), (0.8, 2, 0)],
        # Diagonal
        [(0.8, 2, 0), (0, 0, 0)],
        # Bottom horizontal
        [(0, 0, 0), (0.8, 0, 0)]
    ]
}


class FLS:
    def __init__(self, fps, speed, accel):
        self.fps = fps
        self.speed = speed
        self.accel = accel


class Segment:
    def __init__(self, points, state, order, fls):
        self.points = points
        self.state = state
        self.order = order
        self.smooth_path = None
        self.interpolate(fls)

    def interpolate(self, fls):
        if fls.accel:
            self.smooth_path = interpolate_3d_path_with_accel(self.points, fls.fps, fls.speed, fls.accel)
        else:
            points_per_unit = fls.fps / fls.speed
            self.smooth_path = interpolate_3d_path(self.points, points_per_unit=points_per_unit)

    @property
    def length(self):
        return compute_arc_length(self.smooth_path)

    @property
    def start(self):
        return self.points[0]

    @property
    def end(self):
        return self.points[-1]

    @property
    def is_lit(self):
        return self.state == SegmentState.LIT

    @property
    def is_dark(self):
        return self.state == SegmentState.DARK

    @property
    def is_return(self):
        return self.state == SegmentState.RETURN

    def __repr__(self):
        return f"Segment(order={self.order}, points={self.points}, state={self.state})"


class WritingPath:
    def __init__(self, letter, fls, width=1.0, height=1.5):
        self.letter = letter
        self.looping = True
        self.segments = []
        self.fls = fls
        self.width = width
        self.height = height
        self.create_writing_path()

    def create_writing_path(self):
        pen_strokes = get_letter_strokes(self.letter, self.width, self.height)

        order = 0
        for i, stroke in enumerate(pen_strokes):
            lit_segment = Segment(points=stroke, state=SegmentState.LIT, order=order, fls=self.fls)
            self.segments.append(lit_segment)
            order += 1
            if i + 1 < len(pen_strokes):
                next_segment_start = pen_strokes[i + 1][0]
                prev_segment_end = pen_strokes[i][-1]
                if not is_point_equal(next_segment_start, prev_segment_end):
                    dark_segment = Segment(points=[prev_segment_end, next_segment_start], state=SegmentState.DARK,
                                           order=order, fls=fls)
                    self.segments.append(dark_segment)
                    order += 1

        if self.looping:
            self.add_return_segment()

    def add_return_segment(self):
        if self.segments[-1].state == SegmentState.RETURN:
            return

        path_start = self.segments[0].start
        path_end = self.segments[-1].end

        if not is_point_equal(path_start, path_end):
            return_segment = Segment(points=[path_end, path_start], state=SegmentState.RETURN, order=len(self.segments),
                                     fls=self.fls)
            self.segments.append(return_segment)

    def get_num_lit_segments(self):
        count = 0
        for segment in self.segments:
            if segment.is_lit:
                count += 1
        return count

    def get_num_dark_segments(self):
        count = 0
        for segment in self.segments:
            if segment.is_dark:
                count += 1
        return count

    def get_num_return_segments(self):
        count = 0
        for segment in self.segments:
            if segment.is_return:
                count += 1
        return count

    def get_num_all_segments(self):
        return len(self.segments)

    def is_looping(self):
        return self.looping

    @property
    def length(self):
        return sum([segment.length for segment in self.segments])

    def get_animation_data(self):
        return {
            "duration": self.length / self.fls.speed,
            "segments": [
                {
                    "state": str(segment.state),
                    "path": segment.smooth_path.tolist()
                } for segment in self.segments
            ]
        }

    def get_trajectory_data(self):
        offset = np.array([-self.width / 2, 0.0, 0.0])
        trajectory = {
            "fps": self.fls.fps,
            "duration": self.length / self.fls.speed,
            "start_position": (self.segments[0].smooth_path[0] + offset).tolist(),
            "segments": []
        }

        for j, segment in enumerate(self.segments):
            position = segment.smooth_path[1:] + offset
            velocity = []
            dt = 1 / self.fls.fps

            for i in range(len(position)):
                if i + 1 < len(position):
                    dp = position[i + 1] - position[i]
                    v = dp / dt
                    velocity.append(v.tolist())
                else:
                    if j + 1 < len(self.segments):
                        next_segment = self.segments[j + 1]
                    else:
                        next_segment = self.segments[0]

                    start_next_segment = next_segment.smooth_path[1] + offset
                    dp = start_next_segment - position[i]
                    v = dp / dt
                    velocity.append(v.tolist())

            segment_trajectory = {
                "state": str(segment.state),
                "position": position.tolist(),
                "velocity": velocity
            }
            trajectory["segments"].append(segment_trajectory)

        return trajectory

    def visualize_linear(self):
        fig = plt.figure(figsize=(4, 6))
        ax = fig.add_subplot(111)
        for segment in self.segments:
            color = state_color[segment.state]
            xs = [p[0] for p in segment.points]
            ys = [p[1] for p in segment.points]
            start_x = segment.start[0]
            start_y = segment.start[1]
            end_x = segment.end[0]
            end_y = segment.end[1]
            ax.plot(xs, ys, color=color)
            ax.scatter(start_x, start_y, marker='o', color=color, alpha=1)
            ax.scatter(end_x, end_y, marker='s', color=color, alpha=0.3, s=100)
            ax.text(start_x + 0.05, start_y + 0.05, s=segment.order, color=color)

        ax.set_aspect('equal')

        custom_lines = [
            Line2D([0], [0], marker='o', color='k', linestyle='None', label='Start'),
            Line2D([0], [0], marker='s', color='k', linestyle='None', label='End'),
            Line2D([0], [0], color=state_color[SegmentState.LIT], label='Lit'),
            Line2D([0], [0], color=state_color[SegmentState.DARK], label='Dark'),
            Line2D([0], [0], color=state_color[SegmentState.RETURN], label='Return'),
        ]

        fig.legend(handles=custom_lines)
        plt.axis('off')
        plt.savefig(f"letters/{self.letter}.png", dpi=300)
        plt.close(fig)

    def visualize_trajectory(self, show_control_points=False, save=False):
        fig = plt.figure(figsize=(3, 4))
        ax = fig.add_subplot(111)
        # ax = fig.add_subplot(111, projection='3d')
        for segment in self.segments:
            xy1 = np.array(segment.points)[:, [0, 2]]
            xy2 = segment.smooth_path[:, [0, 2]]
            if show_control_points:
                ax.plot(*xy1.T, 'rs', markersize=3)
            ax.plot(*xy2.T, 'o', color=state_color[segment.state], markersize=1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        # ax.set_title(self.get_filename())

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if save:
            plt.savefig(os.path.join("trajectory_data", self.get_filename('png')), dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
        else:
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.show()

    def visualize_writing_path(self, show_control_points=True, show_segments=True, save=False):
        scale = 1
        fig = plt.figure(figsize=(2, 3))
        ax = fig.add_subplot(111)
        # ax = fig.add_subplot(111, projection='3d')
        for i, segment in enumerate(self.segments):
            xy1 = np.array(segment.points)[:, [0, 2]]
            xy2 = segment.smooth_path[:, [0, 2]]
            if show_control_points:
                if segment.state == SegmentState.LIT:
                    ax.plot(*xy1.T, 'rs', markersize=10)
                    for j, p in enumerate(xy1):
                        ax.text(p[0], p[1], str(j + 1), ha='center', va='center', fontsize=8, zorder=4,
                                fontweight='bold', color="white")

            if show_segments:
                ax.plot(*xy2.T, '-', color=state_color[segment.state])

                start = xy2[0]
                ax.plot(start[0], start[1], 'o', markersize=14, color=state_color[segment.state], markeredgecolor='white', zorder=3)

                ax.text(start[0], start[1], str(i+1), ha='center', va='center', fontsize=10, zorder=4, fontweight='bold', color="white")

                p0 = xy2[0]
                p1 = xy2[20]
                direction = p1 - p0
                direction = direction / np.linalg.norm(direction)  # Normalize

                arrow_length = 0.075
                arrow_start = p0
                arrow_end = p0 + direction * arrow_length

                # Draw arrow
                ax.annotate("",
                            xy=arrow_end,
                            xytext=arrow_start,
                            arrowprops=dict(arrowstyle="->", color=state_color[segment.state], linewidth=2))
        ax.set_aspect('equal')
        ax.axis('off')
        ax.margins(x=0.1, y=0.1)
        # ax.set_title(self.get_filename())

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if save:
            file_name = f"{self.letter}"
            if show_control_points:
                file_name += "_control_points"
            if show_segments:
                file_name += "_segments"
            file_name += ".png"
            plt.savefig(os.path.join("writing_path", file_name), dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()
        else:
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.show()

    def visualize_trajectory_animation(self, save=False):
        interval = 1000 // self.fls.fps
        fig, ax = plt.subplots(figsize=(4, 6))
        ax.set_xlim(-self.width, self.width)
        ax.set_ylim(-0.2, self.height + 0.2)
        ax.set_aspect('equal')
        ax.axis('off')

        traj_data = self.get_trajectory_data()
        positions = [traj_data["start_position"]]
        velocities = [traj_data["segments"][-1]["velocity"][-1]]
        colors = [state_color[SegmentState.LIT]]

        # Flatten segments and gather data
        for segment in traj_data["segments"]:
            positions.extend(segment["position"])
            velocities.extend(segment["velocity"])
            state = SegmentState[segment["state"]]
            colors.extend([state_color[state]] * len(segment["position"]))

        positions = np.array(positions)
        velocities = np.array(velocities)

        point, = ax.plot([], [], 'o', markersize=6)
        path_segments = []  # List of Line2D objects

        # Velocity arrow as a Line2D object (simpler and more visible than quiver)
        velocity_arrow = ax.arrow(0, 0, 0, 0, color='black', width=0.01)
        velocity_patch = [velocity_arrow]  # store current arrow patch

        def init():
            point.set_data([], [])
            return [point, velocity_arrow]

        def update(frame):
            idx = frame % len(positions)
            x, _, y = positions[idx]
            vx, _, vy = velocities[idx]
            color = colors[idx]

            point.set_data([x], [y])
            point.set_color(color)

            # Draw velocity arrow
            if velocity_patch:
                velocity_patch[0].remove()  # Remove the previous arrow
            scale = 0.1  # Adjust this for visual clarity
            arrow = ax.arrow(x, y, vx * scale, vy * scale, color='black', width=0.01)
            velocity_patch[0] = arrow

            # Draw the path up to the current frame
            if frame > 0:
                prev_idx = (frame - 1) % len(positions)
                px, _, py = positions[prev_idx]
                seg_color = colors[idx]
                seg_line = ax.plot([px, x], [py, y], color=seg_color, linewidth=1)[0]
                path_segments.append(seg_line)

            return [point, velocity_patch[0]] + path_segments

        ani = animation.FuncAnimation(fig, update, init_func=init, frames=len(positions),
                                      interval=interval, blit=True, repeat=True)

        ax.set_title(self.get_filename())

        plt.tight_layout(pad=0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        if save:
            ani.save(os.path.join('trajectory_data', self.get_filename('gif')), writer='pillow', fps=self.fls.fps)
            plt.close()
        else:
            plt.show()

    def get_filename(self, postfix=None):
        if self.fls.accel:
            filename = f'{self.letter}_{self.width}x{self.height}m_fps{self.fls.fps}_speed{self.fls.speed}_accel{self.fls.accel}'
        else:
            filename = f'{self.letter}_{self.width}x{self.height}m_fps{self.fls.fps}_speed{self.fls.speed}'

        if postfix is not None:
            return filename + '.' + postfix
        else:
            return filename

    def save_animation_data(self):
        with open(os.path.join('animation_data', self.get_filename('json')), 'w') as f:
            json.dump(self.get_animation_data(), f)

    def save_trajectory_data(self):
        with open(os.path.join('trajectory_data', self.get_filename('json')), 'w') as f:
            json.dump(self.get_trajectory_data(), f)

    def __repr__(self):
        return (f"WritingPath(letter={self.letter}, "
                f"{self.get_num_all_segments()} segments=["
                f"{', '.join([str(s) for s in self.segments])}]")


def get_letter_strokes(letter, size_x=0.4, size_y=0.6):
    """Define natural writing strokes for each letter"""
    # Stroke patterns for uppercase letters
    # Each stroke is a list of (x, y, z) coordinates

    scaled_strokes = []
    if letter.upper() in strokes:
        for stroke in strokes[letter.upper()]:
            scaled_stroke = [(x / 0.8 * size_x, z, y / 2 * size_y) for x, y, z in stroke]
            scaled_strokes.append(scaled_stroke)

    return scaled_strokes


def is_point_equal(point1, point2, threshold=1e-6):
    return np.linalg.norm(np.array(point1) - np.array(point2)) < threshold


def compute_arc_length(points):
    diffs = np.diff(points, axis=0)
    segment_lengths = np.linalg.norm(diffs, axis=1)
    return np.sum(segment_lengths)


def interpolate_3d_path(points, points_per_unit=10, closed_threshold=1e-6):
    points = np.array(points)
    m = len(points)

    if m < 2:
        raise ValueError("Need at least two points to interpolate a path.")

    is_closed = np.linalg.norm(points[0] - points[-1]) < closed_threshold

    # if is_closed:
    #     points = points[:-1]
    #     m -= 1
    #     per = True
    # else:
    #     per = False

    per = False

    # === Fallback for 2-point linear interpolation ===
    if m == 2:
        total_length = np.linalg.norm(points[1] - points[0])
        num_samples = max(2, int(points_per_unit * total_length))
        ts = np.linspace(0, 1, num_samples)

        return (1 - ts)[:, None] * points[0] + ts[:, None] * points[1]

    # === General spline interpolation ===
    x, y, z = points.T
    k = min(3, m - 1)  # Spline degree

    tck, u = splprep([x, y, z], s=0, per=per, k=k)

    def derivative(u_val):
        dx, dy, dz = splev(u_val, tck, der=1)
        return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    total_length = max(1e-6, quad(derivative, 0, 1)[0])
    num_samples = max(2, int(total_length * points_per_unit))

    us = np.linspace(0, 1, num_samples, endpoint=not per)
    smoothed_path = np.array(splev(us, tck)).T

    return smoothed_path


def interpolate_3d_path_with_accel(
    points,
    fps,
    max_speed,      # units/sec
    acceleration,   # units/sec^2
    closed_threshold=1e-6
):
    points = np.array(points)
    m = len(points)

    if m < 2:
        raise ValueError("Need at least two points to interpolate a path.")

    is_closed = np.linalg.norm(points[0] - points[-1]) < closed_threshold
    per = False

    if m == 2:
        return interpolate_linear_with_full_kinematics(points[0], points[1], fps, max_speed, acceleration)

    # === General spline interpolation ===
    x, y, z = points.T
    k = min(3, m - 1)
    tck, _ = splprep([x, y, z], s=0, per=per, k=k)

    def speed_func(u_val):
        dx, dy, dz = splev(u_val, tck, der=1)
        return np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    # Estimate arc length
    us_fine = np.linspace(0, 1, 2000)
    speeds = np.array([speed_func(u) for u in us_fine])
    arc_lengths = cumtrapz(speeds, us_fine, initial=0)
    total_length = arc_lengths[-1]

    # Get traveled distances at each time step
    dt = 1.0 / fps
    distances = simulate_motion_with_accel_decel(total_length, max_speed, acceleration, dt)

    # Map distances to spline parameter u
    dist_to_u = interp1d(arc_lengths, us_fine, kind='linear')
    u_samples = dist_to_u(distances)
    path = np.array(splev(u_samples, tck)).T
    return path


def interpolate_linear_with_full_kinematics(p0, p1, fps, max_speed, acceleration):
    direction = p1 - p0
    length = np.linalg.norm(direction)
    if length < 1e-6:
        return np.array([p0])

    direction /= length
    dt = 1.0 / fps
    distances = simulate_motion_with_accel_decel(length, max_speed, acceleration, dt)
    return np.array([p0 + direction * d for d in distances])


def simulate_motion_with_accel_decel(length, v_max, a, dt, epsilon=1e-6):
    """Simulates distances at fixed time steps considering acceleration, cruising, and deceleration."""
    s_accel = v_max**2 / (2 * a)
    s_decel = s_accel

    if s_accel + s_decel >= length:
        # Triangle profile (no cruise)
        v_peak = np.sqrt(a * length)
        s_accel = s_decel = length / 2
        v_max = v_peak

    distances = [0.0]
    d = 0.0
    v = 0.0

    # Phase 1: Acceleration
    while d < s_accel - epsilon:
        v += a * dt
        d += v * dt
        distances.append(min(d, length))

    # Phase 2: Cruise
    s_cruise = length - s_accel - s_decel
    if s_cruise > epsilon:
        cruise_time = s_cruise / v_max
        n_cruise = int(np.ceil(cruise_time / dt))
        for _ in range(n_cruise):
            d += v_max * dt
            if d >= length - epsilon:
                distances.append(length)
                break
            distances.append(d)

    # Phase 3: Deceleration
    v = v_max
    while d < length - epsilon:
        v = max(v - a * dt, 0)
        if v < epsilon:
            break
        d += v * dt
        distances.append(min(d, length))

    # Ensure final position is exactly at the end
    if distances[-1] < length - epsilon:
        distances.append(length)

    return distances


if __name__ == '__main__':
    if not os.path.exists("animation_data"):
        os.mkdir("animation_data")
    if not os.path.exists("trajectory_data"):
        os.mkdir("trajectory_data")
    if not os.path.exists("writing_path"):
        os.mkdir("writing_path")

    fls = FLS(speed=0.75, fps=30, accel=0.1)
    # fls = FLS(speed=.25, fps=30, accel=0)
    save = True
    for letter in [
        'N', 'E', 'S', 'O'
    ]:
        writing_path = WritingPath(letter, fls=fls, width=0.4, height=0.6)
        writing_path.save_animation_data()
        writing_path.save_trajectory_data()
        writing_path.visualize_writing_path(show_segments=False, save=save)
        writing_path.visualize_writing_path(show_control_points=False, save=save)
        writing_path.visualize_trajectory(save=save)
        writing_path.visualize_trajectory_animation(save=save)
