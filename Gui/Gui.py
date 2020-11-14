
import PySimpleGUI as sg
from Gui.Menubar import SimpleGuiMenuBar
from Gui.Configs import *
from Config import Config, ChromosomeConfig
from AckleyOptimizer import AckleyOptimizer
# Define the window's contents
from Gui.Plotter import Plotter
import GC

class Gui:

    def __init__(self):
        menubar = SimpleGuiMenuBar()
        self.plotter = Plotter()
        functionParameters = FunctionParametersInputs()

        self.components = [
            menubar,
            functionParameters

        ]
        self.layout = [
            [menubar.getInstance()],
            [functionParameters.getInstance()],
            [sg.Button('START')],
            [self.plotter.getInstance()]
        ]

        self.adaptLayout()

    def run(self):

        # Create the window
        #window = sg.Window('Window Title', layout, no_titlebar=True, location=(0, 0), size=(800, 600), keep_on_top=True)
        sg.theme('DarkAmber')
        GC.window = sg.Window('Optymalizacja funkcji Ackleya', self.layout, size=(800, 600))

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = GC.window.read()
            args = [event, values]
            # See if user wants to quit or window was closed
            for i in self.components:
                i.processSignals(args)
            if args[0] == 'START':
                GC.config = self.makeConfig(args[1])
                aopt = AckleyOptimizer()
                #aopt.run()
                best, means, stds = aopt.runGenerations()
                best_values = [b.value for b in best]
                x = range(GC.config.generations)
                figure = self.plotter.best_by_generations_plot(x, means)
                self.plotter.draw_figure_(GC.window['fig_cv'].TKCanvas, figure)
            if args[0] == sg.WINDOW_CLOSED:
                break
            # Output a message to the window
           # window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

        # Finish up by removing from the screen
        GC.window.close()

    def adaptLayout(self):
        for i in range(len(self.layout)):
            while(isinstance(self.layout[i][0], list)):
                listt = self.layout[i]
                self.layout.pop(i)
                index = i
                for ii in listt:
                    self.layout.insert(index, ii)
                    index+=1

    def makeConfig(self, values):
        chromosomeConfig = ChromosomeConfig(
            mk=FunctionParametersInputs.signalMapping()['MK'][values['_MK_']],
            mp=float(values['_MP_']),
            ck=FunctionParametersInputs.signalMapping()['CK'][values['_CK_']],
            cp=float(values['_CP_']),
            ip=float(values['_IP_'])
        )
        print(chromosomeConfig.ck)
        minRange, maxRange = values['_RANGE_'].split(',')
        config = Config(
            generations=int(values['_GENERATIONS_']),
            chromosomeConfig=chromosomeConfig,
            kind=FunctionParametersInputs.signalMapping()['KIND'][values['_KIND_']],
            searchRange=(float(minRange), float(maxRange)),
            populationSize=int(values['_POPULATIONSIZE_']),
            selection=FunctionParametersInputs.signalMapping()['SELECTION'][values['_SELECTION_']],
            precision=int(values['_PRECISION_']),
            selectionParameter=float(values['_SELECTIONPARAMETER_']),
            elitePercent=float(values['_ELITE_PERCENT_'])
        )
        return config
