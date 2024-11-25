import random
import os
import pygame
import numpy
import math

class Cube():
    def __init__(self, pos, size, start_rotation):
        self.size = size
        self.pos = pos
        self.age = 0
        self.angle = list(start_rotation)

        self.root_verts = []
        self.assign_root_verts()

        self.surface = pygame.Surface((2 * math.sqrt(3) * self.size, 2 * math.sqrt(3) * self.size))
        self.surface.set_colorkey((255, 255, 255))

        self.projection_matrix = numpy.matrix([[1, 0, 0], [0, 1, 0], [0,0,0]])

        self.vert_pos = [math.sqrt(3) * self.size, math.sqrt(3) * self.size]
        
        self.projected_points = []
        for i in range(len(self.root_verts)):
            self.projected_points.append([i,0])

        ##print(f"Projection {self.projected_points}")

    def update(self):
        self.calc_rotation(self.angle)
        self.calc_projection()
        ##self.move_cube()
        
        ##self.angle += 0.01
        self.age += 0.001

    def calc_projection(self):
        """
        https://en.wikipedia.org/wiki/Projection_(linear_algebra)
        Projection will need the dot product of the rotation matrices representing yaw(x), pitch(y), and roll(z) into
        the general rotation matrix rmatrix_xyz. The position of the vertices in 2d will be the dot product of
        the general rotation matrix and the projection matrix
        Numpy will be used to help handle matrix operations with dot product method.
        For clarity purposes, all rotation matrices are named as matrices and are not related to coding matrices or arrays.
        """
        i = 0
        for point in self.root_verts:
            
            rmatrix_xyz = numpy.dot(self.rmatrix_z, point.reshape((3, 1)))
            rmatrix_xyz = numpy.dot(self.rmatrix_y, rmatrix_xyz)
            rmatrix_xyz = numpy.dot(self.rmatrix_x, rmatrix_xyz)

            points_2d = numpy.dot(self.projection_matrix, rmatrix_xyz)
  
            x = int(points_2d[0][0].item() * self.size) + self.vert_pos[0]
            y = int(points_2d[1][0].item() * self.size) + self.vert_pos[1]

            self.projected_points[i] = [x, y]
            i += 1

    def calc_rotation(self, angle):

        """
        From https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematics_for_Game_Developers_(Burzynski)/04%3A_Matrices/4.06%3A_Rotation_Matrices_in_3-Dimensions
        Rotation matrices must be defined.
        """
        
        self.rotate_x(angle[0] * math.pi / 180)
        self.rotate_y(angle[1] * math.pi / 180)
        self.rotate_z(angle[2] * math.pi / 180)
    
    def rotate_x(self, angle):
        ##Gamma, yaw
        self.rmatrix_x = numpy.matrix([
            [1,               0,                0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)],
        ])
    def rotate_y(self, angle):
        ##Beta, pitch
        self.rmatrix_y = numpy.matrix([
            [math.cos(angle),  0, math.sin(angle)],
            [0,                1,               0],
            [-math.sin(angle), 0, math.cos(angle)],
        ])     
    def rotate_z(self, angle):
        ##Alpha, roll
        self.rmatrix_z = numpy.matrix([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle),  0],
            [0,                         0,      1],
        ])  

    def assign_root_verts(self):

        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    x = int(math.pow(-1, i))
                    y = int(math.pow(-1, j))
                    z = int(math.pow(-1, k))

                    self.root_verts.append(numpy.matrix([x, y, z]))
                    ##print(f"{self.root_verts}")

    """
    The process of drawing the cube will be to take a corner, draw three lines that converge on it
    Repeat for any unique corners that don't cover existing lines
    """

    def create_edge(self, color, i, j):
        pygame.draw.line(self.surface, color, 
            (self.projected_points[i][0], self.projected_points[i][1]), 
            (self.projected_points[j][0], self.projected_points[j][1]))
        
    def draw_cube(self, surface):
        self.surface.fill((255,255,255))

        corners = []
        for idx in range(len(self.projected_points)):
            corners.append((self.projected_points[idx][0], self.projected_points[idx][1]))
        
        draw_corners = [0, 3, 5, 6]
        adj_edges = [1, 2, 4, 7]
        j = 0

        for i in range(4):
            for n in range(3):
                self.create_edge((0, 0, 0), draw_corners[i], adj_edges[j  % 4])
                j += 1

        ##self.shade_cube(corners)
        surface.blit(self.surface, (self.pos[0] - math.sqrt(3) * self.size, self.pos[1] - math.sqrt(3) * self.size))
        ##surface.blit(self.surface, (self.pos[0], self.pos[1]))

    def shade_cube(self, corners):
        face1 = [corners[0], corners[1], corners[3], corners[2]]
        face2 = [corners[0], corners[4], corners[6], corners[2]]
        face3 = [corners[2], corners[3], corners[7], corners[6]]

        face5 = [corners[4], corners[5], corners[7], corners[6]]
        face6 = [corners[1], corners[5], corners[7], corners[3]]
        face7 = [corners[0], corners[1], corners[5], corners[4]]

        faces = [face1, face2, face3, face5, face6, face7]
        face = []

        j = 0
        for i in range(len(faces)):
            ##pygame.draw.polygon(self.surface, (255,255/6 * i,255/6 * i), faces[i])
            pygame.draw.polygon(self.surface, (0,0,0), faces[i])

        ##pygame.draw.polygon(self.surface, (0,0,0), ((0,0), (150, 100), ( 200, 0)))

    def move_cube(self):
        self.pos[1] += 1

