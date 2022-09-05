def sum_prod_diags(matrix: list[list[int]]) -> int:
    dimension = len(matrix)
    products_sum = 0
    for offset in range(dimension):
        p1 = m1 = 1
        p2 = m2 = int(bool(offset))  # So that products of first diagonals are not duplicated

        for j in range(dimension - offset):
            # Major diagonals
            p1 *= matrix[j][j + offset]
            p2 *= matrix[j + offset][j]
            # Minor diagonals
            m1 *= matrix[dimension - j - 1][j + offset]
            m2 *= matrix[dimension - j - 1 - offset][j]
        products_sum += p1 + p2 - m1 - m2

    return products_sum


if __name__ == "__main__":
    M1 = [[1, 4, 7, 6, 5], [-3, 2, 8, 1, 3], [6, 2, 9, 7, -4], [1, -2, 4, -2, 6], [3, 2, 2, -4, 7]]

    assert sum_prod_diags(M1) == 1098

    M2 = [[1, 4, 7, 6], [-3, 2, 8, 1], [6, 2, 9, 7], [1, -2, 4, -2]]

    assert sum_prod_diags(M2) == -11

    M3 = [[1, 2, 3, 2, 1], [2, 3, 4, 3, 2], [3, 4, 5, 4, 3], [4, 5, 6, 5, 4], [5, 6, 7, 6, 5]]

    assert sum_prod_diags(M3) == 0
