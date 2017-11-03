import rootpy
log = rootpy.log
log = log['tools']

from .yields import PrettyYield
from .sample import Sample

class Category(object):
    def __init__(self, name, cat_names, is_sr=True, is_cr=False):
        self.name = name
        self.cats = cat_names
        self.is_sr = is_sr
        self.is_cr = is_cr
        self.is_vbf = True
        self.is_boost = False
        if 'boost' in self.name:
            self.is_vbf = False
            self.is_boost = True
        


CATEGORIES_HH = [
    Category('hh vbf lowdr', 'hhAll_cba_vbf_lowdr_signal'),
    Category('hh vbf highdr tight', 'hhAll_cba_vbf_highdr_tight_signal'),
    Category('hh vbf highdr loose', 'hhAll_cba_vbf_highdr_loose_signal'),
    Category('hh boost tight', 'hhAll_cba_boost_tight_signal'),
    Category('hh boost loose', 'hhAll_cba_boost_loose_signal'),
]

CATEGORIES_LL = [
    Category('ll vbf tight', 'llAll_cba_vbf_tight_signal'),
    Category('ll vbf loose', 'llAll_cba_vbf_loose_signal'),
    Category('ll vbf top cr', 'llAll_cba_vbf_top', is_sr=False, is_cr=True),
    Category('ll vbf zll cr', 'llAll_cba_vbf_zll', is_sr=False, is_cr=True),
    Category('ll boost tight', 'llAll_cba_boost_tight_signal'),
    Category('ll boost loose', 'llAll_cba_boost_loose_signal'),
    Category('ll boost top cr', 'llAll_cba_boost_top', is_sr=False, is_cr=True),
    Category('ll boost zll cr', 'llAll_cba_boost_zll', is_sr=False, is_cr=True),
]

CATEGORIES_LH = [
     Category('lh vbf tight', ('mhAll_cba_vbf_loose_signal', 'ehAll_cba_vbf_loose_signal')),
     Category('lh vbf loose', ('mhAll_cba_vbf_tight_signal', 'ehAll_cba_vbf_tight_signal')),
     Category('lh vbf top cr', ('mhAll_cba_vbf_top', 'ehAll_cba_vbf_top'), is_sr=False, is_cr=True),
     Category('lh boost tight', ('mhAll_cba_boost_tight_signal', 'ehAll_cba_boost_tight_signal')),
     Category('lh boost loose', ('mhAll_cba_boost_loose_signal', 'ehAll_cba_boost_loose_signal')),
     Category('lh boost top cr', ('mhAll_cba_boost_top', 'ehAll_cba_boost_top'), is_sr=False, is_cr=True),
]

CATEGORIES_LL_SR = [
    Category('ll vbf tight', 'llAll_cba_vbf_tight_signal'),
    Category('ll vbf loose', 'llAll_cba_vbf_loose_signal'),
    Category('ll boost tight', 'llAll_cba_boost_tight_signal'),
    Category('ll boost loose', 'llAll_cba_boost_loose_signal'),
]

CATEGORIES_LH_SR = [
     Category('lh vbf tight', ('mhAll_cba_vbf_loose_signal', 'ehAll_cba_vbf_loose_signal')),
     Category('lh vbf loose', ('mhAll_cba_vbf_tight_signal', 'ehAll_cba_vbf_tight_signal')),
     Category('lh boost tight', ('mhAll_cba_boost_tight_signal', 'ehAll_cba_boost_tight_signal')),
     Category('lh boost loose', ('mhAll_cba_boost_loose_signal', 'ehAll_cba_boost_loose_signal')),
]


categories = {
    'hadhad': CATEGORIES_HH,
    'lephad': CATEGORIES_LH,
    'leplep': CATEGORIES_LL,
    'lephad_sr': CATEGORIES_LH_SR,
    'leplep_sr': CATEGORIES_LL_SR
}

SAMPLES_NAMES = [
    'VBFH', 'ggH', 'ZH', 'WH', 'ttH',
    'Ztt', 'ZttEWK', 'ZttSh',
    'Fake',
    'Top', 'W', 'Zll', 'VV'
]


SIGNAL_SAMPLES = ['VBFH', 'ggH', 'ZH', 'WH', 'ttH']

OTHER_SAMPLES = ['Top', 'W', 'Zll', 'VV']



SAMPLES = [
    Sample(
        'H', 'red', 'H#rightarrow#tau#tau', 
        sub_samples=SIGNAL_SAMPLES),
    Sample('Ztt', 'blue', 'Z#rightarrow#tau#tau'),
    Sample('Fake', 'green', 'Fake'),
    Sample('Others', 'darkred', 'Others', sub_samples=OTHER_SAMPLES),
    Sample('Data', 'black', 'Data'),
]
