
import numpy as np
import scipy.stats as st

def required_sample_size(effect: float, sigma: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """
    Calculate required sample size per group for a two-sample t-test (two-sided)
    to detect a given effect with specified power and significance level.
    - effect: the difference in means to detect.
    - sigma: standard deviation of the outcome (assumed same for both groups).
    - alpha: significance level (two-sided, e.g., 0.05 for 5%).
    - power: desired statistical power (e.g., 0.8 for 80%).
    Returns: required sample size per group (float).
    """
    # Z critical values for significance and power
    Z_alpha2 = st.norm.ppf(1 - alpha/2)   # two-tailed critical value
    Z_beta = st.norm.ppf(power)          # one-tailed for power (beta = 1-power)
    # Sample size formula for two-sample difference in means (approximate using normal)
    n_per_group = 2 * ((Z_alpha2 + Z_beta) * sigma / effect) ** 2
    return n_per_group

def minimum_detectable_effect(n_per_group: int, sigma: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """
    Calculate the minimum detectable effect size for a given per-group sample size,
    significance level, and power in a two-sample test.
    - n_per_group: sample size in each group.
    - sigma: standard deviation of the outcome.
    - alpha: significance level (two-sided).
    - power: desired power.
    Returns: minimum detectable difference in means.
    """
    Z_alpha2 = st.norm.ppf(1 - alpha/2)
    Z_beta = st.norm.ppf(power)
    # Rearranged formula to solve for effect size given n
    mde = (Z_alpha2 + Z_beta) * sigma * np.sqrt(2 / n_per_group)
    return mde

def t_test(control: np.ndarray, treatment: np.ndarray):
    """
    Perform a two-sample Welch's t-test for difference in means between control and treatment.
    - control, treatment: numpy arrays of observations for each group.
    Returns: (t_statistic, p_value)
    """
    stat, p_val = st.ttest_ind(control, treatment, equal_var=False)
    return stat, p_val

def cuped_adjust(control_pre: np.ndarray, control_post: np.ndarray,
                 treatment_pre: np.ndarray, treatment_post: np.ndarray):
    """
    Apply CUPED adjustment using pre-experiment data.
    - control_pre, control_post: arrays for control group (pre-period metric and post-period outcome).
    - treatment_pre, treatment_post: arrays for treatment group (pre-period metric and post-period outcome).
    Returns: (adjusted_control_post, adjusted_treatment_post, theta).
    """
    # Combine data to calculate overall theta
    X = np.concatenate([control_pre, treatment_pre])
    Y = np.concatenate([control_post, treatment_post])
    theta = np.cov(X, Y, bias=True)[0, 1] / np.var(X)  # Cov(X,Y)/Var(X)
    # Compute grand mean of baseline
    X_mean = np.mean(X)
    # Adjust outcomes
    Y_adjusted = Y - theta * (X - X_mean)
    # Split adjusted outcomes back into control and treatment sets
    n_control = len(control_post)
    Y_adj_control = Y_adjusted[:n_control]
    Y_adj_treatment = Y_adjusted[n_control:]
    return Y_adj_control, Y_adj_treatment, theta


def two_prop_z_test(x1: int, n1: int, x2: int, n2: int, alternative: str = "two-sided"):
    """
    Two-proportion z-test (pooled standard error).
    x1, n1: successes and trials in group 1
    x2, n2: successes and trials in group 2
    alternative: 'two-sided' | 'larger' | 'smaller' (tests p2 - p1)
    Returns: (z_stat, p_value)
    """
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p2 - p1) / se
    if alternative == "two-sided":
        p = 2 * (1 - st.norm.cdf(abs(z)))
    elif alternative == "larger":   # H1: p2 - p1 > 0
        p = 1 - st.norm.cdf(z)
    else:                           # H1: p2 - p1 < 0
        p = st.norm.cdf(z)
    return z, p
    
def diff_in_diff(pre_control: np.ndarray, post_control: np.ndarray,
                 pre_treatment: np.ndarray, post_treatment: np.ndarray,
                 alpha: float = 0.05):
    """
    Difference-in-Differences estimate and Welch CI on the change scores.
    Returns: (effect, t_stat, p_value, ci_lower, ci_upper)
    """
    change_control = post_control - pre_control
    change_treatment = post_treatment - pre_treatment

    diff_effect = np.mean(change_treatment) - np.mean(change_control)

    # Welch t test on change scores
    n1, n0 = len(change_treatment), len(change_control)
    s1, s0 = np.var(change_treatment, ddof=1), np.var(change_control, ddof=1)
    se = np.sqrt(s1/n1 + s0/n0)
    t_stat = diff_effect / se
    # Welch-Satterthwaite df
    df = (s1/n1 + s0/n0)**2 / ((s1**2)/((n1**2)*(n1-1)) + (s0**2)/((n0**2)*(n0-1)))
    p_val = 2 * (1 - st.t.cdf(abs(t_stat), df))
    tcrit = st.t.ppf(1 - alpha/2, df)
    ci_lower, ci_upper = diff_effect - tcrit*se, diff_effect + tcrit*se

    return diff_effect, t_stat, p_val, ci_lower, ci_upper
