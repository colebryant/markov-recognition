'''
MPCS 51042 S'20: Markov models and hash tables

Cole Bryant
'''
from map import Map


class Hashtable(Map):
    """Class for a Hash Table. Inherits from Map ABC. Utilizes Linear Probing
    to resolve collisions."""
    MULTIPLIER = 37

    def __init__(self, capacity, defVal, loadFactor, growthFactor):
        self._capacity = capacity
        self._defVal = defVal
        self._loadFactor = loadFactor
        self._growthFactor = growthFactor
        self._cells = [None] * self._capacity
        self.length = 0

    def _hash(self, key):
        """Takes in a string and returns a hash value.
        Inputs: String (key)
        Outputs: Integer (hash value)
        """
        hash_value = 0
        for char in key:
            hash_value = (hash_value * self.MULTIPLIER + ord(char)) % \
                         self._capacity
        return hash_value

    def _rehash(self):
        """Method to rehash hash table.
        No inputs or outputs.
        """
        self._capacity *= self._growthFactor
        old_cells = self._cells
        self.length = 0
        self._cells = [None] * self._capacity

        for item in old_cells:
            if item is not None:
                if item[2]:
                    self.__setitem__(item[0], item[1])

    def __getitem__(self, key):
        """Method to return value associated with key from the hash table.
        Inputs: String (key)
        Outputs: Value (or default value if key not in table)
        """
        cell_index = self._hash(key)
        cell_count = 0
        while True:
            # Check if index and key are correct
            if self._cells[cell_index] is not None:
                if self._cells[cell_index][0] == key and \
                        self._cells[cell_index][2]:
                    return self._cells[cell_index][1]
            elif self._cells[cell_index] is None:
                return self._defVal
            # Linear probe
            if cell_index == self._capacity - 1:
                cell_index = 0
            else:
                cell_index += 1
            cell_count += 1
            if cell_count == self._capacity:
                return self._defVal

    def __setitem__(self, key, value):
        """Method to add or update a key-value pairing in the hash table.
        Inputs: String (key), some value (value). Rehashes the table if
        load factor of table meets qualifications.
        Inputs: String (key), some value (value)
        No outputs.
        """
        cell_index = self._hash(key)
        cell_count = 0
        while True:
            # Set key value pair
            if self._cells[cell_index] is None:
                self._cells[cell_index] = (key, value, True)
                self.length += 1
                # Check for rehash on load factor
                if (self.__len__() / self._capacity) > self._loadFactor:
                    self._rehash()
                break
            # Update key value pair
            elif self._cells[cell_index][0] == key and \
                    self._cells[cell_index][2]:
                self._cells[cell_index] = \
                    (self._cells[cell_index][0], value, True)
                break
            # Linear probe
            else:
                if cell_index == self._capacity - 1:
                    cell_index = 0
                else:
                    cell_index += 1
                cell_count += 1
            if cell_count == self._capacity:
                break

    def __delitem__(self, key):
        """Method to remove key-value pairing from inside the hash table.
        Inputs: String (key)
        No outputs.
        """
        cell_index = self._hash(key)
        cell_count = 0
        while True:
            #
            if self._cells[cell_index] is not None:
                if self._cells[cell_index][0] == key and \
                        self._cells[cell_index][2]:
                    self._cells[cell_index] = (self._cells[cell_index][0],
                                               self._cells[cell_index][1],
                                               False)
                    self.keys_list.remove(key)
                    self.length -= 1
                    break
            # Linear probe
            if cell_index == self._capacity - 1:
                cell_index = 0
            else:
                cell_index += 1
            cell_count += 1
            if cell_count == self._capacity:
                break

    def __contains__(self, key):
        """Method to check if key-value pairing is inside hash table.
        Inputs: String (key)
        Outputs: Boolean
        """
        cell_index = self._hash(key)
        cell_count = 0
        while True:
            if self._cells[cell_index] is not None:
                if self._cells[cell_index][0] == key and \
                        self._cells[cell_index][2]:
                    return True
            else:
                return False
            if cell_index == self._capacity - 1:
                cell_index = 0
            else:
                cell_index += 1
            cell_count += 1
            if cell_count == self._capacity:
                return False

    def keys(self):
        """Returns a list of all the keys inside the hash table.
        No inputs.
        Outputs: List
        """
        return [item[0] for item in self._cells if item is not None and
                item[2]]

    def values(self):
        """Returns a list of all the values inside the hash table.
        No inputs.
        Outputs: List
        """
        return [item[1] for item in self._cells if item is not None and
                item[2]]

    def __len__(self):
        """Returns the number of items inside the hash table.
        No inputs.
        Outputs: Integer
        """
        return self.length

    def __bool__(self):
        """Returns true if hash table is not empty and false if it is empty.
        No inputs.
        Outputs: Boolean
        """
        for item in self._cells:
            if item is not None and item[2]:
                return True
        return False

    class HashtableIterator:
        """Iterator class for Hash Table class"""

        def __init__(self, cells):
            self._items = [cell for cell in cells if cell is not None and
                           cell[2]]
            self._index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self._index < len(self._items):
                i = self._index
                self._index += 1
                return self._items[i][0], self._items[i][1]
            else:
                raise StopIteration

    def __iter__(self):
        """Returns a HashtableIterator of the objects inside the hash table.
        The iterator returns the key-value pair as tuple.
        No inputs.
        Outputs: HashtableIterator
        """
        return self.HashtableIterator(self._cells)

    def __repr__(self):
        """String representation of Hash Table.
        No inputs.
        Outputs: String
        """
        items = ", ".join([str(item[0]) + ": " + str(item[1]) for item in
                           self._cells if item is not None and item[2]])
        return f'Hashtable({items})'
