from matplotlib.pyplot import *
import my_functions as mf

rcParams['image.cmap'] = 'jet'

# filepaths
path = "C:/Users/Michał/Desktop/Mat2Py/3D_test"
sfile = "3D_OXO_mysz_15x15_1.5Gcm_10ms_4.5s_AVG100.sdat"
pfile = sfile.replace('sdat', 'pdat')
fullfile_sdat = path + '/' + sfile
fullfile_pdat = path + '/' + pfile

# load sdat and pdat
pars = np.fromfile(fullfile_pdat, dtype=float)
rawdata = np.fromfile(fullfile_sdat, dtype=float)

# create acq_pars structure
acq_pars = mf.read_pars(pars)

# extract sino and refs
[sino2d, ref] = mf.sino3D_extract(rawdata, acq_pars)

# RECO PARS
fwhm = 5
nbins = 128
interp_factor = 1
img_type = '3D'
filt = 'ramp'
cutoff = 0.5
algorithm = 'sart'
reco_tup = (fwhm, nbins, interp_factor, img_type, filt, cutoff)
reco_pars = mf.reco_pars(reco_tup, acq_pars)

# sinogram formatting
sino2d = mf.deconvolution(sino2d, ref[:1], reco_pars)
sino_d = sino2d
[sino2d, ref] = mf.interp_nbins(sino2d, ref[:1], reco_pars)
sino2d = mf.interp3D(sino2d, interp_factor, acq_pars)
projs = mf.filtering(sino2d, filt, cutoff)

if algorithm == 'fbp':
    reco = mf.fbp3D(sino2d, reco_pars)
elif algorithm == 'sart':
    reco = mf.sart3D(projs, reco_pars)

# imshow(reco[:,33,:],aspect = 'equal',vmin = 0)
# show()
# mdic = {"reco": reco}
# savemat("reco.mat", mdic)

print('all ok')
