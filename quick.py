from tools.plotting import raw_np_plot
from tools import CATEGORIES_VBF_MERGED, CATEGORIES_BOOST_MERGED
from tools.analysis import measurement
from rootpy.io import root_open
from tools.analysis import measurement
from rootpy.plotting import set_style
import ROOT
set_style('ATLAS', shape='rect')
ROOT.gROOT.SetBatch(True)



def make_plot(measurements, categories):
    for meas, cat in zip(measurements, categories):
        ztt = meas.get_sample('Ztt')
        systs = ztt.syst_dict(cat.cats, meas.rfile)
        keys = filter(lambda s: 'theory' in s, systs.keys())
        print meas.channel
        for k in keys:
            print '\t', k
            c = raw_np_plot(meas.rfile, k, cat, ztt)
            c.SaveAs('plots/{}_{}_{}.pdf'.format(k, meas.channel, cat.name.replace(' ', '_')))


# hh_file = root_open('/Users/quentin/cernbox/workspaces/htt_sept28/hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar_rebinned.root')
# hh_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar.root')
# lh_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/lephad_fs46_MMC_Fine_BL_WithModJERVar_WithTheoryEnv.root')
# ll_file = root_open('/Users/quentin/cernbox/workspaces/htt_fine_binning/leplep_17-09-26.all.dilep_pt.root')
hh_file = root_open('hhAll_merged_WSinput_WithTheoryEnv_WithModJERVar_rebinned.root')
lh_file = root_open('lephad_fs46_MMC_Fine_BL_WithModJERVar_WithTheoryEnv_rebinned.root')
ll_file = root_open('leplep_17-09-26.all.dilep_pt_rebinned.root')

hh_m =  measurement(hh_file, 'hadhad')
lh_m =  measurement(lh_file, 'lephad')
ll_m =  measurement(ll_file, 'leplep')

measurements = [hh_m, lh_m, ll_m]

# np_name = 'theory_ztt_qsf'

make_plot(measurements, CATEGORIES_BOOST_MERGED)
make_plot(measurements, CATEGORIES_VBF_MERGED)

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
