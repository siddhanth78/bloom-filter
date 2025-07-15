from bitarray import bitarray
from math import log, ceil
import mmh3
import pickle

class Bloom:
    def __init__(self, num_items=5000, prob=0.01):
        self.num_items = num_items
        self.prob = prob
        self.size = self.get_size()
        self.k = self.num_hashes()
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def get_size(self):
        return int(ceil(-(self.num_items * log(self.prob))/(log(2)**2)))

    def num_hashes(self):
        return int(ceil((self.size/self.num_items) * log(2)))

    def get_array(self):
        return self.bit_array

    def clear_filter(self):
        self.bit_array.setall(0)

    def add_element(self, element):
        for i in range(self.k):
            m = mmh3.hash(element, i) % self.size
            self.bit_array[m] = True

    def in_filter(self, element, print_result=False):
        for i in range(self.k):
            m = mmh3.hash(element, i) % self.size
            if self.bit_array[m] == False:
                if print_result == True:
                    print("False")
                return False
        if print_result == True:
            print("True")
        return True

    def save_filter(self, filter_tag="bloom_filter"):
        filter_dict = {"num_items": self.size, "prob": self.prob, "bit_array": self.bit_array, "num_hashes": self.k, "size": self.size}
        with open(f"{filter_tag}.pkl", "wb") as file:
            pickle.dump(filter_dict, file)

    def load_into_filter(self, info):
        self.num_items = info["num_items"]
        self.prob = info["prob"]
        self.size = info["size"]
        self.k = info["num_hashes"]
        self.bit_array = info["bit_array"]

class CountingBloom:
    def __init__(self, num_items=5000, prob=0.01):
        self.num_items = num_items
        self.prob = prob
        self.size = self.get_size()
        self.k = self.num_hashes()
        self.int_array = [0] * self.size

    def get_size(self):
        return int(ceil(-(self.num_items * log(self.prob))/(log(2)**2)))

    def num_hashes(self):
        return int(ceil((self.size/self.num_items) * log(2)))

    def get_array(self):
        return self.int_array

    def clear_filter(self):
        self.int_array = [0] * self.size

    def add_element(self, element):
        for i in range(self.k):
            m = mmh3.hash(element, i) % self.size
            self.int_array[m] += 1

    def remove_element(self, element):
        remove_in = []
        for i in range(self.k):
            m = mmh3.hash(element, i) % self.size
            if self.int_array[m] == 0:
                print("Element not in set")
                return None
            remove_in.append(m)
        for j in remove_in:
            self.int_array[j] -= 1
        return element

    def in_filter(self, element, print_result=False):
        for i in range(self.k):
            m = mmh3.hash(element, i) % self.size
            if self.int_array[m] == 0:
                if print_result == True:
                    print("False")
                return False
        if print_result == True:
            print("True")
        return True

    def save_filter(self, filter_tag="bloom_filter"):
        filter_dict = {"num_items": self.size, "prob": self.prob, "int_array": self.int_array, "num_hashes": self.k, "size": self.size}
        with open(f"{filter_tag}.pkl", "wb") as file:
            pickle.dump(filter_dict, file)

    def load_into_filter(self, info):
        self.num_items = info["num_items"]
        self.prob = info["prob"]
        self.size = info["size"]
        self.k = info["num_hashes"]
        self.int_array = info["int_array"]


def load_filter(bf, filter_tag="bloom_filter"):
    with open(f"{filter_tag}.pkl", "rb") as file:
       info = pickle.load(file)
    bf.load_into_filter(info)
