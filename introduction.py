from manim import *

class Introduction(Scene):
    def construct(self):
        title = Text('Project Euler')
        subtitle = Text('VISUALIZED')
        
        subtitle.next_to(title, DOWN, buff = 0.5)
        
        self.play(Write(title))
        
        self.wait()
        
        self.play(Write(subtitle))
        self.wait()