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
        self.sample_dict = {}

        self.data = Sample('Data', 'black', 'Data')
        self.sample_dict[self.data.name] = self.data

        self.backgrounds = []
        self.background_keys = []

        self.signals = []
        self.signal_keys = []

        self._build_background()
        self._build_signal()

        self.total_background = Sample('Total', 'blue', 'Total Bkg.',sub_samples=self.background_keys)
        self.total_signal = Sample('Higgs', 'red', 'Higgs', ['ggH', 'VBFH', 'WH', 'ZH', 'ttH'])

    def get_sample(self, sample_name):
        return self.sample_dict[sample_name]

    def build_cat_list(self):
        return [d for d in self.rfile]

    def build_syst_list(self):
        return []

    def _build_signal(self):
        self.signals = [
            Sample('VBFH', convert_color(ROOT.kRed +1, 'mpl'), 'VBF'),
            Sample('ggH', convert_color(ROOT.kRed - 1, 'mpl'), 'ggH'),
            Sample('VH', convert_color(ROOT.kRed - 3, 'mpl'), 'VH', ['WH', 'ZH']),
            Sample('ttH', convert_color(ROOT.kRed - 5, 'mpl'), 'ttH'),
            ]
        for s in self.signals:
            self.sample_dict[s.name] = s

    def _build_background(self):
        """
        """
        Ztt = Sample('Ztt', convert_color(ROOT.kAzure + 1, 'mpl'), 'Z#rightarrow#tau#tau', sub_samples=['Ztt', 'ZttEWK'])
        Fake = Sample('Fake', 'yellow', 'Fake' if self.channel == 'hadhad' else 'Fakes')
        Zll = Sample('Zll', convert_color(ROOT.kCyan - 10, 'mpl'), 'Z#rightarrowll', sub_samples=None if self.channel=='hadhad' else ['Zll', 'ZllEWK'])
        Top = Sample('Top', convert_color(ROOT.kOrange + 1, 'mpl'), 'Top')
        
        if self.channel == 'leplep':
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV', 'ggHWW', 'VBFHWW'])
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'Top', 'Zll', 'ZllEWK', 'VV', 'ggHWW', 'VBFHWW']

        elif self.channel == 'lephad':
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV', 'W', 'WEWK'])
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'Top', 'Zll', 'ZllEWK', 'VV', 'W', 'WEWK']

        elif self.channel == 'hadhad':
            Others = Sample('Others', convert_color(ROOT.kViolet + 1, 'mpl'), 'Others', sub_samples=['VV', 'W'])
            self.background_keys = ['Ztt', 'ZttEWK', 'Fake', 'VV', 'Top', 'Zll', 'W']

        else:
            raise ValueError('Wrong channel')
            
        self.backgrounds = [Ztt, Fake, Zll, Top, Others]

        for b in self.backgrounds:
            self.sample_dict[b.name] = b

        


class systematic(object):

    def __init__(self, name):
        self._samples = []
        self._categories = []
    

    def affected_samples(self):
        return self._samples

    def affected_categories(self):
        return self._categories
