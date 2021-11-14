from manim import *
import numpy as np
import random

pyramid = []
UPPER_BOUND = 99
LOWER_BOUND = 10
n = 5

def getCellOffset(i, j):
    cellAbove = None
    direction = np.array([-0.01, -1, 0])
    if j != i:
        cellAbove = pyramid[i - 1][j]
    else:
        cellAbove = pyramid[i - 1][j - 1]
        direction[0] *= -1
    return (cellAbove, direction)

class Pyramid(Scene):
    def construct(self):
        title = Text('Problem 67: Maximum Path Sum')
        subtitle = Text('Find the maximum path sum in a triangle.', font_size=36)
        
        subtitle.next_to(title, DOWN, buff = 0.5)
        
        self.play(Write(title))
        self.wait()
        
        self.play(Write(subtitle))
        self.wait()
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait()
    
        problemText = Text("Starting from the top of a given pyramid of numbers, what is the maximum sum?", font_size=20)
        problemText.to_edge(UP)
        self.play(Write(problemText))
        
        apex = Text("34")
        apex.next_to(problemText, DOWN, buff=0.5)
        pyramid.append([apex])
        animations = [Write(apex)]
        for i in range(1, n):
            row = []
            for j in range(i + 1):
                num = random.randint(LOWER_BOUND, UPPER_BOUND)
                cell = Text(str(num))
                offset = getCellOffset(i, j)
                cell.next_to(offset[0], offset[1], buff=0.5)
                row.append(cell)
                animations.append(Write(cell))
            pyramid.append(row)
        
        self.play(*animations)
        
        self.wait(2)
        
        boxes = []
        numbersText = []
        currentJ = 0
        actualSum = 0
        for i in range(n):
            cell = pyramid[i][currentJ]
            boxes.append(SurroundingRectangle(cell, buff=0.1))
            
            original = cell.original_text
            actualSum += int(original)
            if i == n - 1: original = "+ " + original
            numText = Text(original)
            numText.next_to(cell, RIGHT, buff=0.5)
            numText.to_edge(RIGHT)
            numbersText.append(numText)
            
            options = [currentJ, currentJ + 1]
            currentJ = random.choice(options)
            
        self.play(Create(boxes[0]), Write(numbersText[0]))
        self.wait()
        for i in range(1, len(boxes)):
            if i != len(boxes) - 1:
                self.play(ReplacementTransform(boxes[i - 1], boxes[i]), Write(numbersText[i]))
            else:
                l = Line()
                l.next_to(numbersText[i], DOWN, buff=0.5)
                self.play(ReplacementTransform(boxes[i - 1], boxes[i]), Write(numbersText[i]), Create(l))
            self.wait(0.5)
        sumText = Text(str(actualSum))
        sumText.next_to(l, DOWN, buff=0.5)
        self.play(Write(sumText))
        self.wait(0.5)
        
        questionText = Text("This is one path; how do we find the best path?", font_size=24)
        questionText.to_edge(DOWN)
        self.play(Write(questionText))
        self.wait(2)
        
        bruteForceText = Text("Brute force? But there are 16 possible paths.", font_size=24)
        bruteForceText.to_edge(DOWN)
        self.play(ReplacementTransform(questionText, bruteForceText))
        self.wait(2)

        hopefulText = Text("There must be a better solution!", font_size=24)
        hopefulText.to_edge(DOWN)
        self.play(ReplacementTransform(bruteForceText, hopefulText))
        self.wait(1.5)
        
        
        animations = []
        animations.append(FadeOut(problemText))
        animations.append(FadeOut(hopefulText))
        animations.append(FadeOut(sumText))
        animations.append(FadeOut(l))
        animations.append(FadeOut(boxes[-1]))
        for txt in numbersText:
            animations.append(FadeOut(txt))
        solutionText = Text("Dynamic Solution", font_size=30)
        solutionText.to_edge(UP)
        self.play(*animations, Write(solutionText))
        self.wait()
        
        for i in range(n - 1):
            boxP = SurroundingRectangle(pyramid[n - 2][i], buff=0.1)
            boxC1 = None
            boxC2 = None
            toAdd = 0
            child1 = pyramid[n - 1][i]
            child2 = pyramid[n - 1][i + 1]
            if (int(child1.text) > int(child2.text)):
                toAdd = int(child1.text)
                boxC1 = SurroundingRectangle(child1, color="#00FF00")
                boxC2 = SurroundingRectangle(child2, color="#FF0000")
            else:
                toAdd = int(child2.text)
                boxC1 = SurroundingRectangle(child1, color="#FF0000")
                boxC2 = SurroundingRectangle(child2, color="#00FF00")
        
            self.play(Create(boxP), Create(boxC1), Create(boxC2))
            self.wait()
            
            summed = int(pyramid[n - 2][i].text) + toAdd
            updatedText = Text(str(summed))
            offset = getCellOffset(n - 2, i)
            updatedText.next_to(offset[0], offset[1], buff=0.5)
            self.play(ReplacementTransform(pyramid[n - 2][i], updatedText), FadeOut(boxP))
            pyramid[n - 2][i] = updatedText
            
            self.wait(0.5)
            fadeOutAnimations = []
            fadeOutAnimations.append(FadeOut(boxC1))        
            fadeOutAnimations.append(FadeOut(boxC2))  
            self.play(*fadeOutAnimations)
            self.wait()
        
        fadeOutAnimations = []
        for i in range(n):
            fadeOutAnimations.append(FadeOut(pyramid[n - 1][i]))
        pyramid.pop()
        
        group = VGroup()
        for row in pyramid:
            for cell in row:
                group += cell
            
        self.play(*fadeOutAnimations, group.animate.shift(DOWN))
        self.wait()
        
        animations = []
        i = n - 3
        while i >= 0:
            for j in range(i + 1):
                child1 = pyramid[i + 1][j]
                child2 = pyramid[i + 1][j + 1]
                summed = int(pyramid[i][j].text)
                if (int(child1.text) > int(child2.text)):
                    summed += int(child1.text)
                else:
                    summed += int(child2.text)
                updatedText = Text(str(summed))
                offset = getCellOffset(i, j)
                if i != 0:
                    updatedText.next_to(offset[0], offset[1], buff=0.5)
                animations.append(ReplacementTransform(pyramid[i][j], updatedText))
                pyramid[i][j] = updatedText
            if i != 0:
                self.play(*animations)
                animations = []
                self.wait(0.5)
            
            for j in range(i + 2):
                animations.append(FadeOut(pyramid[i + 1][j]))
            pyramid.pop()
            
            if i != 0:
                group = VGroup()
                for row in pyramid:
                    for cell in row:
                        group += cell
                animations.append(group.animate.shift(DOWN))
            self.play(*animations)
            self.wait()
            animations = []
            i = i - 1
        
        self.wait(0.1)
        
        final_text = Text("This is the maximum sum achievable!", font_size=36)
        final_text.next_to(pyramid[0][0], DOWN, buff=0.5)
        self.play(Write(final_text))
        self.wait(5)
