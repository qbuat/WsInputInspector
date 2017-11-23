import os

from tools.plotting import raw_np_plot
from tools import (CATEGORIES_VBF_MERGED, CATEGORIES_BOOST_MERGED, 
                   CATEGORIES_LL, CATEGORIES_HH, CATEGORIES_LH)

from tools.analysis import measurement
from rootpy.io import root_open
from rootpy.plotting import set_style
import ROOT
set_style('ATLAS', shape='rect')
ROOT.gROOT.SetBatch(True)
from tools import log; log = log[__name__]


def make_plot(meas, categories, sample='Ztt', key_filter=None, no_plotting=False):
    
    for cat in categories:
        if cat.is_cr:
            continue

        samp = meas.get_sample(sample)
        systs = samp.syst_dict(cat.cats, meas.rfile)
        if key_filter is None:
            keys = sorted(systs.keys())
        else:
            keys = filter(lambda s: key_filter in s, systs.keys())
            keys = sorted(keys)

        log.info('Make plot for NPs:')
        for k in keys:
#             log.info('\t {}'.format(k))
            if no_plotting:
                continue
            c = raw_np_plot(meas.rfile, k, cat, samp)
            c.SaveAs('plots/{}_{}_{}_{}.pdf'.format(meas.channel, cat.name.replace(' ', '_'), sample, k))


# hh_file = root_open('/Users/quentin/cernbox/workspaces/htt_sept28/hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar_rebinned.root')
# hh_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar.root')
# lh_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/lephad_fs46_MMC_Fine_BL_WithModJERVar_WithTheoryEnv.root')
# hh_file = root_open('data/hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar_rebinned.root')
# lh_file = root_open('data/lephad_fs46_MMC_Fine_BL_WithModJERVar_WithTheoryEnv_rebinned.root')
# ll_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/leplep_17-09-26.all.dilep_pt_rebin_fake_WithTheoryEnv_WithModJERVar.root')

hh_file = root_open('/Users/quentin/cernbox/workspaces/htt_nov23/hhAll_merged_WSinput_rebinned_WithTheoryEnv_WithModJERVar.root')
lh_file = root_open('/Users/quentin/cernbox/workspaces/htt_nov20/lephad_mh0059_MMC_rebinned_WithModJERVar_WithTheoryEnv.root')
ll_file = root_open('/Users/quentin/cernbox/workspaces/htt_nov23/leplep_17-11-22.EE-MM-DF-split.MGZttShowerSys.newFakes.mmc_mlm.rebin_WithTheoryEnv_WithModJERVar_fakes.root')
# ll_file = root_open('/Users/quentin/cernbox/workspaces/htt_nov20/leplep_17-11-03.all.dilep_pt_rebin_WithTheoryEnv_WithModJERVar_fakes.root')

# ll_file = root_open('leplep_17-09-26.all.dilep_pt_rebinned.root')

hh_m =  measurement(hh_file, 'hadhad')
lh_m =  measurement(lh_file, 'lephad')
ll_m =  measurement(ll_file, 'leplep')

measurements = [
    hh_m, 
    lh_m, 
    ll_m
    ]

# np_name = 'theory_ztt_qsf'

make_plot(ll_m, CATEGORIES_LL, sample='Ztt', key_filter='ckk', no_plotting=False)

# make_plot(lh_m, CATEGORIES_LH, sample='Fake', key_filter='fake', no_plotting=False)
#make_plot(hh_m, CATEGORIES_HH, sample='Ztt', key_filter=None, no_plotting=False)

# make_plot(measurements, CATEGORIES_VBF_MERGED, no_plotting=True)

# make_plot(measurements, [CATEGORIES_BOOST_MERGED[2]], no_plotting=False)
# make_plot(measurements, [CATEGORIES_VBF_MERGED[2]], no_plotting=False)

# make_plot(measurements, CATEGORIES_LL, no_plotting=False)

# for meas, cat in zip(measurements, CATEGORIES_BOOST_MERGED):
#     ztt = meas.get_sample('Ztt')
#     systs = ztt.syst_dict(cat.cats, meas.rfile)
#     keys = filter(lambda s: 'theory' in s, systs.keys())
#     print meas.channel
#     for k in keys:
#         print '\t', k
#         c = raw_np_plot(meas.rfile, k, cat, ztt)
#         c.SaveAs('plots/{}_{}_{}.pdf'.format(k, meas.channel, cat.name.replace(' ', '_')))

# for meas, cat in zip(measurements, CATEGORIES_VBF_MERGED):
#     ztt = meas.get_sample('Ztt')
#     c = raw_np_plot(meas.rfile, np_name, cat, ztt)
#     c.SaveAs('{}_{}_{}.pdf'.format(np_name, meas.channel, cat.name.replace(' ', '_')))

# print [c.name for c in CATEGORIES_VBF_MERGED]
