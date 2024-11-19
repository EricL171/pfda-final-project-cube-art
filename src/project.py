import random
import os
import pygame
import numpy
import math

class Cube():
    def __init__(self, pos, size, rotation_age):
        self.size = size
        self.pos = pos
        self.age = 0
        self.angle = rotation_age

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
        
        self.rotate_x(angle * math.pi / 180)
        self.rotate_y(45    * math.pi / 180)
        self.rotate_z(45     * math.pi / 180)
    
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
        surface.blit(self.surface, (self.pos[0] - math.sqrt(3) * self.size, self.pos[1] - math.sqrt(3) * self.size))
        ##surface.blit(self.surface, (self.pos[0], self.pos[1]))

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

        self.surface = pygame.Surface((2 * math.sqrt(3) * self.size, 2 * math.sqrt(3) * self.size))
        self.surface.set_colorkey((255, 255, 255))

        self.projection_matrix = numpy.matrix([[1, 0, 0], [0, 1, 0], [0,0,0]])

        self.vert_pos = [math.sqrt(3) * self.size, math.sqrt(3) * self.size]
        
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
         
        pygame.draw.circle(self.surface, (0,0,0), (self.projected_points[0][0], self.projected_points[0][1]), 5)
        pygame.draw.circle(self.surface, (255,0,0), (self.projected_points[1][0], self.projected_points[1][1]), 5)
        pygame.draw.circle(self.surface, (0,255,0), (self.projected_points[2][0], self.projected_points[2][1]), 5)
        pygame.draw.circle(self.surface, (0,0,255), (self.projected_points[3][0], self.projected_points[3][1]), 5)

        surface.blit(self.surface, (self.pos[0] - math.sqrt(2) * self.size, self.pos[1] - math.sqrt(2) * self.size))

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
        self.cubes = []

        self.skip = 0
        self.create_cascade()

    def update(self, dt):
        ##if self.skip % 120 == 0:
        ##self.create_new_cube()

        self.skip += 1

        for cube in self.cubes:
            cube.update()
            ##cube.angle += 1
            
            self.univ_angle = cube.angle
            ##self.size_change()
                
    def create_cascade(self):

        cube = Plane(pos = [self.length * 0.8, self.width * 0.2], size=50, rotation = [90, 0, 0])
        self.cubes.insert(0, cube)

        cube = Plane(pos = [self.length * 0.7, self.width * 0.3], size=50, rotation = [85, 10, 0])
        self.cubes.insert(0, cube)

        cube = Plane(pos = [self.length * 0.6, self.width * 0.4], size=50, rotation = [20, 0, 0])
        self.cubes.insert(0, cube)

    def draw(self, surface):
        for cube in self.cubes:
            cube.draw(surface)
            
class CubeGrid():
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
        
        buffer = 2 * math.sqrt(3) * self.size
        count_x = 0
        count_y = 0
        while (count_x * buffer ) < self.length : 
            while (count_y * buffer) < self.width :
                cube = Cube(pos = [count_x * buffer, count_y * buffer], size=self.size, rotation_age = self.univ_angle)
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

def main():
    pygame.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    ##resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)

    angle = 0
    cubeTrail = CubeGrid(200, 50, 0, resolution)
    ##cube = Cube([150, 150], 50)
    plane1 = PlaneCascade(resolution)

    white = pygame.Color(255, 255, 255)
    running = True
    start = True
    run1 = False
    run3 = False
    states = [start, run1, run3]

    ##surface = pygame.Surface((size=resolution, flags=0, depth=0, display=0, vsync=0))

    while running:

        pygame.key.set_repeat(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   running = False
                match event.key:
                    case pygame.K_1:
                        change_state(states)
                        states[1] = True

                    case pygame.K_2:
                        change_state(states)
                        states[0] = True

                    case pygame.K_3:
                        change_state(states)
                        states[2] = True

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
        
        if run1 == True:
            screen.fill(white)

            cubeTrail.update(dt)

            cubeTrail.draw(screen)

        if run3 == True:
            screen.fill(white)
            plane1.update()
            plane1.draw()
        pygame.display.flip()
        
        start = states[0]
        run1 = states[1]
        run3 = states[2]
        """
        screen.fill(white)
        plane1.update(dt)
        plane1.draw(screen)


        dt = clock.tick(60)
        pygame.display.update()
    pygame.quit()

def change_state(state):
    for idx, cond in enumerate(state):
        state[idx] = False


if __name__ == "__main__":
    main()