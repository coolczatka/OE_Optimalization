from Gui.AbstractSimpleGuiElement import AbstractSimpleGuiElement
import PySimpleGUI as sg
import GC
from Config import OutputConfig
from XmlFile import exportConfig

class SimpleGuiMenuBar(AbstractSimpleGuiElement):

    def __init__(self):
        self.setSgClass(sgclass=sg.Menu)
        definition = [
            ['Opcje', ['Ustawienia wyjścia', 'Zapisz konfigurację', 'Exit',]],
            ['Informacje', ['Wzór funkcji', 'O programie']],
        ]
        self.setDefinition(definition)
        self.instance = self.createElement()

    def processSignals(self, args):
        signal = args[0]
        values = args[1]
        if signal == 'O programie':
            sg.popup('Projekt 1 Obliczenia Ewolucyjne 2020', title="Informacja")
        elif signal == 'Exit':
            args[0] = sg.WINDOW_CLOSED
        elif signal == 'Zapisz konfigurację':
            args[0] = 'EXPORT_CONFIG'
        elif signal == 'Wzór funkcji':
            layout = [
                [sg.Image('Gui/ackley_formula.png')],
                [sg.Button('Ok')]
            ]
            infoWindow = sg.Window('Wzór', layout)
            while True:
                event, values = infoWindow.read()
                if event == sg.WINDOW_CLOSED or event == 'Ok':
                    break
            infoWindow.close()
        elif signal == 'Ustawienia wyjścia':
            layout = [
                [sg.Checkbox('Eksportuj wynik do XML', key='_EXPORT_XML_', default=GC.config.outputConfig.exportToFile)],
                [sg.Checkbox('Zapisz wykresy', key='_SAVE_PLOTS_', default=GC.config.outputConfig.savePlots)],
                [sg.Checkbox('Nowy wykres dla każdego startu', key='_NPFES_', default=GC.config.outputConfig.newPlotForEachStart)],

                [sg.Button('Zapisz', key='_SAVE_SETTINGS_')]
            ]
            optionWindow = sg.Window('Ustawienia wyjścia', layout)

            while True:
                event, values = optionWindow.read()
                if event == sg.WINDOW_CLOSED:
                    break
                elif event == '_SAVE_SETTINGS_':
                    oc = OutputConfig(values['_EXPORT_XML_'], values['_SAVE_PLOTS_'], values['_NPFES_'])
                    GC.config.outputConfig = oc
                    break
            optionWindow.close()

    def getInstance(self):
        return self.instance

