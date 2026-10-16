import math

class Fruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind  # "fruit" or "bomb"
        self.sliced = False

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def contains_point(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.radius

    def segment_hits(self, x1, y1, x2, y2, margin=0):
        # A fast swipe can jump from one side of the fruit to the other
        # between two MOUSEMOTION events, so checking only the reported
        # points misses it. Instead, test the whole blade segment between
        # the previous and current mouse positions against the circle:
        # find the point on the segment closest to the fruit's centre and
        # check whether it lies within the radius.
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx * dx + dy * dy
        t = 0.0
        if length_sq > 0:
            t = ((self.x - x1) * dx + (self.y - y1) * dy) / length_sq
            t = max(0.0, min(1.0, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        return math.hypot(self.x - closest_x, self.y - closest_y) <= self.radius + margin

    def off_screen(self, height):
        return self.y - self.radius > height
