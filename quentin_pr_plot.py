import ROOT
import os
import itertools
import uuid

def get_one_hist(root_file, category, sample):
    try:
        return root_file.Get('{0}/{1}/nominal'.format(category, sample))
    except:
        print root_file, category, sample

def get_prefit_hist(root_file, categories, samples):
    """
    """
    if isinstance(categories, (list, tuple)) and isinstance(samples, (list, tuple)):
        combinations = [p for p in itertools.product(categories, samples)]
        return_hist = get_one_hist(root_file, combinations[0][0], combinations[0][1])
        for comb in combinations[1:]:
            return_hist.Add(get_one_hist(root_file, comb[0], comb[1]))
        return return_hist
    else:
        if isinstance(samples, (list, tuple)):
            return_hist = get_one_hist(root_file, categories, samples[0])
            for sample in samples[1:]:
                return_hist.Add(get_one_hist(root_file, categories, sample))
            return return_hist
        elif isinstance(categories, (list, tuple)):
            return_hist = get_one_hist(root_file, categories[0], samples)
            for category in categories[1:]:
                return_hist.Add(get_one_hist(root_file, category, samples))
            return return_hist
        else:
            return get_one_hist(root_file, categories, samples)

def processed_histogram(h_original, h_weight, rebin=False):
    h_copy = h_original.Clone(uuid.uuid4().hex)
    for ibin in xrange(h_original.GetNbinsX() + 1):
        original_bin_content = h_original.GetBinContent(ibin)
        weight = h_weight.GetBinContent(h_weight.FindBin(h_original.GetBinCenter(ibin)))
        h_copy.SetBinContent(ibin, original_bin_content * weight)
    print [h_copy.GetBinLowEdge(i) for i in xrange(h_copy.GetNbinsX() + 2)]
    return h_copy



local_dir = '/Users/quentin/'
cernbox_dir = 'atlas-hleptons/analyses/SM_Run2_Rel20.7/paper_histograms/'

fit_result = os.path.join(local_dir, cernbox_dir, 'workspaces', 'April2018SingleMuUnblindedData_combinationCBA_HIST.root')
fit_input = os.path.join(local_dir, 'cernbox/workspaces/02June2018SingleMuWithoutXSuncUnblinded/', 'HTauTau13TeVCombinationCBA_histofile.root')


hh_5gev = os.path.join(local_dir, 'cernbox/workspaces/htt_5gev_binning', 'hadhad.root')
lh_5gev = os.path.join(local_dir, 'cernbox/workspaces/htt_5gev_binning', 'lephad.root')
ll_5gev = os.path.join(local_dir, 'cernbox/workspaces/htt_5gev_binning', 'leplep.root')


# making the reweighting histograms
rfile_fit_result = ROOT.TFile.Open(fit_result)
rfile_fit_input = ROOT.TFile.Open(fit_input)
keys = rfile_fit_result.GetListOfKeys()
post_pre_map = {}
post_pre_map['Ztt'] = 'Ztt'
post_pre_map['Fake'] = 'Fake'
post_pre_map['Top'] = 'Top'
post_pre_map['Zll'] = 'Zll'
post_pre_map['Signal'] = ['ggH125', 'VBFH125', 'WH125', 'ZH125', 'ttH125']
post_pre_map['ggHWW'] = 'ggHWW'
post_pre_map['ggHWW'] = 'VBFHWW'
post_pre_map['VV'] = 'VV'
post_pre_map['Others'] = 'Others'
weights = {}
for key in keys:
    if 'sig' not in key.GetName():
        continue
    weights[key.GetName()] = {}
    for samp in post_pre_map.keys():
        print 30 * '--'
        print 'Category:', key.GetName()
        postfit_samples = [k.GetName() for k in rfile_fit_result.Get(key.GetName()).GetListOfKeys()]
        # skip if sample not in category
        if samp not in postfit_samples:
            continue
        pre_samp = post_pre_map[samp]
        if samp == 'Others':
            pre_samp = samp + '_' + key.GetName().split('_')[2].replace('chan', '')
            print pre_samp
        
        print 'Postfit Sample:', samp, ', Prefit sample:', pre_samp 
        h_postfit = rfile_fit_result.Get('{0}/{1}'.format(key.GetName(), samp))
        h_prefit = get_prefit_hist(rfile_fit_input, key.GetName(), pre_samp)


        print h_postfit.GetNbinsX(), [h_postfit.GetBinLowEdge(ibin) for ibin in xrange(h_postfit.GetNbinsX() + 1)]
        h_weight = h_postfit.Clone('weight_' + h_postfit.GetName())
        
        for ibin in xrange(h_postfit.GetNbinsX() + 1):
            pre = h_prefit.GetBinContent(ibin)
            post = h_postfit.GetBinContent(ibin)
            print '[{low}, {high}]: {pre}, {post}, {weight}'.format(
                low=h_postfit.GetBinLowEdge(ibin), high=h_postfit.GetBinLowEdge(ibin + 1),
                pre=pre, post=post, weight= post / pre if pre != 0 else 0.)
            h_weight.SetBinContent(ibin, post / pre if pre != 0 else 0.)
        weights[key.GetName()][samp] = h_weight


