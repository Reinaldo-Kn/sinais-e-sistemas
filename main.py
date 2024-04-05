from manim import *
from scipy.signal import convolve

 
class Convolution(Scene):
    def construct(self):
        # formula da convolução 

        amarelo = "#EB811B"
        azul = "#1965B0"
        texto = "#23373F"
        self.camera.background_color = "#FAFAFA"
        Text.set_default(color=texto, font="Calibri", font_size=64)
        config.graph_color = texto
        linha_1 = Text("A convolução de duas funções").to_edge(UP)
        linha_2 = Text("é dada por")
        linha_2.next_to(linha_1, DOWN)
        formula = MathTex(
            r"y(t) = \int_{-\infty}^{\infty} x(\tau)h(t-\tau)d\tau",color=texto,
            substrings_to_isolate={ 
                "x": "x",
                "h": "h",
             }
            )
        formula.set_color_by_tex_to_color_map({
            "x": amarelo,
            "h": azul,
        })
        formula.scale(1.5)
        formula.to_edge(DOWN)
        self.play(Write(linha_1), Write(linha_2))
        self.wait(2)
        self.play(Write(formula))
        self.wait(3)
        
        linha_3 = Text("Exemplo")
        self.play(FadeOut(linha_1), FadeOut(linha_2),FadeOut(formula),FadeIn(linha_3))
        self.wait(2)
        
        linha_4 = Text("Seja x(t) = u(t) e h(t) = u(t)",t2c={"x(t)": amarelo, "h(t)": azul},t2s={"x(t)": ITALIC, "h(t)": ITALIC, "u(t)": ITALIC},t2f={"x(t)": "Cambria Math", "h(t)": "Cambria Math", "u(t)": "Cambria Math"})
   
        linha_5 = Text("onde u(t) é a função degrau unitário")
        linha_5.next_to(linha_4, DOWN)
        self.play(ReplacementTransform(linha_3, linha_4), Write(linha_5))
        self.wait(1)
        
        funcao_degrau = MathTex(
            r"u(t) = \begin{cases} 0, & \text{se } t < 0 \\ 1, & \text{se } t \geq 0 \end{cases}", color=texto
        )
        funcao_degrau.scale(1.5)
        funcao_degrau.next_to(linha_5, DOWN)
        self.play(Write(funcao_degrau))
        self.wait(3)
        self.play(FadeOut(linha_4), FadeOut(linha_5), FadeOut(funcao_degrau))

        # create the graphs
        
       # x_graph = FunctionGraph(lambda t: 0.75 if t >= 0 else 0).set_color(amarelo)
        #h_graph = FunctionGraph(lambda t: 0.75 if t >= 0 else 0).set_color(azul)
       # x_label = MathTex("x(t) = u(t)").set_color(amarelo)
       # h_label = MathTex("h(t) = u(t)").set_color(azul)
      #  x_label.set_color(amarelo)
       # h_label.set_color(azul)
    
       # ax = Axes(axis_config={'tip_shape': StealthTip}).set_color(texto)
      #  x_label.next_to(ax.c2p(0, 1), UP + RIGHT)
      #  h_label.next_to(ax.c2p(0, 1), UP + RIGHT)
      #  ax.add_coordinates()
      #  self.add(ax)
       # self.wait(1)
      #  self.play(Create(x_graph), Write(x_label))
       # self.wait(3)
      #  self.play(FadeOut(x_graph), FadeOut(x_label), Create(h_graph), Write(h_label))
     #   self.wait(2)
      #  self.play(FadeOut(h_graph), FadeOut(h_label))
        
        # create the convolution 
       # linha_6 = Text ("Na fórmula da convolução").next_to(ax, UP)
       # self.play(FadeIn(linha_6))
       # self.wait(1)
       # self.play(FadeOut(linha_6))
       # labels_ax1 = ax.get_axis_labels(
       #     MathTex(r"\tau"), MathTex(r"x(\tau)")
      #  ).set_color(amarelo)
       # labels_ax2 = ax.get_axis_labels(
       #     MathTex(r"\tau"), MathTex(r"h(-\tau)")
       # ).set_color(azul)
       # self.play(Indicate(labels_ax1))  
       # self.play(Create(x_graph))
       # self.wait(1.5)
       
      #  h_graph = FunctionGraph(lambda t: 0 if t >= 0 else 0.75).set_color(azul)
       # self.play(FadeOut(labels_ax1),FadeOut(x_graph), Indicate(labels_ax2,color=azul),Create(h_graph))
        #self.wait(3)
        #self.play(FadeOut(ax),FadeOut(labels_ax2),FadeOut(h_graph))
        
        ax1 = Axes().set_color(texto)
        ax2 = Axes(y_axis_config={"include_tip": False}).set_color(texto)
        ax3 = Axes(y_axis_config={"include_tip": False}).set_color(texto)
        ax1.scale(1).shift(2*UP).animate.set_color(GRAY)
        ax2.scale(1).animate.set_color(GRAY)    
        ax3.scale(1).shift(2*DOWN).animate.set_color(GRAY)   
        self.play(Create(ax1), Create(ax2), Create(ax3))
        self.wait(1)
        
        #primeira parte 
        linha_6 = Text ("Na fórmula da convolução").next_to(ax1, UP)
        x_graph = FunctionGraph(lambda t: 1 if t >= 0 else 0).set_color(amarelo)
        x_graph.shift(2*UP)
        h_graph = FunctionGraph(lambda t: 1 if t >= 0 else 0).set_color(azul)
 
        labels_ax1 = ax1.get_axis_labels(
            MathTex("t"), MathTex(r"x(t) = u(t)")
        ).set_color(amarelo)
        labels_ax2 = ax2.get_axis_labels(
            MathTex("t"), MathTex(r"h(t) = u(t)")
        ).set_color(azul)
        labels_ax2.next_to(ax2.c2p(0, 0))
        labels_ax2[0].shift(2*UP)
        ax1.add_coordinates()
        ax2.add_coordinates()
        self.add(ax1, ax2)
        self.wait(1)
        self.play(Create(x_graph), Write(labels_ax1))
        self.wait(1)
        self.play(Create(h_graph), Write(labels_ax2))
        self.play(Write(linha_6))
        self.wait(1)
        formula.next_to(ax1,UP)
        self.play(FadeOut(labels_ax1),FadeOut(x_graph),FadeOut(labels_ax2),FadeOut(h_graph))
        self.play(ReplacementTransform(linha_6,formula))
        self.wait(3)
        x_graph = FunctionGraph(lambda t: 1 if t >= 0 else 0).set_color(amarelo)
        h_graph = FunctionGraph(lambda t: 0 if t >= 0 else 1).set_color(azul)
        x_graph.shift(2*UP)
        
        labels_ax1 = ax1.get_axis_labels(
            MathTex(r"\tau"), MathTex(r"x(\tau)")
        )
        labels_ax2 = ax2.get_axis_labels(
            MathTex(r"\tau"), MathTex(r"h(-\tau)")
        )
        labels_ax3 = ax3.get_axis_labels(
            MathTex(r"t"), MathTex(r"y(t)")
        )
        labels_ax1.color = amarelo
        labels_ax2.color = azul
        labels_ax3.color = GREEN
        
        
        labels_ax2.next_to(ax2.c2p(0, 0))
        labels_ax2[0].shift(2*UP)
        labels_ax3.next_to(ax3.c2p(0, 0))
        labels_ax3[0].shift(2*UP)
        self.play(Indicate(labels_ax1),Create(x_graph))
        self.wait(1)
        self.play(Indicate(labels_ax2,color=azul),Create(h_graph))
        
        y_graph = FunctionGraph(lambda t: t if t >= 0 else 0,x_range=[-10,1.5]).set_color(GREEN)
        y_graph.shift(2*DOWN)
    

        reticencias = MathTex(r"\cdots").next_to(y_graph, RIGHT)
      
     
        self.play(AnimationGroup(
            ApplyMethod(h_graph.shift, RIGHT*1.5),
            Create(y_graph),
            run_time=5
        ))
        self.play(Indicate(labels_ax3,color=GREEN),Indicate(reticencias,color=GREEN))
        self.wait(3)
        self.play(FadeOut(y_graph),FadeOut(reticencias),FadeOut(labels_ax1),FadeOut(labels_ax2),FadeOut(labels_ax3),FadeOut(h_graph),FadeOut(x_graph),FadeOut(ax1),FadeOut(ax2),FadeOut(ax3),FadeOut(formula))
        self.wait(1)
        nome = Text("Reinaldo-Kn",font="Jayadhira LILA EE 0.1").set_color(BLACK)
        make = Text("Feito por").set_color(BLACK)
        nome.next_to(make,DOWN)
        self.play(Create(make))
        self.play(Write(nome))
        self.wait(2)