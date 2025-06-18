from enum import Enum

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


class SegmentState(Enum):
    LIT = 1
    DARK = 2
    RETURN = 3


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
        # Vertical line
        [(0, 0, 0), (0, 2, 0)],
        # Top horizontal
        [(0, 2, 0), (0.8, 2, 0)],
        # Middle horizontal
        [(0, 1, 0), (0.6, 1, 0)],
        # Bottom horizontal
        [(0, 0, 0), (0.8, 0, 0)]
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
        [(0.4, 2, 0), (0.7, 1.7, 0), (0.8, 1, 0), (0.7, 0.3, 0),
         (0.4, 0, 0), (0.1, 0.3, 0), (0, 1, 0), (0.1, 1.7, 0), (0.4, 2, 0)]
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
        [(0.6, 1.7, 0), (0.35, 2, 0), (0, 1.7, 0), (0.15, 1.2, 0), (0.35, 1, 0),
         (0.55, .8, 0), (0.7, 0.3, 0), (0.35, 0, 0), (0.1, 0.3, 0)]
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


class Segment:
    def __init__(self, points, state, order):
        self.points = points
        self.state = state
        self.order = order

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
    def __init__(self, letter):
        self.letter = letter
        self.looping = True
        self.segments = []
        self.create_writing_path()

    def create_writing_path(self):
        strokes = get_letter_strokes(self.letter)

        order = 0
        for i, stroke in enumerate(strokes):
            lit_segment = Segment(points=stroke, state=SegmentState.LIT, order=order)
            self.segments.append(lit_segment)
            order += 1
            if i + 1 < len(strokes):
                next_segment_start = strokes[i + 1][0]
                prev_segment_end = strokes[i][-1]
                if not is_point_equal(next_segment_start, prev_segment_end):
                    dark_segment = Segment(points=[prev_segment_end, next_segment_start], state=SegmentState.DARK,
                                           order=order)
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
            return_segment = Segment(points=[path_end, path_start], state=SegmentState.RETURN, order=len(self.segments))
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

    def visualize(self):
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

    def __repr__(self):
        return (f"WritingPath(letter={self.letter}, "
                f"{self.get_num_all_segments()} segments=["
                f"{', '.join([str(s) for s in self.segments])}]")


def get_letter_strokes(letter, size_x=1.5, size_y=1):
    """Define natural writing strokes for each letter"""
    # Stroke patterns for uppercase letters
    # Each stroke is a list of (x, y, z) coordinates

    scaled_strokes = []
    if letter.upper() in strokes:
        for stroke in strokes[letter.upper()]:
            scaled_stroke = [(x * size_x, y * size_y, z) for x, y, z in stroke]
            scaled_strokes.append(scaled_stroke)

    return scaled_strokes


def is_point_equal(point1, point2):
    return point1[0] == point2[0] and point1[1] == point2[1] and point1[2] == point2[2]


if __name__ == '__main__':
    # writing_path = WritingPath('E')

    for letter in strokes.keys():
    # letter = 'W'
        writing_path = WritingPath(letter)
        writing_path.visualize()
        print(f"{letter}, {writing_path.get_num_lit_segments()}, {writing_path.get_num_dark_segments()}, {writing_path.get_num_return_segments()}, {writing_path.get_num_all_segments()}")
