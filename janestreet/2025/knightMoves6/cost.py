# layout of chess board

gridLayout = [
    ['A' , 'B' , 'B' , 'C' , 'C' , 'C'], # 6
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 5
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 4
    ['A' , 'A' , 'B' , 'B' , 'C' , 'C'], # 3
    ['A' , 'A' , 'A' , 'B' , 'B' , 'C'], # 2
    ['A' , 'A' , 'A' , 'B' , 'B' , 'C'], # 1
#     a     b     c     d     e     f
]

# two trips, 
# one from a6 to f1 and a1 to f6
# diagonals

# add by same number or multiply by different num, 
# prime factorization is 2024 = 1012 * 2 = 506 * 4  = 253 .. = 11 x 23 x 8


# distributing the 3 2s in the prime factorization ot check for possible patterns 
#   - 22 x 23 x 4
#   - 11 x 46 x 4
#   - 44 x 23 x 2
#   - 11 x 92 x 2
#   - 22 x 46 x 2


# also, you want the longest walk possible to minimize A, B, C. 

