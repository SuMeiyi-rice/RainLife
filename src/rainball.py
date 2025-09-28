import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 1. Load CSV and calculate monthly rainfall
CSV_PATH = r"D:/GitHub/RainLife/daily_HKO_RF_ALL.csv"
df = pd.read_csv(CSV_PATH, header=3,
                 names=['年/Year', '月/Month', '日/Day', '數值/Value', '數據完整性/data Completeness'])
df['數值/Value'] = pd.to_numeric(df['數值/Value'], errors='coerce').fillna(0)
monthly_df = df.groupby(['年/Year', '月/Month'], as_index=False)['數值/Value'].sum()
monthly_df.rename(columns={'數值/Value': 'Monthly Rainfall'}, inplace=True)

print('Monthly rainfall data preview:')
print(monthly_df.head(12))

# 2. Dynamic times table circle mapping visualization
def times_table_circle(ax, N, k, R, color, lw=1.0, alpha=0.7):
    theta = np.linspace(0, 2*np.pi, N, endpoint=False)
    points = np.stack([R*np.cos(theta), R*np.sin(theta)], axis=1)
    for i in range(N):
        j = int((k*i) % N)
        x0, y0 = points[i]
        x1, y1 = points[j]
        ax.plot([x0, x1], [y0, y1], color=color, lw=lw, alpha=alpha, zorder=2)

FRAMES_PER_MONTH = 30  # Frames displayed per month, 1s transition
def lerp(a, b, t):
    return a + (b - a) * t
def lerp_tuple(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))

def animate_func(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    month_idx = (frame // FRAMES_PER_MONTH) % len(monthly_df)
    next_idx = (month_idx + 1) % len(monthly_df)
    t = (frame % FRAMES_PER_MONTH) / (FRAMES_PER_MONTH - 1)
    row1 = monthly_df.iloc[month_idx]
    row2 = monthly_df.iloc[next_idx]
    rain1 = float(row1['Monthly Rainfall'])
    rain2 = float(row2['Monthly Rainfall'])
    rain = lerp(rain1, rain2, t)
    def rain_norm_fn(r):
        return min(1.0, max(0.0, (r - 50) / 250))
    rain_norm1 = rain_norm_fn(rain1)
    rain_norm2 = rain_norm_fn(rain2)
    rain_norm = lerp(rain_norm1, rain_norm2, t)
    # Reduce point count to optimize performance
    N1 = 110 + int(100*rain_norm1)
    N2 = 130 + int(100*rain_norm2)
    N = int(lerp(N1, N2, t))
    k1 = 2 + 8*rain_norm1 + 2*np.sin(frame/18)
    k2 = 2 + 8*rain_norm2 + 2*np.sin((frame+FRAMES_PER_MONTH)/18)
    k = lerp(k1, k2, t)
    # Circle overall size varies with rainfall, smaller rainfall means smaller overall size
    min_scale = 0.65  # Minimum scaling ratio
    max_scale = 1.0   # Maximum scaling ratio
    scale1 = min_scale + (max_scale - min_scale) * rain_norm1
    scale2 = min_scale + (max_scale - min_scale) * rain_norm2
    scale = lerp(scale1, scale2, t)
    R_outer = 1.0 * scale
    R_inner1 = (0.55 + 0.25*rain_norm1) * scale1
    R_inner2 = (0.55 + 0.25*rain_norm2) * scale2
    R_inner = lerp(R_inner1, R_inner2, t)
    # Outer circle: white for low rainfall, blue gradient for high rainfall
    white = (1, 1, 1)
    blue = (80/255, 180/255, 255/255)
    color1 = lerp_tuple(white, blue, rain_norm1)
    color2 = lerp_tuple(white, blue, rain_norm2)
    color = lerp_tuple(color1, color2, t)
    lw1 = 0.3 + 1.4*rain_norm1
    lw2 = 0.3 + 1.4*rain_norm2
    lw = lerp(lw1, lw2, t)
    times_table_circle(ax, N, k, R_outer, color, lw=lw, alpha=0.7)
    # Inner circle: white for low rainfall, blue-purple gradient for high rainfall
    bluepurple = (106/255, 90/255, 205/255)  # Blue-purple
    k21 = k1*1.5 + 1.5*np.cos(frame/25)
    k22 = k2*1.5 + 1.5*np.cos((frame+FRAMES_PER_MONTH)/25)
    k2v = lerp(k21, k22, t)
    color21 = lerp_tuple(white, bluepurple, rain_norm1)
    color22 = lerp_tuple(white, bluepurple, rain_norm2)
    color2v = lerp_tuple(color21, color22, t)
    lw21 = 0.15 + 1.0*rain_norm1
    lw22 = 0.15 + 1.0*rain_norm2
    lw2v = lerp(lw21, lw22, t)
    alpha2v = 0.5
    times_table_circle(ax, N, k2v, R_inner, color2v, lw=lw2v, alpha=alpha2v)
    ax.plot(0, 0, 'o', color='white', ms=6, alpha=0.7, zorder=3)
    show_row = row1 if t < 0.5 else row2
    show_rain = rain1 if t < 0.5 else rain2
    ax.set_title(f"{int(show_row['年/Year'])}-{int(show_row['月/Month'])}  Rain: {show_rain:.1f} mm", color='w', fontsize=16)

fig, ax = plt.subplots(figsize=(7,7), facecolor='black')
total_frames = len(monthly_df) * FRAMES_PER_MONTH
ani = animation.FuncAnimation(fig, animate_func, frames=total_frames, interval=33, repeat=True)
plt.show()