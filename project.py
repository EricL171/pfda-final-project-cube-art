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

        self.surface = pygame.Surface((self.size, self.size))
        self.surface.set_colorkey((255, 255, 255))

        self.projection_matrix = numpy.matrix([[1, 0, 0], [0, 1, 0], [0,0,0]])

        self.vert_pos = [self.size, self.size]
        self.projected_points = []

    def update(self):
        """
        https://en.wikipedia.org/wiki/Projection_(linear_algebra)
        Projection will need the dot product of the rotation matrices representing yaw(x), pitch(y), and roll(z) into
        the general rotation matrix rmatrix_xyz. The position of the vertices in 2d will be the dot product of
        the general rotation matrix and the projection matrix
        Numpy will be used to help handle matrix operations with dot product method.
        """
        self.calc_rotation(self.angle)


        for point in self.root_verts:
            
            rmatrix_xyz = numpy.dot(self.rmatrix_z, point.reshape((3, 1)))
            rmatrix_xyz = numpy.dot(self.rmatrix_y, rmatrix_xyz)
            rmatrix_xyz = numpy.dot(self.rmatrix_x, rmatrix_xyz)

            print(f"General rotation matrix: {rmatrix_xyz}")
            points_2d = numpy.dot(self.projection_matrix, rmatrix_xyz)
            print(f"Points 2d matrix: {points_2d}")

        self.angle += 0.001
        self.age += 0.001

    def calc_rotation(self, angle):

        """
        From https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematics_for_Game_Developers_(Burzynski)/04%3A_Matrices/4.06%3A_Rotation_Matrices_in_3-Dimensions
        Rotation matrices must be defined.
        """
        self.r_mod = [math.sin(angle), math.cos(angle)]

        ##Gamma, yaw
        self.rmatrix_x = numpy.matrix([
            [1,             0,              0],
            [0, self.r_mod[1], -self.r_mod[0]],
            [0, self.r_mod[0], self.r_mod[1]],
        ])

        ##Beta, pitch
        self.rmatrix_y = numpy.matrix([
            [self.r_mod[1],  0, self.r_mod[0]],
            [0,              1,             0],
            [-self.r_mod[0], 0, self.r_mod[1]],
        ])
        
        ##Alpha, roll
        self.rmatrix_z = numpy.matrix([
            [self.r_mod[1], -self.r_mod[0], 0],
            [self.r_mod[0], self.r_mod[1],  0],
            [0,                         0,  1],
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

    def draw_cube(self):
        self.surface.fill((255,255,255))


def main():
    pygame.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)


    cube = Cube(100, 100)
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

        pygame.display.flip()

        dt = clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()