import pygame
import pymunk
import pymunk.pygame_util
import math


class Environment:
    def __init__(self, game_state, radius):
        self.players_positions = game_state[0]
        self.players_shapes = []
        self.opponent_shapes = []
        self.opponents_positions = game_state[1]
        self.ball_position = (game_state[2][0][0] + game_state[5][0], game_state[2][0][1] + game_state[5][1])
        self.player_goal_position = game_state[3]
        self.opponent_goal_position = game_state[4]
        self.playground = game_state[5]
        self.space = None
        self.static_body = None
        self.walls_elasticity = 0.8
        self.walls_thickness = 5
        self.max_force = 1600
        self.radius = radius
        self.soccer_ball_shape = None
        self.player_goal_criteria = self.opponent_goal_position[0]
        self.opponent_goal_criteria = self.player_goal_position[0] + self.player_goal_position[2]

    def initialize_space(self):
        self.space = pymunk.Space()
        self.static_body = self.space.static_body

    def create_walls(self):
        static_lines = [pymunk.Segment(self.static_body, (self.playground[0], self.playground[1]),
                                       (self.playground[0] + self.playground[2], self.playground[1]), self.walls_thickness),  # 1
                        pymunk.Segment(self.static_body, (self.playground[0], self.playground[1] + self.playground[3]),
                                       (self.playground[0] + self.playground[2], self.playground[1] + self.playground[3]), self.walls_thickness),  # 2
                        pymunk.Segment(self.static_body, (self.playground[0], self.playground[1]),
                                       (self.playground[0], self.player_goal_position[1]),
                                       self.walls_thickness),  # 3
                        pymunk.Segment(self.static_body,
                                       (self.playground[0], self.player_goal_position[1] + self.player_goal_position[3]),
                                       (self.playground[0], self.playground[1] + self.playground[3]), self.walls_thickness),  # 4
                        pymunk.Segment(self.static_body, (self.playground[0] + self.playground[2], self.playground[1]),
                                       (self.playground[0] + self.playground[2], self.opponent_goal_position[1]), self.walls_thickness),  # 5
                        pymunk.Segment(self.static_body,
                                       (self.playground[0] + self.playground[2], self.playground[1] + self.playground[3]),
                                       (self.playground[0] + self.playground[2], self.opponent_goal_position[1] + self.opponent_goal_position[3]), self.walls_thickness),  # 6
                        pymunk.Segment(self.static_body,
                                       (self.player_goal_position[0], self.player_goal_position[1]),
                                       (self.player_goal_position[0], self.player_goal_position[1] + self.player_goal_position[3]),
                                       self.walls_thickness),  # 7
                        pymunk.Segment(self.static_body,
                                       (self.opponent_goal_position[0] + self.opponent_goal_position[2], self.opponent_goal_position[1]),
                                       (self.opponent_goal_position[0] + self.opponent_goal_position[2],
                                        self.opponent_goal_position[1] + self.opponent_goal_position[3]),
                                       self.walls_thickness),  # 8
                        pymunk.Segment(self.static_body,
                                       (self.playground[0], self.player_goal_position[1]),
                                       (self.player_goal_position[0], self.player_goal_position[1]),
                                       self.walls_thickness),  # 9
                        pymunk.Segment(self.static_body,
                                       (self.player_goal_position[0], self.player_goal_position[1] + self.player_goal_position[3]),
                                       (self.playground[0],
                                        self.player_goal_position[1] + self.player_goal_position[3]),
                                       self.walls_thickness),  # 10
                        pymunk.Segment(self.static_body,
                                       (self.opponent_goal_position[0], self.opponent_goal_position[1]),
                                       (self.opponent_goal_position[0] + self.opponent_goal_position[2],
                                        self.opponent_goal_position[1]),
                                       self.walls_thickness),  # 11
                        pymunk.Segment(self.static_body,
                                       (self.opponent_goal_position[0], self.opponent_goal_position[1] + self.opponent_goal_position[3]),
                                       (self.opponent_goal_position[0] + self.opponent_goal_position[2],
                                        self.opponent_goal_position[1] + self.opponent_goal_position[3]),
                                       self.walls_thickness)  # 12
                        ]
        for line in static_lines:
            line.elasticity = self.walls_elasticity
            self.space.add(line)

    def create_soccer_ball(self, radius=10, mass=10, elasticity=0.8, color=(255, 255, 255, 255)):
        moment = pymunk.moment_for_circle(mass, 0, radius, (0, 0))

        soccer_ball_body = pymunk.Body(mass, moment)
        self.soccer_ball_shape = pymunk.Circle(soccer_ball_body, radius)

        self.soccer_ball_shape.elasticity = elasticity
        soccer_ball_body.position = self.ball_position
        self.soccer_ball_shape.color = color

        pivot = pymunk.PivotJoint(self.static_body, soccer_ball_body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = self.max_force

        self.space.add(soccer_ball_body, self.soccer_ball_shape, pivot)

        return self.soccer_ball_shape

    def create_soccer_players(self, player_position, color, mass=20, elasticity=0.8):
        moment = pymunk.moment_for_circle(mass, 0, self.radius, (0, 0))

        soccer_player_body = pymunk.Body(mass, moment)
        soccer_player_shape = pymunk.Circle(soccer_player_body, self.radius)

        soccer_player_shape.elasticity = elasticity
        soccer_player_body.position = player_position
        soccer_player_shape.color = color

        pivot = pymunk.PivotJoint(self.static_body, soccer_player_body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = self.max_force

        self.space.add(soccer_player_body, soccer_player_shape, pivot)

        return soccer_player_shape

    def create_teams(self):
        for player_position in self.players_positions:
            player_shape = self.create_soccer_players(player_position, (255, 0, 0, 255))
            self.players_shapes.append(player_shape)

        for opponent_position in self.opponents_positions:
            opponent_shape = self.create_soccer_players(opponent_position, (0, 0, 255, 255))
            self.opponent_shapes.append(opponent_shape)

    @staticmethod
    def shoot(player_shape, angle, force):
        x_impulse = math.cos(math.radians(angle))
        y_impulse = math.sin(math.radians(angle))
        player_shape.body.apply_impulse_at_local_point((force * x_impulse, force * -y_impulse), (0, 0))

    def check_player_goal_scored(self):
        object_x, object_y = self.soccer_ball_shape.body.position

        # Check if the ball's position is within the gate coordinates
        if object_x >= self.player_goal_criteria:
            print("Player GOAL!!")
            return True

        return False

    def check_opponent_goal_scored(self):
        object_x, object_y = self.soccer_ball_shape.body.position

        # Check if the ball's position is within the gate coordinates
        if object_x <= self.opponent_goal_criteria:
            print("Opponent GOAL!!")
            return True

        return False

    def check_objects_stopped(self):
        # check if all the objects have stopped moving
        get_state = True
        objects = self.players_shapes + self.opponent_shapes
        for obj in objects:
            if int(obj.body.velocity[0]) != 0 or int(obj.body.velocity[1]) != 0:
                get_state = False

        if int(self.soccer_ball_shape.body.velocity[0]) != 0 or int(self.soccer_ball_shape.body.velocity[1]) != 0:
            get_state = False

        return get_state

    def visualize(self, player_id, degree, force):

        # Initialize the pygame window
        width, height = self.playground[2] + 2 * self.playground[0], self.playground[3] + 2 * self.playground[1]
        FPS = 120
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Soccer Stars")
        clock = pygame.time.Clock()

        draw_options = pymunk.pygame_util.DrawOptions(screen)

        running = True

        while running:
            self.check_player_goal_scored()
            self.check_opponent_goal_scored()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Environment.shoot(self.players_shapes[player_id], degree, force)
                if event.type == pygame.QUIT:
                    running = False

            # if self.check_objects_stopped():
            #     for i in self.opponent_shapes:
            #         print(i.body.position)

            screen.fill((0, 255, 0))

            # Step the physics simulation
            dt = 1.0 / FPS
            self.space.step(dt)

            self.space.debug_draw(draw_options)
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    @staticmethod
    def capture_screenshot(space, width, height, file_name):
        # Create a surface to capture the screenshot
        screen_surface = pygame.Surface((width, height))

        # Set up the draw options
        draw_options = pymunk.pygame_util.DrawOptions(screen_surface)
        screen_surface.fill((0, 255, 0))

        # Step the physics simulation
        dt = 1.0 / 120
        space.step(dt)

        # Draw the Pymunk debug drawing onto the surface
        space.debug_draw(draw_options)

        # Save the screenshot
        pygame.image.save(screen_surface, file_name)

    def simulate(self):
        self.initialize_space()
        self.create_soccer_ball()
        self.create_walls()
        self.create_teams()
