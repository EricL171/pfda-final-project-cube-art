import pygame
import numpy
import math

class Cube():
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos
        self.age = 0
        self.angle = self.age

        self.root_verts = []
        self.assign_root_verts()

        self.surface = pygame.Surface((2 * math.sqrt(3) * self.size, 2 * math.sqrt(3) * self.size))
        ##self.surface.set_colorkey((255, 255, 255))

        self.projection_matrix = numpy.matrix([[1, 0, 0], [0, 1, 0], [0,0,0]])

        self.vert_pos = [math.sqrt(3) * self.size, math.sqrt(3) * self.size]
        
        self.projected_points = []
        for i in range(len(self.root_verts)):
            self.projected_points.append([i,0])

        ##print(f"Projection {self.projected_points}")

    def update(self):
        """
        https://en.wikipedia.org/wiki/Projection_(linear_algebra)
        Projection will need the dot product of the rotation matrices representing yaw(x), pitch(y), and roll(z) into
        the general rotation matrix rmatrix_xyz. The position of the vertices in 2d will be the dot product of
        the general rotation matrix and the projection matrix
        Numpy will be used to help handle matrix operations with dot product method.
        For clarity purposes, all rotation matrices are named as matrices and are not related to coding matrices or arrays.
        """
        self.calc_rotation(self.angle)
        ##print(f"{self.angle}")

        i = 0
        for point in self.root_verts:
            
            rmatrix_xyz = numpy.dot(self.rmatrix_z, point.reshape((3, 1)))
            rmatrix_xyz = numpy.dot(self.rmatrix_y, rmatrix_xyz)
            rmatrix_xyz = numpy.dot(self.rmatrix_x, rmatrix_xyz)

            ##print(f"General rotation matrix: {rmatrix_xyz}")
            points_2d = numpy.dot(self.projection_matrix, rmatrix_xyz)
            ##print(f"{points_2d[0][0]}")
            ##print(f"Points 2d matrix: {points_2d}")

            
            ##print(f"points {points_2d[0][0]}")
            x = int(points_2d[0][0].item() * self.size) + self.vert_pos[0]
            y = int(points_2d[1][0].item() * self.size) + self.vert_pos[1]
            
            ##print(f"x {x}, y {y}, x_1 {x_1}, y_1 {y_1}")

            self.projected_points[i] = [x, y]
            i += 1
        self.angle += 0.001
        self.age += 0.001

    def calc_rotation(self, angle):

        """
        From https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematics_for_Game_Developers_(Burzynski)/04%3A_Matrices/4.06%3A_Rotation_Matrices_in_3-Dimensions
        Rotation matrices must be defined.
        """
        
        self.rotate_x(angle)
        self.rotate_y(angle)
        self.rotate_z(angle)

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
                    print(f"{self.root_verts}")

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

        ##for n in range(4):
            
        corner_index = 0
        corners = [0, 3, 5, 6]
        adj_edges = [1, 2, 4, 7]
        j = 0

        for i in range(4):
            self.create_edge((255, 0, 0), corners[i], adj_edges[j  % 4])
            j += 1
            
            self.create_edge((0, 255, 0), corners[i], adj_edges[j  % 4])
            j+= 1
            
            self.create_edge((0, 0, 255), corners[i], adj_edges[j  % 4])
            j += 1
        
        surface.blit(self.surface, (self.pos[0] - math.sqrt(3) * self.size, self.pos[1] - math.sqrt(3) * self.size))
        ##surface.blit(self.surface, (self.pos[0], self.pos[1]))




def main():
    pygame.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)


    cube = Cube(100, [150, 150])
    white = pygame.Color(255, 255, 255)
    running = True
    while running:

        pygame.key.set_repeat(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   running = False

        ##rain.update(dt)
        cube.update()

        screen.fill(white)
        ##rain.draw(screen)
        cube.draw_cube(screen)
        pygame.display.flip()

        dt = clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()