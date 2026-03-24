import torch
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from sunpy.visualization.colormaps.color_tables import aia_color_table
import astropy.units as u

modalities = {
    "br": 0,
    "bp": 1,
    "bt": 2,
    "dopplergram": 3,
    "continuum": 4,
    "aia_1700": 5,
    "aia_1600": 6,
    "aia_0335": 7,
    "aia_0304": 8,
    "aia_0211": 9,
    "aia_0193": 10,
    "aia_0171": 11,
    "aia_0131": 12,
    "aia_0094": 13
}

def spower(x, p):
    """ Signed power transform. """
    return np.sign(x) * np.power(np.abs(x), p)

def get_default_transforms(channel):
    """Returns a Transform which resizes 2D samples (1xHxW) to a target_size (1 x target_size x target_size)

    Apply the normalization necessary for the SDO ML Dataset. Depending on the channel, it:
      - clips the "pixels" data in the predefined range (see above)
      - applies a log10() on the data
      - normalizes the data to the [0, 1] range
      - normalizes the data around 0 (standard scaling)
    also refer to
       - https://pytorch.org/vision/stable/transforms.html
       - https://github.com/i4Ds/SDOBenchmark/blob/master/dataset/data/load.py#L363
       - https://gitlab.com/jdonzallaz/solarnet-thesis/-/blob/master/solarnet/data/transforms.py

    Args:
        channel (str, optional): [The SDO channel]. Defaults to 171.
    Returns:
        [Transform]
    """
    preprocess_config = CHANNEL_PREPROCESS[channel]
    scaling_str = preprocess_config["scaling"]

    # Base transform
    if scaling_str == "log10":
        base_transform = lambda x: np.log10(x)
    elif scaling_str == "sqrt":
        base_transform = lambda x: np.sqrt(x)
    else:
        base_transform = lambda x: x

    # Normalization
    mean = base_transform(preprocess_config["min"])
    std = base_transform(preprocess_config["max"]) - base_transform(preprocess_config["min"])

    def lambda_transform(x):
        x = np.clip(x, preprocess_config["min"], preprocess_config["max"])
        x = base_transform(x)
        return x

    def transform(x):
        x = lambda_transform(x)
        x = (x - mean) / std
        x = (x - 0.5) / 0.5
        return x

    return transform

def plot_magnetogram(x, ax=None, vmax=3000.0, p=None, b0=200.0, cmap="PuOr", colorbar=False):
    """ Plot a magnetogram Br, Bp or Bt. Use one of these transforms:
    - signed-power: b -> sign(b) |b|^p
    - arcsinh: b -> arcsinh(b/b0)
    """
    assert b0 is None or p is None, "Cannot specify both b0 (used for arcsinh) and p (used for power transform)"
    if isinstance(x, torch.Tensor):
        x = x.detach().cpu().numpy()
    # define transform to apply
    def transform(b):
        if b0 is not None:
            return np.arcsinh(b/b0)
        elif p is not None  :
            return spower(b, p)
        else:
            return b
    def inverse_transform(b):
        if b0 is not None:
            return np.sinh(b) * b0
        elif p is not None:
            return spower(b, 1/p)
        else:
            return b
    # plot
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    else:
        fig = ax.get_figure()
    vmin, vmax = transform(-vmax), transform(vmax)
    im = ax.imshow(transform(x), cmap=cmap, vmin=vmin, vmax=vmax)
    if colorbar:
        cbar = plt.colorbar(im, ax=ax)
        def inverse_format(value, tick_number):
            return int(inverse_transform(value))
        cbar.formatter = plt.FuncFormatter(inverse_format)
        cbar.update_ticks()  # Refresh colorbar ticks with original values
    return fig

def plot_aia(x, ax=None, wavelength="0094A", colorbar=False, vmin=-1, vmax=1, apply_transform=True):
    """
    Plot an AIA (Atmospheric Imaging Assembly) image with the appropriate colormap and normalization.

    Args:
        x (np.ndarray): The input image array (2D, typically float32 or float64).
        ax (matplotlib.axes.Axes, optional): The matplotlib axis to plot on. If None, a new figure and axis are created.
        wavelength (str, optional): The AIA wavelength channel to use (e.g., "0094A", "0171A"). Determines the colormap and normalization.
        colorbar (bool, optional): If True, display a colorbar with tick labels in the original data units.

    Returns:
        im: The matplotlib image object returned by `imshow`.
        ax: The matplotlib axis used for plotting.

    The function applies the standard preprocessing transform for the given AIA wavelength (as defined in `get_default_transforms` and `CHANNEL_PREPROCESS`),
    then displays the image using the corresponding AIA colormap from SunPy. If `colorbar` is True, a colorbar is added with tick labels converted back to the original data units
    using the inverse of the preprocessing transform. The axis is turned off for a cleaner image display.

    Example:
        im, ax = plot_aia(image, wavelength="0171A", colorbar=True)
    """
    if isinstance(x, torch.Tensor):
        x = x.detach().cpu().numpy()
    # Define transform to apply
    transform = get_default_transforms(wavelength)
    preprocess_config = CHANNEL_PREPROCESS[wavelength]
    def inverse_transform(x):
        scaling = preprocess_config["scaling"]
        if scaling == "log10":
            minv = preprocess_config["min"]
            maxv = preprocess_config["max"]
            mean = np.log10(minv)
            std = np.log10(maxv) - np.log10(minv)
            # Undo Normalize(mean=0.5, std=0.5): x = x*0.5 + 0.5
            x = x * 0.5 + 0.5
            # Undo Normalize(mean, std): x = x*std + mean
            x = x * std + mean
            # Undo log10: x = 10**x
            x = np.power(10, x)
        elif scaling == "sqrt":
            minv = preprocess_config["min"]
            maxv = preprocess_config["max"]
            mean = np.sqrt(minv)
            std = np.sqrt(maxv) - np.sqrt(minv)
            x = x * 0.5 + 0.5
            x = x * std + mean
            x = np.power(x, 2)
        else:
            minv = preprocess_config["min"]
            maxv = preprocess_config["max"]
            mean = minv
            std = maxv - minv
            x = x * 0.5 + 0.5
            x = x * std + mean
        return x
    # Apply transform
    if apply_transform:
        x_show = transform(torch.from_numpy(x).unsqueeze(0))
        x_show = x_show.squeeze(0).detach().cpu().numpy()
        vmin = -1
        vmax = 1
    else:
        x_show = np.asarray(x)
    # Choose colormap
    cmap = aia_color_table(int(wavelength[:-1]) * u.angstrom)
    # Plot
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    else:
        fig = ax.get_figure()
    im = ax.imshow(x_show, cmap=cmap, vmin=vmin, vmax=vmax)
    if colorbar:
        cbar = plt.colorbar(im, ax=ax)
        if apply_transform:
            def inverse_format(value, tick_number):
                val = inverse_transform(value)
                # Round to nearest integer, but format as int only if close to int
                if np.isclose(val, np.round(val), atol=1e-2):
                    return f"{int(np.round(val))}"
                else:
                    return f"{val:.1f}"
            cbar.formatter = plt.FuncFormatter(inverse_format)
            cbar.update_ticks()  # Refresh colorbar ticks with original values
    return fig


