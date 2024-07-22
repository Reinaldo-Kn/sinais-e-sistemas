# -*- coding: utf-8 -*-
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import Math, display
from sympy import lambdify
from sympy.polys.partfrac import apart

def symdisp(expr, var, unit=" "):
    """
    Display sympy expressions in Latex style.

    :param expr: expression in latex [string]
    :param var: sympy variable, function, expression.
    :param unit: string indicating unit of var [string]
    """
    display(Math(expr + sp.latex(var) + "\;" + "\mathrm{"+unit+"}"))


# função para arredondamento de floats em expressões simbólicas
def round_expr(expr, numDig):
    """
    Rounds numerical values in sympy expressions

    :param expr: sympy symbolic expression
    :param numDig: number of rounding decimals

    :return: rounded expression
    """
    return expr.xreplace({n: round(n, numDig) for n in expr.atoms(sp.Number)})


# Função para plot de funções do sympy
def symplot(t, F, interval, funLabel, colors, xlabel="tempo [s]", ylabel=""):
    """
    Create plots of sympy symbolic functions.

    :param t: sympy variable
    :param F: sympy function F(t) or list of functions
    :param interval: array of values of t where F should be evaluated [np.array]
    :param funLabel: curve label(s) to be displayed in the plot [string or list of strings]
    :param colors: color(s) for the plot(s) [string or list of strings]
    :param xlabel: label for x-axis [string]
    :param ylabel: label for y-axis [string]
    """
    fig = plt.figure()
    if type(F) == list:
        for indLabel, f in enumerate(F):
            plotFunc(t, f, interval, funLabel[indLabel], colors[indLabel], xlabel, ylabel )
    else:
        plotFunc(t, F, interval, funLabel, colors, xlabel, ylabel)
    plt.grid()
    plt.close()
    return fig


def plotFunc(t, F, interval, funLabel, color, xlabel, ylabel):
    func = sp.lambdify(
        t, F, modules=["numpy", {"Heaviside": lambda t: np.heaviside(t, 0)}]
    )
    f_num = func(interval)

    plt.plot(interval, f_num, label=funLabel, color=color)
    plt.legend(loc="upper right")
    plt.xlim([min(interval), max(interval)])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def genGIF(x, y, figName, xlabel=[], ylabel=[], title=[], plotcols=[], centralAxes=False, squareAxes=False, fram=200, inter=20):
    """
    Create and save a plot animation as GIF

    :param x: x-axis values [np array]
    :param y: y-axis values [np array]
    :param figName: figure file name w/ folder path [string]
    :param xlabel: xlabel [string]
    :param ylabel: ylabel [string]
    :param fram: number of frames [int]
    :param inter: time interval between frames [milliseconds]

    """
    figAnin = plt.figure()
    
    #if squareAxes:
    #plt.axis('square')

    May = np.max(np.abs(y))
    min_y = np.min(y)
    max_y = np.max(y)

    Max = np.max(np.abs(x))
    min_x = np.min(x)
    max_x = np.max(x)


    Max_xy = np.max([np.abs(x), np.abs(y)])
    min_xy = np.min([x, y])
    max_xy = np.max([x, y])

    if squareAxes:
        #plt.axis('equal')
        ax = plt.axes(            
            ylim=(
                 min_xy - 0.1 * Max_xy,
                 max_xy + 0.1 * Max_xy,
            ),
            xlim=(
                 min_xy - 0.1 * Max_xy,
                 max_xy + 0.1 * Max_xy,
            ),
        )
    else:
        ax = plt.axes(
            xlim=(min_x, max_x),
            ylim=(
                min_y - 0.1 * May,
                max_y + 0.1 * May,
            ),
        )

    if not len(plotcols):
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']
        plotcols= colors[:2]
    #print(colors)

    lines = []
    for index in range(2):
        if index == 0:
            lobj = ax.plot([],[],lw=2,color=plotcols[index])[0]
        else:
            lobj = ax.plot([],[],'o',lw=2,color=plotcols[index])[0]
        lines.append(lobj)

   # (line,) = ax.plot([], [])
    ax.grid()

    plt.axhline(color='black', lw=1)
    plt.axvline(color='black', lw=1)

    if centralAxes:
        # Move left y-axis and bottom x-axis to centre, passing through (0,0)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')

        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    indx = np.arange(0, len(x), int(len(x) / fram))

    if len(xlabel):
        plt.xlabel(xlabel)

    if len(ylabel):
        plt.ylabel(ylabel)

    if len(title):
        plt.title(title)

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        for idx, line in enumerate(lines):
            if idx == 0:
                line.set_data(x[:indx[i]], y[:indx[i]])
            else:
                line.set_data(x[indx[i]], y[indx[i]])

        return lines

    anim = FuncAnimation(
        figAnin,
        animate,
        init_func=init,
        frames=fram,
        interval=inter,
        blit=True,
    )

    anim.save(figName, dpi=200, writer="imagemagick")
    plt.close()

