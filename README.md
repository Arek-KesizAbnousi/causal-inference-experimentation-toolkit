# Causal Inference & Experimentation Toolkit

## Description

This project provides a toolkit for designing and analyzing controlled experiments (**A/B tests**) and other causal inference analyses. It demonstrates key data science skills in experimental design, statistical analysis, and causal methods. The toolkit includes:

- **A/B Testing Utilities** – Functions for power analysis and sample size calculation (to plan experiments), hypothesis testing (t-tests for differences in means), and a variance reduction technique called **CUPED** (using pre-experiment data to reduce variance and save ~15–20% sample size).
- **Difference-in-Differences Analysis** – Tools to perform a two-way fixed effects analysis on simulated panel data, isolating causal effects in a pre/post study with treatment and control groups.
- **Simulation Validation** – Scripts to validate the statistical rigor of experiments (e.g., running 1000 A/A tests to ensure ~5% false positive rate and ~95% confidence interval coverage, as expected).

This toolkit is implemented in Python and uses libraries like NumPy and SciPy for statistical computations. It aligns with industry practices for experiment analysis (e.g., as used in tech companies for product improvements).

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Acknowledgments](#acknowledgments)

## Project Overview

**Causal Inference & Experimentation Toolkit** is a self-contained project showcasing how to design experiments and apply causal inference techniques to glean insights from data. It was developed to demonstrate competencies in:

- **Experimental Design:** Determining how large an experiment needs to be to detect a meaningful effect (power and sample size analysis).
- **Statistical Testing:** Implementing hypothesis tests (t-tests) to compare experimental groups and validate results.
- **Causal Inference Methods:** Using advanced techniques like CUPED and Difference-in-Differences to improve estimate accuracy and handle observational data.
- **Analytical Rigor:** Verifying that methods are statistically sound (e.g., calibrating false positive rates through simulation).

The repository contains code to perform these analyses on synthetic data, but the methods can be applied to real-world product or business experiments (e.g., user conversion lift from a new feature, or revenue impact of an ad strategy change).

## Project Structure
```plaintext
causal-inference-experimentation-toolkit/
├── experiment_toolkit.py # Core Python module with toolkit functions
├── example_usage.py # Example script demonstrating usage of the toolkit
├── images/
│ └── did_plot.png # Illustration of Difference-in-Differences (used in README)
├── requirements.txt # (Optional) Dependencies like numpy and scipy
└── README.md # Project documentation (you are reading this)
```

- **`experiment_toolkit.py`:** Contains the implementation of functions for power calculations, minimum detectable effect, t-tests, CUPED adjustment, and diff-in-diff analysis.
- **`example_usage.py`:** Runs through examples of using the toolkit:
  - Calculating required sample size and minimum detectable effect.
  - Simulating 1000 A/A tests to check false positive rate and confidence interval coverage.
  - Demonstrating CUPED on synthetic data (showing variance reduction).
  - Simulating a Difference-in-Differences scenario and estimating the treatment effect.
- **`images/did_plot.png`:** A plot illustrating the difference-in-differences outcome for a treatment vs. control group over time (used in the README for visual aid).

## Installation

This project requires **Python 3.x** and the following Python packages:
- **NumPy**
- **SciPy**

You can install the dependencies using pip:

```bash
pip install numpy scipy
```
## Usage 

You can use the toolkit by importing the module functions or by running the provided example script.


  ### 1. Using the toolkit:
  Import the functions from experiment_toolkit.py:

 ### 2. Running the demonstration script:
  
 Execute ```example_usage.py ```to see the toolkit in action with simulated data:
 
 This will output:

- **Power analysis results:** e.g., sample size needed for a given effect, or the minimum detectable effect for a given sample.

- **A/A test validation:** the observed false positive rate and 95% confidence interval coverage across 1000 simulations with no true difference.

- **CUPED demonstration:** the value of the adjustment coefficient (θ) and how much the variance was reduced.

- **Diff-in-Diff analysis:** the estimated effect vs. the true effect and the statistical significance of that estimate.


## Results

To illustrate the kind of analysis this toolkit enables, consider the following Difference-in-Differences scenario:



Figure: Example of a Difference-in-Differences outcome. Both Treatment and Control groups increase over time due to a general trend, but the Treatment group gains an additional lift after the intervention. The diff-in-diff estimator (treatment effect) is the extra increase seen in the Treatment group relative to Control.





In our simulated diff-in-diff test (see example_usage.py), the toolkit correctly estimates the true effect (within simulation error) and reports a statistically significant result (very low p-value), demonstrating that the method works.




Likewise, the A/A test simulations confirm that our t-test implementation yields ~5% false positives (as expected by the 0.05 significance level), and the confidence intervals contain the true difference ~95% of the time. The CUPED example shows a reduction in variance of roughly 15–20%, meaning an experiment could reach the same conclusions with fewer samples when using the adjusted metric.


## Acknowledgments


This project was inspired by common practices in online experimentation and causal analysis. Techniques like CUPED and diff-in-diff are used by data science teams at major tech companies to draw reliable conclusions from data. The implementation here is for demonstration purposes, using simulated data to showcase the methods and their validity.




