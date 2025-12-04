import numpy as np
from .primes import is_prime

def set_if_inside (matrix: np.ndarray, x: int, y: int, value: int):
    """
    Set `matrix[x, y] = value` if (x, y) is inside the array bounds.

    Parameters
    ----------
    matrix : np.ndarray
        2D grid to modify.
    x, y : int
        Index coordinates.
    value : int
        Value to assign.

    Returns
    -------
    bool
        True if the position was inside and updated, False otherwise.
    """
    
    rows, cols = matrix.shape
    if 0 <= x < rows and  0 <= y < cols:
        matrix[x, y] = value
        return True
    return False
    
def fill_primes(matrix,offset):
    """
    Fill a 2D numpy array with an Ulam-style prime spiral.

    The spiral starts from the center of the matrix, with the first
    number equal to `offset`. Each subsequent integer is placed while
    walking in an outward spiral pattern.

    Cells are set to:
    - 2 at the center (starting position),
    - 1 where the corresponding number is prime,
    - unchanged (0) otherwise.

    Parameters
    ----------
    matrix : np.ndarray
        2D square array to fill. Initialized with zeros.
    offset : int, optional
        Starting integer for the spiral (default is 1).

    Returns
    -------
    np.ndarray
        The modified matrix containing the prime marking.
    """
    
    rows, cols = matrix.shape

    # Start from the center of the grid
    
    mid = rows // 2
    incr = 1
    side = 0
    current_value = offset
    step_length = 0
    step_increment = 1  # Spiral step growth factor
    x, y = mid,mid

    # Mark the center with a special value (2)
    set_if_inside (matrix,x,y,2)

    # We need to place up to rows * cols numbers
    max_value = rows * cols + offset
    
    while current_value < max_value:
        # Move right and up
        step_length += 1
        for _ in range(step_length):
            x += step_increment
            if is_prime(current_value):
                set_if_inside(matrix, x, y, 1)
            current_value += 1
        for _ in range(step_length):
            y += step_increment
            if is_prime(current_value):
                set_if_inside(matrix, x, y, 1)
            current_value += 1
       
        # Move left and down (step_length increases)
        step_length += 1
        for _ in range(step_length):
            x -= step_increment
            if is_prime(current_value):
                set_if_inside(matrix, x, y, 1)
            current_value += 1
        for _ in range(step_length):
            y -= step_increment
            if is_prime(current_value):
                set_if_inside(matrix, x, y, 1)
            current_value += 1
    
    return matrix
