import numpy as np
import matplotlib.pyplot as plt
import wobble
from time import time
import glob

if __name__ == "__main__":
    start_time = time()
    # dataset = '_feb' # or '_old' or ''
    # dataset = '_old'
    dataset = ''
    starname = 'video'
    niter = 150 # for optimization
    K_star = 0
    K_t = 3  

    for index in range(18):
        fname = 'data/video_e2ds_%d.hdf5' % index
        dataset = str(index)
        orders = np.arange(40,69)
        data = wobble.Data(fname, orders=orders, min_snr=1, order=4,
                            plot_continuum=False, plot_dir='results/continuum/')
        results = wobble.Results(data=data)
        epochs_to_plot = data.epochs

        print("data loaded")
        print("time elapsed: {0:.2f} min".format((time() - start_time)/60.0))
        elapsed_time = time() - start_time
        
        for r,o in enumerate(orders):
            model = wobble.Model(data, results, r)
            model.add_star('star')#, starting_rvs = np.copy(data.pipeline_rvs))
            model.add_telluric('tellurics',rvs_fixed=True, variable_bases=K_t, 
                                    learning_rate_template=0.01)
            print("--- ORDER {0} ---".format(o))
            wobble.optimize_order(model, niter=niter, save_history=True, basename='results/history',
                                      epochs_to_plot=epochs_to_plot, rv_uncertainties=True, movies=False)
            # plots:
            fig, ax = plt.subplots(1, 1, figsize=(8,5))
            ax.plot(data.dates, results.star_rvs[r] + data.bervs - np.mean(results.star_rvs[r] + data.bervs), 
                    'k.', alpha=0.8)
            #ax.plot(data.dates, data.pipeline_rvs + data.bervs - np.mean(data.pipeline_rvs + data.bervs), 
            #        'r.', alpha=0.5)   
            ax.set_ylabel('RV (m/s)', fontsize=14)     
            ax.set_xlabel('BJD', fontsize=14)   
            plt.savefig('results/results_rvs{0}_o{1}.png'.format(dataset, o))
            plt.close(fig) 
            
            for e in epochs_to_plot:
                fig, (ax, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[4, 1]}, figsize=(12,5))
                xs = np.exp(data.xs[r][e])
                ax.scatter(xs, np.exp(data.ys[r][e]), marker=".", alpha=0.5, c='k', label='data', s=40)
                mask = data.ivars[r][e] <= 1.e-8
                ax.scatter(xs[mask], np.exp(data.ys[r][e][mask]), marker=".", alpha=1., c='white', s=20)
                ax.plot(xs, np.exp(results.star_ys_predicted[r][e]), c='r', alpha=0.8)
                ax2.scatter(xs, np.exp(data.ys[r][e]) - np.exp(results.star_ys_predicted[r][e]), 
                            marker=".", alpha=0.5, c='k', label='data', s=40)
                ax2.scatter(xs[mask], np.exp(data.ys[r][e][mask]) - np.exp(results.star_ys_predicted[r][e])[mask], 
                            marker=".", alpha=1., c='white', s=20)
                ax.set_ylim([0.0,1.4])
                ax2.set_ylim([-0.2,0.2])
                ax.set_xticklabels([])
                fig.tight_layout()
                fig.subplots_adjust(hspace=0.05)
                plt.savefig('results/results_synth{0}_o{1}_e{2}.png'.format(dataset, o, e))
                plt.close(fig)
            '''
            for e in epochs_to_plot:
                fig, (ax, ax2) = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[4, 1]}, figsize=(12,5))
                xs = np.exp(data.xs[r][e])
                ax.scatter(xs, np.exp(data.ys[r][e]), marker=".", alpha=0.5, c='k', label='data', s=40)
                mask = data.ivars[r][e] <= 1.e-8
                ax.scatter(xs[mask], np.exp(data.ys[r][e][mask]), marker=".", alpha=1., c='white', s=20)
                ax.plot(xs, np.exp(results.star_ys_predicted[r][e]), c='r', alpha=0.8)
                ax.plot(xs, np.exp(results.tellurics_ys_predicted[r][e]), c='b', alpha=0.8)
                ax2.scatter(xs, np.exp(data.ys[r][e]) - np.exp(results.star_ys_predicted[r][e]
                                                            + results.tellurics_ys_predicted[r][e]), 
                            marker=".", alpha=0.5, c='k', label='data', s=40)
                ax2.scatter(xs[mask], np.exp(data.ys[r][e][mask]) - np.exp(results.star_ys_predicted[r][e]
                                                            + results.tellurics_ys_predicted[r][e])[mask], 
                            marker=".", alpha=1., c='white', s=20)
                ax.set_ylim([0.0,1.3])
                ax2.set_ylim([-0.08,0.08])
                ax.set_xticklabels([])
                fig.tight_layout()
                fig.subplots_adjust(hspace=0.05)
                plt.savefig('results/results_synth_o{0}_e{1}.png'.format(o, e))
                plt.close(fig)
            '''         
            
                
            print("order {1} optimization finished. time elapsed: {0:.2f} min".format((time() - start_time)/60.0, o))
            print("this order took {0:.2f} min".format((time() - start_time - elapsed_time)/60.0))
            elapsed_time = time() - start_time
            
        results.combine_orders('star')
        
        fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10,5), sharex=True)
        wobble_rvs = results.star_time_rvs + data.bervs - data.drifts
        wobble_rvs -= np.mean(wobble_rvs)
        ax.errorbar(data.dates, wobble_rvs, 
                    results.star_time_sigmas, fmt='o', ls='', c='k', label='wobble', alpha=0.7)
        pipeline_rvs = data.pipeline_rvs + data.bervs
        pipeline_rvs -= np.mean(pipeline_rvs)
        ax2.errorbar(data.dates, pipeline_rvs, 
                    data.pipeline_sigmas, fmt='o', ls='', c='r', label='pipeline', alpha=0.7)
        ax2.set_xlabel('JD')
        ax.set_ylabel(r'wobble RV (m s$^{-1}$)', fontsize=14)
        ax2.set_ylabel(r'pipeline RV (m s$^{-1}$)', fontsize=14)
        fig.tight_layout()
        fig.subplots_adjust(hspace=0.05)
        plt.savefig('results/results_rvs%s.png' % dataset)
        plt.close(fig)

        print("total runtime:{0:.2f} minutes".format((time() - start_time)/60.0))
        
        results.write('results/results_video_%s.hdf5' % dataset)
        
        with open('rvs_%s.csv' % dataset, 'w') as f:
            f.write('JD, RV_wobble, RV_err_wobble, RV_pipeline, RV_err_pipeline\n')
            for i in range(data.N):
                f.write('{0:.8f}, {1:.4f}, {2:.4f}, {3:.4f}, {4:.4f}\n'.format(data.dates[i], 
                        wobble_rvs[i], results.star_time_sigmas[i], pipeline_rvs[i], data.pipeline_sigmas[i]))
    print('Finished!')
            