from __future__ import annotations
import ipywidgets as widgets
from IPython.display import display, clear_output
from ipywidgets import Output
import numpy as np
import matplotlib.pyplot as plt
from .ulam_spiral import fill_primes
from .goodness import detect_diagonal_segments, ulam_goodness


def display_primes(matrix: np.ndarray, output: Output | None = None, ) -> np.ndarray:
    """
    Fill and display an Ulam prime spiral.

    The function:
    1. Plots the filled matrix result with matplotlib, marking:
       - the center (value == 2) in red,
       - prime positions (value == 1) in blue.

    Parameters
    ----------
    matrix : np.ndarray
        2D square array to fill and visualize.
    output : ipywidgets.Output, optional
        Jupyter output widget for displaying/refreshing the plot.
        If None, plotting is done directly.

    Returns
    -------
    np.ndarray
        The filled matrix.
    """

    # Extract coordinates of primes and center
    ys, xs = np.where(matrix == 1)
    y0, x0 = np.where(matrix == 2)
    size = matrix.shape[0]
    
    def _plot() -> None:
        clear_output(wait=True)
        plt.close("all")

        # Scale figure size relative to matrix size (simple heuristic)
        fig_size = max(4, size // 60)
        plt.figure(figsize=(fig_size, fig_size))

        # Center point in red
        if len(x0) > 0:
            plt.scatter(x0, y0, c="red", s=1, label="center")

        # Prime points in blue
        plt.scatter(xs, ys, c="blue", s=1, label="primes")

        plt.xlim(0, size)
        plt.ylim(0, size)
        plt.axis("on")
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    if output is not None:
        with output:
            _plot()
    else:
        _plot()

    return matrix

def show_with_diagonals(matrix: np.ndarray, diagonal_mask:np.ndarray, output: Output | None = None, figsize_scale:float=60.0 ) -> None:
    """
    Display an Ulam spiral with diagonal segments highlighted.

    Parameters
    ----------
    matrix : np.ndarray
        Ulam matrix filled by fill_primes().
        Values:
            0 = non-prime
            1 = prime
    diagonal_mask : np.ndarray
        Same shape as matrix. 1s mark detected diagonal segments.
    figsize_scale : float
        Controls figure size. Larger values = bigger plot.

    Notes
    -----
    - Blue points = primes
    - Red points  = diagonal segments detected by detect_diagonal_segments()
    """
    prime_y, prime_x = np.where(matrix == 1)
    diag_y, diag_x = np.where(diagonal_mask == 1)
    size = matrix.shape[0]

    
    def _plot() -> None:
        clear_output(wait=True)
        plt.close("all")

        # Scale figure size relative to matrix size (simple heuristic)
        fig_size = max(4, size // figsize_scale)
        plt.figure(figsize=(fig_size, fig_size))

        # Prime points in blue
        plt.scatter(prime_x, prime_y, c="blue", s=1, label="primes")

        # Diagonal points in red
        plt.scatter(diag_x, diag_y, c="red", s=1, label="diagonals")

        plt.xlim(0, size)
        plt.ylim(0, size)
        plt.axis("on")
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    if output is not None:
        with output:
            _plot()
    else:
        _plot()
    
    


"""
Interactive prime (Ulam) spiral explorer with animation.

Requires:
- display_primes(matrix, size, offset)
- fourier_lowpass(matrix, radius)

Both are assumed to be defined elsewhere in your notebook/module.
"""

INITIAL_LIMIT = 100_000
INITIAL_OFFSET = 1
INITIAL_ANIMATE = 10
INITIAL_GAP_TOLERANCE = 5
INITIAL_MIN_RUN = 50
PADDING = 10


output = widgets.Output()

def create_zero_matrix (limit: int, padding: int) -> np.ndarray:
    """
    Create a square zero matrix large enough to hold numbers up to `limit`
    arranged approximately in a sqrt(limit) x sqrt(limit) grid.

    Parameters
    ----------
    limit : int
        Maximum number you want to place in the spiral.
    padding : int
        Extra pixels added to each dimension.

    Returns
    -------
    np.ndarray
        2D zero-initialized matrix.
    """
    size = int(round(limit ** 0.5))
    return np.zeros((size+padding,size+padding))


def build_ulam_spiral_ui () -> None:

    """
    Build and display an interactive UI for exploring a prime spiral:
    - set limit (how many numbers to check),
    - set offset (starting number),
    - display the prime spiral,
    - run a simple "animation" with changing offsets.
    """
    initial_limit:int = INITIAL_LIMIT
    initial_offset:int=INITIAL_OFFSET
    initial_animate:int=INITIAL_ANIMATE
    initial_gap_tolerance:int=INITIAL_GAP_TOLERANCE
    initial_min_run:int=INITIAL_MIN_RUN
    
    # Shared state for callbacks
    matrix: np.ndarray | None = None  # will be created on demand

    # --- Widgets ---
    limit_text = widgets.IntText(
        value=initial_limit,
        description='Limit:',
        placeholder='Enter a number',
    )

    offset_text = widgets.IntText(
        value=initial_offset,
        description='Offset:',
        placeholder='Enter a number',
    )

    gap_tolerance_text = widgets.IntText(
        value=initial_gap_tolerance,
        description='Gap tolerance:',
        placeholder='Enter a number',
    )

    min_run_text = widgets.IntText(
        value=initial_min_run,
        description='Minimum run length:',
        placeholder='Enter a number',
    )

    
    
    
    animate_text = widgets.IntText(
        value=initial_animate,
        description='Animation length:',
        placeholder='Enter a number',
    )


    button_display = widgets.Button(
        description="Display primes",
        button_style="info", 
        tooltip='Use the number in the text box',
    )


    button_animate = widgets.Button(
        description="Animate",
        tooltip="Display spiral with varying offsets",
    )
    
    toggle_diagonals = widgets.ToggleButton(
        value = False
        description="Display diagonals",
        button_style="info", 
    )

    

    # --- Callback: generate / update prime spiral ---
    def on_display_clicked(_button: widgets.Button) -> None:
        nonlocal matrix
        try:
            limit = limit_text.value
            offset = offset_text.value
            if limit <=0:
                raise ValueError("Limit must be positive")
            matrix = create_zero_matrix(limit, padding=10)
            size = matrix.shape[0] 
            matrix = fill_primes(matrix, offset=offset)
            matrix = display_primes(matrix, output= output)
       
        except Exception as exc:
            with output:
                clear_output(wait=True)
                print(f"Error while updating primes:  {exc}")


    def on_animate_clicked(_button: widgets.Button) -> None:
        nonlocal matrix
        try:
            limit = limit_text.value
            animate = animate_text.value
            offset = offset_text.value
            matrix = create_zero_matrix(limit, padding=10)
            # Display the map with a changing starting point - as an animation
            size = matrix.shape[0]            
            for j in range(animate):
                matrix = create_zero_matrix(limit, padding=10)
                matrix = fill_primes(matrix, offset=offset+j*2+1)
                matrix = display_primes(matrix, output=output)
        except ValueError:
            print("Error " )
  
    def on_diagonals_clicked(_toggle: widgets.ToggleButton, change) -> None:
        nonlocal matrix
        if change["new] = True:
            try:
                limit = limit_text.value
                gap_tolerance = gap_tolerance_text.value
                min_run = min_run_text.value
                # matrix = display_primes(matrix,offset_text.value, output)
                mask = detect_diagonal_segments(matrix,gap_tolerance = gap_tolerance, min_run = min_run)
                show_with_diagonals(matrix, mask, output, 60)
            except ValueError:
                print("Error " )
        else:
            matrix = display_primes(matrix, output=output)
            


    
    # Bind the function to the button's click event
    button_display.on_click(on_display_clicked)
    button_animate.on_click(on_animate_clicked)
    toggle_diagonals.observe(on_diagonals_clicked, names="value")
    


    # --- Show UI ---
    row1 = widgets.HBox([limit_text, offset_text, button_display])
    row2 = widgets.HBox([gap_tolerance_text, min_run_text, button_diagonal])
    row3 = widgets.HBox([animate_text, button_animate])
    display(widgets.VBox([row1, row2, output]))


