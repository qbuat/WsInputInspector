import math
import matplotlib.pyplot as plt
import numpy as np

#     set_style('ATLAS', mpl=True)




def yields_chart(rfile, samples, Data, cat):

    y_pos = np.arange(len(samples))
    x_pos = [s.yields(rfile, cat)[0] for s in samples]
    x_pos_er = [s.yields(rfile, cat)[1] for s in samples]

    #         plt.subplot(len(cats) + 1, 1, ip + 1)
    plt.barh(
        y_pos, x_pos, xerr=x_pos_er, align='center', 
        alpha=0.6 if s.name is 'Data' else 0.4,  
        color=[s.color for s in samples])

    # stacking bar (ugly but works I guess)
    bottom = np.cumsum(np.array([
                s.yields(rfile, cat)[0] for s in samples]),
                       axis=0)
    plt.barh(
        len(samples), samples[0].yields(rfile, cat)[0], 
        xerr=samples[0].yields(rfile, cat)[1],
        align='center', alpha=0.4, color=samples[0].color)
    for isample, s in enumerate(samples[1:]):
        plt.barh(
            len(samples), s.yields(rfile, cat)[0], 
            xerr=s.yields(rfile, cat)[1],
            align='center', alpha=0.4, color=s.color, 
            left=bottom[isample])
    plt.barh(
        len(samples) + 1, Data.yields(rfile, cat)[0], 
        xerr=Data.yields(rfile, cat)[1],
        alpha=0.6, align='center', color=Data.color)

    plt.yticks(np.arange(len(samples) + 2), [s.name for s in samples] + ['Total', 'Data'], fontsize=10)
    plt.title(cat)
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
