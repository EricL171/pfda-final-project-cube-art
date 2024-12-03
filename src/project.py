import random
import os
import pygame
import numpy
import math

class Cube():
    def __init__(self, pos, size, start_rotation):
        self.size = size
        self.pos = list(pos)
        self.age = 0
        self.angle = list(start_rotation)
        self.enable_shade = False

        self.corners = []
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

        self.corners = []
        for idx in range(len(self.projected_points)):
            self.corners.append((self.projected_points[idx][0], self.projected_points[idx][1]))
        
        draw_corners = [0, 3, 5, 6]
        adj_edges = [1, 2, 4, 7]
        j = 0

        for i in range(4):
            for n in range(3):
                self.create_edge((0, 0, 0), draw_corners[i], adj_edges[j  % 4])
                j += 1

        if self.enable_shade:
            self.shade_cube()
        surface.blit(self.surface, (self.pos[0] - math.sqrt(3) * self.size, self.pos[1] - math.sqrt(3) * self.size))
        ##surface.blit(self.surface, (self.pos[0], self.pos[1]))

    def shade_cube(self):
        face1 = [self.corners[0], self.corners[1], self.corners[3], self.corners[2]]
        face2 = [self.corners[0], self.corners[4], self.corners[6], self.corners[2]]
        face3 = [self.corners[2], self.corners[3], self.corners[7], self.corners[6]]

        face5 = [self.corners[4], self.corners[5], self.corners[7], self.corners[6]]
        face6 = [self.corners[1], self.corners[5], self.corners[7], self.corners[3]]
        face7 = [self.corners[0], self.corners[1], self.corners[5], self.corners[4]]

        faces = [face1, face2, face3, face5, face6, face7]
        face = []

        j = 0
        for i in range(len(faces)):
            ##pygame.draw.polygon(self.surface, (255,255/6 * i,255/6 * i), faces[i])
            pygame.draw.polygon(self.surface, (255/(i+1),255/(i+1),255), faces[i])

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

class CubeCascade():
    def __init__(self, resolution):
        
        self.length = resolution[0]
        self.width = resolution[1]
        self.origin = (self.length/2, self.width/2)
        self.mouse_rel = 0
        self.cubes = []

        self.skip = 0
        self.xpos = []
        self.ypos = []
        self.rotations = []
        self.sizes = []
        self.start_size = 50
        self.univ_angle = (0, 0, 0)

        self.casc_length = 20

        for l in range(self.casc_length):
            cube = Cube(pos = (self.length/2, self.width/2), size= l * (self.start_size/self.casc_length), start_rotation = self.univ_angle)
            self.cubes.append(cube)

    def update(self, dt, mouse_pos, mouse_rel):
        
        ##self.casc_length += 1
        self.mouse_x = mouse_pos[0]
        self.mouse_y = mouse_pos[1]
        self.mouse_rel = mouse_rel

        for cube in self.cubes:
            cube.update()
            
            self.univ_angle = cube.angle
            ##self.size_change()
        
        self.calc_transforms(self.mouse_x, self.mouse_y)
    
    def calc_transforms(self, x_pos,y_pos):
        mid = int(self.casc_length/2)
        mag_x = self.origin[0] - x_pos
        mag_y = self.origin[1] - y_pos
        
        idx = 0
        for cube in self.cubes:
            
            if idx == mid:
                pass
            else:
                cube.pos[0] = self.origin[0] + (mid-idx) * mag_x/5
                cube.pos[1] = self.origin[1] + (mid-idx) * mag_y/5
        
            
            CubeControl(cube, (self.length, self.width), self.mouse_rel, 0)
            idx += 1

    
    def draw_line(self, surface):
        self.line_surf = pygame.Surface((self.length, self.width))
        self.line_surf.set_colorkey((255, 255, 255))

        self.line_surf.fill((255,255,255))
        pygame.draw.line(self.line_surf, (0,0,0), self.origin, (self.mouse_x, self.mouse_y))
        surface.blit(self.line_surf, (0,0))
        


    def draw(self, surface):
        for cube in self.cubes:
            cube.draw_cube(surface)
            ##self.draw_line(surface)
        
class PlaneTrail():
    def __init__(self, resolution, pos, size):
        
        self.length = resolution[0]
        self.width = resolution[1]
        self.pos = pos
        self.planes = []
        self.size = size

        self.skip = 0
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.rotations = []
        self.sizes = []
        self.start_size = size

        self.side = random.randrange(-1, 2, 2)
        self.y_vel = -self.size / 10
        self.accel = 2

    def update(self, dt):
        
        if self._trail_is_offscreen() != True:
            plane = Plane(pos = (self.x, self.y), size= self.size , rotation = (0, 0, 0))
            self.planes.insert(0, plane)
            self._update_trail(dt)
            self._update_pos(dt)
            ##print("Trail is running")
    
    def _update_trail(self, dt):
        for idx, plane in enumerate(self.planes):
            plane.update()
    
    def _update_pos(self,dt):    
        self.pos = self.calc_new_pos(dt)

    def calc_new_pos(self, dt):
        self.x += self.side * self.size / 10

        self.y = self.y + self.y_vel
        self.y_vel = self.y_vel + self.accel
        
        if (self.y+ self.size) > self.width:
            self.y_vel = self.y_vel * -1 * 0.8
            self.y_vel += self.accel
            self.y = self.width - self.size
        
    def draw(self, surface):
        ##for plane in self.planes:
            ##plane.draw(surface)
        self.planes[0].draw(surface)

    def _trail_is_offscreen(self):

        trail_is_offscreen = False
        
        if self.x > self.length or self.x < 0:
            trail_is_offscreen = True
    
        return trail_is_offscreen

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
            cube.enable_shade = True

