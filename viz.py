def display_primes(matrix: np.ndarray, offset:int = 1, output: Output | None = None, ) -> np.ndarray:
    """
    Fill and display an Ulam prime spiral.

    The function:
    1. Fills `matrix` with prime indicators using `fill_primes`.
    2. Plots the result with matplotlib, marking:
       - the center (value == 2) in red,
       - prime positions (value == 1) in blue.

    Parameters
    ----------
    matrix : np.ndarray
        2D square array to fill and visualize.
    offset : int, optional
        Starting integer for the spiral (default is 1).
    output : ipywidgets.Output, optional
        Jupyter output widget for displaying/refreshing the plot.
        If None, plotting is done directly.

    Returns
    -------
    np.ndarray
        The filled matrix.
    """
    
    matrix = fill_primes(matrix, offset=offset)

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