class Plane():
    def __init__(self, pos, size, rotation):
        self.size = size
        self.pos = pos
        self.age = 0
        self.angle = rotation

        self.root_verts = []
        self.assign_root_verts()

        self.surface = pygame.Surface((2*math.sqrt(2) * self.size, 2*math.sqrt(2) * self.size))
        self.surface.set_colorkey((255, 255, 255))

        self.projection_matrix = numpy.matrix([[1, 0, 0], [0, 1, 0], [0,0,0]])

        self.vert_pos = [math.sqrt(2) * self.size, math.sqrt(2) * self.size]
        
        self.projected_points = []
        for i in range(len(self.root_verts)):
            self.projected_points.append([i,0])

    def update(self):
        self.calc_rotation()
        self.calc_projection()
        
        ##self.angle += 0.1
        self.age += 0.001

    def calc_projection(self):

        i = 0
        for point in self.root_verts:
            
            rmatrix_xyz = numpy.dot(self.rmatrix_z, point.reshape((3, 1)))
            rmatrix_xyz = numpy.dot(self.rmatrix_y, rmatrix_xyz)
            rmatrix_xyz = numpy.dot(self.rmatrix_x, rmatrix_xyz)

            points_2d = numpy.dot(self.projection_matrix, rmatrix_xyz)
  
            x = int(points_2d[0][0].item() * self.size) + self.vert_pos[0]
            y = int(points_2d[1][0].item() * self.size) + self.vert_pos[1]

            self.projected_points[i] = [x, y]
            i += 1

    def calc_rotation(self):

        self.rotate_x(self.angle[0] * math.pi / 180)
        self.rotate_y(self.angle[1] * math.pi / 180)
        self.rotate_z(self.angle[2] * math.pi / 180)
    
    def rotate_x(self, angle):
        ##Gamma, yaw
        self.rmatrix_x = numpy.matrix([
            [1,               0,                0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)],
        ])
    def rotate_y(self, angle):
        ##Beta, pitch
        self.rmatrix_y = numpy.matrix([
            [math.cos(angle),  0, math.sin(angle)],
            [0,                1,               0],
            [-math.sin(angle), 0, math.cos(angle)],
        ])     
    def rotate_z(self, angle):
        ##Alpha, roll
        self.rmatrix_z = numpy.matrix([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle),  0],
            [0,                         0,      1],
        ])  

    def assign_root_verts(self):

        for i in range(0, 2):
            for j in range(0, 2):
                x = int(math.pow(-1, i))
                y = int(math.pow(-1, j))
                self.root_verts.append(numpy.matrix([x, y, 0]))

    def create_edge(self, color, i, j):
        pygame.draw.line(self.surface, color, 
            (self.projected_points[i][0], self.projected_points[i][1]), 
            (self.projected_points[j][0], self.projected_points[j][1]))
        
    def draw(self, surface):
        self.surface.fill((255,255,255))

        corners = []
        for idx in range(len(self.projected_points)):
            corners.append((self.projected_points[idx][0], self.projected_points[idx][1]))
        
        draw_corners = [0, 1, 2, 3]
        adj_edges = [1, 2]
        j = 0

        self.create_edge((0, 0, 0), draw_corners[0], draw_corners[1])
        self.create_edge((0, 0, 0), draw_corners[1], draw_corners[3])
        self.create_edge((0, 0, 0), draw_corners[3], draw_corners[2])
        self.create_edge((0, 0, 0), draw_corners[2], draw_corners[0])
         
        
        ##pygame.draw.circle(self.surface, (0,0,0), (self.projected_points[0][0], self.projected_points[0][1]), 5)
        
        ##surface.blit(self.surface, (self.pos[0] - math.sqrt(2) * self.size, self.pos[1] - math.sqrt(2) * self.size))
        surface.blit(self.surface, (self.pos[0] - math.sqrt(2) * self.size, self.pos[1] - math.sqrt(2) * self.size))

class Point():
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self, surface):
        
        pygame.draw.circle(surface, self.color, self.pos, self.size)

