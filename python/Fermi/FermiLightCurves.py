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
    def light_curve(self, source_name, eband='100_300000', duration=86400.,
                    filter_uls=False):
        if ((eband not in self.ebands) or 
            (duration not in self.durations) or
            (source_name not in self.sources)):
            raise RuntimeError("Invalid light curve spec: " + str(locals()))
        flux = self.data.field('FLUX_%s' % eband)
        error = self.data.field('ERROR_%s' % eband)
        ul = self.data.field('UL_%s' % eband)
        if filter_uls:
            index = np.where((self.data.field('NAME') == source_name) & 
                             (ul == False))
        else:
            index = np.where(self.data.field('NAME') == source_name)
        return self.tmid[index], flux[index], error[index], ul[index]

if __name__ == '__main__':
    import pylab_plotter as plot
    plot.pylab.ion()

    lcdata = FermiLightCurveData('gll_asp_0457833600_v00.fit')

    source = '3C 454.3'
    t, f, df, ul = lcdata.light_curve(source)
    win = plot.xyplot(t, f, yerr=df, xname='MJD', yname='flux (ph/cm^2/s)',
                      yrange=(0, 1.1*max(f)))
    win.set_title('%s, 100 to 300000 MeV' % source)
    plot.save('3C_454.3_100_300000.png')

    t1, f1, df1, ul1 = lcdata.light_curve(source, eband='300_1000')
    win1 = plot.xyplot(t1, f1, yerr=df1, xname='MJD', yname='flux (ph/cm^2/s)',
                       yrange=(0, 1.1*max(f1)))
    win1.set_title('%s, 300 to 1000 MeV' % source)
    plot.save('3C_454.3_300_1000.png')

    t2, f2, df2, ul2 = lcdata.light_curve(source, eband='1000_300000')
    win2 = plot.xyplot(t2, f2, yerr=df2, xname='MJD', yname='flux (ph/cm^2/s)',
                       yrange=(0, 1.1*max(f2)))
    win2.set_title('%s, 1000 to 300000 MeV' % source)
    plot.save('3C_454.3_1000_300000.png')

    
