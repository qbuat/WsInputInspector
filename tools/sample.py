import rootpy
log = rootpy.log
log = log['sample']

class Sample(object):

    def __init__(self, name, color, title, sub_samples=None):
        self._name = name
        self._color = color
        self._title = title
        self._sub_samples = sub_samples
    
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
                return rfile['{0}/{1}/{2}'.format(
                        cat, self.name, hist_name)]
            except:
                raise ValueError('wrong name 1')

        else:
            hlist = []
            for s in self._sub_samples:
                try:
                    h = rfile['{0}/{1}/{2}'.format(
                            cat, s, hist_name)]
                except:
                    raise ValueError('wrong name 2')
                hlist.append(h)
            sum_hist = hlist[0]
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

            sum_hist = hlist[0]
            for h in hlist[1:]:
                sum_hist += h
            return sum_hist

