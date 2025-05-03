import random

def standard_crossover(parent1_repr, parent2_repr):
    """
    Performs standard one-point crossover on two parent representations.

    This operator selects a random crossover point (not at the edges) and 
    exchanges the tail segments of the two parents to produce two offspring. 
    The crossover point is the same for both parents and ensures at least one 
    gene is inherited from each parent before and after the point.

    Parameters:
        parent1_repr (str or list): The first parent representation.
        parent2_repr (str or list): The second parent representation.
            Both parents must have the same length and type.

    Returns:
        tuple: A pair of offspring representations (offspring1, offspring2), 
        of the same type as the parents.

    Raises:
        ValueError: If parent representations are not the same length.
    """

    if not (isinstance(parent1_repr, list) or isinstance(parent1_repr, str)):
        raise ValueError("Parent 1 representation must be a list or a string")
    if not (isinstance(parent2_repr, list) or isinstance(parent2_repr, str)):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length")

    # Choose random crossover point
    xo_point = random.randint(1, len(parent1_repr) - 1)

    offspring1_repr = parent1_repr[:xo_point] + parent2_repr[xo_point:]
    offspring2_repr = parent2_repr[:xo_point] + parent1_repr[xo_point:]

    return offspring1_repr, offspring2_repr