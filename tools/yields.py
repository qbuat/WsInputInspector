import logging;
import os
logging.basicConfig()
log = logging.getLogger('yields')
log.setLevel(logging.INFO)

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

