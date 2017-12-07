import ROOT
import os
import uuid
from rootpy.plotting import set_style
set_style('ATLAS', shape='rect')
ROOT.gROOT.SetBatch(True)

class correlation_matrix(object):

    def __init__(self, corr_hist):
        self._corr = corr_hist
        self._labels = [str(label) for label in self._corr.GetXaxis().GetLabels()]

    @property
    def names(self):
        return self._labels

    def correlation(self, x, y):
        if not x in self._labels:
            return -999.
        
        if not y in self._labels:
            return -999.

        corr_value = self._corr.GetBinContent(
            self._corr.GetXaxis().FindBin(x),
            self._corr.GetYaxis().FindBin(y))
        return corr_value
        

def correlation_plot(cats, corr_matrices, x_cor, y_cor):
    ""
    ""
    c = ROOT.TCanvas('c_{}'.format(uuid.uuid1().hex), '', 1000, 400)
    c.SetTopMargin(0.1)
    c.SetLeftMargin(0.05)

    size = len(cats)
    ymin, ymax = -1.1, 1.1
    gr = ROOT.TGraphAsymmErrors(size)
    h = ROOT.TH1F('h_{}'.format(uuid.uuid1().hex), 'h_temp', size, 0, size)

    for ic, cat in enumerate(cats):
        corr = corr_matrices[cat].correlation(x_cor, y_cor)
        gr.SetPoint(ic, ic + 0.7, corr)
        gr.SetPointError(ic, 0.5, 0.5, 0, 0)
        h.GetXaxis().SetBinLabel(ic + 1, cat)

    h.GetXaxis().SetTitle('Fit')
    h.GetYaxis().SetTitle('Correlation')
    h.GetXaxis().SetTitleSize(0.5 * h.GetXaxis().GetTitleSize())
    h.GetYaxis().SetTitleSize(0.5 * h.GetYaxis().GetTitleSize())
    h.GetYaxis().SetTitleOffset(0.5)
    h.GetXaxis().SetLabelSize(0.4 * h.GetXaxis().GetLabelSize())
    h.GetYaxis().SetLabelSize(0.5 * h.GetYaxis().GetLabelSize())
    h.GetYaxis().SetRangeUser(ymin, ymax)
    
    ttext = ROOT.TText(
        c.GetLeftMargin(), 1 - c.GetTopMargin() + 0.02,
        'Correlation between {0} and {1}'.format(x_cor, y_cor))
    ttext.SetNDC(True)
    ttext.SetTextSize(20)
    lines = [
        ROOT.TLine(0, 1.0, size, 1.0),
        ROOT.TLine(0, 0.5, size, 0.5),
        ROOT.TLine(0, -0.5, size, -0.5),
        ROOT.TLine(0, -1.0, size, -1.0),
        ]
    h.Draw('HIST')
    gr.Draw('sameP')
    ttext.Draw('same')
    for l in lines:
        l.SetLineStyle(ROOT.kDashed)
        l.Draw('same')
    c.Update()
    return c





DIR = '/Users/quentin/Desktop/19NovFCCoutputs/'

dirs = {
    'comb' : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'll'   : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_ll_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'lh'   : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_lh_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'hh'   : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_hh_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'vbf'  : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_vbf_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'llvbf': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_llvbf_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'lhvbf': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_lhvbf_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'hhvbf': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_hhvbf_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'bst'  : 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_bst_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'llbst': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_llbst_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'lhbst': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_lhbst_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
    'hhbst': 'FitCrossChecks_Bigjob.19NovSingleMuNozttcr_hhbst_Htautau_13TeV_19NovSingleMuNozttcr_Systs_125_combined',
}

cats = ['comb', 'll', 'lh', 'hh', 'vbf', 'llvbf', 'lhvbf', 'hhvbf', 'bst', 'llbst', 'hhbst']


rfiles = {}
corr_matrices = {}
for k, d in dirs.items():
    r = ROOT.TFile(os.path.join(DIR, d, 'FitCrossChecks.root'))
    canv = r.Get('PlotsAfterGlobalFit/unconditionnal/can_CorrMatrix_GlobalFit_unconditionnal_mu1')
    corr_hist = canv.GetListOfPrimitives()[0]
    rfiles[k] = r
    corr_matrices[k] = correlation_matrix(corr_hist)


a = 'SigXsecOverSM'
b = 'ZttTheory_MUR_MUF'
c = correlation_plot(cats, corr_matrices, a, b) 
c.SaveAs('corr.png'.format(a, b))
# for n in corr_matrices['comb'].names:
#     print n



