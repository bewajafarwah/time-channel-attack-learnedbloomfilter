import math
import mmh3
from bitarray import bitarray
from typing import Any

class BloomFilter:
    def __init__(self, n: int, fpr: float) -> None:
        self.fpr = fpr
        self.size = self._get_size(n)

        self.hash_count = self._get_hash_count(n)
        
        self.array = bitarray(self.size)
        self.array.setall(0)

    def _get_size(self, n: int) -> int:
        size = (-1 * n * math.log(self.fpr)) / (math.log(2) ** 2)
        return int(size)
    
    def _get_hash_count(self, n: int) -> int:
        hc = (self.size / n) * math.log(2)
        return int(hc)

    def _get_hash_input(self, key: Any) -> str:
        hash_input = str(key)
        return hash_input

    def add(self, key: Any) -> None:
        for i in range(self.hash_count):
            hash_input = self._get_hash_input(key)
            array_index = mmh3.hash(hash_input, i) % self.size
            self.array[array_index] = True
    
    def query(self, key: Any) -> bool:
        for i in range(self.hash_count):
            hash_input = self._get_hash_input(key)
            array_index = mmh3.hash(hash_input, i) % self.size
            if not self.array[array_index]:
                return False
        return True