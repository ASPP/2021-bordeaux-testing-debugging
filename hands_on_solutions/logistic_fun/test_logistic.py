import numpy as np
from numpy.testing import assert_allclose
import pytest

from logistic import f, iterate_f


@pytest.mark.parametrize(
    'x, r, expected',
    [
        (0.1, 2.2, 0.198),
        (0.2, 3.4, 0.544),
        (0.75, 1.7, 0.31875),
    ]
)
def test_f(x, r, expected):
    result = f(x, r)
    assert_allclose(result, expected)


@pytest.mark.parametrize(
    'x, r, it, expected',
    [
        (0.1, 2.2, 1, [0.198]),
        (0.2, 3.4, 4, [0.544, 0.843418, 0.449019, 0.841163]),
        (0.75, 1.7, 2, [0.31875, 0.369152]),
    ]
)
def test_iterate_f(x, r, it, expected):
    result = iterate_f(it, x, r)
    assert_allclose(result, expected, rtol=1e-5)


def test_attractor_converges(random_state):
    for _ in range(100):
        x = random_state.uniform(0, 1)
        result = iterate_f(100, x, 1.5)
        assert_allclose(result[-1], 1/3)



def test_chaotic_behavior(random_state):
    r = 3.8
    for _ in range(10):
        x = random_state.uniform(0, 1)
        result = iterate_f(100000, x, r)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)
        assert min(np.abs(np.diff(result[-1000:]))) > 1e-6


def test_fuzzy_sdic(random_state):
    """
    `f` is a function and `x0` and `y0` are two possible seeds.
    If `f` has SDIC then:
    there is a number `delta` such that for any `x0` there is a `y0` that is not
    more than `init_error` away from `x0`, where the initial condition `y0` has
    the property that there is some integer n such that after n iterations, the
    orbit is more than `delta` away from the orbit of `x0`. That is
    |xn-yn| > delta
    """
    deltas = random_state.rand(100)
    result_list = []
    for delta in deltas:
        x0 = random_state.rand()
        init_error = random_state.rand()
        y0max = x0 + init_error
        n = 10000
        l_x = iterate_f(n, x0, 3.8)
        l_y = iterate_f(n, y0max, 3.8)
        result_list.append(any(abs(l_x - l_y)>delta))
    assert any(result_list)