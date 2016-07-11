import logging;
import os
logging.basicConfig()
log = logging.getLogger(os.path.basename(__file__))
log.setLevel(logging.INFO)


from tools import PrettyYield
from tools import CATEGORIES, SAMPLES, SIGNAL_SAMPLES, OTHER_SAMPLES


LINE = """
{0} & {1} & {2} & {3} & {4} &  \multicolumn{{3}}{{c|}}{{ {5} }} & {6}\\\\
& & & & & {7} & {8} & {9} & \\\\
"""
def latex_line(data, ztt, fakes, top, ewk, diboson, signal, sel='Preselection'):
    y_data = PrettyYield(data)
    y_ztt = PrettyYield(ztt)
    y_fakes = PrettyYield(fakes)
    y_top = PrettyYield(top)
    y_ewk = PrettyYield(ewk)
    y_diboson = PrettyYield(diboson)
    y_signal = PrettyYield(signal)
    y_others = PrettyYield(top + ewk + diboson)
    y_bkg = PrettyYield(ztt + fakes + top + ewk + diboson)
    return LINE.format(
        sel,
        str(y_data),
        str(y_bkg),
        str(y_ztt),
        str(y_fakes),
        str(y_others),
        str(y_signal),
        str(y_top),
        str(y_ewk),
        str(y_diboson))
        


data = PrettyYield(10, stat_uncert=2)
print data

latex_template = """
\\begin{{tabular}}{{r|ccccccc|c}}
\hline
\hline
\multirow{{2}}{{*}}{{Category}} & \multirow{{2}}{{*}}{{Data}} & \multirow{{2}}{{*}}{{Total Bkg.}} & \multirow{{2}}{{*}}{{\DY}} & \multirow{{2}}{{*}}{{Fakes}} & \multicolumn{{3}}{{c|}}{{Others}} & \multirow{{2}}{{*}}{{Signal}}\\\\
\cline{{6-8}}
 & & & & & Top & EWK & Diboson &\\\\
\hline
Preselection & {0:1.2f} & {1:1.2f} $\pm$ {2:1.2f} & {3:1.2f} $\pm$ {4:1.2f & {5:1.2f} $\pm$ {6:1.2f} & \multicolumn{{3}}{{c|}}{{{7:1.2f} $\pm$ {8:1.2f}} & {9:1.2f}\\\\
 & & & & & 1111 $\pm$ 11 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & \\\\
\hline
VBF & 99999 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & \multicolumn{{3}}{{c|}}{{1111 $\pm$ 11}} & 10\\\\
 & & & & & 1111 $\pm$ 11 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & \\\
\hline
Boosted & 99999 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & \multicolumn{{3}}{{c|}}{{1111 $\pm$ 11}} & 10\\\\
 & & & & & 1111 $\pm$ 11 & 1111 $\pm$ 11 & 1111 $\pm$ 11 & \\\\
\hline
\hline
\end{{tabular}}
"""

# latex_line = """
# {16} & {0:1.2f} & {1:1.2f} $\pm$ {2:1.2f} & {3:1.2f} $\pm$ {4:1.2f} & {5:1.2f} $\pm$ {6:1.2f} & \multicolumn{{{3}}}{{c|}}{{ {7:1.2f} $\pm$ {8:1.2f} }} & {9:1.2f}\\\\
#  & & & & & {10:1.2f} $\pm$ {11:1.2f} & {12:1.2f} $\pm$ {13:1.2f} & {14:1.2f} $\pm$ {15:1.2f} & \\\\
# """


def pretty_yield_line(
    data,
    ztautau, 
    fakes,
    ztautau_err=None, fakes_err=None,
    others=None, others_err=None,
    diboson=None, diboson_err=None,
    top=None, top_err=None,
    ewk=None, ewk_err=None,
    total_bkg=None, total_bkg_err=None,
    signal=None,
    name='Preselection'):


    if others is None or top is None or ewk is None or diboson is None:
        log.warning('Can not perform Others background closure test')

    if others is None:
        if top is None or ewk is None or diboson is None:
            log.error('Can not compute Others background')
            raise RuntimeError 

        else:
            log.info('will compute Others from the individual components')
            others = ewk + top + diboson
    else:
        others_alt = ewk + top + diboson
        rel_dif = (others - others_alt) / others * 100.
        if abs(rel_dif) > 1e-2:
            log.warning('Non closure for Others of {0}%'.format(rel_dif))


    if total_bkg is None:
        log.warning('Can not perform total bakground closure test')
        log.info('Will compute the total background from the idnividual components')
    else:
        total_bkg_alt = ztautau + fakes + others
        rel_dif = (total_bkg - total_bkg_alt) / total_bkg * 100.
        log.info(rel_dif)
        if abs(rel_dif) > 1e-2:
            log.warning('Non closure for Total Background of {0}%'.format(rel_dif))
        
#data, ztt, fakes, top, ewk, diboson, signal, sel='Preselection')
    return latex_line(
        data, ztautau, fakes, top, ewk, diboson, signal, sel=name)

