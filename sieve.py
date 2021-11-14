from manim import *

class titlePrimeSieve(Scene):
    def construct(self):
        title = Text('Problem 10: Summation of Primes')
        subtitle = Text('Find the sum of all the primes below two million.')
        
        subtitle.next_to(title, DOWN, buff = 0.5)
        subtitle.scale(0.6)
        
        self.play(Write(title), Write(subtitle))
        self.wait()
        
        self.play(title.animate.to_edge(UP), subtitle.animate.to_edge(UP *2.5))
        
        explain = Text('We can use the Sieve of Eratosthenes, an ancient algorithm, to find primes below a certain number.\n We simply mark a prime and eliminate its multiples. The next unmarked number is the next prime.')
        explain.scale(0.4)
        
        self.play(Write(explain), run_time = 4)
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(explain))

class PrimeSieve(Scene):
    def construct(self):        
        title = Text('This is the Sieve of Eratosthenes')
        subtitle = Text('VISUALIZED')
        
        subtitle.next_to(title, DOWN, buff = 0.5)
        
        self.play(Write(title))
        self.wait()
        
        self.play(Write(subtitle))
        self.wait()
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait()
        
        
        t0 = MathTable(
            [[j+(i-1)*10+1 for j in range(10)] for i in range(1, 11)],
            h_buff=1, include_outer_lines=True)
        
        
        t0.width = 10
        
        
        self.play(DrawBorderThenFill(t0))
        self.wait()
        

        
        
        def next_num():
            num = 2
            while num < 110:
                yield num
                num += 1
                
        num = next_num()
        Sieved = []
        Primes = []
        
        for i in range(9):
            dummy_number = next(num)
            if dummy_number not in Sieved:
                Primes.append(dummy_number)
            
                for i in range(2, 51):
                    if i*dummy_number < 101:
                        Sieved.append(i*dummy_number)

                i = dummy_number // 10 + 1          
                j = dummy_number % 10 

                r = t0.get_entries((i,j))
                r.set_fill(GREEN, opacity = 1)

                self.play(DrawBorderThenFill(r))
                self.wait()

                Animations = []
                for x in range(1, 11):
                    for y in range(1, 11):
                        num_at_point = (x-1)*10 + y
                        if  num_at_point % dummy_number == 0 and [x, y] != [i, j]:
                            k=t0.get_entries((x,y))
                            k.set_fill(RED, opacity = 1)
                            Animations.append(DrawBorderThenFill(k))


                self.play(AnimationGroup(*Animations, lag_ratio = 0.005 ))
                self.wait()
                
                
        Animations = []        
        for i in range(91):
            dummy_number = next(num)
            if dummy_number not in Sieved and dummy_number < 101:
                Primes.append(dummy_number)

                i = dummy_number // 10 + 1          
                j = dummy_number % 10 

                r = t0.get_entries((i,j))
                r.set_fill(GREEN, opacity = 1)
                Animations.append(DrawBorderThenFill(r))

        self.play(AnimationGroup(*Animations, lag_ratio = 0.05 ))    
                
        self.play(t0.animate.shift(DOWN * 5))
        
        string_of_primes1 = str(Primes[0:-10]).translate({ord(i): None for i in '[]'})
        string_of_primes2 = str(Primes[-10:]).translate({ord(i): None for i in '[]'})
                
        prime_list = Text("Prime Numbers Under 100:\n" + string_of_primes1 + '\n' + string_of_primes2)
        prime_list.next_to(t0, UP, buff = 1)
        prime_list.scale(0.6)
        
        self.play(Write(prime_list))
        self.wait()