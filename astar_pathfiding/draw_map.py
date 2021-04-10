import arcade
import pymunk
import math

# Viewport settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PathFiding A*"

# Physics steps
DT = 1 / 80.0

# Map settings
HEIGHT = 500
WIDTH = SCREEN_WIDTH
DIV = 25
G_W = WIDTH // DIV
G_H = HEIGHT // DIV

# For Line
VERTICAL_LINE_GRADIENT = 1e5

class Button:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
    
    def clicked(self, x, y):
        if x > self.center_x + self.width / 2:
            return False
        if x < self.center_x - self.width / 2:
            return False
        if y > self.center_y + self.height / 2:
            return False
        if y < self.center_y - self.height / 2:
            return False
        return True

    def change_text(self, text):
        self.text = text


class Line(object):
    
    def __init__(self, point_on_line, point_perpendicular_to_line):
        dx = point_on_line.x - point_perpendicular_to_line.x
        dy = point_on_line.y - point_perpendicular_to_line.y

        self.slope_perpendicular = VERTICAL_LINE_GRADIENT if dx == 0 else dy / dx
        self.slope = VERTICAL_LINE_GRADIENT if self.slope_perpendicular == 0 else -1 / self.slope_perpendicular

        self.y_intercept = point_on_line.y - self.slope * point_on_line.x
        self.point_on_line1 = point_on_line
        self.point_on_line2 = point_on_line + pymunk.Vec2d(1, self.slope)

        self.approach_side = self.__get_side(point_perpendicular_to_line)

    def has_crossed_line(self, p):
        return self.__get_side(p) != self.approach_side
    
    def __get_side(self, p):
        return (p.x - self.point_on_line1.x) * (self.point_on_line2.y - self.point_on_line1.y) > (p.y - self.point_on_line1.y) * (self.point_on_line2.x - self.point_on_line1.x)

    def draw_line(self, length):
        line_dir = pymunk.Vec2d(1, self.slope).normalized()
        line_centre = self.point_on_line1
        return arcade.create_line_strip((line_centre - line_dir * length / 2, line_centre + line_dir * length / 2), arcade.color.BAKER_MILLER_PINK)


class Obstacle:
    def __init__(self, position):
        self.radius = 3
        self.colour = arcade.color.RED
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, self.radius)

    def return_shape(self):
        return self.shape

    def get_obstacle(self):
        return arcade.create_ellipse_filled(self.body.position.x, self.body.position.y, self.radius, self.radius, self.colour)


class Path:
    
    def __init__(self):
        self.turn_dist = 10
        self.thickness = 16
        self.points = None
        self.turn_boundaries = []
        self.road_back = arcade.ShapeElementList()
        self.road_front = arcade.ShapeElementList()
        self.draw_points = arcade.ShapeElementList()
        self.draw_boundaries = arcade.ShapeElementList()

    def add_spots(self, points):
        self.points = points
        self.points.reverse()
        
        previous_point = self.points[0]
        for point in self.points:
            dir_to_current_point = (point - previous_point).normalized()
            turn_boundary_point = point - dir_to_current_point * self.turn_dist * 2.5 if point == self.points[-1] else point - dir_to_current_point * self.turn_dist
            self.turn_boundaries.append(Line(turn_boundary_point, previous_point - dir_to_current_point * self.turn_dist))
            previous_point = turn_boundary_point

        self.__setup_draw()
        

    def get_points_and_boundaries(self):
        return self.points, self.turn_boundaries

    def draw_path(self, debug):
        self.road_back.draw()
        self.road_front.draw()
        if debug:
            self.draw_points.draw()
            self.draw_boundaries.draw()

    def __setup_draw(self):
        self.road_back.append(arcade.create_line_strip(self.points, arcade.color.DARK_GRAY, self.thickness))
        self.road_front.append(arcade.create_line_strip(self.points, arcade.color.BLACK, 1))
        
        for e in self.points:
            self.draw_points.append(arcade.create_ellipse(e.x, e.y, 1, 1, arcade.color.YELLOW))
        
        for b in self.turn_boundaries:
            self.draw_boundaries.append(b.draw_line(20))


class Spot:
    
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.parent = None
        self.wall = False
    
    def __lt__(self, other):
        if self.get_f() == other.get_f():
            return self.h < other.h
        return self.get_f() < other.get_f()

    def __repr__(self):
        return f"x: {self.x} | y: {self.y} | f: {self.get_f()} | g: {self.g} | h: {self.h}\n"

    def get_f(self):
        return self.h + self.g
    
    def is_not_wall(self):
        return not self.wall
    
    def set_wall(self):
        if not self.wall: 
            # This will prevent a wall from being declassified as not a wall
            # if the user by mistake clicks on the wall again
            self.wall = True

    def reset(self):
        self.g = 0
        self.h = 0
        self.parent = None

