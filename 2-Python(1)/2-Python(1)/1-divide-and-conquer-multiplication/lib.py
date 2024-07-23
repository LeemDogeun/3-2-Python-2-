from __future__ import annotations
import copy

class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.matrix[key[0]][key[1]] = value

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]
                    result[i, j] %= self.MOD

        return result

    def __pow__(self, n: int) -> Matrix:
        assert self.shape[0] == self.shape[1], "Matrix must be square for exponentiation"
    
        def matrix_pow(matrix: Matrix, exp: int) -> Matrix:
            if exp == 0:
                return Matrix.eye(matrix.shape[0])
            elif exp == 1:
                return matrix
            elif exp % 2 == 0:
                half_pow = matrix_pow(matrix, exp // 2)
                return half_pow @ half_pow
            else:
                return matrix @ matrix_pow(matrix, exp - 1)
    
        return matrix_pow(self, n)

    def __repr__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])
