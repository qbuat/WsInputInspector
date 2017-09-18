from . import log
log = log[__name__]

from sample import Sample

class measurement(object):

    def __init__(self, rfile):

        self.rfile = rfile
        self.categories = self.build_cat_list()
        self.systematics = self.build_syst_list(self)
        self.data = Sample('Data', 'black', 'Data')
        self.background = Sample(
            'TotalBkg', 'blue',
            ['Ztt', 'Zttewk', 'W', 'Zll', 'Top', 'VV', 'Fake'])
        self.others = Sample(
            'Others', 'darkred', 
            ['W', 'Zll', 'Top', 'VV'])


        self.ztt  = Sample(
            'Ztt', 'lightblue', 'Z#rightarrow#tau#tau', 
            sub_samples=['Ztt', 'Zttewk'])

        self.ewk = Sample(
            'ewk', 'orange', 'ewk', 
            sub_samples=['W', 'Zll'])
        self.diboson = Sample('VV', 'black', 'VV')
        self.top = Sample('Top', 'darkblue', 'Top')
        self.fake = Sample('Fake', 'grey', 'Fake')


        self.signal = Sample('Higgs', 'red', ['ggH', 'VBFH', 'WH', 'ZH', 'ttH'])

    def build_cat_list(self):
        return [d for d in self.rfile]

    def build_syst_list(self):
        return []




class systematic(object):

    def __init__(self, name):
        self._samples = []
        self._categories = []
    

    def affected_samples(self):
        return self._samples

    def affected_categories(self):
        return self._categories
