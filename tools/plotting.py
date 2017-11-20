import math
import matplotlib.pyplot as plt
import numpy as np

#     set_style('ATLAS', mpl=True)

from rootpy.plotting import Canvas
import ROOT


def yields_chart(rfile, samples, Data, cat, draw_label=True):

    cat_name = cat.name
    cat = cat.cats
    y_pos = np.arange(len(samples))
    x_pos = [s.yields(rfile, cat)[0] for s in samples]
    x_pos_er = [s.yields(rfile, cat)[1] for s in samples]

    #         plt.subplot(len(cats) + 1, 1, ip + 1)
    plt.barh(
        y_pos, x_pos, xerr=x_pos_er, align='center', 
        alpha=0.6 if s.name is 'Data' else 0.9,  
        color=[s.color for s in samples])

    # stacking bar (ugly but works I guess)
    bottom = np.cumsum(np.array([
                s.yields(rfile, cat)[0] for s in samples]),
                       axis=0)
    plt.barh(
        len(samples), samples[0].yields(rfile, cat)[0], 
        xerr=samples[0].yields(rfile, cat)[1],
        align='center', alpha=0.9, color=samples[0].color)
    for isample, s in enumerate(samples[1:]):
        plt.barh(
            len(samples), s.yields(rfile, cat)[0], 
            xerr=s.yields(rfile, cat)[1],
            align='center', alpha=0.9, color=s.color, 
            left=bottom[isample])
    plt.barh(
        len(samples) + 1, Data.yields(rfile, cat)[0], 
        xerr=Data.yields(rfile, cat)[1],
        alpha=0.6, align='center', color=Data.color)
    min, max = plt.xlim()
    plt.xlim(0, max)
    plt.yticks(np.arange(len(samples) + 2), [s.name for s in samples] + ['Total', 'Data'], fontsize=10)
    plt.title(cat_name)
#     plt.xlabel('yield')
#     return plt.figure()

