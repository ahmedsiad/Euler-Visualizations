import numpy as np
import random

RADIUS = 0.4
grid = []
for i in range(3):
    row = []
    for j in range(3):
        row.append(str(random.randint(100, 999)))
    grid.append(row)
    
class Node:
    def __init__(self, label, position=ORIGIN):
        self.name = label
        self.label = Text(str(label), font_size=20)
        self.circle = Circle(radius=RADIUS)
        self.neighbors = []
        self.position = position
        self.circle.move_to(position)
        self.label.move_to(position)
    
    def set_position_offset(self, obj, offset):
        self.circle.next_to(obj, offset * 5)
        self.label.move_to(self.circle.get_center())
    
    
class Edge: 
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.line = Line(node1.circle.get_center(), node2.circle.get_center())
        unit_vector = self.line.get_unit_vector()
        start, end = self.line.get_start_and_end()
        new_start = start + unit_vector * RADIUS
        new_end = end - unit_vector * RADIUS
        self.line = Line(new_start, new_end)
        self.weight = int(weight)
        self.weight_text = None
        
class Dijsktra(Scene):
    def construct(self):
        title = Text('Project Euler: Problem 83')
        subtitle = Text('VISUALIZED')
        
        subtitle.next_to(title, DOWN, buff = 0.5)
        
        self.play(Write(title))
        self.wait()
        
        self.play(Write(subtitle))
        self.wait()
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait()
        
        title = Text("Starting from the top left of this grid, what is the minimum path sum to the bottom right?",
                     t2c={"minimum path sum":BLUE}, font_size=16, disable_ligatures=True)
        title.to_edge(UP)
        
        self.play(Write(title))
        self.wait(0.5)
        
        grid_table = Table([*grid])
        grid_table.next_to(title, DOWN, buff=1)
        
        self.play(DrawBorderThenFill(grid_table))
        self.wait(2)
        
        brute_force_text = Text("We could try every possible path, but is there a better way?", font_size=18)
        brute_force_text.to_edge(DOWN)
        
        self.play(Write(brute_force_text))
        self.wait(1.5)
        
        self.play(FadeOut(title), FadeOut(grid_table), FadeOut(brute_force_text))
        
        
        title = Text("Using a Weighted Graph")
        title.to_edge(UP)
        
        self.play(Write(title))
        self.wait()
        
        graph, edges_list = self.create_graph(grid)
        group, edges = self.create_graph_object(graph, edges_list)
        whole_graph = VGroup(group, edges)
        
        weights_fadeIn = []
        weights_list = []
        for edge in edges_list:
            weight_text = Text(str(edge.weight))
            weight_text.scale(0.4)
            unit_vector = edge.line.get_unit_vector()
            normal = np.array([unit_vector[1], unit_vector[0], 0])
            weight_text.move_to(edge.line.get_midpoint() + normal * 0.25)
            weights_fadeIn.append(FadeIn(weight_text))
            weights_list.append(weight_text)
            edge.weight_text = weight_text
            
        setup_text = Text("We can represent our table using a weighted graph.", font_size=16)
        setup_text.next_to(graph[2].circle, RIGHT, buff=1.5)
        
        self.play(FadeIn(whole_graph), *weights_fadeIn, FadeIn(setup_text))
        self.wait()
        
        setup_sub_text = Text("Now we can use Dijkstra's Algorithm", t2c={"Dijkstra's Algorithm": YELLOW}, font_size=16, disable_ligatures=True)
        setup_sub_text.next_to(setup_text, DOWN, buff=0.5)
        self.play(FadeIn(setup_sub_text))
        self.wait(2)
        
        tracker_array = []
        for i in range(9):
            tracker_array.append([chr(ord("A") + i), "∞"])
        tracker_array[0][1] = "0"
        tracker_table = Table([*tracker_array], col_labels=[Text("Node"), Text("Distance")])
        tracker_table.next_to(graph[5].circle, RIGHT)
        tracker_table.scale(0.35)
        self.play(FadeIn(tracker_table), FadeOut(setup_text), FadeOut(setup_sub_text))
        self.wait()
        
        visited = []
        unvisited = [chr(ord("A") + i) for i in range(9)]
        
        while len(unvisited) > 0:
            visiting_node = None
            shortest_distance = 1e6
            for ch in unvisited:
                distance = tracker_array[ord(ch) - ord("A")][1]
                if distance == "∞": continue
                if int(distance) < shortest_distance:
                    shortest_distance = int(distance)
                    visiting_node = self.find_node(ch, graph)

            boxes = []
            boxes_animation = []
            boxes.append(SurroundingRectangle(visiting_node.circle, buff=0.1))
            boxes_animation.append(Create(boxes[0]))
            neighbors, neighbors_edges = self.get_neighbors(visiting_node.name, edges_list, unvisited)
            for nb in neighbors:
                box_nb = SurroundingRectangle(nb.circle, buff=0.1)
                boxes.append(box_nb)
                boxes_animation.append(Create(box_nb))
            for nbe in neighbors_edges:
                box_nbw = SurroundingRectangle(nbe.weight_text, color=GREEN, buff=0.1)
                boxes.append(box_nbw)
                boxes_animation.append(Create(box_nbw))
            if len(boxes_animation) > 0: self.play(*boxes_animation)
            self.wait()
            
            update_table_animations = []
            current_tracker = list(filter(lambda x: x[0] == visiting_node.name, tracker_array))[0]
            current_distance = int(current_tracker[1])
            for i in range(len(neighbors)):
                nb = neighbors[i]
                nbe = neighbors_edges[i]
                total_distance = current_distance + nbe.weight
                nb_tracker = list(filter(lambda x: x[0] == nb.name, tracker_array))[0]
                if nb_tracker[1] == "∞" or int(nb_tracker[1]) > total_distance:
                    nb_tracker[1] = str(total_distance)
                
                    entry = tracker_table.get_entries((ord(nb.name) - ord("A") + 2, 2))
                    new_entry = Text(str(nb_tracker[1]))
                    new_entry.scale(0.35)
                    new_entry.move_to(entry.get_center())
                    entry.become(new_entry)
                    update_table_animations.append(Write(entry))
            if len(update_table_animations) > 0: self.play(*update_table_animations)
            self.wait()
            
            boxes_animation = []
            for box in boxes:
                boxes_animation.append(FadeOut(box))
            if len(boxes_animation) > 0: self.play(*boxes_animation)
            self.wait()
            
            unvisited.remove(visiting_node.name)
            visited.append(visiting_node.name)
        
        self.wait()
        tracker_I = tracker_table.get_entries((10, 2))
        box = SurroundingRectangle(tracker_I, buff=0.1)
        
        finishing_text = Text("Now add the value in the top left of the original grid to the value in I since we ommitted it from the graph.", font_size=14)
        finishing_text.to_edge(DOWN, buff=0.75)
        
        self.play(Create(box), Write(finishing_text))
        self.wait(3)
        
        value_I = int(list(filter(lambda x: x[0] == "I", tracker_array))[0][1])
        total = value_I + int(grid[0][0])
        
        answer_text = Text(str(value_I) + " + " + grid[0][0] + " = " + str(total), font_size=24)
        answer_text.next_to(finishing_text, DOWN)
        self.play(Write(answer_text))
        self.wait(5)
        
        
    def get_neighbors(self, label, edges, unvisited):
        neighbors = []
        neighbors_edges = []
        for edge in edges:
            if edge.node1.name == label and edge.node2.name in unvisited:
                neighbors.append(edge.node2)
                neighbors_edges.append(edge)
            elif edge.node2.name == label and edge.node1.name in unvisited:
                neighbors.append(edge.node1)
                neighbors_edges.append(edge)
        return neighbors, neighbors_edges
    
    def find_node(self, label, graph):
        for node in graph:
            if node.name == label:
                return node
            
    def create_graph(self, weights):
        graph = []
        edges = []
        
        nodeA = Node("A")
        nodeB = Node("B")
        nodeC = Node("C")
        nodeD = Node("D")
        nodeE = Node("E", LEFT * 4)
        nodeF = Node("F")
        nodeG = Node("G")
        nodeH = Node("H")
        nodeI = Node("I")
        
        nodeA.set_position_offset(nodeE.circle, LEFT + UP)
        nodeB.set_position_offset(nodeE.circle, UP)
        nodeC.set_position_offset(nodeE.circle, RIGHT + UP)
        nodeD.set_position_offset(nodeE.circle, LEFT)
        nodeF.set_position_offset(nodeE.circle, RIGHT)
        nodeG.set_position_offset(nodeE.circle, LEFT + DOWN)
        nodeH.set_position_offset(nodeE.circle, DOWN)
        nodeI.set_position_offset(nodeE.circle, RIGHT + DOWN)
        
        edgeAB = Edge(nodeA, nodeB, weights[0][1])
        edgeAD = Edge(nodeA, nodeD, weights[1][0])
        edgeBE = Edge(nodeB, nodeE, weights[1][1])
        edgeBC = Edge(nodeB, nodeC, weights[0][2])
        edgeCF = Edge(nodeC, nodeF, weights[1][2])
        edgeDE = Edge(nodeD, nodeE, weights[1][1])
        edgeDG = Edge(nodeD, nodeG, weights[2][0])
        edgeEH = Edge(nodeE, nodeH, weights[1][1])
        edgeEF = Edge(nodeE, nodeF, weights[1][1])
        edgeFI = Edge(nodeF, nodeI, weights[2][2])
        edgeGH = Edge(nodeG, nodeH, weights[2][1])
        edgeHI = Edge(nodeH, nodeI, weights[2][2])
        
        edges.append(edgeAB)
        edges.append(edgeAD)
        edges.append(edgeBE)
        edges.append(edgeBC)
        edges.append(edgeCF)
        edges.append(edgeDE)
        edges.append(edgeDG)
        edges.append(edgeEH)
        edges.append(edgeEF)
        edges.append(edgeFI)
        edges.append(edgeGH)
        edges.append(edgeHI)
        
        graph.append(nodeA)
        graph.append(nodeB)
        graph.append(nodeC)
        graph.append(nodeD)
        graph.append(nodeE)
        graph.append(nodeF)
        graph.append(nodeG)
        graph.append(nodeH)
        graph.append(nodeI)
        
        return graph, edges
    
    def create_graph_object(self, graph, edges_list):
        nodes = []
        edges = []
        for node in graph:
            node.circle.set_fill(color=BLUE, opacity=0.5)
            node.circle.set_stroke(color=BLUE)
            group = VGroup(node.circle, node.label)
            nodes.append(group)
        for edge in edges_list:
            edge.line.set_color(color=GRAY)
            group = VGroup(edge.line)
            edges.append(group)
            
        return VGroup(*nodes), VGroup(*edges)