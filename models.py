from manim import *

import numpy as np
import pymunk as pk

class Stick(VGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = {
            'pos': ORIGIN,
            'length': 1,
            'angle': 0,
            'width':10,
            'color':WHITE,
            
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self.add(Line(self.config['pos']+self.config['length']*RIGHT,
                      self.config['pos'],
                      stroke_width=self.config['width'], color=self.config['color']))
        self.radius = self.config['length']/10
        
        self.add(Circle(radius=self.radius, color=self.config['color'], fill_opacity=0).move_to(
            self.config['pos']-self.radius*RIGHT))
        self.add(Circle(radius=self.radius, color=self.config['color'], fill_opacity=0).move_to(
            self.config['pos'] + (self.config['length'] + self.radius)*RIGHT))

        self.rotate(self.config['angle'], about_point=self.config['pos'])

class StickNumBase(VGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = {
            'pos': ORIGIN,
            'size': 2,
            'stick_width':10,
            'color':WHITE,
            'margin':0.2,
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                
        m = self.config['margin']
        s = self.config['size']
        self.radius = self.config['size']/40
        
        ps = [
            self.config['pos']+np.array([-s/4,2*m+s/2+self.radius,0]),
            self.config['pos']+np.array([s/4+m,m,0]),
            self.config['pos']+np.array([s/4+m,-m,0]),
            self.config['pos']+np.array([-s/4,-2*m-s/2-self.radius,0]),
            self.config['pos']+np.array([-s/4-m,-m,0]),
            self.config['pos']+np.array([-s/4-m,m,0]),
            self.config['pos']+np.array([-s/4,0,0]),
        ]
        a_s = [
            0,
            np.pi/2,
            -np.pi/2,
            0,
            -np.pi/2,
            np.pi/2,
            0
        ]
        for p, a in zip(ps, a_s):
            s_ = Stick(pos=p, length=s/2,
                      width=self.config['stick_width'], color=self.config['color'], angle=a)
            self.add(s_)
        
        self.lookup = {
            '1':[1,2],
            '2':[0,1,6,4,3],
            '3':[0,1,6,2,3],
            '4':[5,6,1,2],
            '5':[0,5,6,2,3],
            '6':[0,5,6,2,3,4],
            '7':[0,1,2],
            '8':list(range(7)),
            '9':[0,1,2,3,5,6],
            '0':list(range(6))
        }

      
class LineEnvelope(VGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = {
            'background_color': BLACK,
            'circle_color': PINK,
            'line_color': RED,
            'line_width': 2,
            'node_num':20,
            'node_color': PINK,
            'node_radius': 0.03,
            'circle_radius':3.4,
            'position': ORIGIN,
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self.create_circle_node()
        self.create_line()
            
    def create_circle_node(self):
        self.circle = Circle(radius=self.config['circle_radius'], color=self.config['circle_color'], 
                             stroke_width=2*self.config['line_width']).move_to(self.config['position'])
        self.nodes = VGroup()
        d_a = np.pi*2/self.config['node_num']
        # for i in np.roll(range(self.config['node_num']), self.config['node_num']//4):
        for i in range(self.config['node_num']):
            p = np.array([-np.sin(d_a * (i + 1) + np.pi), np.cos(d_a * (i + 1) + np.pi), 0]) * self.config['circle_radius']
            node = Circle(radius=self.config['node_radius'],
                          color=self.config['node_color'],
                          fill_color=self.config['node_color'],
                          fill_opacity=1).move_to(self.circle.get_center() + p)
            self.nodes.add(node)

            
    def create_line(self):
        for i in range(1, self.config['node_num']+1):
            line = Line(self.nodes[i-1].get_center(),
                        self.nodes[(2 * i - 1)%self.config['node_num']].get_center(),
                        color=self.config['line_color'], stroke_width=self.config['line_width'])
            self.add(line)
    
    def get_heart_points(self):
        self.heat_points = []
        for i in range(self.config['node_num']-2):
            self.heat_points.append(line_intersection([self[i].get_start(),self[i].get_end()],
                                                      [self[i+1].get_start(),self[i+1].get_end()]))
        return self.heat_points


class CircleEnvelope(VGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = {
            'background_color':BLACK,
            'circle_color':PINK,
            'circle_num':36,
            'circle_radius':1.5,
            'circle_width':2,
            'position': UP,
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        self.create_base_circle()
        self.create_circles()
                
    def create_base_circle(self):
        self.base_circle = Circle(radius=self.config['circle_radius'],
                                  color=WHITE,
                                  stroke_width=self.config['circle_width']).move_to(self.config['position'])
    def create_circles(self):
        d_a = np.pi*2/self.config['circle_num']
        v0 = UP * self.config['circle_radius']
        
        for i in range(self.config['circle_num']):
            vi = np.array([-np.sin(d_a * (i+1)), np.cos(d_a * (i+1)), 0]) * self.config['circle_radius']
            circle = Circle(radius=np.sqrt(sum((vi-v0) ** 2)),
                            color=self.config['circle_color'],
                            stroke_width=self.config['circle_width']).move_to(self.base_circle.get_center() + vi)
            self.add(circle)

class Tree(VGroup):
    def __init__(self, base_mob=None, **kwargs):
        super().__init__()
        self.config = {
            'background_color': BLACK,
            'base_branch': (DOWN * 3, DOWN),
            'derived_branch': [(DOWN, LEFT), (DOWN, RIGHT)],
            'layer_num': 8,
        }
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
        
        self.base_mob = base_mob if base_mob!=None else Line(self.config['base_branch'][0], self.config['base_branch'][1], stroke_width=20)
        self.create_tree()
        
    def create_tree(self, change_stroke=True):
        old_points = self.config['base_branch']
        self.add(self.base_mob.copy())
        for i in range(self.config['layer_num']):
            layer_i = VGroup()
            for new_points in self.config['derived_branch']:
                layer_i.add(self.generate_new_branch(self[-1], old_points, new_points))
            if change_stroke:
                layer_i.set_stroke(width=self.base_mob.get_stroke_width() * 1.35 ** (-i) + 0.5)
            self.add(layer_i)
        return self
    
    def generate_new_branch(self, mob, old_points, new_points):
        old_vect, new_vect = old_points[1] - old_points[0], new_points[1] - new_points[0]
        old_angle, new_angle = np.angle(complex(*old_vect[:2])), np.angle(complex(*new_vect[:2]))
        mob_new = mob.copy().shift(new_points[0] - old_points[0])\
            .rotate(new_angle-old_angle, about_point=new_points[0])\
            .scale(abs(complex(*new_vect[:2]))/(abs(complex(*old_vect[:2]))+1e-6), about_point=new_points[0])
        return mob_new
    
    
class PhysicsBody(Animation):
    def __init__(self, mobject, pos, rot, **kwargs):
        super().__init__(mobject, rate_func='linear',)
        self.run_nums = len(pos) - 1
        self.pos = pos
        self.rot = rot
        self.angle = self.rot[0]
        mobject.rotate(self.angle)
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        pos = self.pos[int(self.run_nums * alpha)]
        rot = self.rot[int(self.run_nums * alpha)]
        # x, y = pos
        # self.mobject.move_to(np.array([x, y, 0]))
        self.mobject.move_to(pos)
        
        self.mobject.rotate(rot - self.angle)
        self.angle = rot


def manim2pymunk(p):
    return [(p[0] + 7)*100, (p[1]-4)*100]

def pymunk2manim(p):
    return [(p[0] - 700)/100, (p[1] + 400)/100, 0]

if __name__ == "__main__":
    mode = 'pygame'
    if mode == 'pygame':
        le = LineEnvelope(node_num=60)
        ps = le.get_heart_points()
        
        # pymunk test
        space = pk.Space()
        space.gravity = (0, 1000)
        # ground
        for i in range(len(ps)-1):
            p1 = manim2pymunk(ps[i])
            p2 = manim2pymunk(ps[i+1])
            seg = pk.Segment(space.static_body, p1, p2, 2)
            seg.friction = 0.5
            seg.elasticity = 1
            space.add(seg)
        # balls
        balls = []
        
        for x in range(2):
            mass = 1
            moment = pk.moment_for_circle(mass, 0, 20)
            body = pk.Body(mass, moment)
            
            body.position = 400, 0
            shape = pk.Circle(body, 20)
            shape.friction = 0.5
            shape.elasticity = 0.95
            space.add(body, shape)
            balls.append(body)
        
        import pygame
        import pymunk.pygame_util as pkg    
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        draw_options = pkg.DrawOptions(screen)
        # pkg.positive_y_is_up = True
        fps = 60
        running = True
        while running:
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and (event.key in [pygame.K_ESCAPE, pygame.K_q])
                ):
                    
                    running = False
            
            screen.fill(pygame.Color("white"))
            space.debug_draw(draw_options)
            pygame.display.update()
            clock.tick(fps)
            space.step(1.0 / fps)
        pygame.quit()
    elif mode == 'manim':
        import os
        os.system("manim {} TestScene".format(__file__))