category_map = {
    'Htt_yearAll_chanll_catboostloose_regsig_selCBA': 'llAll_cba_boost_loose_signal',
    'Htt_yearAll_chanll_catboosttight_regsig_selCBA': 'llAll_cba_boost_tight_signal',
    'Htt_yearAll_chanll_catvbfloose_regsig_selCBA': 'llAll_cba_vbf_loose_signal',
    'Htt_yearAll_chanll_catvbftight_regsig_selCBA': 'llAll_cba_vbf_tight_signal',
    'Htt_yearAll_chanlh_catboostlowpth_regsig_selCBA': ['ehAll_cba_boost_loose_signal', 'mhAll_cba_boost_loose_signal'],
    'Htt_yearAll_chanlh_catboosthighpth_regsig_selCBA': ['ehAll_cba_boost_tight_signal', 'mhAll_cba_boost_tight_signal'],
    'Htt_yearAll_chanlh_catvbfloose_regsig_selCBA': ['ehAll_cba_vbf_loose_signal', 'mhAll_cba_vbf_loose_signal'],
    'Htt_yearAll_chanlh_catvbftight_regsig_selCBA': ['ehAll_cba_vbf_tight_signal', 'mhAll_cba_vbf_tight_signal'],
    'Htt_yearAll_chanhh_catboostloose_regsig_selCBA': 'hhAll_cba_boost_loose_signal',
    'Htt_yearAll_chanhh_catboosttight_regsig_selCBA': 'hhAll_cba_boost_tight_signal',
    'Htt_yearAll_chanhh_catvbflowdr_regsig_selCBA': 'hhAll_cba_vbf_lowdr_signal',
    'Htt_yearAll_chanhh_catvbfhighdrloose_regsig_selCBA': 'hhAll_cba_vbf_highdr_loose_signal',
    'Htt_yearAll_chanhh_catvbfhighdrtight_regsig_selCBA': 'hhAll_cba_vbf_highdr_tight_signal',
}    


rfile_5gev = {
    'll': ROOT.TFile.Open(ll_5gev),
    'lh': ROOT.TFile.Open(lh_5gev),
    'hh': ROOT.TFile.Open(hh_5gev),
}

post_5gev_map = {}
post_5gev_map['Data'] = 'Data'
post_5gev_map['Ztt'] = ['Ztt', 'ZttEWK']
post_5gev_map['Fake'] = 'Fake'
post_5gev_map['Top'] = 'Top'
post_5gev_map['Zll'] = ['Zll' , 'ZllEWK']
post_5gev_map['Signal'] = ['ggH', 'VBFH', 'WH', 'ZH', 'ttH']
post_5gev_map['ggHWW'] = 'ggHWW'
post_5gev_map['ggHWW'] = 'VBFHWW'
post_5gev_map['VV'] = 'VV'
post_5gev_map['Others'] = {'hh': ['Zll', 'Top', 'W', 'VV'], 'lh': ['VV'], 'll': []}

postfit_pr = {}
for k in weights.keys():
    postfit_pr[k] = {}
    samples = weights[k].keys()
    decay_channel = k.split('_')[2].replace('chan', '')
    for s in samples:
        print 
        print k, decay_channel, s
        cat_5gev = category_map[k]
        samp_5gev = post_5gev_map[s]
        if s == 'Others':
            samp_5gev = post_5gev_map[s][decay_channel]
        h_w = weights[k][s]
        print cat_5gev, samp_5gev
        h = get_prefit_hist(rfile_5gev[decay_channel], cat_5gev, samp_5gev)
        h_postfit_applied = processed_histogram(h, h_w)
        postfit_pr[k][s] = h_postfit_applied


print postfit_pr
