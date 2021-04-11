import arcade
import pymunk
import math
from heapq import heappop, heappush

from .draw_map import G_H, G_W, DIV


class AStar:


    #A star algorithm implementation
    #f(n) = g(n) + h(n)
    def __init__(self, div):
        # Lists for calculation and path finding
        self.spots = []
        self.open_set = []
        self.closed_set = []
        self.final_path = []
        self.obstacles = []

        # Lists for drawing
        self.path_shape_list = arcade.ShapeElementList()
        self.spots_shape_list = arcade.ShapeElementList()
        self.spots_list = [] # This list is required to avoid n ^ 2 list traversal
        
        # Start and Goal
        self.START = None
        self.GOAL = None

################### Map Update ###################

    # Main Update Function
    def update_map(self, goal_selected):
        current = None
        if goal_selected:
            if len(self.open_set) > 0:
                current = heappop(self.open_set)
                if current == self.GOAL:  #Nếu đã đến được mục tiêu GOAL, thì kết thúc
                    self.final_path.insert(0, pymunk.Vec2d(current.x * G_W + G_W / 2, current.y * G_H + G_H / 2))
                    return {'status': True, 'path': self.final_path}
                
                self.closed_set.append(current) #Duyệt qua thì đóng
                neighbours = self.__get_neighbours(current) #Xét các neighbours xung quanh current
                for neigh in neighbours:
                    if neigh.is_not_wall() and neigh not in self.closed_set: 
                        new_cost = current.g + self.__heuristic(neigh, current) #A*: f(n) = g(n) + h(n)
                        if new_cost < neigh.g or neigh not in self.open_set: #Nếu new_cost có giá trị nhỏ hơn thì gán neigh.g cho new_cost
                            neigh.g = new_cost                               #neigh.h cho hàm heuristic
                            neigh.h = self.__heuristic(neigh, self.GOAL)     #Cứ lặp lại như vậy cho đến khi tới được mục tiêu
                            neigh.parent = current

                            if neigh not in self.open_set:
                                heappush(self.open_set, neigh)
            #Đoạn code trên là giải thuật A*            
    
        if goal_selected and not len(self.open_set) > 0:
            return {'status': False, 'path': None}


        self.calculate_and_draw_path(current)


################### Draw Functions ###################

    # Draw Functions
    def calculate_and_draw_path(self, current):
        self.path_shape_list = arcade.ShapeElementList()
        path = []
        points_list = []
        if current:
            temp = current
            point = pymunk.Vec2d(temp.x * G_W + G_W / 2, temp.y * G_H + G_H / 2)
            points_list.append((point.x, point.y))
            path.append(point)
            while temp.parent:
                temp = temp.parent
                point = pymunk.Vec2d(temp.x * G_W + G_W / 2, temp.y * G_H + G_H / 2)
                points_list.append((point.x, point.y))
                path.append(point)
        
            if len(points_list) > 2:
                line_strip = arcade.create_line_strip(points_list, arcade.color.BAKER_MILLER_PINK, 5)
                self.path_shape_list.append(line_strip)
            self.final_path = path.copy()
    
    def draw_pathfinder(self):
        self.path_shape_list.draw()
    
    def draw_grid(self):
        self.spots_shape_list.draw()


################### Grid Calculations ###################
    
    # Inital Grid Calculations
    def calculate_inital_grid(self):
        for col in self.spots:
            for spot in col:
                shape = arcade.create_rectangle_outline(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.BLUE)
                self.spots_list.append(shape)
        for shape in self.spots_list:
            self.spots_shape_list.append(shape)
        
    # Add data to AStar
    def add_spots(self, spots):
        self.spots.append(spots)
                

################### Setters ###################

    # Set data to AStar
    def set_wall(self, row, col):
        spot = self.spots[row][col]
        self.spots_list[row * DIV + col] = arcade.create_ellipse_filled(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, 3, 3, arcade.color.RED)
        self.spots[row][col].set_wall()
        self.obstacles.append(pymunk.Vec2d(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2))
        self.__recalculate_grid()

    #Set initial State 
    def set_start(self, row, col):
        spot = self.spots[row][col]
        if spot.is_not_wall():
            self.START = spot
            self.open_set.append(self.START)
            self.spots_list[row * DIV + col] = arcade.create_rectangle_filled(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.YELLOW)
            self.__recalculate_grid()
            return self.START
        else:
            return None
    #Set goal state
    def set_goal(self, row, col):
        spot = self.spots[row][col]
        if spot.is_not_wall():
            self.GOAL = spot
            self.spots_list[row * DIV + col] = arcade.create_rectangle_filled(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.RED)
            self.__recalculate_grid()
            return self.GOAL
        return None
      
    def next_state(self):
        # Set goal as new start colour
        spot = self.GOAL
        self.spots_list[spot.x * DIV + spot.y] = arcade.create_rectangle_filled(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.BITTER_LEMON)
        # Reset previous start colour
        spot = self.START
        self.spots_list[spot.x * DIV + spot.y] = arcade.create_rectangle_filled(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.WHITE)
        # Update changes
        self.__recalculate_grid()
        # Add new outline
        self.spots_list[spot.x * DIV + spot.y] = arcade.create_rectangle_outline(spot.x * G_W + G_W / 2, spot.y * G_H + G_H / 2, G_W, G_H, arcade.color.BLACK)
        # Set goal as new start
        self.START = self.GOAL
        self.START.reset()
        self.GOAL = None
        self.reset_goal()


    # Get data from UserMap
    def get_obstacles(self):
        return self.obstacles

################### Private Functions ###################

    # Private Functions
    #Tính toán lại grid
    def __recalculate_grid(self):
        self.spots_shape_list = arcade.ShapeElementList()
        for shape in self.spots_list:
            self.spots_shape_list.append(shape)

    #Set hàm tính toán khoảng cách từ ô n tới goal (g(n))
    def __heuristic(self, a, b):
        distance = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
        return distance


    #Get Neighbours của trạng thái current
    #Có thể dễ hình dung như sau, một ô 3x3 đánh stt từ 1 tới 9, ô current là 6 thì với 
    #giải thuật dưới đây, ta có thể get đc list [1,2,3,4,5,7,8,9]
    def __get_neighbours(self, spot):
        neighbours = []
        if spot.x < DIV - 1:
            neighbours.append(self.spots[spot.x + 1][spot.y]) #Append ô bên phải spot(current)
        if spot.x > 0:
            neighbours.append(self.spots[spot.x - 1][spot.y]) #Append ô bên trái spot(current)
        if spot.y < DIV - 1:
            neighbours.append(self.spots[spot.x][spot.y + 1]) #Append ô bên trên spot(current)
        if spot.y > 0:
            neighbours.append(self.spots[spot.x][spot.y - 1]) #Append ô bên dưới spot(current)
        if spot.x > 0 and spot.y > 0:
            neighbours.append(self.spots[spot.x - 1][spot.y - 1]) #Append ô số 7 (giả sử spot là ô số 5 trên bàn phím 9 số)
        if spot.x < DIV - 1 and spot.y > 0:
            neighbours.append(self.spots[spot.x + 1][spot.y - 1]) #Append ô số 9
        if spot.x > 0 and spot.y < DIV - 1:
            neighbours.append(self.spots[spot.x - 1][spot.y + 1]) #Append ô số 1
        if spot.x < DIV - 1 and spot.y < DIV - 1:
            neighbours.append(self.spots[spot.x + 1][spot.y + 1]) #Append ô số 3
        return neighbours
