
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

def diff_in_diff(pre_control: np.ndarray, post_control: np.ndarray,
                 pre_treatment: np.ndarray, post_treatment: np.ndarray):
    """
    Compute the Difference-in-Differences estimate given outcomes for control and treatment groups
    before and after an intervention.
    - pre_control, post_control: arrays of outcomes for control group (pre and post intervention).
    - pre_treatment, post_treatment: arrays of outcomes for treatment group (pre and post).
    Returns: (diff_in_diff_estimate, t_statistic, p_value).
    """
    # Calculate change for each unit in each group
    change_control = post_control - pre_control
    change_treatment = post_treatment - pre_treatment
    # Diff-in-diff estimate: difference in average changes
    diff_effect = np.mean(change_treatment) - np.mean(change_control)
    # Statistical test for significance (Welch's t-test on the change scores)
    t_stat, p_val = st.ttest_ind(change_treatment, change_control, equal_var=False)
    return diff_effect, t_stat, p_val
