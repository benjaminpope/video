import numpy as np
import matplotlib.pyplot as plt
import h5py

if __name__ == '__main__':
    order = 0 # can be 0-28 inclusive
    
    with h5py.File('results/results_video.hdf5') as f:
        wave = np.exp(f['order{0}'.format(order)]['star_template_xs']) # stored in log form
        flux = np.exp(f['order{0}'.format(order)]['star_template_ys'])
        
    plt.plot(wave, flux, color='k')
    plt.ylabel('Normalized Flux', fontsize=14)
    plt.xlabel(r'Wavelength ($\AA$)', fontsize=14)
    plt.show()