class Sample(object):

    def __init__(self, name, color, title, sub_samples=None):
        self._name = name
        self._color = color
        self._title = title
        print sub_samples
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

    def hist(self, rfile, cat):
        if self._sub_samples is None:
            try:
                return rfile['{0}/{1}/nominal'.format(
                        cat, self.name)]
            except:
                print cat, self.name
                raise ValueError('wrong name 1')

        else:
            hlist = []
            for s in self._sub_samples:
                try:
                    h = rfile['{0}/{1}/nominal'.format(
                            cat, s)]
                except:
                    print cat, s
                    raise ValueError('wrong name 2')
                hlist.append(h)
            sum_hist = hlist[0]
            for h in hlist[1:]:
                sum_hist += h
            return sum_hist
