from rootpy.plotting.base import convert_color
from . import log
log = log[__name__]
import ROOT

from sample import Sample

class measurement(object):

    def __init__(self, rfile, channel):

        self.rfile = rfile
        self.channel = channel
        self.categories = self.build_cat_list()
        self.systematics = self.build_syst_list()
        self.data = Sample('Data', 'black', 'Data')
        self.backgrounds = []
        self.background_keys = []
        self._build_background(self.channel)
        self.total_background = Sample('Total', 'blue', 'Total Bkg.',sub_samples=self.background_keys)

        self.total_signal = Sample('Higgs', 'red', 'Higgs', ['ggH', 'VBFH', 'WH', 'ZH', 'ttH'])
        self.signals = [
            Sample('VBFH', convert_color(ROOT.kRed +1, 'mpl'), 'VBF'),
            Sample('ggH', convert_color(ROOT.kRed - 1, 'mpl'), 'ggH'),
            Sample('VH', convert_color(ROOT.kRed - 3, 'mpl'), 'VH', ['WH', 'ZH']),
            Sample('ttH', convert_color(ROOT.kRed - 5, 'mpl'), 'ttH'),
            ]
    def build_cat_list(self):
        return [d for d in self.rfile]

    def build_syst_list(self):
        return []

    def _build_background(self, channel):
        if channel == 'leplep':
            Ztt = Sample(
                'Ztt', convert_color(ROOT.kAzure + 1, 'mpl'), 'Z#rightarrow#tau#tau', sub_samples=['Ztt', 'ZttEWK'])
            Fake = Sample('Fake', 'yellow', 'Fakes')
            Zll = Sample('Zll', convert_color(ROOT.kCyan - 10, 'mpl'), 'Z#rightarrowll', sub_samples=['Zll', 'ZllEWK'])
            Top = Sample('Top', convert_color(ROOT.kOrange + 1, 'mpl'), 'Top')
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV', 'ggHWW', 'VBFHWW'])
            self.backgrounds = [
                Ztt, Fake, Zll, Top, Others
                ]
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'Top', 'Zll', 'ZllEWK', 'VV', 'ggHWW', 'VBFHWW']
        elif channel == 'hadhad':
            Ztt = Sample(
                'Ztt', convert_color(ROOT.kAzure + 1, 'mpl'), 'Z#rightarrow#tau#tau', sub_samples=['Ztt', 'ZttEWK'])
            Fake = Sample('Fake', 'yellow', 'Fake')
            Diboson = Sample('VV', convert_color(ROOT.kSpring - 1, 'mpl'), 'Di-Boson')
            Zll = Sample('Zll', convert_color(ROOT.kCyan - 10, 'mpl'), 'Z#rightarrowll')
            Top = Sample('Top', convert_color(ROOT.kOrange + 1, 'mpl'), 'Top')
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV', 'W'])
            self.backgrounds = [
                Ztt, Fake, Zll, Top, Others
                ]
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'VV', 'Top', 'Zll', 'W']
        elif channel == 'lephad':
            Ztt = Sample(
                'Ztt', convert_color(ROOT.kAzure + 1, 'mpl'), 'Z#rightarrow#tau#tau', sub_samples=['Ztt', 'ZttEWK'])
            Fake = Sample('Fake', 'yellow', 'Fakes')
            Top = Sample('Top', convert_color(ROOT.kOrange + 1, 'mpl'), 'Top')
            Zll = Sample('Zll', convert_color(ROOT.kCyan - 10, 'mpl'), 'Z#rightarrowll', sub_samples=['Zll', 'ZllEWK'])
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV'])
            self.backgrounds = [
                Ztt, Fake, Zll, Top, Others
                ]
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'Top', 'Zll', 'ZllEWK', 'VV']
        else:
            raise ValueError('Wrong channel')
            

        


class systematic(object):

    def __init__(self, name):
        self._samples = []
        self._categories = []
    

    def affected_samples(self):
        return self._samples

    def affected_categories(self):
        return self._categories