class PlaneGrid():
    def __init__(self, pos, size, angle, resolution):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.univ_angle = 0
        self.length = resolution[0]
        self.width = resolution[1]
        self.cubes = []

        self.skip = 0
        self.create_grid()

    def update(self, dt):
        ##if self.skip % 120 == 0:
        ##self.create_new_cube()

        self.skip += 1

        for cube in self.cubes:
            cube.update()
            cube.angle += 1
            self.univ_angle = cube.angle
            ##self.size_change()
                
    def create_grid(self):
        
        buffer = 2 * math.sqrt(2) * self.size
        count_x = 0
        count_y = 0
        while (count_x * buffer ) < self.length : 
            while (count_y * buffer) < self.width :
                cube = Plane(pos = [count_x * buffer, count_y * buffer], size=self.size, rotation = [90,0,0])
                self.cubes.insert(0, cube)
                count_y += 1

            count_y = 0
            count_x +=1


    def draw(self, surface):
        for cube in self.cubes:
            cube.draw(surface)

class PlaneCascade():
    def __init__(self, resolution):
        
        self.length = resolution[0]
        self.width = resolution[1]
        self.planes = []

        self.skip = 0
        self.xpos = []
        self.ypos = []
        self.rotations = []
        self.sizes = []
        self.start_size = 50

        self.casc_length =5
        self.create_cascade()

    def update(self, dt):
        
        ##self.casc_length += 1

        for plane in self.planes:
            plane.update()
            ##cube.angle += 1
            
            self.univ_angle = plane.angle
            ##self.size_change()
        self.create_cascade()
    
    def calc_transforms(self):
        
        x_line = 0
        y_line = 0

        for idx in range(self.casc_length):
            
            calc_res = math.pow(self.width, 2) / self.length

            print(f"{calc_res}")
            x_line = self.length /(self.casc_length+5) * idx + self.start_size
            y_line = math.sqrt((calc_res * x_line))

            
            self.xpos.append(x_line)
            self.ypos.append(y_line)
            self.rotations.append([90 * (1 - 1 * idx/self.casc_length), 0, 45 * (1 - 1 * idx/self.casc_length)])
        
    def create_cascade(self):

        self.calc_transforms()
        for idx in range(self.casc_length):
            plane = Plane(pos = [self.xpos[idx], self.ypos[idx]], size=self.start_size + 10 * idx, rotation = self.rotations[idx])
            
            self.planes.insert(0, plane)
        

    def draw(self, surface):
        for plane in self.planes:
            plane.draw(surface)

##class PlaneTrail():
    ##def

class PointGrid():
    def __init__(self, resolution):

        self.length = resolution[0]
        self.width = resolution[1]
        self.points = []
        self.surf = pygame.Surface(resolution)
        self.surf.fill((255,255,255))
        self.surf.set_colorkey((255, 255, 255))

        ##pygame.draw.circle(self.surf, (0,0,0), (0,0), 50)
        self.skip = 0
        self.create_grid()

    def update(self, dt, surface):
        
        for point in self.points:
            point.draw(self.surf)
            ##point.size += 1
            ##self.size_change()
        surface.blit(self.surf, (0,0))
                
    def create_grid(self):
        
        buffer = 20
        count_x = 0
        count_y = 0
        while (count_x * buffer ) <= self.length : 
            while (count_y * buffer) <= self.width :
                point = Point((count_x * buffer, count_y * buffer), 1, (0,0,0))
                self.points.insert(0, point)
                count_y += 1
            count_x += 1
            count_y = 0
    
    ##def connect_grid(self):
        ##for cube in self.cubes:

class CubeGrid():
    def __init__(self, pos, size, angle, resolution):
        self.pos = pos
        self.size = size
        self.angle = angle
        self.univ_angle = (0, 0, 0)
        self.length = resolution[0]
        self.width = resolution[1]
        self.cubes = []

        self.skip = 0
        self.create_grid()

    def update(self, dt):
        ##if self.skip % 120 == 0:
        ##self.create_new_cube()

        self.skip += 1

        for cube in self.cubes:
            cube.update()
            cube.angle[0] += 1
            cube.angle[1] += 1
            self.univ_angle = cube.angle
            ##self.size_change()
                
    def create_grid(self):
        
        buffer = 2 * math.sqrt(3) * self.size
        count_x = 0
        count_y = 0
        while (count_x * buffer ) < self.length : 
            while (count_y * buffer) < self.width :
                cube = Cube(pos = [count_x * buffer, count_y * buffer], size=self.size, start_rotation = self.univ_angle)
                self.cubes.insert(0, cube)
                count_y += 1
            ##print(f"y {count_y}")
            count_y = 0
            count_x +=1
            ##print(f"cubes {count_x}")
    
    ##def connect_grid(self):
        ##for cube in self.cubes:

    def size_change(self):
        for cube in self.cubes:
            cube.size -= 0.001

    def draw(self, surface):
        for cube in self.cubes:
            cube.draw_cube(surface)

