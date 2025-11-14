import numpy as np
from experiment_toolkit import (
    required_sample_size, minimum_detectable_effect,
    t_test, cuped_adjust, diff_in_diff
)

# 1. Power and sample size calculations
alpha = 0.05
power = 0.8
sigma = 1.0
effect = 0.1  # desired effect size to detect (e.g., difference of 0.1 in means)
n_required = required_sample_size(effect=effect, sigma=sigma, alpha=alpha, power=power)
mde_for_100 = minimum_detectable_effect(n_per_group=100, sigma=sigma, alpha=alpha, power=power)
print(f"To detect an effect of {effect} with 80% power at 5% significance, each group needs ~{n_required:.0f} samples.")
print(f"For 100 samples per group, the minimum detectable effect (80% power, 5% alpha) is ~{mde_for_100:.3f}.")

# 2. A/A test simulation (to check false positive rate and CI coverage)
np.random.seed(0)
iterations = 1000
n_per_group = 50
false_positives = 0
ci_misses = 0
alpha = 0.05
for i in range(iterations):
    # Simulate two groups with identical distributions (no true effect)
    control = np.random.normal(0, 1, n_per_group)
    treatment = np.random.normal(0, 1, n_per_group)
    # Perform t-test
    _, p_val = t_test(control, treatment)
    if p_val < alpha:
        false_positives += 1
    # Construct 95% confidence interval for the difference in means
    diff = treatment.mean() - control.mean()
    # Pooled variance estimate for two-sample t (for CI calculation)
    pooled_var = (((n_per_group-1)*np.var(control, ddof=1) + (n_per_group-1)*np.var(treatment, ddof=1))
                  / (2*n_per_group - 2))
    se_diff = np.sqrt(pooled_var * (2 / n_per_group))
    # 95% t critical value
    from scipy.stats import t
    df = 2 * n_per_group - 2
    t_crit = t.ppf(1 - alpha/2, df)
    ci_lower = diff - t_crit * se_diff
    ci_upper = diff + t_crit * se_diff
    # Check if true difference (0) is outside the CI
    if ci_lower > 0 or ci_upper < 0:
        ci_misses += 1

fp_rate = false_positives / iterations * 100
ci_coverage = 100 - (ci_misses / iterations * 100)
print(f"False positive rate over {iterations} A/A tests: {fp_rate:.1f}% (expected ~5%)")
print(f"95% CI coverage over {iterations} A/A tests: {ci_coverage:.1f}% (expected ~95%)")

# 3. CUPED variance reduction demonstration
np.random.seed(1)
N = 1000  # samples per group for demonstration
# Simulate a baseline metric (pre-experiment) and an outcome that depends on the baseline
baseline_ctrl = np.random.normal(0, 1, N)
baseline_treat = np.random.normal(0, 1, N)
# Outcome has a true relationship with baseline (e.g., correlation ~0.5), no actual treatment effect for this demo
outcome_ctrl = 0.5 * baseline_ctrl + np.random.normal(0, 1, N)
outcome_treat = 0.5 * baseline_treat + np.random.normal(0, 1, N)
# Apply CUPED adjustment
adj_ctrl, adj_treat, theta = cuped_adjust(baseline_ctrl, outcome_ctrl, baseline_treat, outcome_treat)
# Calculate variance before and after adjustment
var_before = np.var(np.concatenate([outcome_ctrl, outcome_treat]))
var_after = np.var(np.concatenate([adj_ctrl, adj_treat]))
reduction_percent = (1 - var_after/var_before) * 100
print(f"CUPED adjustment coefficient theta = {theta:.3f}")
print(f"Variance before CUPED: {var_before:.3f}, after: {var_after:.3f} (reduced by ~{reduction_percent:.1f}%)")

# 4. Difference-in-Differences simulation
np.random.seed(2)
n_ctrl_units = 50
n_treat_units = 50
# Each unit has a random baseline level (unit fixed effect)
unit_effect_ctrl = np.random.normal(0, 2, n_ctrl_units)
unit_effect_treat = np.random.normal(0, 2, n_treat_units)
time_effect = 3.0      # common trend affecting all units in post period
treatment_effect = 5.0 # true treatment effect applied to treatment group in post period
# Generate pre-period outcomes
pre_control = unit_effect_ctrl + np.random.normal(0, 1, n_ctrl_units)
pre_treatment = unit_effect_treat + np.random.normal(0, 1, n_treat_units)
# Generate post-period outcomes (add time effect to both, and treatment effect to treatment group)
post_control = unit_effect_ctrl + time_effect + np.random.normal(0, 1, n_ctrl_units)
post_treatment = unit_effect_treat + time_effect + treatment_effect + np.random.normal(0, 1, n_treat_units)
# Compute diff-in-diff estimate and significance
diff_est, t_stat, p_val = diff_in_diff(pre_control, post_control, pre_treatment, post_treatment)
print(f"Diff-in-diff estimate: {diff_est:.2f} (true effect was {treatment_effect})")
print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2e}")
