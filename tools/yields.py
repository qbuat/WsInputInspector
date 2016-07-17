import logging;
import os
logging.basicConfig()
log = logging.getLogger('yields')
log.setLevel(logging.INFO)



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
        sel.replace('_', '\_'),
        str(y_data),
        str(y_bkg),
        str(y_ztt),
        str(y_fakes),
        str(y_others),
        str(y_signal),
        str(y_top),
        str(y_ewk),
        str(y_diboson))

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

    return latex_line(
        data, ztautau, fakes, top, ewk, diboson, signal, sel=name)


class PrettyYield(object):

    def __init__(self, nominal, stat_uncert=None, syst_uncert=None):
        self.nominal = nominal

        # stat uncert
        if stat_uncert is None:
            log.warning('No stat uncert')
            self.stat_uncert = None
        elif isinstance(stat_uncert, (float, int)):
            log.info('symmetric stat uncer')
            self.stat_uncert = stat_uncert
        elif isinstance(stat_uncert, (list, tuple)):
            if len(stat_uncert) != 2:
                raise ValueError
                log.error('wrong size of the stat uncert')

            else:
                self.stat_uncert = stat_uncert
                self.stat_uncert_high = stat_uncert[0]
                self.stat_uncert_low = stat_uncert[1]

        # syst uncert
        if syst_uncert is None:
            log.warning('No syst uncert')
            self.syst_uncert = None
        elif isinstance(syst_uncert, (float, int)):
            log.info('symmetric syst uncer')
            self.syst_uncert = syst_uncert
        elif isinstance(syst_uncert, (list, tuple)):
            if len(syst_uncert) != 2:
                log.error('wrong size of the syst uncert')
                raise ValueError
            else:
                self.syst_uncert = syst_uncert
                self.syst_uncert_high = syst_uncert[0]
                self.syst_uncert_low = syst_uncert[1]

    def __str__(self):
        if self.stat_uncert == None:
            if self.syst_uncert == None:
                return '{0:1.2f}'.format(self.nominal)
            elif isinstance(self.syst_uncert, (list, tuple)):
                return '{0:1.2f} \pm X.XX ^{+{1:1.2f}}_{-{2:1.2f}}'.format(
                    self.nominal,
                    self.syst_uncert_high,
                    self.syst_uncert_low)
            else:
                return '{0:1.2f} \pm X.XX \pm {1:1.2f}'.format(
                    self.nominal,
                    self.syst_uncert)
        elif isinstance(self.stat_uncert, (list, tuple)):
            if self.syst_uncert == None:
                return '{0:1.2f} ^{+{1:1.2f}}_{-{2:1.2f}}'.format(
                    self.nominal,
                    self.stat_uncert_high,
                    self.stat_uncert_low)
            elif isinstance(self.syst_uncert, (list, tuple)):
                return '{0:1.2f} ^{+{1:1.2f}}_{-{2:1.2f}} ^{+{3:1.2f}}_{-{4:1.2f}}'.format(
                    self.nominal,
                    self.stat_uncert_high,
                    self.stat_uncert_low,
                    self.syst_uncert_high,
                    self.syst_uncert_low)
            else:
                return '{0:1.2f} ^{+{1:1.2f}}_{-{2:1.2f}}\pm {3:1.2f}'.format(
                    self.nominal,
                    self.stat_uncert_high,
                    self.stat_uncert_low,
                    self.syst_uncert)
        else:
            if self.syst_uncert == None:
                return '{0:1.2f} \pm {1:1.2f}'.format(
                    self.nominal,
                    self.stat_uncert)
            elif isinstance(self.syst_uncert, (list, tuple)):
                return '{0:1.2f} \pm {1:1.2f} ^{+{2:1.2f}}_{-{3:1.2f}}'.format(
                    self.nominal,
                    self.stat_uncert,
                    self.syst_uncert_high,
                    self.syst_uncert_low)
            else:
                return '{0:1.2f} \pm {1:1.2f} \pm {2:1.2f}'.format(
                    self.nominal,
                    self.stat_uncert,
                    self.syst_uncert)