##class Circle():

def main():
    pygame.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    ##resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)

    mouse_pos = (resolution[0]/2, resolution[1]/2)
    mouse_rel = (0,0)
    mouse_hold = False
    mouse_scroll = 0
    mouse_button_state = pygame.mouse.get_pressed(3)
    mouse_motion_state = ()

    cubeTrail = CubeGrid(200, 50, 0, resolution)
    cube = Cube([resolution[0]/2, resolution[1]/2], 50, (20, 10, 0))
    plane1 = PlaneCascade(resolution)
    points = PointGrid(resolution)

    white = pygame.Color(255, 255, 255)
    running = True
    states = [True, False, False, False, False, False, False, False, False, False]

    pygame.mouse.set_pos(mouse_pos)
    ##surface = pygame.Surface((size=resolution, flags=0, depth=0, display=0, vsync=0))

    while running:

        ##pygame.key.set_repeat(100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   running = False
                match event.key:
                    case pygame.K_0:
                        change_state(states)
                        states[0] = True
                        print(event)

                    case pygame.K_1:
                        change_state(states)
                        states[1] = True
                        print(event)

                    case pygame.K_2:
                        change_state(states)
                        states[2] = True
                        print(event)

                    case pygame.K_3:
                        change_state(states)
                        states[3] = True
                        print(event)
            
            if states[1]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button_state = pygame.mouse.get_pressed(3)
                    if mouse_button_state[0] == True:
                        mouse_hold = True
                        mouse_rel = (0, 0)
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_state = pygame.mouse.get_pressed(3)
                    if mouse_button_state[0] == False:
                        mouse_hold = False
                        ##mouse_rel = (0, 0)

                if event.type == pygame.MOUSEWHEEL:
                    mouse_scroll = event.y
                        
                if event.type == pygame.MOUSEMOTION:   
                    if mouse_hold == True:                   
                        mouse_rel = pygame.mouse.get_rel()
                        
                
                        
                        

        if states[0]:
            
            screen.fill(white)
            ##path = os.path.join("pfda-final-project-cube-art\src\placeholder2.png")
            startscreen = pygame.image.load("placeholder.png")
            pygame.transform.scale(startscreen, resolution, screen)
            ##screen.blit(startscreen, (0, 0))
        if states[1]:
            
            CubeControl(cube, resolution, mouse_rel, mouse_scroll)
            if pygame.mouse.get_rel() == (0, 0) and mouse_hold:
                mouse_rel = (0, 0)

            screen.fill(white)
            cube.update()
            cube.draw_cube(screen)
            mouse_scroll = 0

        if states[2]:
            screen.fill(white)

            cubeTrail.update(dt)
            cubeTrail.draw(screen)
        
        if states[3]:
            screen.fill(white)
            plane1.update(dt)
            plane1.draw(screen)
            
        """              
        print(f"state {states}")
        screen.fill(white)
        if start == True:
            ##start = True
            screen.fill(white)
            ##print("In start")
            ##path = os.path.join("pfda-final-project-cube-art\src\placeholder2.png")
            startscreen = pygame.image.load("placeholder.png")
            pygame.transform.scale(startscreen, resolution, screen)
            ##screen.blit(startscreen, (0, 0))
        
        if run0 == True:
            screen.fill(white)

        if run1 == True:
            screen.fill(white)

            cube.update()
            cube.draw_cube(screen)


        if run2 == True:
            screen.fill(white)

            cubeTrail.update(dt)

            cubeTrail.draw(screen)

        if run3 == True:
            screen.fill(white)
            plane1.update()
            plane1.draw()
            
        pygame.display.flip()
        
        if run4 == True:
            screen.fill(white)
            
        start = states[0]
        run1 = states[1]
        run3 = states[2]
        """
        
        """
        plane1.update(dt)
        plane1.draw(screen)
        points.update(dt, screen)
        """

        ##cube.update()
        ##cube.draw_cube(screen)

        ##pygame.draw.circle(screen, (0,0,0), (50,50), 50)

        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
    pygame.quit()
    print("Exiting program...")

def change_state(state):
    for idx, cond in enumerate(state):
        state[idx] = False

def CubeControl(cube, resolution, pos_diff, scroll):
    
    x = -180 * (pos_diff[1])/ resolution[1]
    y = 180 * (pos_diff[0])/ resolution[0]
    z = 180 * 0

    cube.angle[0] += x
    cube.angle[1] += y
    cube.angle[2] += z

    ##cube.size += scroll

if __name__ == "__main__":
    main()