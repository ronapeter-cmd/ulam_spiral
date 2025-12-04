def is_prime(n: int) -> bool:
    """
    Return True if `n` is a prime number, otherwise False.

    Uses a simple optimized trial division:
    - handle small numbers directly,
    - eliminate multiples of 2 and 3,
    - then test numbers of the form 6k ± 1 up to sqrt(n).
    """
    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
