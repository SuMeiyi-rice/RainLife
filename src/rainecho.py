"""
Echoes of Early Rains: HK Observatory's Debut Data Visualization
An artistic representation of Hong Kong's rainfall data from 1884 to 1885, the first two years.
This visualization centers on the first two years of rainfall data ever recorded by the Hong Kong Observatory
these figures are not just numbers, but the "source" and "starting point" of Hong Kong's rainfall archives.
I wish to evoke these echoes of rain, vanishing into the “long river of time.”
"""

import sys
window_closed = [False]
def handle_close(evt):
    window_closed[0] = True
    plt.close('all')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Data loading
CSV_PATH = r"D:/GitHub/RainLife/daily_HKO_RF_ALL.csv"
df = pd.read_csv(CSV_PATH, header=3,
                 names=['年/Year', '月/Month', '日/Day', '數值/Value', '數據完整性/data Completeness'])
df['數值/Value'] = pd.to_numeric(df['數值/Value'], errors='coerce').fillna(0)
monthly_df = df.groupby(['年/Year', '月/Month'], as_index=False)['數值/Value'].sum()

# Canvas parameters
fig, ax = plt.subplots(figsize=(12.8, 7.2))
fig.set_size_inches(12.8, 7.2, forward=True)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_aspect('equal', adjustable='box')
ax.axis('off')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-0.9, 0.9)

fade_alpha = 0.48
rect = Rectangle((-1.6, -0.9), 3.2, 1.8, color='black', alpha=fade_alpha, zorder=9)
ax.add_patch(rect)

# rain4  Echoes Parameters
SEED = 7
n_arms = 3
r_min, r_max = 0.15, 1.10
spiral_k = 0.085
base_dtheta = 0.04
n_particles_max = 50
rng = np.random.default_rng(SEED)
theta0 = rng.uniform(0, 2*np.pi, n_particles_max)
arm_idx = rng.integers(0, n_arms, n_particles_max)
arm_phase = 2*np.pi * arm_idx / n_arms
dtheta = base_dtheta + rng.uniform(-0.035, 0.035, n_particles_max)
r_base = r_min + 0.6 * rng.random(n_particles_max)
particle_scale = np.random.default_rng(SEED+99).uniform(0.6, 1.5, n_particles_max)
activated_mask = np.zeros(n_particles_max, dtype=bool)
activated_frame = np.full(n_particles_max, -1, dtype=int)
tail_particles = 48
frames_per_month = int(0.4 / 0.015)

frame_offset = 0
ring_patch = None
pulse_patches = []

# Register the close event listener
fig.canvas.mpl_connect('close_event', handle_close)

try:
    for month_idx, row in monthly_df.head(24).iterrows():
        if window_closed[0]:
            break
        rain = float(row['數值/Value'])
        # Normalize rainfall for visualization (50mm-300mm range)
        # rain_norm: 0.0 = 50mm or below, 1.0 = 300mm or above
        # This normalization drives both particle count and color intensity
        rain_norm = np.clip((rain - 50) / (300 - 50), 0, 1)
        n_particles = int(12 + 38 * rain_norm)
        if n_particles < n_particles_max:
            start = (n_particles_max - n_particles) // 2
            end = start + n_particles
            new_indices = range(start, end)
        else:
            new_indices = range(n_particles_max)
        for i in new_indices:
            if not activated_mask[i]:
                activated_frame[i] = frame_offset
        activated_mask[list(new_indices)] = True
        active_indices = np.where(activated_mask)[0]
        # Monthly animation frame loop
        for f in range(frames_per_month):
            if window_closed[0]:
                break
            t_anim = (frame_offset + f) * 0.09
            
            pass
            # --- Echo particles on the upper level ---
            all_x, all_y, all_size, all_color = [], [], [], []
            max_size = 30 + 60 * rain_norm
            min_size = 0.8 + 5 * rain_norm
            for idx, i in enumerate(active_indices):
                scale = particle_scale[i]
                # Color variation based on rainfall intensity:
                # - Low rainfall (≤50mm): White particles only
                # - Medium rainfall (50-300mm): Mixed blue and purple-red particles  
                # - Blue particles: White → Blue (cooler tones for gentle rain)
                # - Purple-red particles: White → Purple → Red (warmer tones for heavy rain)
                is_blue = (i % 2 == 0) if rain_norm > 0.0 else False
                if rain <= 300:
                    if rain_norm <= 0.0:
                        # No significant rainfall (≤50mm): Pure white particles
                        base_rgb = (1.0, 1.0, 1.0)
                    else:
                        if is_blue:
                            # Blue branch: White → Blue transition
                            # As rainfall increases, blue becomes more saturated
                            # Formula: Blue channel = 1.0, Green = 0.3 + 0.7*(1-intensity)
                            base_rgb = (0.0, 0.3 + 0.7*(1-rain_norm), 1.0)
                        else:
                            # Purple-Red branch: White → Purple → Red progression
                            # Represents escalating rainfall intensity with warm colors
                            # Rain_excess amplifies the transition for dramatic effect
                            rain_excess = min(rain_norm*1.5, 1.0)
                            if rain_excess < 0.5:
                                # First half: White to Purple (50-175mm range)
                                base_from = (1.0, 1.0, 1.0)
                                base_to = (0.7, 0.2, 1.0)
                                t = rain_excess / 0.5
                            else:
                                # Second half: Purple to Red (175-300mm range)
                                base_from = (0.7, 0.2, 1.0)
                                base_to = (1.0, 0.1, 0.1)
                                t = (rain_excess - 0.5) / 0.5
                            base_rgb = tuple((1-t)*c1 + t*c2 for c1, c2 in zip(base_from, base_to))
                tail_len = min(tail_particles, frame_offset + f - activated_frame[i] + 1)
                for j in range(tail_len):
                    t = frame_offset + f - j
                    if t < activated_frame[i]:
                        continue
                    theta = theta0[i] + dtheta[i] * t + arm_phase[i]
                    r = r_base[i] + spiral_k * theta
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    fade = 1.0 - j / tail_particles
                    rgb = tuple(0.7 + 0.3 * fade * (c / 1.0) for c in base_rgb)
                    alpha = 0.02 + 0.98 * (fade ** 2.2)
                    size = (min_size + (max_size - min_size) * fade) * scale
                    all_x.append(x)
                    all_y.append(y)
                    all_size.append(size)
                    all_color.append((*rgb, alpha))
            to_remove = [c for c in ax.collections if getattr(c, 'zorder', None) == 10]
            for c in to_remove:
                c.remove()
            ax.scatter(all_x, all_y, s=all_size, c=all_color, zorder=10)
            ax.set_title(f"{int(row['年/Year'])}-{int(row['月/Month'])}  Rain: {rain:.1f} mm", color='w', fontsize=22)
            plt.pause(0.015)
        frame_offset += frames_per_month
except KeyboardInterrupt:
    pass

plt.show()
sys.exit(0)
