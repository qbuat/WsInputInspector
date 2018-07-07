import ROOT
import os
import itertools
import uuid
import array
import math

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

def processed_histogram(h_original, h_weight=None, rebin_width=5.):
    h_copy = h_original.Clone(uuid.uuid4().hex)

    if h_weight is not None:
        for ibin in xrange(h_original.GetNbinsX() + 1):
            original_bin_content = h_original.GetBinContent(ibin)
            weight = h_weight.GetBinContent(h_weight.FindBin(h_original.GetBinCenter(ibin)))
            h_copy.SetBinContent(ibin, original_bin_content * weight)

    xmax = 200.
    xmin = 50.
    n_bins = int(abs(xmax - xmin) / rebin_width)
    new_bins = array.array('d', [xmin + rebin_width * i for i in xrange(n_bins + 1)])
    print [h_copy.GetBinLowEdge(i) for i in xrange(h_copy.GetNbinsX() + 2)]
    h_copy = h_copy.Rebin(n_bins, "", new_bins)
    print [h_copy.GetBinLowEdge(i) for i in xrange(h_copy.GetNbinsX() + 2)]
    return h_copy


def pr_plot(hist_dict, categories, bin_width=5., label='All SRs', error_graph=None):

    others_list = {
        'll': ['Zll', 'Top', 'ggHWW', 'VBFHWW', 'VV'],
        'lh': ['Zll', 'Top', 'Others'],
        'hh': ['Others']
        }
    xmin = 50.
    xmax = 200.
    n_bins = int(abs(xmax - xmin) / bin_width)

    # Define histograms
    h_others = ROOT.TH1F(uuid.uuid4().hex, "Others", n_bins, xmin, xmax)
    h_fake   = ROOT.TH1F(uuid.uuid4().hex, "Fake", n_bins, xmin, xmax)
    h_ztt    = ROOT.TH1F(uuid.uuid4().hex, "Ztt", n_bins, xmin, xmax)
    h_bkg    = ROOT.TH1F(uuid.uuid4().hex, "Bkg", n_bins, xmin, xmax)
    h_signal = ROOT.TH1F(uuid.uuid4().hex, "Signal", n_bins, xmin, xmax)
    h_data   = ROOT.TH1F(uuid.uuid4().hex, "Data", n_bins, xmin, xmax)
    h_model  = ROOT.TH1F(uuid.uuid4().hex, "Model", n_bins, xmin, xmax)
    h_template = ROOT.TH1F(uuid.uuid4().hex, "h_template", n_bins, xmin, xmax)
    r_template = ROOT.TH1F(uuid.uuid4().hex, "r_template", n_bins, xmin, xmax)
    
    # add histograms from the dictionnary
    for cat in categories:
        decay_channel = cat.split('_')[2].replace('chan', '')
        for sample in others_list[decay_channel]:
            h_others.Add(hist_dict[cat][sample])
        
        h_fake .Add(hist_dict[cat]['Fake'])
        h_ztt   .Add(hist_dict[cat]['Ztt'])
        h_signal.Add(hist_dict[cat]['Signal'])
        h_data  .Add(hist_dict[cat]['Data'])

    h_bkg.Add(h_ztt)
    h_bkg.Add(h_fake)
    h_bkg.Add(h_others)
    
    rescale_error = ROOT.TGraphAsymmErrors()
    rescale_error_ratio = ROOT.TGraphAsymmErrors()
    if error_graph:
        for i in xrange(h_bkg.GetNbinsX()):
            bc = h_bkg.GetBinContent(i + 1)
            x = ROOT.Double(0.)
            y = ROOT.Double(0.)
            error_graph.GetPoint(i, x, y)
            e_x_lo = error_graph.GetErrorXlow(i)
            e_x_hi = error_graph.GetErrorXhigh(i)
            e_y_lo = error_graph.GetErrorYlow(i)
            e_y_hi = error_graph.GetErrorYhigh(i)
            r = bc / y if y != 0. else 0.
            rescale_error.SetPoint(i, x, bc)
            rescale_error.SetPointError(i, e_x_lo, e_x_hi, r * e_y_lo, r * e_y_hi)
            rescale_error_ratio.SetPoint(i, x, 0.)
            rescale_error_ratio.SetPointError(i, e_x_lo, e_x_hi, r * e_y_lo, r * e_y_hi)
            
    rescale_error.SetLineWidth(0)
    rescale_error.SetFillStyle(3004)
    rescale_error_ratio.SetFillStyle(3004)

    h_model.Add(h_bkg)
    h_model.Add(h_signal)


    ratio_sig = h_model.Clone("Ratio_signal")
    ratio_sig.Add(h_bkg, -1)
    ratio_sig.SetTitle(ratio_sig.GetName())
    ratio_data = h_data.Clone("Ratio_data")
    ratio_data.Add(h_bkg, -1)
    ratio_data.SetTitle(ratio_data.GetName())

    model_stack = ROOT.THStack("Model", "")
    model_stack.Add(h_fake)
    model_stack.Add(h_others)
    model_stack.Add(h_ztt)
    model_stack.Add(h_signal)
    
    # make it fancy
    decoration = {
        'Others': (ROOT.kViolet + 1, ROOT.kViolet + 1, 0, 0),
        'Fake': (ROOT.kYellow, ROOT.kYellow, 0, 0),
        'Ztt': (ROOT.kAzure + 1, ROOT.kAzure + 1, 0, 0,),
        'Signal': (ROOT.kWhite, ROOT.kRed, 0, 2),
        'Data': (ROOT.kWhite, ROOT.kBlack, 20, 2),
        'Ratio_signal': (ROOT.kWhite, ROOT.kRed, 0, 2),
        'Ratio_data': (ROOT.kWhite, ROOT.kBlack, 20, 2),
        }

    y_max = max(h.GetBinContent(h.GetMaximumBin()) for h in [h_data, h_model])
    for h in [h_others, h_fake, h_ztt, h_signal, h_data, ratio_sig, ratio_data]:
        h.SetFillColor  (decoration[h.GetTitle()][0])
        h.SetLineColor  (decoration[h.GetTitle()][1])
        h.SetMarkerStyle(decoration[h.GetTitle()][2])
        h.SetLineWidth  (decoration[h.GetTitle()][3])
        h.GetYaxis().SetTitle('Events / {0} GeV'.format(int(bin_width)))
    c = ROOT.TCanvas(uuid.uuid4().hex, "", 800, 800)
    c.SetBottomMargin(0.01)
    pad1 = ROOT.TPad(uuid.uuid4().hex, "The pad 80% of the height", 0.0, 0.3, 1.0, 1.0, 0)
    pad2 = ROOT.TPad(uuid.uuid4().hex, "The pad 20% of the height", 0.0, 0.05, 1.0, 0.41, 0)
    pad2.SetBottomMargin(0.25)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    h_template.GetYaxis().SetTitle('Events / {0} GeV'.format(int(bin_width)))
    h_template.GetYaxis().SetRangeUser(0.001, 1.4 * y_max)
    h_template.Draw("HIST")
    model_stack.Draw("same HIST")
    if error_graph:
        rescale_error.Draw('sameE2')
    h_data.Draw('samePE')

    # legend
    legend = ROOT.TLegend(0.65, 0.65, 0.97, 0.93)#- pad1.GetLeftMargin(), 1 - pad1.GetTopMargin())
    legend.AddEntry(h_data, 'Data 2015+2016', 'lp')
    legend.AddEntry(h_signal, 'H#rightarrow#tau#tau (#mu = 1.09)', 'f')
    legend.AddEntry(h_ztt, 'Z#rightarrow#tau#tau', 'f')
    legend.AddEntry(h_others, 'Other Backgr.', 'f')
    legend.AddEntry(h_fake, 'Misidentified #tau', 'f')
    if error_graph:
        legend.AddEntry(rescale_error, 'Uncertainty', 'f')
    legend.Draw('same')

    # labels
    atlas_label = ROOT.TLatex(0.2, 0.88, 'ATLAS Internal')
    atlas_label.SetNDC(True)
    atlas_label.SetTextFont(72)
    atlas_label.SetTextSize(0.05)
    atlas_label.Draw()

    ene_lumi_label = ROOT.TLatex(0.2, 0.82, '#sqrt{s} = 13 TeV, 36.1 fb^{-1}')
    ene_lumi_label.SetNDC(True)
    ene_lumi_label.SetTextFont(42)
    ene_lumi_label.SetTextSize(0.05)
    ene_lumi_label.Draw()

    region_label = ROOT.TLatex(0.2, 0.76, label)
    region_label.SetNDC(True)
    region_label.SetTextFont(42)
    region_label.SetTextSize(0.05)
    region_label.Draw()

    pad1.RedrawAxis()
    pad2.cd()

    r_template.GetXaxis().SetTitle('m_{#tau#tau}^{MMC} [GeV]')
    r_template.GetXaxis().SetTitleOffset(2. * ratio_data.GetXaxis().GetTitleOffset())
    r_template.GetYaxis().SetTitle('Data - Bkg')
    r_template.GetYaxis().SetRangeUser(
        -1.1 * (ratio_data.GetBinContent(ratio_data.GetMaximumBin()) + ratio_data.GetBinError(ratio_data.GetMaximumBin())),
         1.1 * (ratio_data.GetBinContent(ratio_data.GetMaximumBin()) + ratio_data.GetBinError(ratio_data.GetMaximumBin())))
    r_template.SetLineColor(ROOT.kGray)
    r_template.SetLineWidth(2)
    r_template.SetLineStyle(ROOT.kDashed)
    r_template.Draw('HIST')
    rescale_error_ratio.Draw('sameE2')
    ratio_data.Draw("samePE")
    ratio_sig.Draw("sameHIST")
    pad2.RedrawAxis()
    c.Update()
    c.SaveAs("pr_plot_{0}_{1}GeV.pdf".format(label.replace(' ', '_'), int(bin_width)))
    return c



