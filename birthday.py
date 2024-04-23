from manim import *
import numpy as np
import pymunk as pk

from models import *


class MainScene(Scene):
    def play_c_try(self, c, direction=RIGHT):
        self.play(c.animate.shift(direction), run_time=1)
        self.wait(0.2)
        self.play(c.animate.shift(-direction), run_time=0.8)
    
    def play_smile(self, c):
        eye_c = Dot(color=c.color, radius=c.radius/8)
        d = c.radius*0.5
        el = eye_c.copy().move_to(c.get_center()).shift(UP*d + LEFT*d)
        er = eye_c.copy().move_to(c.get_center()).shift(UP*d + RIGHT*d)
        m = Arc(radius=d/2, angle=PI/2, start_angle=-2*PI/3,color=c.color).move_to(c.get_center()).shift(DOWN*d)
        self.play(Create(el), Create(er), Create(m), run_time=1)
        # self.play(Create(m))
        self.wait(0.2)
        self.play(FadeOut(el,er,m))
    
    def play_smile_sunglass(self, c):
        d = c.radius*0.6
        sg = ImageMobject("sun-glasses.png").scale(0.35).move_to(c.get_center()).shift(UP*c.radius*0.2)
        m = Arc(radius=d/2, angle=PI/2, start_angle=-2*PI/3,color=c.color).move_to(c.get_center()).shift(DOWN*d)
        self.play(FadeIn(sg), Create(m), run_time=1)
        self.wait(0.2)
        self.play(FadeOut(sg,m))
    
    
    def create_stick_num(self, num):
        stick = VGroup()
        for ind in self.snb.lookup[str(num)]:
            stick.add(self.snb[ind].copy())
        return stick
    
    def construct(self):
        self.camera.frame_rate = 60
        self.ball_c1 = Circle(radius=0.5, color=RED, fill_opacity=0.4).shift(DOWN * 5)
        self.add(self.ball_c1)
        self.play_c_try(self.ball_c1, UP*1.2)
        self.ball_c1.move_to([-8, 0, 0])
        self.wait(0.2)
        self.play_c_try(self.ball_c1, RIGHT*1.2)
        
        number_line = NumberLine(x_range=[-1, 30, 9], length=14,
                                 include_numbers=True,
                                 include_tip=True,
                                 )
        self.play(self.ball_c1.animate.move_to(number_line.number_to_point(0)), run_time=1)
        self.play(Create(number_line))
        ani = self.ball_c1.animate
        self.play(ani.move_to(number_line.number_to_point(28)), ani.scale(3), run_time=2)
        self.play(ani.move_to(number_line.number_to_point(18)), ani.scale(0.4), run_time=2)
        self.play(FadeOut(number_line))
        self.play_smile(self.ball_c1)

        axes = Axes(x_range=[1, 10], y_range=[0, 1200, 300], x_length=8, y_length=6)

        self.play(Create(axes)) 
        self.play(self.ball_c1.animate.move_to(axes.c2p(3.6, 900)), run_time=1)
        

        func1 = axes.plot(lambda x:x**3+10, color=BLUE)
        func1_label = Text("智慧",color=BLUE).move_to(func1.get_end()).shift(UP*0.5)
        func2 = axes.plot(lambda x:6*x**2+10*x+100, color=YELLOW)
        func2_label = Text("颜值",color=YELLOW).move_to(func2.get_end()).shift(UP*0.5 + RIGHT)
        
        func3 = axes.plot(lambda x:np.exp(x)+50, x_range=(1,7), color=RED)
        func3_label = Text("魅力",color=RED).move_to(func3.get_end()).shift(UP*0.5 + LEFT)
        
        self.play(Create(func1), Write(func1_label))
        self.play(Create(func2), Write(func2_label))
        self.play(Create(func3), Write(func3_label))
        self.play_smile_sunglass(self.ball_c1)
        self.play(FadeOut(func1,func2,func3,func1_label,func2_label,func3_label,axes))
        
        
        self.ball_c2 = Circle(radius=0.66, color=BLUE, fill_opacity=0.4).shift(RIGHT*5 + DOWN * 5)
        self.play(self.ball_c2.animate.shift(UP), run_time=1)
        self.play(self.ball_c2.animate.shift(UP*1.2), run_time=1)
        
        self.play(self.ball_c2.animate.shift(UP*1.2 + LEFT*1.5), self.ball_c1.animate.shift(UP*0.2+LEFT*0.6), run_time=1)
        # show circle-envelope heart
        p1 = self.ball_c1.get_center()
        p2 = self.ball_c2.get_center()
        self.circle_heart = CircleEnvelope(circle_num=36, circle_radius=1, circle_width=2,
                                           position=(p1+p2)/2 + UP*0.4 + LEFT*0.16)
        circle_t = self.ball_c2.copy()
        
        self.add(circle_t)
        self.play(circle_t.animate.shift(UP), run_time=1)
        self.play(circle_t.animate.move_to(self.circle_heart[0].get_center()), run_time=1)
        self.play(ReplacementTransform(circle_t, self.circle_heart[0]), run_time=1)
        for c in self.circle_heart[1:]:
            self.play(Create(c, run_time=0.02))
        # animation n=62

        self.play(Rotate(self.ball_c1, angle=PI*2 + np.arctan2(abs(p1[1]), abs(p1[0])), about_point=self.circle_heart.get_center()),
                  Rotate(self.ball_c2, angle=PI*2 + np.arctan2(abs(p2[1]), abs(p2[0])), about_point=self.circle_heart.get_center()),
                  run_time=2)

        line = Line(self.ball_c2.get_left(), self.ball_c1.get_right(),  stroke_width=6, color=PINK)
        self.play(ReplacementTransform(self.circle_heart, line))
        line.add_updater(lambda x: x.put_start_and_end_on(self.ball_c2.get_left(), self.ball_c1.get_right()))
        self.play(self.ball_c1.animate.move_to([-1,0,0]), self.ball_c2.animate.move_to([1,0,0]), run_time=1)
        self.play(self.ball_c1.animate.move_to([-2,0,0]), self.ball_c2.animate.move_to([2,0,0]), run_time=1)
        

        # STICKs
        self.stick = Stick(pos=[-2,0,0], length=4, width=10, color=RED)
        self.play(ReplacementTransform(VGroup(line, self.ball_c1, self.ball_c2), self.stick))
        self.play(self.stick.animate.shift(UP*1.5), run_time=1)
        self.play(Rotate(self.stick,PI*4), run_time=1)
        
        self.snb = StickNumBase(size=0.96, stick_width=12, color=RED)
        sn_d2 = self.create_stick_num(2)
        sn_d2.move_to([-0.2,2.2,0])
        self.play(ReplacementTransform(self.stick, sn_d2[0]), run_time=1)
        self.play(Write(sn_d2[1:]), run_time=1)
        sn_day = [sn_d2]
        for n in [9,2,2]:
            sn = self.create_stick_num(n).next_to(sn_day[-1], RIGHT)
            # sn = self.create_stick_num(n).move_to(sn_day[-1].get_right() + RIGHT)
            self.play(Write(sn), run_time=1)
            sn_day.append(sn)
        label_days = Text("Days", color=BLUE).next_to(sn_day[-1], RIGHT, aligned_edge=DOWN)
        self.play(Write(label_days))
        
        sn_s0 = self.create_stick_num(0).next_to(sn_day[-1], DOWN).shift(DOWN*1.5)
        # sn_s0.move_to([-6.2,-1,0])
        sn_sec = [sn_s0]
        # self.play(Write(sn_s2))
        for n in [2,5,2,4,6,0,8,0][::-1]:
            sn = self.create_stick_num(n).next_to(sn_sec[-1], LEFT)
            sn_sec.append(sn)
        label_secs = Text("Seconds", color=BLUE).next_to(sn_sec[0], RIGHT, aligned_edge=DOWN)
        self.play(Write(label_secs))
        
        for sn in sn_sec[::-1]:
            self.play(Write(sn), run_time=0.5)
        
        run_time=6
        sn_ts = [sn_sec[0]]
        for t in range(1, run_time):
            sn_t = self.create_stick_num(t).move_to(sn_ts[t-1].get_center())
            self.play(ReplacementTransform(sn_ts[t-1], sn_t), run_time=1)
            sn_ts.append(sn_t)
        
        sn_t = self.create_stick_num(6).move_to(sn_ts[-1].get_center())
        self.play(ReplacementTransform(sn_ts[-1], sn_t),
                  FadeOut(*sn_sec[1:]),
                  FadeOut(*sn_day),
                  FadeOut(label_secs, label_days),
                  run_time=1)
        # create F
        sn_f = VGroup()
        for i in [0,4,5,6]:
            sn_f.add(self.snb[i].copy())
        sn_f.move_to(sn_t.get_center())
        self.play(ReplacementTransform(sn_t, sn_f))
        ani = sn_f.animate
        self.play(ani.set_height(2.25), ani.move_to(2.25 * DOWN))

        layer_num = 6
        colors = color_gradient([RED, GREEN, BLUE], layer_num+1)
        tree = Tree(sn_f, layer_num=layer_num,
                    base_branch=(DOWN * 3.2, DOWN * 1),
                    derived_branch=[(DOWN + RIGHT * 0.06, LEFT * 1 + UP * 0.3), (DOWN + LEFT * 0.06, DOWN * 0.1 + RIGHT * 1.25)])
        for i in range(layer_num+1):
            tree[i].set_color(colors[i])
        for i in range(tree.config['layer_num']):
            self.play(TransformFromCopy(tree[i], tree[i+1]), rate_func=linear, run_time=1 + i ** 0.5 * 0.25)
            self.wait(0.2)
        
        self.play(FadeOut(tree))
        self.play(FadeOut(sn_f[1:]))
        
        self.ball_c1 = Circle(radius=0.5, color=RED, fill_opacity=0.4).scale(3*0.4).move_to(sn_f[0][1].get_center())
        self.ball_c2 = Circle(radius=0.66, color=BLUE, fill_opacity=0.4).move_to(sn_f[0][2].get_center())
        line = Line(self.ball_c2.get_left(), self.ball_c1.get_right(),  stroke_width=6, color=PINK)
        line.add_updater(lambda x: x.put_start_and_end_on(self.ball_c2.get_left(), self.ball_c1.get_right()))
        clc = VGroup(line, self.ball_c1, self.ball_c2)
        self.play(ReplacementTransform(sn_f[0], clc))
        self.play(self.ball_c1.animate.shift(LEFT*1.2, UP*1.6), self.ball_c2.animate.shift(RIGHT*1.2, UP*1.6))
        
        p1 = self.ball_c1.get_center()
        p2 = self.ball_c2.get_center()
        self.line_heart = LineEnvelope(node_num=60, line_color=PINK, line_width=2, position=(p1+p2)*0.5, circle_radius=4)
        # get inverted heart points
        line_heart_rolled = VGroup()
        for i in range(60):
            line_heart_rolled.add(self.line_heart[(i+30)%60])
            
        self.play(line.animate.move_to(line_heart_rolled[0]), run_time=1)
        self.play(ReplacementTransform(line, line_heart_rolled[0]), run_time=1)
        for c in line_heart_rolled[1:]:
            self.play(Create(c, run_time=0.02))

        self.heart_seg = VGroup()
        ps = self.line_heart.get_heart_points()
        for i in range(len(ps)-1):
            self.heart_seg.add(Line(ps[i], ps[i+1], color=PINK, stroke_width=3))

        self.play(self.line_heart.animate.set_opacity(0.2), run_time=0.2)
        self.play(Create(self.heart_seg), run_time=1)
        self.play(FadeOut(self.line_heart), run_time=1)
        
        # add physics via pymunk
        space = pk.Space()
        space.gravity = (0, -260)
        
        line_seg = VGroup()
        lh = Line([-7,-3.5,0], [7,-3.5,0], stroke_width=6, color=WHITE)
        line_seg.add(lh)
        lv1 = Line([-7,-3.5,0], [-7,3.5,0], stroke_width=6, color=WHITE)
        line_seg.add(lv1)
        lv2 = Line([7,-3.5,0], [7,3.5,0], stroke_width=6, color=WHITE)
        line_seg.add(lv2)
        for l in line_seg:
            p1 = manim2pymunk(l.get_start())
            p2 = manim2pymunk(l.get_end())
            seg = pk.Segment(space.static_body, p1, p2, 2)
            seg.friction = 0.5
            seg.elasticity = 1
            space.add(seg)
            
        
        self.play(Rotate(self.heart_seg, PI))
        self.play(Create(line_seg))
        static_seg = []
        for l in self.heart_seg:
            p1 = manim2pymunk(l.get_start())
            p2 = manim2pymunk(l.get_end())
            seg = pk.Segment(space.static_body, p1, p2, 2)
            seg.friction = 0.5
            seg.elasticity = 1
            space.add(seg)
            static_seg.append(seg)
        
        
        mass = 0.8
        moment = pk.moment_for_circle(mass, 0, self.ball_c1.radius*3*0.4*100)
        body_c1 = pk.Body(mass, moment)
        shape_c1 = pk.Circle(body_c1, self.ball_c1.radius*3*0.4*100)
        shape_c1.friction = 0.2
        shape_c1.elasticity = 0.9
        body_c1.position = manim2pymunk(self.ball_c1.get_center())
        space.add(body_c1, shape_c1)
        
        mass = 1.2
        moment = pk.moment_for_circle(mass, 0, self.ball_c2.radius*100)
        body_c2 = pk.Body(mass, moment)
        shape_c2 = pk.Circle(body_c2, self.ball_c2.radius*100)
        shape_c2.friction = 0.2
        shape_c2.elasticity = 0.9
        body_c2.position = manim2pymunk(self.ball_c2.get_center())
        space.add(body_c2, shape_c2)
        
        tex = Text("生 日 快 乐", font_size=100, color=RED).shift(UP*2)
        text_points = tex.get_all_points()

        step = 1 / self.camera.frame_rate
        s_ball_start_f = self.camera.frame_rate
        s_ball_interval = 2
        s_ball_radius = 0.12
        s_ball_num = len(text_points)

        run_frame = len(text_points) * s_ball_interval + s_ball_start_f + 8*self.camera.frame_rate
        remove_static_f = run_frame - 4 * self.camera.frame_rate
        
        shape_c1_pos = np.zeros((int(run_frame), 3))
        shape_c1_angle = np.zeros(int(run_frame))
        shape_c2_pos = np.zeros((int(run_frame), 3))
        shape_c2_angle = np.zeros(int(run_frame))
        shape_balls_pos = np.ones([s_ball_num, int(run_frame), 3])*10
        shape_balls_angle = np.zeros([s_ball_num, int(run_frame)])
        balls = []
        balls_r = []
        p = manim2pymunk(self.heart_seg.get_center())
        for t in range(int(run_frame)):
            space.step(step)
            if (t - s_ball_start_f >= 0) and (len(balls)<s_ball_num) and (t % s_ball_interval == 0):
                mass = 0.2 + np.random.rand()*0.05 - 0.025
                r = s_ball_radius + np.random.rand()*s_ball_radius*0.4 - 0.2*s_ball_radius
                moment = pk.moment_for_circle(mass, 0, r*100)
                body = pk.Body(mass, moment)
                body.position = p[0] + np.random.rand()*12-6, 100 + np.random.rand()*10-20
                shape = pk.Circle(body, r*100)
                shape.friction = 0.3
                shape.elasticity = 0.9
                space.add(body, shape)
                balls.append(body)
                balls_r.append(r)
                
            shape_c1_pos[t] = pymunk2manim(body_c1.position)
            shape_c1_angle[t] = body_c1.angle
            shape_c2_pos[t] = pymunk2manim(body_c2.position)
            shape_c2_angle[t] = body_c2.angle
            for i, b in enumerate(balls):
                shape_balls_pos[i, t] = pymunk2manim(b.position)
                shape_balls_angle[i, t] = b.angle
            if t == remove_static_f:
                for s in static_seg:
                    space.remove(s)
            
        print('finish physic calculation')
        ball_shapes = VGroup()
        for b, r in zip(balls, balls_r):
            p = pymunk2manim(b.position)
            shape = Dot(p, radius=r, color=YELLOW_A)
            ball_shapes.add(shape)
        
        # before remove static
        ani = [PhysicsBody(ball_shapes[i],
                           shape_balls_pos[i][:remove_static_f],
                           shape_balls_angle[i][:remove_static_f]) for i in range(len(ball_shapes))]
        ani += [PhysicsBody(self.ball_c1, shape_c1_pos[:remove_static_f], shape_c1_angle[:remove_static_f]),
                PhysicsBody(self.ball_c2, shape_c2_pos[:remove_static_f], shape_c2_angle[:remove_static_f])]
        self.play(*ani, run_time=remove_static_f/self.camera.frame_rate)
        
        
        self.play(FadeOut(self.heart_seg), run_time=0.2)
        
        # after remove static
        ani = [PhysicsBody(ball_shapes[i],
                           shape_balls_pos[i][remove_static_f:],
                           shape_balls_angle[i][remove_static_f:]) for i in range(len(ball_shapes))]
        ani += [PhysicsBody(self.ball_c1, shape_c1_pos[remove_static_f:], shape_c1_angle[remove_static_f:]),
                PhysicsBody(self.ball_c2, shape_c2_pos[remove_static_f:], shape_c2_angle[remove_static_f:])]
        self.play(*ani, run_time=(run_frame-remove_static_f)/self.camera.frame_rate)

        # move all the balls to the text
        ani = []
        for i, b in enumerate(ball_shapes):
            ani.append(b.animate.move_to(text_points[i]))
        self.play(*ani, run_time=2)
        
        
        self.play(self.ball_c1.animate.move_to(ORIGIN + LEFT*3 + DOWN*1.8),
                  self.ball_c2.animate.move_to(ORIGIN + RIGHT*3 + DOWN*1.8))
        
        # self.play(VGroup(self.ball_c1, self.ball_c2).animate.move_to(ORIGIN + DOWN*2), run_time=1)
        
        bubble = SVGMobject(file_name="chat-bubble2.svg", stroke_width=4, width=2).scale(1.3)
        bubble_b = bubble.copy().flip().next_to(self.ball_c2, UP*0.5).shift(LEFT*self.ball_c2.radius*3)
        bubble_b.set(stroke_color=BLUE)
        text = Text("生日快乐!", font_size=24, color=BLUE).move_to(bubble_b.get_center())
        self.play(FadeIn(bubble_b), run_time=0.5)
        self.play(Write(text), run_time=1)
        
        
        bubble_r = bubble.copy().next_to(self.ball_c1, UP*0.5).shift(RIGHT*self.ball_c1.radius*3)
        bubble_r.set(stroke_color=RED)
        text1 = Text("死鬼(￣▽￣)", font_size=24, color=RED).move_to(bubble_r.get_center())
        self.play(FadeIn(bubble_r), run_time=0.5)
        self.play(Write(text1), run_time=1)
        
        self.play(FadeOut(bubble_r, bubble_b, text, text1))
        
        line = Line(self.ball_c2.get_left(), self.ball_c1.get_right(),  stroke_width=6, color=PINK)
        line.add_updater(lambda x: x.put_start_and_end_on(self.ball_c2.get_left(), self.ball_c1.get_right()))
        self.play(Create(line))
        self.play(self.ball_c1.animate.move_to([-self.ball_c1.radius*1.2, -1.8, 0]),
                  self.ball_c2.animate.move_to([self.ball_c2.radius + 0.01, -1.8, 0]))
        # self.play(self.ball_c1.animate.shift(RIGHT*4.5), self.ball_c2.animate.shift(LEFT*4.5))
        
        self.wait(1)