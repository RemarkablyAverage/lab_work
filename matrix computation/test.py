import spam
from spam import SpMatrix

x = spam.SpMatrix(6,5,initsize=4)

x[2,3] = 2.2
print x[1,1]
print x[2,3]
#Error:
#print x[3,10]

for i in xrange(x.nrows):
    for j in xrange(x.ncols):
        x[i,j] = 1.0 / (1 + i + 2*j)
x[2,2] = 22

print "%r x %r matrix" % (x.nrows, x.ncols)
x.print_dense()

A = SpMatrix(200,200)
B = SpMatrix(200,200)

A[0,0] = 1
A[2,3] = 1
A[111,111] = 1
B[111,111] = 1
print spam.l1_diff(A, B)
