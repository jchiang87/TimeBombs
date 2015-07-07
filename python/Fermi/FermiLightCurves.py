import numpy as np
import pyfits

def mjd(met):
    met0 = 240019201.
    mjd0 = 54688.
    return mjd0 + (met - met0)/86400.

class FermiLightCurveData(object):
    def __init__(self, infile):
        self._hdu = pyfits.open(infile)['LIGHTCURVES']
        self.data = self._hdu.data
        self.sources = sorted(list(self._column_values('NAME')))
        self.ebands = ('100_300000', '300_1000', '1000_300000')
        self.durations = sorted(list(self._column_values('DURATION')))
        self.tmid = mjd((self.data.field('START') + self.data.field('STOP'))/2.)
    def _column_values(self, colname):
        return set(self.data.field(colname))
    def light_curve(self, source_name, eband='100_300000', duration=86400.):
        if ((eband not in self.ebands) or 
            (duration not in self.durations) or
            (source_name not in self.sources)):
            raise RuntimeError("Invalid light curve spec: " + str(locals()))
        flux = self.data.field('FLUX_%s' % eband)
        error = self.data.field('ERROR_%s' % eband)
        ul = self.data.field('UL_%s' % eband)
        index = np.where(self.data.field('NAME') == source_name)
        return self.tmid[index], flux[index], error[index], ul[index]

if __name__ == '__main__':
    import pylab_plotter as plot
    plot.pylab.ion()

    lcdata = FermiLightCurveData('gll_asp_0457833600_v00.fit')

    t, f, df, ul = lcdata.light_curve('3C 454.3')
    plot.xyplot(t, f, df, yrange=(0, 1.1*max(f)))

    t, f, df, ul = lcdata.light_curve('3C 454.3', eband='300_1000')
    plot.xyplot(t, f, df, yrange=(0, 1.1*max(f))).set_title('300 to 1000')

    t, f, df, ul = lcdata.light_curve('3C 454.3', eband='1000_300000')
    plot.xyplot(t, f, df, yrange=(0, 1.1*max(f))).set_title('1000 to 30000')

    
