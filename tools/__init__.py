from .yields import PrettyYield
from .sample import Sample

CATEGORIES_15 = [
#     'hh15_QCD_fit',
    'hh15_preselection',
    'hh15_CBA_vbf',
    'hh15_vbf_lowdr',
    'hh15_vbf_highdr_tight',
    'hh15_vbf_highdr_loose',
    'hh15_CBA_boost',
    'hh15_boost_tight',
    'hh15_boost_loose',
]
CATEGORIES_16 = [
#     'hh16_QCD_fit',
    'hh16_preselection',
    'hh16_CBA_vbf',
    'hh16_vbf_lowdr',
    'hh16_vbf_highdr_tight',
    'hh16_vbf_highdr_loose',
    'hh16_CBA_boost',
    'hh16_boost_tight',
    'hh16_boost_loose',
]

CATEGORIES_MERGED = [
#     'hhAll_QCD_fit',
    'hhAll_preselection',
    'hhAll_CBA_vbf',
    'hhAll_vbf_lowdr',
    'hhAll_vbf_highdr_tight',
    'hhAll_vbf_highdr_loose',
    'hhAll_CBA_boost',
    'hhAll_boost_tight',
    'hhAll_boost_loose',
]


SAMPLES_NAMES = [
    'VBFH', 'ggH', 'ZH', 'WH', 'ttH',
    'Ztt', 'Zttewk', 'ZttSh',
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
