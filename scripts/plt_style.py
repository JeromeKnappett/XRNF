"""
Custom plot style for the latex template ltu-thesis using the SciencePlots colour scheme 'muted' and batlow colourmap

Requires
https://github.com/garrettj403/SciencePlots ## for plot style
https://pypi.org/project/cmcrameri/         ## for batlow colour map

To use:

    from plt_style import *

"""

import matplotlib.pyplot as plt
import numpy as np

# Plot Style
plt.style.use(["science"])
#        ["science",'no-latex'])
#"ieee"
#'muted'
# Plot Parameters
fig_width_pt = 426.79134  # Get this from LaTeX using \\showthe\\columnwidth\n",
inches_per_pt = 1.0 / 72.27  # Convert pt to inches\n",
golden_mean = (np.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio\n",
fig_width = fig_width_pt * inches_per_pt  # width in inches\n",
fig_height = fig_width * golden_mean  # height in inches\n",
fig_size = [fig_width, fig_height]

SMALL_SIZE = 4
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# plt.rcParams["image.cmap"]  = cm.batlow
plt.rc("font", size=10)  # controls default text sizes\n",
plt.rc("axes", titlesize=10)  # fontsize of the axes title\n",
plt.rc("axes", labelsize=10)  # fontsize of the x and y labels\n",
plt.rc("xtick", labelsize=8)  # fontsize of the tick labels\n",
plt.rc("ytick", labelsize=8)  # fontsize of the tick labels\n",
plt.rc("legend", fontsize=8)  # legend fontsize\n",
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title\n",
plt.rcParams["text.usetex"] = True
plt.rcParams["figure.figsize"] = fig_size
plt.rcParams[
    "figure.dpi"
] = 200  # Default dpi, useful so that plots are a decent size in jupyter
