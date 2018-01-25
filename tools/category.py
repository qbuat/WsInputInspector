from . import log; log = log[__name__]

class Category(object):
    def __init__(
        self, name, cat_names, 
        is_sr=True, 
        is_cr=False, 
        is_vbf=False, 
        is_boost=False):
        """
        """
        self.name = name

        if isinstance(cat_names, (list, tuple)):
            self.cats = cat_names
        else:
            self.cats = [cat_names]

        self.is_sr = is_sr
        self.is_cr = is_cr


        if 'boost' in self.name:
            self.is_vbf = False
            self.is_boost = True
        elif 'vbf' in self.name:
            self.is_vbf = True
            self.is_boost = False
        else:
            log.warning('Category {} is neither vbf nor boost'.format(self.name))
            self.is_vbf = False
            self.is_boost = False
