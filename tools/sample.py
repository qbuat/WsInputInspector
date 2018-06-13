from . import log; log = log[__name__]
import math


def sys_envelop(nom, sys_list):
    err = 0
    if nom == 0:
        return err
    for s in sys_list:
        err_s = (s - nom) / nom
        err = math.sqrt(err * err + err_s * err_s)
    return err * nom


class Sample(object):

    def __init__(self, name, color, title, sub_samples=None):
        self._name = name
        self._color = color
        self._title = title
        self.mpl_title = self._title.replace('#', '\\')
        self._sub_samples = sub_samples

    def __str__(self):
        return '{0}: {1}'.format(type(self), self.name) 
    


    def systematics(self, cat, rfile):

        _sys_high = []
        _sys_low = []
        cat_list = cat
        if not isinstance(cat, (list, tuple)):
            cat_list = list(cat)

        if self._sub_samples is None:
            for c in cat_list:
                for h in rfile.Get('{0}/{1}'.format(
                        c, self.name)):
                    if h.name.endswith('_high'):
                        _sys_high.append(h.name)
                    if h.name.endswith('_low'):
                        _sys_low.append(h.name)
        else:
            for samp in self._sub_samples:
                for c in cat_list:
                    for h in rfile.Get('{0}/{1}'.format(
                            c, samp)):
                        if h.name.endswith('_high') and h.name not in _sys_high:
                            _sys_high.append(h.name)
                        if h.name.endswith('_low') and h.name not in _sys_low:
                            _sys_low.append(h.name)


        return [_sys_high, _sys_low]

    def syst_dict(self, cat, rfile):
        sys_high, sys_low = self.systematics(cat, rfile)
        dictionary = {}
        for high in sys_high:
            key = high[:-5]

            low = key + '_low'
            if not low in sys_low:
                low = ''

            if not key in dictionary.keys():
                dictionary[key] = {'high': high, 'low': low}

        for low in sys_low:
            key = low[:-4]

            if key in dictionary.keys():
                continue

            high = key + '_high'
            if not low in sys_low:
                high = ''

            dictionary[key] = {'high': high, 'low': low}
        return dictionary
            



    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def title(self):
        return self._title

    def hist_one_cat(self, rfile, cat, hist_name):

        if self._sub_samples is None:
            try:
                return rfile.Get('{0}/{1}/{2}'.format(
                        cat, self.name, hist_name))
            except:
                if hist_name == 'nominal':
                    raise ValueError('wrong names {0}/{1}/{2}'.format(cat, self.name, hist_name))
                else:
                    print Warning('\t wrong name: {0}, {1}, {2}'.format(cat, self.name, hist_name))
                    log.warning('try to use nominal instead of {}'.format(hist_name))
                    return rfile.Get('{0}/{1}/nominal'.format(
                            cat, self.name))
        else:
            hlist = []
            for s in self._sub_samples:
                try:
                    h = rfile.Get('{0}/{1}/{2}'.format(
                            cat, s, hist_name))
                    hlist.append(h)
                except:
                    print Warning('\t wrong name: {0}, {1}, {2}'.format(cat, s, hist_name))
                    if hist_name != 'nominal':
                        log.warning('try to use nominal instead of {}'.format(hist_name))
                        try:
                            h = rfile.Get('{0}/{1}/nominal'.format(cat, s))
                            hlist.append(h)
                        except:
                            raise ValueError('\t wrong name: nominal does not exist either')

            sum_hist = hlist[0].Clone()
            for h in hlist[1:]:
                sum_hist += h
            return sum_hist

    def hist(self, rfile, cat, name='nominal'):
        if isinstance(cat, str):
            return self.hist_one_cat(rfile, cat, name)
        elif isinstance(cat, (list, tuple)):
            hlist = []
            for c in cat:
                h = self.hist_one_cat(rfile, c, name)
                hlist.append(h)

            sum_hist = hlist[0].Clone()
            for h in hlist[1:]:
                sum_hist += h
            return sum_hist

    def yields(self, rfile, cat, name='nominal', bin_range=None):
        if bin_range is None:
            return self.hist(rfile, cat, name).integral(
                overflow=True, error=True)
        else:
            if not isinstance(bin_range, (list, tuple)):
                raise ValueError
            if len(bin_range) != 2:
                raise ValueError

            xbin1, xbin2 = bin_range[0], bin_range[1]
            return self.hist(rfile, cat, name).integral(xbin1=xbin1, xbin2=xbin2, error=True)


    def yields_systs(self, rfile, cat, sym=True):
        nom, _ = self.yields(rfile, cat)
        yields_high, yields_low = [], []
        systs_high, systs_low = self.systematics(cat, rfile)
        for s in systs_high:
            y, _ = self.yields(rfile, cat, name=s)
            yields_high.append(y)
        for s in systs_low:
            y, _ = self.yields(rfile, cat, name=s)
            yields_low.append(y)
        
        _high, _low = sys_envelop(nom, yields_high), sys_envelop(nom, yields_low)
        if sym == True:
            sys = max(_high, _low)
            if sys != 0:
                return sys
            else:
                return None
        else:
            return _high, _low

