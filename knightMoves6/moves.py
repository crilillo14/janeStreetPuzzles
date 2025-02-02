
class Square:
    def __init__(self , value) -> None:
        self.value = value
        
# represent each square with a square object
        
class Node:
    def __init__(self, square) -> None:
        self.square = square
        self.next = None
    
# when generating paths, need a node object to iterate through the paths, sufficient to just store initial node in array to access whole path.


        
        


gridLayout = [
    ['A' , 'B' , 'B' , 'C' , 'C' , 'C'], # 6
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 5
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 4
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 3
    ['A' , 'A' , 'A' , 'B' , 'B' , 'C'], # 2
    ['A' , 'A' , 'A' , 'B' , 'B' , 'C'], # 1
#     a     b     c     d     e     f
]


# Firstly, understand how many moves it takes to go from corner to corner.
# thinking, modified version of knights tour to see what walk lengths are possible
# not only the minimum steps, but also 

board = [[-1 for _ in range(6)] for _ in range(6)]

size = 6


# start at a1 go to f6,  [5][0] to [0][5]

def bfs(start , end) -> Path: 




# then 