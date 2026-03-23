import numpy as np


def expected_calibration_error(y_true, y_prob, n_bins=10):
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    bin_ids = np.digitize(y_prob, bins) - 1
    bin_ids = np.clip(bin_ids, 0, n_bins - 1)

    ece = 0.0
    for bin_idx in range(n_bins):
        mask = bin_ids == bin_idx
        if np.any(mask):
            mean_prob = y_prob[mask].mean()
            mean_true = y_true[mask].mean()
            ece += mask.mean() * abs(mean_prob - mean_true)

    return ece