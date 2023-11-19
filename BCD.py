import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sig

# X is in shape (ntrials, msamples+1)
# The last column is the image label

ds1 = pd.read_csv("P3TE/loading_data/data_faces_target_6_10t_29i_l3.csv")
labs1 = np.loadtxt("P3TE/loading_data/labels_faces_target_6_10t_29i_l3.csv",
                   delimiter=',',
                   dtype='int')


#####
test_targets = [0, 1, 2, 4, 5, 6, 7, 8]

for j in test_targets:
    X_target = X.iloc[np.where(X['image'] == 3)]
    X_probe = X.iloc[np.where(X['image'] == j)]

    tester = np.arange(len(X))
    tps = np.concatenate((np.where(X['image'] == j), np.where(X['image'] == 3))).flatten()
    xirr_inds = np.delete(tester, tps)
    X_irr = X.iloc[xirr_inds]

    bootstrap_index = 0
    for i in range(100):
        target_inds = np.random.choice(np.arange(len(X_target)), 50, replace=False)
        probe_inds = np.random.choice(np.arange(len(X_probe)), 50, replace=False)
        irr_inds = np.random.choice(np.arange(len(X_irr)), 50, replace=False)

        xtd = X_target.loc[:,X_target.columns != 'image']
        xpd = X_probe.loc[:,X_probe.columns != 'image']
        xid = X_irr.loc[:,X_irr.columns != 'image']

        Xtsamp = xtd.iloc[target_inds]
        Xpsamp = xpd.iloc[probe_inds]
        Xisamp = xid.iloc[irr_inds]

        Xtot = pd.concat([Xtsamp, Xpsamp, Xisamp], ignore_index=True, axis=0)
        xtotbar = Xtot.mean(axis=0)

        xtargetbar_dc = Xtsamp.mean(axis=0) - xtotbar
        xprobebar_dc = Xpsamp.mean(axis=0) - xtotbar
        xirrbar_dc = Xisamp.mean(axis=0) - xtotbar

        dc_corr_PT = np.corrcoef(xprobebar_dc, xtargetbar_dc)[0,1]
        dc_corr_PI = np.corrcoef(xprobebar_dc, xirrbar_dc)[0,1]

        bootstrap_index += (dc_corr_PT > dc_corr_PI)

    print(j, bootstrap_index)

