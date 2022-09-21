from statistics import median
from collections import namedtuple
from math import sqrt

Point = namedtuple('Point', ['x', 'y'])
PairDistance = namedtuple('PairDistance', ['points', 'distance'])


def dist_func(point_a: Point, point_b: Point) -> float:
    return sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)


def _closest_pair(
    points: list[Point],
) -> PairDistance:
    """
    Find closest pair of points on 2d plane using divide-and-conquer algorithm.
    Running time of this solution is O(n) = n*log(n)
    See http://people.csail.mit.edu/indyk/6.838-old/handouts/lec17.pdf for details
    and computational complexity estimation.
    """
    if len(points) >= 4:
        median_x_value = median([point.x for point in points])
        res_left, res_right = (
            _closest_pair([point for point in points if point.x < median_x_value]),
            _closest_pair([point for point in points if point.x >= median_x_value]),
        )
        min_dst_pair = sorted((res_left, res_right), key=lambda x: x.distance)[0]
        min_distance = min_dst_pair.distance
        # Check points within min_distance from the median_x_value (split line)
        points_to_check = sorted(
            [
                point
                for point in points
                if median_x_value - min_distance < point.x < median_x_value + min_distance
            ],
            key=lambda point: point.y,
        )
        for i, point_a in enumerate(points_to_check[:-1]):
            for point_b in points_to_check[
                i + 1 : i + 8
            ]:  # There may be up to 7 other points within min_distance vicinity (see link in docstring)
                if (cur_dist := dist_func(point_a, point_b)) < min_distance:
                    min_distance = cur_dist
                    min_dst_pair = PairDistance(points=(point_a, point_b), distance=cur_dist)
    elif len(points) == 3:
        min_dst_pair = sorted(
            (
                PairDistance(points=(points[0], points[1]), distance=dist_func(points[0], points[1])),
                PairDistance(points=(points[0], points[2]), distance=dist_func(points[0], points[2])),
                PairDistance(points=(points[1], points[2]), distance=dist_func(points[1], points[2])),
            ),
            key=lambda x: x.distance,
        )[0]
    else:
        min_dst_pair = PairDistance(points=(points[0], points[1]), distance=dist_func(points[0], points[1]))
    return min_dst_pair


def closest_pair(points: tuple[tuple[int, int]]) -> tuple[tuple[int, int]]:
    pair = _closest_pair([Point(x=item[0], y=item[1]) for item in points]).points
    return ((pair[0].x, pair[0].y), (pair[1].x, pair[1].y))


def assert_equals(x, y):
    try:
        assert x == y
    except AssertionError as exc:
        print(f'# Error\n{x} != {y}')
        raise


if __name__ == '__main__':
    # print(
    #     closest_pair(
    #         ((2, 2), (2, 8), (5, 5), (6, 3), (6, 7), (7, 4), (7, 9))  # A  # B  # C  # D  # E  # F  # G
    #     ),
    #     ((6, 3), (7, 4)),
    # )

    # print(
    #     closest_pair(
    #         (
    #             (2, 2),
    #             (2, 8),
    #             (5, 5),
    #             (6, 3),
    #             (5.90, 4),
    #             (6.05, 3.95),
    #             (6, 7),
    #             (7, 4),
    #             (7, 9),
    #         )  # A  # B  # C  # D  # E  # F  # G
    #     ),
    #     ((6.49, 3.95), (6.51, 4)),
    # )

    # print(
    #     closest_pair(
    #         (
    #             (2, 2),  # A
    #             (2, 8),  # B
    #             (5, 5),  # C
    #             (5, 5),  # C
    #             (6, 3),  # D
    #             (6, 7),  # E
    #             (7, 4),  # F
    #             (7, 9),  # G
    #         )
    #     ),
    #     ((5, 5), (5, 5)),
    # )

    res = closest_pair(
        (
            (0.34254190548120844, -0.4352645004407133),
            (0.13654831654770386, -0.49079619804808955),
            (0.3411296616868056, -0.8790572797756137),
            (0.34179261317248444, -0.7948273603267124),
            (0.4380163151894094, -0.4130424128584955),
            (0.26305152762829426, -0.5906826212142876),
            (0.20392780605686123, -0.7209542316028631),
            (0.23960467337946761, -0.7955627090744175),
            (0.4718424635441121, -0.535126014094463),
            (0.13898086967676104, -0.9670160245549624),
            (0.4093846681078857, -0.5768185490735611),
            (0.05007652071287089, -0.6598524708852953),
            (0.20075901883435981, -0.6269460433272465),
            (0.43370432096625466, -0.759182368442386),
            (0.22762582803130674, -0.9477307202274678),
            (0.4125319372480635, -0.7415897675075463),
            (0.1314548960203536, -0.8592186275513636),
            (0.5480797121620516, -0.8396513198301734),
            (0.4636121828847085, -0.8909421374372289),
            (0.06362034211014175, -0.7239939328829629),
            (0.5161569767659209, -0.6547535221736791),
            (0.024920093316606745, -0.5418215710960853),
            (0.4147292518513249, -0.6629861428293855),
            (0.2845992473144673, -0.6806869559830533),
            (0.2447810765884102, -0.4664686572858052),
            (0.5591643198863674, -0.7453686392332656),
        )
    )
    print(f'Res {res=}')
    print(
        f'Dist {dist_func(Point(x=0.43370432096625466, y=-0.759182368442386),Point(x=0.4125319372480635, y=-0.7415897675075463),)}'
    )
    # assert res == ((0.4125319372480635, -0.7415897675075463), (0.43370432096625466, -0.759182368442386))

    print('Success')
