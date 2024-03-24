from manim import *
from scipy.signal import convolve

 
class Convolution(Scene):
    def construct(self):
        # formula da convolução 
        linha_1 = Text("A convolução de duas funções").to_edge(UP)
        linha_2 = Text("é dada por:")
        linha_2.next_to(linha_1, DOWN)
        
        formula = MathTex(
            r"(x * h)(t) = \int_{-\infty}^{\infty} x(\tau)h(t-\tau)d\tau",
            substrings_to_isolate={ 
                "x": "x",
                "h": "h",
             }
            )
        formula.set_color_by_tex_to_color_map({
            "x": YELLOW,
            "h": BLUE,
        })
        formula.scale(1.5)
        
        self.play(Write(linha_1))
        self.play(Write(linha_2))   
        self.wait(2)
        self.play(ReplacementTransform(linha_1, formula),FadeOut(linha_2))
        self.wait(3)
        
        linha_3 = Text("Por exemplo:")
        self.play(FadeOut(formula),FadeIn(linha_3))
        self.wait(2)
        
        linha_4 = Text("Sejam x(t) = u(t) e h(t) = u(t)",t2c={"x(t)": YELLOW, "h(t)": BLUE})
   
        linha_5 = Text("onde u(t) é a função degrau unitário")
        linha_5.next_to(linha_4, DOWN)
        self.play(ReplacementTransform(linha_3, linha_4), Write(linha_5))
        self.wait(1)
        
        funcao_degrau = MathTex(
            r"u(t) = \begin{cases} 0, & \text{se } t < 0 \\ 1, & \text{se } t \geq 0 \end{cases}"
        )
        funcao_degrau.next_to(linha_5, DOWN)
        self.play(Write(funcao_degrau))
        self.wait(3)
        self.play(FadeOut(linha_4), FadeOut(linha_5), FadeOut(funcao_degrau))

        # create the graphs
        
        x_graph = FunctionGraph(lambda t: 0.75 if t >= 0 else 0)
        h_graph = FunctionGraph(lambda t: 0.75 if t >= 0 else 0).set_color(BLUE)
        x_label = MathTex("x(t) = u(t)").set_color(YELLOW_A)
        h_label = MathTex("h(t) = u(t)").set_color(BLUE_A)
        x_label.set_color(YELLOW)
        h_label.set_color(BLUE)
        
        # create the axis
        
        ax = Axes(axis_config={'tip_shape': StealthTip})
        x_label.next_to(ax.c2p(0, 1), UP + RIGHT)
        h_label.next_to(ax.c2p(0, 1), UP + RIGHT)
        ax.add_coordinates()
        self.add(ax)
        self.wait(1)
        self.play(Create(x_graph), Write(x_label))
        self.wait(3)
        self.play(FadeOut(x_graph), FadeOut(x_label), Create(h_graph), Write(h_label))
        self.wait(2)
        self.play(FadeOut(h_graph), FadeOut(h_label))
        
        # create the convolution 
        linha_6 = Text ("Na fórmula da convolução:").next_to(ax, UP)
        self.play(FadeIn(linha_6))
        self.wait(1)
        self.play(FadeOut(linha_6))
        labels_ax1 = ax.get_axis_labels(
            MathTex(r"\tau"), MathTex(r"x(\tau)")
        )
        labels_ax2 = ax.get_axis_labels(
            MathTex(r"\tau"), MathTex(r"h(-\tau)")
        )
        self.play(Indicate(labels_ax1))  
        self.play(Create(x_graph))
        self.wait(1.5)
       
        h_graph = FunctionGraph(lambda t: 0 if t >= 0 else 0.75).set_color(BLUE)
        self.play(FadeOut(labels_ax1),FadeOut(x_graph), Indicate(labels_ax2,color=BLUE),Create(h_graph))
        self.wait(3)
        self.play(FadeOut(ax),FadeOut(labels_ax2),FadeOut(h_graph))
        
        ax1 = Axes()
        ax2 = Axes()
        ax3 = Axes()
        ax1.scale(0.4).shift(2*UP).animate.set_color(GRAY)
        ax2.scale(0.4).animate.set_color(GRAY)    
        ax3.scale(0.4).shift(2*DOWN).animate.set_color(GRAY)   
        self.play(Create(ax1), Create(ax2), Create(ax3))
        self.wait(1)
        x_graph = FunctionGraph(lambda t: 1 if t >= 0 else 0).set_color(YELLOW)
        h_graph = FunctionGraph(lambda t: 0 if t >= 0 else 1).set_color(BLUE)
        
        x_graph.shift(2*UP)
        
        labels_ax1 = ax1.get_axis_labels(
            MathTex(r"\tau").scale(0.6), MathTex(r"x(\tau)").scale(0.6),
        )
        labels_ax2 = ax2.get_axis_labels(
            MathTex(r"\tau").scale(0.6), MathTex(r"h(-\tau)").scale(0.6)
        )
        labels_ax3 = ax3.get_axis_labels(
            MathTex(r"t").scale(0.6), MathTex(r"y(t)").scale(0.6)
        )
        labels_ax1.color = YELLOW
        labels_ax2.color = BLUE
        labels_ax3.color = GREEN
        
        
        
        self.play(Indicate(labels_ax1),Create(x_graph),Indicate(labels_ax2,color=BLUE),Create(h_graph))


        y_graph = FunctionGraph(lambda t: t if t >= 0 else 0,x_range=[-10,1]).set_color(GREEN)
        y_graph.shift(2*DOWN)
        reticencias = MathTex(r"\cdots").next_to(y_graph, RIGHT)
        self.play(Indicate(labels_ax3,color=GREEN),Create(y_graph),Indicate(reticencias,color=GREEN))
        self.wait(3)
        self.play(FadeOut(y_graph))
        