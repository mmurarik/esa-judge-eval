"""Small statistics helpers. Each choice is justified where it is used in REPORT.md / DESIGN.md."""
import numpy as np
from scipy import stats as st


def coincidence(a, b, k=3):
    """k x k coincidence matrix for units with exactly two ratings (codes 0..k-1)."""
    m = np.zeros((k, k))
    np.add.at(m, (a, b), 1)
    return m + m.T


def alpha(o, metric="nominal"):
    """Krippendorff's alpha from a coincidence matrix (Krippendorff 2011, 'Computing Krippendorff's Alpha-Reliability')."""
    k = len(o)
    n_c = o.sum(1)
    n = n_c.sum()
    if metric == "nominal":
        d = 1 - np.eye(k)
    else:  # ordinal
        d = np.zeros((k, k))
        for c in range(k):
            for j in range(c + 1, k):
                d[c, j] = d[j, c] = (n_c[c:j + 1].sum() - (n_c[c] + n_c[j]) / 2) ** 2
    do = (o * d).sum() / n
    de = (np.outer(n_c, n_c) * d).sum() / (n * (n - 1))
    return 1 - do / de if de > 0 else np.nan


def binary(o, positive):
    """Collapse a coincidence matrix to 2 x 2: categories in `positive` vs the rest."""
    pos = np.zeros(len(o), bool)
    pos[list(positive)] = True
    return np.array([[o[np.ix_(~pos, ~pos)].sum(), o[np.ix_(~pos, pos)].sum()],
                     [o[np.ix_(pos, ~pos)].sum(), o[np.ix_(pos, pos)].sum()]])


def cluster_boot(per_cluster, fn, B=2000, seed=20261112):
    """Percentile 95% range, resampling clusters (source passages) with replacement.

    per_cluster: array (n_clusters, ...) of additive summaries; fn maps their sum to a statistic.
    """
    rng = np.random.default_rng(seed)
    n = len(per_cluster)
    out = [fn(per_cluster[rng.integers(0, n, n)].sum(0)) for _ in range(B)]
    return np.nanpercentile(out, [2.5, 97.5])


def cp(k, n, conf=0.95):
    """Two-sided Clopper-Pearson (exact binomial) range."""
    a = 1 - conf
    lo = 0.0 if k == 0 else st.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else st.beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def cp_upper(k, n, conf=0.95):
    """One-sided exact binomial upper bound."""
    return 1.0 if k == n else st.beta.ppf(conf, k + 1, n - k)
