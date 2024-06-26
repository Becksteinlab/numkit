# -*- coding: utf-8 -*-
# numkit.integration test cases
# Part of GromacsWrapper
# Copyright (c) Oliver Beckstein <orbeckst@gmail.com>
# Published under the Modified BSD Licence.

"""
===================================
 Test cases for numkit.integration
====================================

"""
import pytest

import numpy
from numpy.testing import assert_equal, assert_almost_equal

import numkit.integration


class Test_simps_error(object):
    # special case with constant spacing and constant error (=1.0) so
    # that one can easily calculate the correct errors
    @pytest.fixture
    def spacings(self):
        even_x = numpy.linspace(0,10,10)
        odd_x = numpy.linspace(0,10,11)
        return {
            'even_x': even_x,                             # const spacing
            'even_dx': numpy.diff(even_x)[0],
            'even_dy': 1.0 * numpy.ones(10, dtype=float), # const error
            'odd_x': odd_x,                               # const spacing
            'odd_dx': numpy.diff(odd_x)[0],
            'odd_dy': 1.0 * numpy.ones(11, dtype=float),  # const error
        }

    def err_analytic_odd(self, spacings):
        # error for all dy and dx equal, using only Simpson's rule:
        #  err**2 = (h/3)^2(df1^2 + (4df2)^2 + (2df3)^2 + ... + (4df_N-1)^2 + (dfN)^2)
        #  err**2 = (h/3)^2 dy^2 (10(N-1)-(2^2-1)+1)
        dy = spacings['odd_dy'][0]
        N = spacings['odd_dy'].shape[0]
        h = spacings['odd_dx']
        return numpy.sqrt((h/3)**2 * dy**2 * (10*(N-1)-2))

    def err_analytic_even(self, spacings):
        # err**2 = (h/6)^2((3df1)^2 + ((3+2)df2)^2 + (8df3)^2 + (4df4)^2 + (8df5)^2 + ... + (2dfN)^2)
        # special case for constant dy and constant spacing
        dy = spacings['even_dy'][0]
        N = spacings['even_dy'].shape[0]
        h = spacings['even_dx']
        #err_analytic**2 = (h/6.0)**2 * dy**2 * (2*3**2 + 12 + (8**2+4**2)*0.5*(N-2) - (4**2-2**2) + 2**2)
        return numpy.sqrt((h/6.0)**2 * dy**2 * (40.*N - 58.))

    def test_odd_const_dx(self, spacings):
        err_dx = numkit.integration.simps_error(spacings['odd_dy'], dx=spacings['odd_dx'])
        err_analytic = self.err_analytic_odd(spacings)
        assert_equal(err_dx, err_analytic, err_msg="Simps error for const spacing dx")

    def test_odd_const_x(self, spacings):
        err_x =  numkit.integration.simps_error(spacings['odd_dy'], x=spacings['odd_x'])
        err_analytic = self.err_analytic_odd(spacings)
        assert_equal(err_x, err_analytic, err_msg="Simps error for const spacing dx, from abscissas")

    def test_odd_const_x_dx(self, spacings):
        err_dx = numkit.integration.simps_error(spacings['odd_dy'], dx=spacings['odd_dx'])
        err_x =  numkit.integration.simps_error(spacings['odd_dy'], x=spacings['odd_x'])
        assert_equal(err_x, err_dx, err_msg="Simps error for const spacing: either scalar dx or abscissas x")

    def test_even_first(self, spacings):
        err_analytic = self.err_analytic_even(spacings)
        err = numkit.integration.simps_error(spacings['even_dy'], dx=spacings['even_dx'], even="first")
        assert_almost_equal(err, err_analytic,
                            err_msg="Even # points, first: Simps+Trapezoid stat. error: const dx and const dy")

    def test_even_last(self, spacings):
        err_analytic = self.err_analytic_even(spacings)
        err = numkit.integration.simps_error(spacings['even_dy'], dx=spacings['even_dx'], even="last")
        assert_almost_equal(err, err_analytic,
                            err_msg="Even # points, last: Trapezoid+Simps stat. error: const dx and const dy")

    def test_even_avg(self, spacings):
        err_analytic = self.err_analytic_even(spacings)
        err = numkit.integration.simps_error(spacings['even_dy'], dx=spacings['even_dx'], even="avg")
        assert_almost_equal(err, err_analytic,
                            err_msg="Even # points, avg: Simps+Trapezoid stat. error: const dx and const dy")

    def Xtest_h1h2(self):
        x = numpy.array([0,1,2,4.,5])
        y = 2*x
        dy = numpy.array([1.,1,1,1,1])

        err = numkit.integration.simps_error(dy,x=x)
        # check correctness!!
        assert_almost_equal(err, 2.7613402542968153, err_msg="Simps error for un-even spacing")


def test_uneven_spacing():
    # simple regression test
    DY = numpy.array([0.1, 0.2, 0.1, 0.2, 1.0])
    X = numpy.array([-1, 0, 2, 2.5, 5])
    err = numkit.integration.simps_error(DY, x=X)
    assert err == pytest.approx(0.7632168761236874)