def main():
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    dbg_msg = False
    resolution = (1200, 800)
    ##resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)

    mouse_pos = (resolution[0]/2, resolution[1]/2)
    mouse_rel = (0,0)
    mouse_rhold = False
    mouse_lhold = False
    mouse_scroll = 0
    mouse_button_state = pygame.mouse.get_pressed(3)

    cube_01 = Cube([resolution[0]/2, resolution[1]/2], 50, (20, 10, 0))
    grid_02 = CubeGrid(200, 50, 0, resolution)
    cube_casc_03 = CubeCascade(resolution)
    plane_trails_04 = []
    
    points = PointGrid(resolution)


    white = pygame.Color(255, 255, 255)
    black = pygame.Color(0, 0, 0)
    running = True
    states = [True, False, False, False, False, False, False, False, False, False]
    enable_grid = False

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
                        change_state(states, screen)
                        states[0] = True
                        if dbg_msg:
                            print(event)

                    case pygame.K_1:
                        change_state(states, screen)
                        states[1] = True
                        if dbg_msg:
                            print(event)

                    case pygame.K_2:
                        change_state(states, screen)
                        states[2] = True
                        if dbg_msg:
                            print(event)

                    case pygame.K_3:
                        change_state(states, screen)
                        states[3] = True
                        if dbg_msg:
                            print(event)
                    
                    case pygame.K_4:
                        change_state(states, screen)
                        states[4] = True
                        if dbg_msg:
                            print(event)

                    case pygame.K_F1:
                        
                        if dbg_msg:
                            dbg_msg = False
                            print("Disabled Debug Messages")
                        else:
                            dbg_msg = True
                            print("Enabled Debug Messages")

                        print(event)
                    
                    case pygame.K_F2:                       
                        print(f"States {states}")

                    case pygame.K_F3:                       
                        if enable_grid:
                            enable_grid = False
                        else:
                            enable_grid = True

                    case _:
                        if dbg_msg:
                            print(event)
                            print("This button does nothing!")
            
            

            if states[1]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button_state = pygame.mouse.get_pressed(3)
                    
                    if mouse_button_state[0] == True:
                        mouse_lhold = True
                        
                    if mouse_button_state[2] == True:
                        mouse_rhold = True
                        mouse_rel = (0, 0)
                    
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_button_state = pygame.mouse.get_pressed(3)
                    if mouse_button_state[0] == False:
                        mouse_rhold = False
                        ##mouse_rel = (0, 0)

                if event.type == pygame.MOUSEWHEEL:
                    mouse_scroll = event.y
                        
                if event.type == pygame.MOUSEMOTION:   
                    if mouse_rhold == True:                   
                        mouse_rel = pygame.mouse.get_rel()
                        

            if states[4]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        plane_trails_04 = []
                        screen.fill(white)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button_state = pygame.mouse.get_pressed(3)
                    if mouse_button_state[0] == True:
                        planeTrail = PlaneTrail(resolution, mouse_pos, 25)
                        plane_trails_04.insert(0, planeTrail)
                        ##plane_trails_04.append()
                             

        if enable_grid:
            points.update(dt, screen)

        """
        if dbg_msg:
            dbg_text = "Debug Mode Enabled"
            dbg_font = pygame.font.SysFont("Courier", 10)  
            dbg_surf = dbg_font.render(dbg_text, False, black)  
            screen.blit(dbg_surf, (5, 10))
        """

        if states[0]:
            
            screen.fill(white)
            ##path = os.path.join("pfda-final-project-cube-art\src\placeholder2.png")
            startscreen = pygame.image.load("placeholder.png")
            pygame.transform.scale(startscreen, resolution, screen)
            ##screen.blit(startscreen, (0, 0))

        if states[1]:
            
            pos_text = "X: " + str(cube_01.angle[0]) + " Y: " + str(cube_01.angle[1]) + " Z: " + str(cube_01.angle[2])
            print(pos_text)
            my_font = pygame.font.SysFont("Courier", 150)  
            text_surf = my_font.render(pos_text, False, black)  

            CubeControl(cube_01, resolution, mouse_rel, mouse_scroll)
            if pygame.mouse.get_rel() == (0, 0) and mouse_rhold:
                mouse_rel = (0, 0)

            screen.fill(white)
            cube_01.update()
            cube_01.draw_cube(screen)

            text_pos = "X: " + str(cube_01.angle[0]) + " Y: " + str(cube_01.angle[1]) + " Z: " + str(cube_01.angle[2])
            my_font = pygame.font.SysFont("Courier", 10)  
            text_surf = my_font.render(text_pos, False, black)  
            screen.blit(text_surf, (5, 10))
            mouse_scroll = 0

        if states[2]:
            screen.fill(white)

            grid_02.update(dt)
            grid_02.draw(screen)
        
        if states[3]:

            mouse_rel = pygame.mouse.get_rel()
            screen.fill(white)
            cube_casc_03.update(dt, mouse_pos, mouse_rel)
            cube_casc_03.draw(screen)
        
        if states[4]:
            ##screen.fill(white)
            for trails in plane_trails_04:
                trails.update(dt)
                trails.draw(screen)
        

        ##cube.update()
        ##cube.draw_cube(screen)

        ##pygame.draw.circle(screen, (0,0,0), (50,50), 50)

        mouse_pos = pygame.mouse.get_pos()
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
    pygame.quit()
    print("Exiting program...")

def change_state(state, screen):
    for idx in range(0, 9):
        state[idx] = False
    screen.fill((255, 255, 255))

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