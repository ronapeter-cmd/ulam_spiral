"""
goodness.py

Tools for detecting diagonal structures and computing a "goodness score"
for Ulam spiral matrices.

The goals:
- detect visually coherent diagonal line segments (with gap tolerance)
- highlight them (via a mask)
- compute a scalar quality score describing how pronounced these structures are
"""

import numpy as np

# ============================================================
# 1. Helper: find gap-tolerant runs in a 1D binary sequence
# ============================================================
def find_runs_1d(array: np.ndarray, gap_tolerance: int = 1):
    """
    Detect continuous runs of 1's in a 1D binary array, allowing small gaps.

    Parameters
    ----------
    array : np.ndarray
        1D array containing 0s and 1s.
    gap_tolerance : int
        Maximum number of consecutive zeros that are allowed within a run.
        Example: [1,0,1] → one run if gap_tolerance >= 1.

    Returns
    -------
    list of (start, end)
        Index intervals representing the (smoothed) runs.
        'end' is non-inclusive (Python slicing convention).
    """
    # Ensure binary
    array = (array > 0).astype(int)
    
    if array.size == 0:
        return []
    
    # Expand small gaps:
    # convolution with a ones-kernel marks any window that contains at least one 1
    if gap_tolerance > 0:
      kernel = np.ones (gap_tolerance + 1, dtype=int)
      conv = np.convolve (array, kernel, mode="same")
      smoothed = (conv > 0).astype(int)
    else:
      smoothed = array
    # Identify transitions: 0 -> 1 (run start), 1 -> 0 (run end)
    padded = np.r_[0, smoothed, 0]
    diff = np.diff(padded)
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]
    return list(zip(starts,ends))

# ============================================================
# 2. Diagonal segment detector (↘ and ↙ directions)
# ============================================================

def detect_diagonal_segments (matrix: np.ndarray, gap_tolerance:int=1, min_run:int=5) -> np.ndarray:
  """
    Detect visually coherent diagonal line segments in an Ulam matrix.
    Both main diagonals (↘) and anti-diagonals (↙) are scanned.

    Parameters
    ----------
    matrix : np.ndarray
        2D array containing 0 = non-prime, 1 = prime
    gap_tolerance : int
        Number of zeros allowed inside a "continuous" run.
    min_run : int
        Minimum run length to consider a diagonal segment meaningful.

    Returns
    -------
    mask : np.ndarray
        2D binary mask (same shape as matrix).
        mask[i,j] = 1 indicates a detected diagonal segment pixel.
    """

  rows, cols = matrix.shape
  mask = np.zeros_like(matrix, dtype=bool)
  # -----------------------------
  # Scan main-diagonal direction ↘
  # (diagonals defined by i - j = constant)
  # -----------------------------
  for k in range (-rows +1, cols):
    diag = np.diag(matrix, k=k)
    runs = find_runs_1d(diag, gap_tolerance = gap_tolerance)

    for start, end in runs:
        if end - start < min_run:
            continue
        # Map diag indexes back to matrix coordinates
        for idx in range (start, end):
            if k >= 0:
                i = idx
                j = idx + k
            else:  # k < 0
                i = idx - k
                j = idx
            if 0 <= i < rows and 0 <= j < cols:
                mask[i,j] = 1

  # -----------------------------
  # Scan anti-diagonal direction ↙
  # Use horizontal flip to reuse diagonal logic
  # -----------------------------
  flipped_matrix = np.fliplr(matrix)
  flipped_mask = np.zeros_like(matrix, dtype=bool)

  for k in range (-rows +1, cols):
      diag = np.diag(flipped_matrix, k=k)
      runs = find_runs_1d(diag, gap_tolerance = gap_tolerance)
      
      for start, end in runs:
          if end - start < min_run:
              continue
            # Map diag indexes back to matrix coordinates
          for idx in range (start, end):
              if k >= 0:
                i = idx
                j = idx + k
              else:  # k < 0
                i = idx - k
                j = idx
              if 0 <= i < rows and 0 <= j < cols:
                  flipped_mask[i,j] = 1
  # Flip back and combine both direction masks
  mask |= np.fliplr(flipped_mask)

  return mask

# ============================================================
# 2. Diagonal segment detector (↘ and ↙ directions)
# ============================================================

def detect_horizontal_vertical_segments (matrix: np.ndarray, gap_tolerance:int=1, min_run:int=5) -> np.ndarray:
    
  """
    Detect visually coherent horizontal and vertical line segments in an Ulam matrix.

    Parameters
    ----------
    matrix : np.ndarray
        2D array containing 0 = non-prime, 1 = prime
    gap_tolerance : int
        Number of zeros allowed inside a "continuous" run.
    min_run : int
        Minimum run length to consider a segment meaningful.

    Returns
    -------
    mask : np.ndarray
        2D binary mask (same shape as matrix).
        mask[i,j] = 1 indicates a detected segment pixel.
    """

  rows, cols = matrix.shape
  mask = np.zeros_like(matrix, dtype=bool)
  # -----------------------------
  # Scan horizontal direction ->
  # -----------------------------
  for k in range (0, rows):
      row = matrix[k,:]
      runs = find_runs_1d(row, gap_tolerance = gap_tolerance)
      for start, end in runs:
          if end - start < min_run:
              continue
            # Map row indexes back to matrix coordinates
          for idx in range (start, end):
              i = k
              j = idx
              if 0 <= i < rows and 0 <= j < cols:
                  mask[i,j] = 1

  # -----------------------------
  # Scan horizontal direction ->
  # -----------------------------
  vertical_mask = np.zeros_like(matrix, dtype=bool)
  for k in range (0, cols):
      row = matrix[:,k]
      runs = find_runs_1d(row, gap_tolerance = gap_tolerance)
      for start, end in runs:
          if end - start < min_run:
              continue
            # Map row indexes back to matrix coordinates
          for idx in range (start, end):
              i = idx
              j = k
              if 0 <= i < rows and 0 <= j < cols:
                  vertical_mask[i,j] = 1
                  mask |= vertical_mask
    
  return mask


# ============================================================
# 3. Goodness score: how "diagonal" is the Ulam matrix?
# ============================================================

def ulam_goodness (matrix: np.ndarray, gap_tolerance:int=1, min_run: int=5) -> float:  
    """
    Compute a normalized "goodness score" for an Ulam spiral matrix.

    The idea:
    - detect diagonal line segments (with tolerance for small gaps)
    - compute the fraction of the matrix covered by these segments

    Parameters
    ----------
    matrix : np.ndarray
        Ulam matrix (0/1/2 codes).
    gap_tolerance : int
        How many zeros can appear inside what the human eye sees as a line.
    min_run : int
        Minimum diagonal length to count as meaningful.

    Returns
    -------
    float
        Normalized score in approximately the range [0, 1].
        Higher values indicate stronger diagonal structure.
    """
    mask = detect_diagonal_segments (matrix, gap_tolerance=gap_tolerance, min_run=min_run)
    mask |= detect_horizontal_vertical_segments (matrix, gap_tolerance=gap_tolerance, min_run=min_run)
    total_marked = mask.sum()
    size = matrix.shape[0]
    
    # Normalize by total pixel count

    score = total_marked / (size*size)
    return float(score)



    
    
