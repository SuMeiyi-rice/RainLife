# RainLife Data Visualization Project

This project is a Python-based data visualization tool designed to illustrate rainfall variations in Hong Kong .
This project comprises two visualizations: one displays rainfall variations recorded by the Hong Kong Observatory from its inception in 1884 to the present day, while the other illustrates changes in rainfall data during the initial two years of record-keeping.

## Features
- Virtual environment support
- Popular visualization libraries: matplotlib, seaborn, pandas
- Example Jupyter notebook

## Setup
1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Launch Jupyter Notebook:
   ```powershell
   jupyter notebook
   ```

## Directory Structure
- `src/`: Project source code directory
- `notebooks/`: Jupyter examples
- `requirements.txt`: Dependencies list

## Examples
Please refer to notebooks/example.ipynb for data visualization demonstrations.

## Running the Visualizations
The project includes two main visualization scripts:

1. **Spiral Particle Animation** (`src/rainecho.py`):
   ```powershell
   python src/rainecho.py
   ```
   Creates "Echoes of Early Rains" - a spiral particle animation showing rainfall    intensity through color and particle count.
   An artistic representation of Hong Kong's rainfall data from 1884 to 1885, the first two years.
   This visualization centers on the first two years of rainfall data ever recorded by the Hong Kong Observatory
   these figures are not just numbers, but the "source" and "starting point" of Hong Kong's rainfall archives.
   I wish to evoke these echoes of rain, vanishing into the “long river of time.”

2. **Dynamic Circle** (`src/rainball.py`):
   ```powershell
   python src/rainball.py
   ```
   Alternative circle visualization with dual-layer effects.
   Running a multiplicative mapping on two circles, it presents a life sphere of rain through variations in size, line thickness, and density.


Each script will open an interactive matplotlib window displaying the animated rainfall visualization.Each file preprocesses the CSV table to output only the variation in monthly rainfall, presenting the data visualization of monthly rainfall.