CHANNEL_PREPROCESS = {
    "4500A": {"min": 4000, "max": 20000, "scaling": "log10"},
    "1700A": {"min": 220,  "max": 5000,  "scaling": "log10"},
    "1600A": {"min": 10,   "max": 800,   "scaling": "log10"},
    "0335A": {"min": 0.4,  "max": 1000,  "scaling": "log10"},
    "0304A": {"min": 0.1,  "max": 3500,  "scaling": "log10"},
    "0211A": {"min": 7,    "max": 3500,  "scaling": "log10"},
    "0193A": {"min": 20,   "max": 5500,  "scaling": "log10"},
    "0171A": {"min": 5,    "max": 3500,  "scaling": "log10"},
    "0131A": {"min": 0.7,  "max": 1900,  "scaling": "log10"},
    "0094A": {"min": 0.1,  "max": 800,   "scaling": "log10"},
}

CHANNEL_NAMES = [
    "br", "bp", "bt", "dopplergram", "continuum", 
    "aia_1700", "aia_1600", "aia_0335", "aia_0304", 
    "aia_0211", "aia_0193", "aia_0171", "aia_0131", "aia_0094",
    "gong_6768"
]

class Wvl:
    """Helper class to convert between wavelength strings and indices."""
    @staticmethod
    def str_to_int(wvl_str):
        """Example: '0335A' -> 335"""
        if wvl_str[-1] == "A":
            wvl_str = wvl_str[:-1]
        return int(wvl_str.lstrip("0"))
    @staticmethod
    def int_to_str(num_value):
        """Example: 335 -> '0335A'"""
        return f"{num_value:04d}A"
    @staticmethod
    def idx_to_str(idx):
        """Example: 13 -> '0335A'"""
        channel_str = CHANNEL_NAMES[idx]
        wvl_int = int(channel_str.lstrip("aia_"))
        return Wvl.int_to_str(wvl_int)
    @staticmethod
    def str_to_idx(wvl_str):
        """Example: '0335A' -> 13"""
        wvl_int = Wvl.str_to_int(wvl_str)
        wvl_str = f"aia_{wvl_int:04d}"
        return CHANNEL_NAMES.index(wvl_str)
    @staticmethod
    def int_to_idx(wvl_int):
        """Example: 335 -> 13"""
        wvl_str = f"aia_{wvl_int:04d}"
        return CHANNEL_NAMES.index(wvl_str)

def plot_sdo(x, idx, ax=None):
    """Helper function to plot a SDO channel (idx=0,...,13). 
    x must be of shape [C, H, W] or [H, W]."""
    if x.ndim == 3:
        x_plot = x[idx,:,:]
    else:
        x_plot = x
    if idx < 4 or idx == 14:  # Magnetogram or Dopplergram
        return plot_magnetogram(x_plot, ax=ax)
    elif idx == 4:  # Continuum
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        else:
            fig = ax.get_figure()
        if isinstance(x_plot, torch.Tensor):
            x_plot = x_plot.detach().cpu().numpy()
        ax.imshow(x_plot, cmap="gray", vmin=0, vmax=1)
        return fig
    else:
        wvl = Wvl.idx_to_str(idx)
        return plot_aia(x_plot, ax=ax, wavelength=wvl)

def make_videoo(x_obs: torch.Tensor, idx: int):
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    ax.axis("off")

    # Make the axes fill the whole figure
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_position([0, 0, 1, 1])

    def update(frame):
        ax.clear()
        ax.axis("off")
        ax.set_position([0, 0, 1, 1])
        return plot_sdo(x_obs[:, frame, :, :], idx, ax=ax)

    plt.close()

    return FuncAnimation(fig, update, frames=x_obs.shape[0], interval=33, blit=False)

def make_video(x_obs: torch.Tensor, modality: str):
    return make_videoo(x_obs, modalities[modality])