import os
import argparse
import rootpy
import array
from rootpy.io import root_open
from rootpy.plotting import Hist
from prettytable import PrettyTable
log = rootpy.log 
log = log['comparator']


categories = {
    'vbf_highdr_loose': {
        'eric': 'hh15_vbf_highdr_loose',
        'laurence': 'hh15_vbf_highdr_loose',},
    'vbf_highdr_tight': {
        'eric': 'hh15_vbf_highdr_tight',
        'laurence': 'hh15_vbf_highdr_tight',},
    'vbf_lowdr': {
        'eric': 'hh15_vbf_lowdr',
        'laurence': 'hh15_vbf_lowdr',},
    'boost_tight': {
        'eric': 'hh15_boost_tight',
        'laurence': 'hh15_boost_tight',},
    'boost_loose': {
        'eric': 'hh15_boost_tight',
        'laurence': 'hh15_boost_tight',},
}        
    
samples = {
    'VBFH': {'eric': 'VBFH', 'laurence': 'VBFH'},
    'ggH': {'eric': 'ggH', 'laurence': 'ggH'},
    'ZH': {'eric': 'ZH', 'laurence': 'ZH'},
    'WH': {'eric': 'WH', 'laurence': 'WH'},
    'ttH': {'eric': 'ttH', 'laurence': 'tth'},
    'Ztt': {'eric': 'Ztt', 'laurence': 'Ztt'},
    'Fake': {'eric': 'Fake', 'laurence': 'Fake'},
    'Data': {'eric': 'Data', 'laurence': 'Data'},
    'Others': {'eric': None, 'laurence': 'Others'},
}



def h_others(file, cat, h_name='nominal'):
    htop = file[cat + '/Top/' + h_name]
    h_vv = file[cat + '/VV/' + h_name]
    h_W =  file[cat + '/W/' + h_name]
    h_zll =  file[cat + '/Zll/' + h_name]
    hothers = htop.Clone()
    hothers.Reset()
    hothers.name = 'others'
    hothers = htop + h_vv + h_W + h_zll
    return hothers

def rebin_eric(h, cat):

    htemp = h.Clone()
    if cat == 'hh15_boost_loose':
        bins = array.array('d', [50, 65, 75, 85, 95, 110, 135, 150, 200])
        rebin_h = htemp.Rebin(8, h.name, bins)
    elif cat == 'hh15_boost_loose':
        bins = array.array('d', [50, 80, 110, 135, 150, 200])
        rebin_h = htemp.Rebin(5, h.name, bins)
    elif cat == 'hh15_vbf_highdr_loose':
        bins = array.array('d', [50, 80, 110, 135, 150, 200])
        rebin_h = htemp.Rebin(5, h.name, bins)
    elif cat == 'hh15_vbf_highdr_tight':
        bins = array.array('d', [50, 80, 110, 135, 150, 200])
        rebin_h = htemp.Rebin(5, h.name, bins)
    elif cat == 'hh15_vbf_lowdr':
        bins = array.array('d', [50, 90, 110, 135, 150, 200])
        rebin_h = htemp.Rebin(5, h.name, bins)
    return rebin_h

def rebin_laurence(h):
    bins = list(h.xedges())
    new_bins = [50] + bins[1:-2] + [200]
    hnew = Hist(new_bins)
    for i in xrange(h.GetNbinsX() + 1):
        hnew.SetBinContent(i, h.GetBinContent(i))
        hnew.SetBinError(i, h.GetBinError(i))
    hnew.name = h.name
    hnew.title = h.title
    return hnew

def remap_hist(h):
    h_remapped = Hist(h.GetNbinsX(), 0, h.GetNbinsX())
    print h, type(h)
    for ibin in xrange(h_remapped.GetNbinsX() + 1):
        h_remapped.SetBinContent(ibin, h.GetBinContent(ibin))
    h_remapped.name = h.GetName() + '_remap'
    return h_remapped


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    parser.add_argument('file2')

    args = parser.parse_args()
    log.info('start')


    log.info('Laurence')
    with root_open(args.file1) as f1:
        for cat, sample, c in f1.walk():
            print "'{0}',".format(cat)

    log.info('Eric')
    with root_open(args.file2) as f2:
        for a, b, c, in f2.walk():
            print "'{0}',".format(a)


    yields = {}
    for k, cat in categories.items():
        log.info(100 * '-')
        log.info('')
        log.info(cat)
        log.info('')
        yields[k] = {}
        for s, sample in samples.items():
            if s in ('ZH', 'WH', 'ttH'):
                continue
            #             log.info(sample)
            h1 = root_open(args.file1)['{0}/{1}/nominal'.format(
                    cat['laurence'], sample['laurence'])]

            if s is not 'Others':
                h2 = root_open(args.file2)['{0}/{1}/nominal'.format(
                        cat['eric'], sample['eric'])]
            else:
                h2 = h_others(root_open(args.file2), cat['eric'])

            yields[k][s] = {
                'laurence': h1.Integral(0, h1.GetNbinsX() + 1),
                'eric': h2.Integral(0, h2.GetNbinsX() + 1),
                'diff': h1.Integral(0, h1.GetNbinsX() + 1) - h2.Integral(0, h2.GetNbinsX() + 1)}
            
            log.info(list(h1.xedges()))
#             log.info(rebin_laurence(h1))
            log.info(list(h2.xedges()))
    cats = [c for c in categories.keys()]
    tab = PrettyTable(['Sample', 'analyser'] + cats)
    def process_line(tab, sample):
        tab.add_row([
                sample, 'eric'] + [yields[c][sample]['eric'] for c in cats])
        tab.add_row([
                '', 'laurence'] + [yields[c][sample]['laurence'] for c in cats])
        tab.add_row([
                '', 'diff'] + [yields[c][sample]['diff'] for c in cats])
        tab.add_row(['' for i in xrange(len(cats) + 2)])
    process_line(tab, 'Data')
    process_line(tab, 'Ztt')
    process_line(tab, 'Fake')
    process_line(tab, 'Others')
    process_line(tab, 'ggH')
    process_line(tab, 'VBFH')
#     process_line(tab, 'ZH')
#     process_line(tab, 'WH')


    print tab