def sample_pie(rfile, samples, cat, no_explode=False):
    
    total = sum([s.yields(rfile, cat)[0] for s in samples])
    fractions = [100. * s.yields(rfile, cat)[0] / total for s in samples]
    explode = [0.1] + [0 for i in xrange(len(fractions) - 1)]
    if no_explode:
        explode = None
    labels = [s.name for s in samples]
    colors = [s.color for s in samples]

    plt.pie(fractions, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.xlabel(cat)
#     fig = plt.figure()
#     ax = fig.gca()
#     return fig


def significance_chart(rfile, sig, bkg, cats):

    y_pos = np.arange(len(cats))
    s_over_b = []
    for cat in cats:
        s_over_b.append(
            sig.yields(rfile, cat)[0] /  bkg.yields(rfile, cat)[0])

    plt.barh(
        y_pos, s_over_b, align='center', 
        alpha=0.4, color='red')
    plt.yticks(y_pos, cats)
    plt.xlabel('s/b ratio')
    plt.tight_layout()
#     plt.savefig('toto.png')
#     return plt.figure()

def syst_yields_chart(rfile, sample, syst, cats):



    y_pos = np.arange(len(cats))
    variations = []
    for cat in cats:
        nom = sample.yields(rfile, cat)[0]
        y_sys =  sample.yields(rfile, cat, name=syst)[0]
        variations.append(1 - y_sys / nom)
    print variations
    plt.barh(
        y_pos, variations, align='center',
        alpha=0.4, color='red')
    plt.yticks(y_pos, cats, fontsize=10)
    plt.tight_layout()
    plt.title(syst)
#     plt.savefig('figures/{0}.png'.format(syst))
#     plt.close()


def raw_np_plot(rfile, syst, cat, sample):

    h_nom  = sample.hist(rfile, cat.cats)
    systs = sample.syst_dict(cat.cats, rfile)

    c = Canvas()
    c.SetRightMargin(0.1)



    h_template = h_nom.Clone()
    h_template /= h_nom
    h_template.fillstyle = '//'
    h_template.fillcolor = 'black'
    h_template.markersize = 0.
    h_template.yaxis.SetRangeUser(0.5, 1.5)
    h_template.xaxis.title = h_nom.xaxis.title
    h_template.yaxis.title = 'Fractional Uncertainty'
    h_template.name = 'Stat_Uncert'
    h_template.title = 'Stat Uncert.'
    h_template.legendstyle = 'f'
    h_template.Draw('E2')

    if systs[syst]['high'] != '':
        do_high = True
        h_high = sample.hist(rfile, cat.cats, systs[syst]['high'])
        h_high_r = h_high.Clone()
        h_high_r /= h_nom
        h_high_r.linewidth = 3
        h_high_r.fillstyle = 0
        h_high_r.color = 'red'
        h_high_r.name = 'high'
        h_high_r.title = 'high'
        h_high_r.legendstyle = 'f'
        h_high_r.Draw('SAMEHIST')
    else:
        do_high = False

        
    if systs[syst]['low'] != '':
        do_low = True
        h_low  = sample.hist(rfile, cat.cats, systs[syst]['low']) 
        h_low_r = h_low.Clone()
        h_low_r /= h_nom
        h_low_r.linewidth = 3
        h_low_r.fillstyle = 0
        h_low_r.color = 'blue'
        h_low_r.name = 'low'
        h_low_r.title = 'low'
        h_low_r.legendstyle = 'f'
        h_low_r.Draw('SAMEHIST')
    else:
        do_low = False

    ROOT.gPad.SetTicks(0, 0)
    max_hist =  1.2 * h_nom.GetBinContent(h_nom.GetMaximumBin())
    right_axis = ROOT.TGaxis(
        ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(),
        ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax(), 
        0, max_hist, 510,"+L")
    right_axis.SetLineColor(ROOT.kViolet)
    right_axis.SetLabelColor(ROOT.kViolet)
    right_axis.SetTextColor(ROOT.kViolet)
    right_axis.SetTitle('')
    right_axis.Draw('same')

    h_nom_draw = h_nom.Clone()
    h_nom_draw *= (ROOT.gPad.GetUymax() - ROOT.gPad.GetUymin()) / max_hist
    for b in h_nom_draw:
        b.value += ROOT.gPad.GetUymin()
    h_nom_draw.color = 'purple'
    h_nom_draw.markersize = 0.5 * h_nom_draw.markersize
    h_nom_draw.name = 'Nominal'
    h_nom_draw.title = 'Nominal'
    h_nom_draw.legendstyle = 'lep'
    h_nom_draw.Draw('sameE')

    syst_label = ROOT.TText(c.GetLeftMargin() + 0.03, 1 - c.GetTopMargin() - 0.04, 'NP: ' + syst)
    syst_label.SetNDC(True)
    syst_label.SetTextSize(20)
    syst_label.Draw('same')

    cat_label = ROOT.TText(c.GetLeftMargin() + 0.03, 1 - c.GetTopMargin() - 0.08, 'Cat.: ' + cat.name)
    cat_label.SetNDC(True)
    cat_label.SetTextSize(20)
    cat_label.Draw('same')

    samp_label = ROOT.TLatex(
        c.GetLeftMargin() + 0.03, 1 - c.GetTopMargin() - 0.12, 
        'Samp.: ' + sample.title)
    samp_label.SetNDC(True)
    samp_label.SetTextSize(20)
    samp_label.Draw('same')

    leg = ROOT.TLegend(
        0.7, 0.75, 1 - c.GetRightMargin(), 1 - c.GetTopMargin())
    leg.AddEntry(h_nom_draw, 'Nominal', 'lep')
    leg.AddEntry(h_template, 'Stat. Uncert.', 'f')
    if do_high:
        leg.AddEntry(h_high_r, 'High', 'l')
    if do_low:
        leg.AddEntry(h_low_r, 'Low', 'l')
    leg.SetTextSize(18)
    leg.SetFillStyle(0)
    leg.Draw()
    c.RedrawAxis()
    c.Update()
    return c
