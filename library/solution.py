from abc import ABC, abstractmethod

class Solution(ABC):
    def __init__(self, repr=None):
        # To initialize a solution we need to know it's representation. If no representation is given, a solution is randomly initialized.
        if repr == None:
            repr = self.random_initial_representation()
        # Attributes
        self.repr = repr

    # Method that is called when we run print(object of the class)
    def __repr__(self):
        return str(self.repr)

    # Other methods that must be implemented in subclasses
    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def random_initial_representation(self):
        pass

class WSSolution(Solution):
    def __init__(self, repr=None, relationship_matrix=relationship_matrix, nr_of_tables=8):
        self.relationship_matrix = relationship_matrix
        self.nr_of_tables = nr_of_tables
        self.table_capacity = len(relationship_matrix) // nr_of_tables
        super().__init__(repr=repr)

    def random_initial_representation(self):
        tables = []
        left_idxs = [idx for idx in range(len(self.relationship_matrix))]
        for i in range(self.nr_of_tables):
            tables.append([])
            for j in range(self.table_capacity):
                idx = random.choice(left_idxs)
                left_idxs.remove(idx)
                # Check if idx is already in a table
                #while any(idx in table for table in tables):
                    #idx = random.randint(0, len(self.relationship_matrix) - 1)
                tables[i].append(idx)
        
        return tables

    def fitness(self, verbose=False):
        total_happiness = 0
        i = 1
        for table in self.repr:
            # Sum relationship scores for all unique guest pairs at the table
            table_happiness = sum(self.relationship_matrix[a, b] for a, b in combinations(table, 2))
            total_happiness += table_happiness
            if verbose:
                print(f"Table {i} Happiness = {table_happiness}")
                i += 1
        return total_happiness
    
class WSSearchableSolution(WSSolution):
    def get_neighbors(self):
        """Generates all valid neighbors by swapping two guests between tables."""
        neighbors = []

        # Loop through all pairs of guests at different tables
        for i in range(len(self.repr)):
            for j in range(len(self.repr[i])):
                for k in range(len(self.repr)):
                    for l in range(len(self.repr[k])):
                        if (i, j) != (k, l):  # Skip swapping guests at the same position
                            new_seating = deepcopy(self.repr)  # Use `repr` which holds the seating
                            new_seating[i][j], new_seating[k][l] = new_seating[k][l], new_seating[i][j]

                            # Create a new WSSearchableSolution with the modified seating arrangement
                            neighbor = WSSearchableSolution(
                                repr=new_seating,
                                relationship_matrix=self.relationship_matrix,  # Use relationship_matrix
                                nr_of_tables=self.nr_of_tables
                            )
                            neighbors.append(neighbor)

        return neighbors

    def get_random_neighbor(self):
        """Generates a random valid neighbor by swapping two guests between different tables."""
        new_seating = deepcopy(self.repr)  # Use `repr` for seating arrangement

        # Randomly pick two different tables
        table_indices = list(range(len(new_seating)))
        t1, t2 = random.sample(table_indices, 2)

        # Make sure the tables are not empty
        if not new_seating[t1] or not new_seating[t2]:
            return deepcopy(self)

        # Randomly pick a guest from each table
        g1 = random.randrange(len(new_seating[t1]))
        g2 = random.randrange(len(new_seating[t2]))

        # Swap the guests
        new_seating[t1][g1], new_seating[t2][g2] = new_seating[t2][g2], new_seating[t1][g1]

        return WSSearchableSolution(
            repr=new_seating,
            relationship_matrix=self.relationship_matrix,  # Use relationship_matrix
            nr_of_tables=self.nr_of_tables
        )