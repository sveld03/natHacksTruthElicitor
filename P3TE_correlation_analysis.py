def spit_out_answers(data_file, label_file, target):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import scipy.signal as sig
    
    dataset = pd.read_csv(data_file);
    labels = np.loadtxt(label_file, delimiter=',', dtype='int');
    
    def create_lab_data(ds, labs, msamps, channels):
        # get trigger col
        ds_trigger = ds['Trigger'].values
    
        # get image events
        img_starts = []
        for i in range(len(ds_trigger) - 1):
            if (ds_trigger[i] == 0) and (ds_trigger[i+1] == 1):
                img_starts.append(i+1)
        img_starts = np.array(img_starts)
        
        # filter signals
        bpfilt = sig.butter(4, (1, 10), 'bandpass', output='sos', fs=250)
        filt_sigs = []
        for i in channels:
            filt_sigs.append(sig.sosfilt(bpfilt, ds[i]))
        filt_sigs = np.array(filt_sigs)
    
        # get EEG values averaged across channels (without O1 and O2)
        channel_avg_eeg = []
        for i in img_starts:
            img_obs = filt_sigs[:,i:i+msamps].mean(axis=0)
            channel_avg_eeg.append(img_obs)
        channel_avg_eeg = np.array(channel_avg_eeg)
    
        # create labeled data
        eeg_img_ds = pd.DataFrame(channel_avg_eeg, columns=list(range(msamps)))
        eeg_img_ds['image'] = labs
    
        return eeg_img_ds
    
    all_channels = ['channel1',
                    'channel2',
                    'channel3',
                    'channel4',
                    'channel5',
                    'channel6',
                    'channel7',
                    'channel8'];
    
    X = create_lab_data(dataset, labels, 250, all_channels);
    
    def pti_bcd_test(X, target, suspects, n_iters, n_samples):
        X_eeg = X.loc[:,X.columns != 'image']
    
        suspect_BIs = {}
        suspect_corrPTs = []
        suspect_corrPIs = []
    
        for suspect in suspects:
            X_target = X_eeg.iloc[np.where(X['image'] == target)]
            X_test_probe = X_eeg.iloc[np.where(X['image'] == suspect)]
    
            tp_inds = np.concatenate((np.where(X['image'] == suspect),
                                      np.where(X['image'] == target))).flatten()
            irrelevant_inds = np.delete(np.arange(len(X)),tp_inds)
            X_irr = X_eeg.iloc[irrelevant_inds]
    
            corrPTs = []
            corrPIs = []
    
            bootstrap_index = 0
            for i in range(n_iters):
                target_inds = np.random.choice(np.arange(len(X_target)), n_samples, replace=False)
                probe_inds = np.random.choice(np.arange(len(X_test_probe)), n_samples, replace=False)
                irr_inds = np.random.choice(np.arange(len(X_irr)), n_samples, replace=False)
    
                X_t_samp = X_target.iloc[target_inds] # random sample of targets
                X_p_samp = X_test_probe.iloc[probe_inds] # random sample of test probes
                X_i_samp = X_irr.iloc[irr_inds] # random sample of irrelevant subjects
    
                X_samp_total = pd.concat([X_t_samp, X_p_samp, X_i_samp],
                                          ignore_index=True,
                                          axis=0)
                X_samp_total_bar = X_samp_total.mean(axis=0)
    
                X_t_bar = X_t_samp.mean(axis=0)
                X_p_bar = X_p_samp.mean(axis=0)
                X_i_bar = X_i_samp.mean(axis=0)
    
                corr_dc_PT = np.corrcoef(X_p_bar - X_samp_total_bar, X_t_bar - X_samp_total_bar)[0,1]
                corr_dc_PI = np.corrcoef(X_p_bar - X_samp_total_bar, X_i_bar - X_samp_total_bar)[0,1]
    
                corrPTs.append(corr_dc_PT)
                corrPIs.append(corr_dc_PI)
    
                bootstrap_index += (corr_dc_PT > corr_dc_PI)
            
            suspect_BIs[suspect] = bootstrap_index / n_iters
            suspect_corrPTs.append(corrPTs)
            suspect_corrPIs.append(corrPIs)
    
            #print(f'Image {suspect} BI positive proportion: {bootstrap_index / n_iters}')
    
        guess = list(suspect_BIs.keys())[np.argmax(list(suspect_BIs.values()))]
        
        X_target = X_eeg.iloc[np.where(X['image'] == target)]
        X_probe = X_eeg.iloc[np.where(X['image'] == guess)]
    
        irr_inds = np.concatenate((np.where(X['image'] == target),
                                   np.where(X['image'] == guess))).flatten()
    
        X_irr = X_eeg.iloc[irr_inds]
    
        plt.plot(X_target.mean(axis=0), label='Target')
        plt.plot(X_probe.mean(axis=0), label='Guessed Probe')
        plt.plot(X_irr.mean(axis=0), label='Irrelevant')
        plt.legend()
    
        return(guess)
        print(suspect_BIs)
    
    suspects = np.arange(10);
    suspects = np.delete(suspects, target);
    return(pti_bcd_test(X, target, suspects, 100, 5));





