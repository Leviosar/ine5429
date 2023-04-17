from random import randint
from time import time

def miller_rabin(n: int, iterations: int = 40):
    """Uses Miller-Rabin method to check if a number is composite.

    Args:
        n (int): number to be tested.
        iterations (int, optional): max number of iterations. Defaults to 40.

    Returns:
        bool: If False, the number definitely is composite. If True it may be a prime number.
    """
    # Handling base cases
    if n == 2 or n == 3:
        return True
    
    # Handling even numbers
    if n % 2 == 0:
        return False
    
    r = 0
    d = n - 1

    # Choosing an r that satisfies n - 1 = 2 ^ r * d
    while d % 2 == 0:
        r += 1
        d = d // 2

    # Try to find proof that n is composite until reach the max iteration number 
    for _ in range(iterations):

        # Choosing a test number for this iteration
        a = randint(2, n - 2)
        
        # Third argument of Python's POW is a mod, which can increase efficiency in some cases as asserted on the docs
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            
            if x == n - 1:
                break
        else:
            # Only enters if never reached the break statement above
            return False
        
    # If after all iterations the numbers isn't flagged as composite, then maybe it's a prime
    return True

def fermat(n: int, iterations: int = 40):
    """Uses Fermat primality test to check if a given number is composite
    
    Inspiration: https://en.wikipedia.org/wiki/Fermat_primality_test
    
    Args:
        n: number to be tested
        iterations (int, optional): max number of iterations. Defaults to 40.
    """

    # Handling base cases
    if n == 2:
        return True

    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0 or n % 11 == 0:
        return False

    if (n ** 2 - 1) % 24 != 0:
        return False

    for _ in range(iterations):
        a = randint(2, n - 1)

        if pow(a, n - 1, n) != 1:
            return False

    return True

def is_prime(n, method="miller_rabin"):
    match method:
        case "miller_rabin":
            return miller_rabin(n)
        case "fermat":
            return fermat(n)