#     return latex_line.format(
#         data, total_bkg, total_bkg_err, 
#         ztautau, ztautau_err, fakes, fakes_err,
#         others, others_err,
#         top, top_err,
#         ewk, ewk_err,
#         diboson, diboson_err,
#         signal, name)


line_presel_nodeta = pretty_yield_line(
    3498, # data
    1538.42, #ztt
    1829.19, #fakes
    diboson=12.70,
    top=51.01,
    ewk=68.02 + 0.45,
    total_bkg=3499.8,
    signal=6.49 + 22.32 + 0.29 + 1.36 + 0.75, 
    name='Presel. (no deta)')

line_presel = pretty_yield_line(
    3219, #data
    1519.79, #ztt
    1564.62, #fakes
    diboson=12.43, 
    top=45.14,
    ewk=59.68 + 0.45,
    total_bkg=3202.1, # bkg
    signal=6.19 + 21.41 + 0.27 + 1.36 + 0.71,
    name='Preselection')
    
line_rest = pretty_yield_line(
    1440, #data
    514.90, #ztt,
    907.23, #fakes
    diboson=2.97,
    top=8.67,
    ewk=18.56 + 0.45,
    total_bkg=1452.8,
    signal=0.89 + 7.22 + 0.02 + 0.00 + 0.15,
    name='rest')

line_vbf = pretty_yield_line(
    438, #data,
    211.82, #ztt
    174.67, #fakes
    diboson=1.55,
    top=8.97,
    ewk=8.59 + 0.00,
    total_bkg=405.6,
    signal=3.45 + 3.44 + 0.04 + 0.03 + 0.05,
    name='MVA VBF')

line_boost = pretty_yield_line(
    1341, #data
    793.08, #ztt
    482.72, #fakes
    diboson=7.90,
    top=27.50,
    ewk=32.54 + 0.00,
    signal=1.85 + 10.75 + 0.21 + 1.33 + 0.52,
    name='MVA Boost')

line_vbf_lowdr = pretty_yield_line(
    65, # data,
    49.75, # ztt
    8.84, # fake
    diboson=0.46,
    top=1.11,
    ewk=1.83 + 0.00,
    signal=1.63 + 1.28 + 0.01 + 0.03 + 0.01,
    name='VBF low dR')

line_vbf_highdr_tight = pretty_yield_line(
    71, # data
    29.38, # ztt
    42.75, #fake
    diboson=0.30,
    top=1.51,
    ewk=0.94 + 0.00,
    signal=1.25 + 0.56 + 0.00 + 0.00 + 0.00,
    name='VBF high dR tight')

line_vbf_highdr_loose = pretty_yield_line(
    144, #data
    59.99, # ztt
    60.43, # fake
    diboson=0.34,
    top=1.86,
    ewk=3.76 + 0.00,
    signal=0.49 + 0.66 + 0.00 + 0.00 + 0.01,
    name='VBF high dR loose')

line_boost_tight = pretty_yield_line(
    472,#data
    390.02, # ztt
    68.54, # Fake
    diboson=4.19,
    top=5.90,
    ewk=7.74 + 0.00,
    signal=0.92+ 5.23 + 0.15 + 0.55 + 0.29,
    name='Boost Tight')
    
line_boost_loose = pretty_yield_line(
    800, # data
    394.69, # ztt
    333.12, #fake
    diboson=3.53,
    top=21.51,
    ewk=23.28 + 0.00,
    signal=0.89 + 5.78 + 0.08 + 0.78 + 0.21,
    name='Boost Loose')

print line_presel_nodeta
print '\hline'
print line_presel
print '\hline'
print line_rest
print '\hline'
print line_vbf
print '\hline'
print line_vbf_lowdr
print '\hline'
print line_vbf_highdr_tight
print '\hline'
print line_vbf_highdr_loose
print '\hline'
print line_boost
print '\hline'
print line_boost_tight
print '\hline'
print line_boost_loose
print '\hline'

# print line_presel


if __name__ == '__main__':
    
    import argparse
    from rootpy.io import root_open

    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    args = parser.parse_args()


    rfile = root_open(args.file1, 'read')
    lines = []
    for cat in CATEGORIES:
        log.info(cat)
        
        line = pretty_yield_line(
            int(rfile['{0}/Data/nominal'.format(cat)].Integral()),
            rfile['{0}/Ztt/nominal'.format(cat)].Integral(),
            rfile['{0}/Fake/nominal'.format(cat)].Integral(),
            diboson=rfile['{0}/VV/nominal'.format(cat)].Integral(),
            top=rfile['{0}/Top/nominal'.format(cat)].Integral(),
            ewk=(rfile['{0}/W/nominal'.format(cat)] + rfile['{0}/Zll/nominal'.format(cat)]).Integral(),
            signal=(
                rfile['{0}/VBFH/nominal'.format(cat)] +
                rfile['{0}/ggH/nominal'.format(cat)] +
                rfile['{0}/ZH/nominal'.format(cat)] +
                rfile['{0}/WH/nominal'.format(cat)] +
                rfile['{0}/ttH/nominal'.format(cat)]).Integral(),
            name=cat)
        lines.append(line)


    for line in lines:
        print line
        print '\hline'
