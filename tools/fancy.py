import math
import rootpy
log = rootpy.log
log = log['fancy']

def syst_uncert_builder(rfile, cat='hh16_boost_tight', sample='Ztt'):

    sys_high = []
    sys_low = []

    for _, _, systs in rfile['{0}/{1}/'.format(cat, sample)].walk():
        for sys in systs:
            if 'high' in sys:
                sys_high.append(sys)
            elif 'low' in sys:
                sys_low.append(sys)
            else:
                log.info('skip %s' % sys)

    return sys_low, sys_high


def syst_envelop(hist_nom, hists_low, hists_high):
    '''
    return a high/low variation around the nominal 
    histogram normalized |sys - nom| / nom
    '''
    hist_high = syst_var(hist_nom, hists_high, ext='_syshigh')
    hist_low = syst_var(hist_nom, hists_low, ext='_syslow')
    return hist_low, hist_high

def syst_var(hist_nom, hists_var, ext='_syshigh'):
    hist_var = hist_nom.Clone()
    hist_var.Reset()
    hist_var.name = hist_nom.name + ext
    for ib in xrange(hist_nom.GetNbinsX() + 2):
        bc_nom = hist_nom.GetBinContent(ib)
        if bc_nom == 0:
            log.warning('Bin {0} in {1} is empty!'.format(ib, hist_nom.name))
            hist_var.SetBinContent(ib, 0)
            hist_var.SetBinError(ib, 0)
        else:
            bc_var = 0
            for h in hists_var:
                var = (h.GetBinContent(ib) - bc_nom) / bc_nom
                bc_var += math.sqrt(bc_var * bc_var + var * var)
            hist_var.SetBinContent(ib, bc_var)
            hist_var.SetBinError(ib, 0)
    return hist_var

def envelop(hist_nom, hist_low, hist_high):
    '''
    return the syst + stat envelop normalized as
    |var - nom| / nom
    '''
    hist_env_high = envelop_oneside(hist_nom, hist_high)
    hist_env_low  = envelop_oneside(hist_nom, hist_low)
    return hist_env_low, hist_env_high

def envelop_oneside(hist_nom, hist_var):
    hist_var = hist_nom.Clone()
    hist_var.Reset()
    hist_var.name = hist_nom.name + '_totaluncert'
    for ib in xrange(hist_nom.GetNbinsX() + 2):
        bc_nom = hist_nom.GetBinContent(ib)
        if bc_nom == 0:
            log.warning('Bin {0} in {1} is empty!'.format(ib, hist_nom.name))
            hist_var.SetBinContent(ib, 0)
            hist_var.SetBinError(ib, 0)
        else:
            bc_stat = hist_nom.GetBinError(ib)
            bc_var = (hist_var.GetBinContent(ib) + 1) * bc_nom
            bc_env = math.sqrt(bc_stat * bc_stat + bc_var * bc_var)
            bc_env = math.fabs((bc_env - bc_nom) / bc_nom)
            hist_var.SetBinContent(ib, bc_env)
            hist_var.SetBinError(ib, 0)
    return hist_var