if __name__ == '__main__':

    from AtlasStyle import setStyle
    setStyle(False)
    local_dir = '/Users/quentin/'
    cernbox_dir = 'hleptons/analyses/SM_Run2_Rel20.7/paper_histograms/'

    fit_result = os.path.join(local_dir, cernbox_dir, 'workspaces', 'April2018SingleMuUnblindedData_combinationCBA_HIST.root')
    fit_input = os.path.join(local_dir, 'cernbox/workspaces/02June2018SingleMuWithoutXSuncUnblinded/', 'HTauTau13TeVCombinationCBA_histofile.root')


    hh_5gev = os.path.join(local_dir, 'cernbox/workspaces/htt_5gev_binning', 'hadhad.root')
    lh_5gev = os.path.join(local_dir, 'cernbox/workspaces/htt_5gev_binning', 'lephad_1gev.root')
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
    post_pre_map['VBFHWW'] = 'VBFHWW'
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
    post_5gev_map['VBFHWW'] = 'VBFHWW'
    post_5gev_map['VV'] = 'VV'
    post_5gev_map['Others'] = {'hh': ['Zll', 'Top', 'W', 'VV'], 'lh': ['VV'], 'll': []}

    postfit_pr = {}
    rebin_width = 10.
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
            h_postfit_applied = processed_histogram(h, h_weight=h_w, rebin_width=rebin_width)
            postfit_pr[k][s] = h_postfit_applied
        h_data = get_prefit_hist(rfile_5gev[decay_channel], cat_5gev, 'Data')
        postfit_pr[k]['Data'] = processed_histogram(h_data, rebin_width=rebin_width)

    print postfit_pr


    rfile_error_all = ROOT.TFile('/Users/quentin/hleptons/analyses/SM_Run2_Rel20.7/paper_histograms/workspaces/31MayPaper10GeVWithMGvsSHshapeCombination_HIST.root')
    error_graph_all = rfile_error_all.Get('Htt_yearAll_chanAll_catAll_regsig_selCBA/Error')
    c = pr_plot(postfit_pr, postfit_pr.keys(), bin_width=rebin_width, error_graph=error_graph_all)

    boost_categories = filter(lambda k: 'boost' in k, postfit_pr.keys())
    rfile_error_boost = ROOT.TFile('/Users/quentin/hleptons/analyses/SM_Run2_Rel20.7/paper_histograms/workspaces/31MayPaper10GeVWithMGvsSHshapeBoost_HIST.root')
    error_graph_boost = rfile_error_boost.Get('Htt_yearAll_chanAll_catboost_regsig_selCBA/Error')
    c1 = pr_plot(postfit_pr, boost_categories, bin_width=rebin_width, label='All Boosted SRs', error_graph=error_graph_boost)

    vbf_categories = filter(lambda k: 'vbf' in k, postfit_pr.keys())
    rfile_error_vbf = ROOT.TFile('/Users/quentin/hleptons/analyses/SM_Run2_Rel20.7/paper_histograms/workspaces/31MayPaper10GeVWithMGvsSHshapeVBF_HIST.root')
    error_graph_vbf = rfile_error_vbf.Get('Htt_yearAll_chanAll_catvbf_regsig_selCBA/Error')
    c2 = pr_plot(postfit_pr, vbf_categories, bin_width=rebin_width, label='All VBF SRs', error_graph=error_graph_vbf)
    print boost_categories