def genConvGIF(
    x,
    h,
    t,
    totalTime,
    ti,
    tf,
    figName,
    xlabel=[],
    ylabel=[],
    fram=200,
    inter=20,
    plotConv=False,
    colors=['blue', 'orange', 'green'],
    figsize=(8, 6),
    enable_legend = False,
    xlim = None,
    ylim = None
):
    """
    Create and save a convolution plot animation as GIF

    :param x: x(t) function [sympy expr]
    :param h: h(t) function [sympy expr]
    :param t: t time variable [sympy variable]
    :param totalTime: array of time instants where the functions will be evaluated [nparray]
    :param ti: time when animation starts [scalar]
    :param tf: time when animation stops [scalar]
    :param figName: figure file name w/ folder path [string]
    :param xlabel: xlabel [string]
    :param ylabel: ylabel [string]
    :param fram: number of frames [int]
    :param inter: time interval between frames [milliseconds]
    :param colors: colors for the plots [list of strings]
    :param figsize: figure size (width, height) [tuple]
    """
    x_func = lambdify(t, x, modules=["numpy", {"Heaviside": lambda t: np.heaviside(t, 0)}])
    h_func = lambdify(t, h, modules=["numpy", {"Heaviside": lambda t: np.heaviside(t, 0)}])

    x_num = x_func(totalTime)
    h_num = h_func(totalTime)
    dt = totalTime[1] - totalTime[0]

    if plotConv:
        y_num = np.convolve(h_num, x_num, "same") * dt
        ymax = np.max([x_num, h_num, y_num])
        ymin = np.min([x_num, h_num, y_num])
    else:
        ymax = np.max([x_num, h_num])
        ymin = np.min([x_num, h_num])

    figAnim = plt.figure(figsize=figsize)  # Adjust figsize here
    ax = plt.axes()
        # Aplicando xlim e ylim se fornecidos
    if xlim is not None:
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(totalTime.min(), totalTime.max())

    if ylim is not None:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(ymin - 0.1 * np.abs(ymax), ymax + 0.1 * np.abs(ymax))

        
    line1, line2, line3 = ax.plot([], [], [], [], [], [])
    line1.set_label(ylabel[0])
    line2.set_label(ylabel[1])

    if plotConv:
        line3.set_label(ylabel[2])

    ax.grid()
    
    if enable_legend:
        ax.legend(loc="upper right")


    # plot static function
    figh = symplot(t, h, totalTime, "h(t)", colors[0])

    if len(xlabel):
        plt.xlabel(xlabel)

    def init():
        line1.set_data(figh.get_axes()[0].lines[0].get_data())
        line1.set_color(colors[0])
        return (line1,)

    plt.close(figh)

    delays = totalTime[:: int(len(totalTime) / fram)]
    ind = np.arange(0, len(totalTime), int(len(totalTime) / fram))

    ind = ind[delays > ti]
    delays = delays[delays > ti]

    ind = ind[delays < tf]
    delays = delays[delays < tf]

    totalFrames = len(delays)

    def animate(i):
        figx = symplot(t, x.subs({t: delays[i] - t}), totalTime, "x(t-τ)",colors[1])
        line2.set_data(figx.get_axes()[0].lines[0].get_data())
        line2.set_color(colors[1])
        if plotConv:
            line3.set_data(totalTime[:ind[i]], y_num[:ind[i]])
            line3.set_color(colors[2])
        plt.close(figx)
        return line2, line3

    anim = FuncAnimation(
        figAnim,
        animate,
        init_func=init,
        frames=totalFrames,
        interval=inter,
        blit=True,
    )
    plt.tight_layout()
    anim.save(figName, dpi=200, writer="imagemagick")
    plt.close()
