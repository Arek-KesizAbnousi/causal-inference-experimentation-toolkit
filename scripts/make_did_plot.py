# scripts/make_did_plot.py
import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# Synthetic means (illustrative): both groups rise due to time trend; treatment has extra lift post
ctrl_pre, ctrl_post = 100.0, 110.0          # control: +10 trend
trt_pre,  trt_post  = 100.0, 115.0          # treatment: +10 trend +5 treatment effect

x = np.array([0, 1])                         # 0 = Pre, 1 = Post
ctrl = np.array([ctrl_pre, ctrl_post])
trt  = np.array([trt_pre,  trt_post])

plt.figure(figsize=(6, 4))
plt.plot(x, ctrl, marker="o", label="Control")
plt.plot(x, trt,  marker="o", label="Treatment")
plt.xticks([0, 1], ["Pre", "Post"])
plt.axvline(0.5, linestyle="--", linewidth=1)  # visual split between periods

# Annotate the DiD effect at Post (the extra lift of treatment over control)
did_effect = (trt_post - trt_pre) - (ctrl_post - ctrl_pre)
plt.annotate(
    "Treatment effect (DiD)",
    xy=(1, trt_post), xytext=(0.72, trt_post + 4),
    arrowprops=dict(arrowstyle="->", lw=1)
)

plt.ylabel("Outcome")
plt.title("Difference-in-Differences (illustration)")
plt.legend()
plt.tight_layout()
plt.savefig("images/did_plot.png", dpi=150)
print(f"Saved images/did_plot.png  (DiD effect ≈ {did_effect:.1f})")
