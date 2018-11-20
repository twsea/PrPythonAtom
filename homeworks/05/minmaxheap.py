import operator
new_less_than_operator = operator.lt
new_greater_than_operator = operator.gt

class Heap():
    
    def __init__(self, array, is_max_heap):
        self.array = array[:]
        self.array_length = len(self.array)
        self.is_max_heap = is_max_heap
        if is_max_heap:
            self.comparator = operator.gt
        else:
            self.comparator = operator.lt
        self._build_heap()  
        
    def add(self, elem_with_priority):
        self.array.append(elem_with_priority)
        self._shift_up(self.array_length)
        self.array_length += 1
        
    def _shift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.comparator(self.array[i][1], self.array[parent][1]):
            self.array[parent], self.array[i] = self.array[i], self.array[parent]
            i = parent
            parent = (i - 1) // 2  
            
    def _shift_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        
        heap_size = self.array_length - 1
        if left <= heap_size and self.comparator(self.array[left][1], self.array[largest][1]):
            largest = left
        if right <= heap_size and self.comparator(self.array[right][1], self.array[largest][1]):
            largest = right
        if largest != i:
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self._shift_down(largest)    
            
    def _build_heap(self):
        for i in range(0, self.array_length // 2 + 1)[::-1]:
            self._shift_down(i)

    def show_tree_heap(self, total_width=33, fill=' '):
        tree = self.array        
        import math
        from io import StringIO
        output = StringIO()
        last_row = -1
        for i, n in enumerate(tree):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            output.write(str(n).center(col_width, fill))
            last_row = row
        print (output.getvalue())
        print ('-' * total_width)
        print()

class MaxHeap(Heap):
    
    def __init__(self, array):
        super().__init__(array, True)
        
    def extract_maximum(self):
        max_el = self.array[0]
        self.array[0] = self.array[self.array_length - 1]
        self.array_length -= 1
        self._shift_down(0)
        return max_el        
        