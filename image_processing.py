import glob
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astroquery.astrometry_net import AstrometryNet
from astride import Streak
from astropy.io import fits
from astropy.wcs import WCS
from skyfield.api import Topos, load, S, E
from skyfield.toposlib import wgs84




def find_streaks():

    plt.style.use(astropy_mpl_style)
    for filename in glob.glob("*.fits"):
        fits.info(filename)
        # Read a fits image and create a Streak instance.
        streak = Streak(filename)

        # Detect streaks.
        streak.detect()

        # Write outputs and plot figures.
        streak.write_outputs()
        streak.plot_figures()


def plate_solve():
    ast = AstrometryNet()
    # this is an api key just for my account I think, you can probably use it though, 
    # can't remember exactly but if you get stuck maybe I can help you. Let me now
    ast.api_key = 'fzyialllobrsoflj'
    f = open('headers.txt', "w")

    for filename in glob.glob("*.fits"):
        hdu = fits.open(filename)
        print("\nPlate solving for " + filename)
        file_header = ast.solve_from_image(filename, force_image_upload=True) # parameters can be adjusted for faster solve
        hdu[0].header = file_header
        # create seperate .fits file with different header
        hdu.writeto(filename.strip('.fits') + '_platesolved.fits')

    print('\nFinished')


def compute_radec():
    # two images which have 3 unique points
    image1_name = 'L_00008'
    # image2_name = 'L_00009'
    # pixel values of the points which I found in gimp
    position1 = [3855, 1540]
    # position1 = [4536, 1074]
    # position2 = [2588, 790]
    # position3 = [742, 524]
    # location in auckland
    lat, lon, alt = -36.8866372, 174.845310, 60

    hdu1 = fits.open(image1_name + '.fits')
    hdu1_ps = fits.open(image1_name + '_platesolved.fits')
    # hdu2 = fits.open(image2_name + '.fits')
    # hdu2_ps = fits.open(image2_name + '_platesolved.fits')

    t1 = hdu1[0].header
    # t2 = hdu2[0].header
    w1 = WCS(hdu1_ps[0].header)
    # w2 = WCS(hdu2_ps[0].header)

    sky1 = w1.pixel_to_world(position1[0], position1[1])
    # sky2 = w1.pixel_to_world(position2[0], position2[1])
    # sky3 = w2.pixel_to_world(position3[0], position3[1])

    # for use in orbdetpy
    # real_obs = [[t1['DATE-OBS'] + 'Z', sky1.ra.value, sky1.dec.value]],
                # ['2021-02-18T09:00:01.6032613Z', sky2.ra.value, sky2.dec.value],
                # [t2['DATE-OBS'] + 'Z', sky3.ra.value, sky3.dec.value]]

    # ts = load.timescale()
    # site = wgs84.latlon(36.8866372 * S, 174.845310 * E, elevation_m=60)
    # satellite = load.tle_file('44064')
    # difference = satellite - site
    # difference.at(ts.tt_jd())
    # difference.at(ts.tt_jd())


    return real_obs

if __name__ == "__main__":
    compute_radec()
