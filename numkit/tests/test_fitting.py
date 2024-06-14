# -*- coding: utf-8 -*-
# numkit.integration test cases
# Part of GromacsWrapper
# Copyright (c) Oliver Beckstein <orbeckst@gmail.com>
# Published under the Modified BSD Licence.

"""
===================================
 Test cases for numkit.fitting
====================================

"""
import numkit.fitting

import numpy as np
from numpy.testing import assert_equal, assert_almost_equal, assert_allclose

import pytest

@pytest.fixture(scope="module")
def linear_data(m=-2.8, t=123.45, sigma=1.5):
    def f(x):
        return m*x + t
    # make random numbers consistent
    np.random.seed(2018)
    X = np.linspace(-20, 20, 100)
    dY = sigma*np.random.standard_normal(size=len(X))
    Y = f(X) + dY
    return X, Y, dY

@pytest.fixture(scope="module")
def exp_decay_data(a=2.30785, sigma=1.5):
    def f(x):
        return np.exp(-a*x)
    # make random numbers consistent
    np.random.seed(2018)
    X = np.linspace(-4, 10, 100)
    dY = sigma*np.random.standard_normal(size=len(X))
    Y = f(X) + dY
    return X, Y, dY


@pytest.fixture(scope="module")
def gaussian_data(mu=-4.2, s=0.455, a=8.0, sigma=0.5):
    def f(x):
        return a/(np.sqrt(2*np.pi*s**2)) * np.exp(-(x-mu)**2/(2*s**2))
    # make random numbers consistent
    np.random.seed(2018)
    X = np.linspace(-10, 2, 100)
    dY = sigma*np.random.standard_normal(size=len(X))
    Y = f(X) + dY
    return X, Y, dY



@pytest.fixture(scope="module")
def linfit_noerror(linear_data):
    X, Y, _ = linear_data
    return numkit.fitting.linfit(X, Y)

@pytest.fixture(scope="module")
def linfit_witherror(linear_data):
    X, Y, dY = linear_data
    return numkit.fitting.linfit(X, Y, dy=dY)

@pytest.mark.parametrize("quantity,expected", [
    ("intercept", 123.29089673580293),
    ("slope", -2.8087043835295797),
    ("sigma_intercept", 0.1389869156801219),
    ("sigma_slope", 0.011916849634869048),
    ("parameter_correlation", 0),
    ("chi_square", 189.3101547566785),
    ("Q", 1.0)])
def test_linfit_noerror(linfit_noerror, quantity, expected):
    assert_almost_equal(linfit_noerror[quantity], expected)

@pytest.mark.parametrize("quantity,expected", [
    ("intercept", 123.4425486304815),
    ("slope", -2.8047542762556232),
    ("sigma_intercept", 0.007963180881154172),
    ("sigma_slope", 0.0025757387307418587),
    ("parameter_correlation", 0.7171768191864278),
    ("chi_square", 96.28302496281943),
    ("Q", 0.5301523165173313)])
def test_linfit_witherror(linfit_witherror, quantity, expected):
    assert_almost_equal(linfit_witherror[quantity], expected)


@pytest.fixture(scope="class")
def FitLin(linear_data):
    X, Y, _ = linear_data
    return numkit.fitting.FitLin(X, Y, parameters=(1, 0))

class TestFitLin(object):
    ref_x = np.linspace(-9.3, 5.7, 5)
    ref_y = np.array([149.4118475, 138.8792061, 128.3465646,
                      117.8139232, 107.2812817])

    def test_parameters(self, FitLin):
        assert_almost_equal(FitLin.parameters, [-2.8087044, 123.2908967])

    def test_fitting(self, FitLin):
        Y = FitLin.fit(self.ref_x)
        assert_almost_equal(Y, self.ref_y)


@pytest.fixture(scope="class")
def FitExp(exp_decay_data):
    X, Y, _ = exp_decay_data
    return numkit.fitting.FitExp(X, Y, parameters=(1.0,))

class TestFitExp(object):
    ref_x = np.linspace(-5, 5, 5)
    ref_y = np.array([1.0267685e+05, 3.2043229e+02, 1.0000000e+00,
                      3.1207841e-03, 9.7392934e-06])

    def test_parameters(self, FitExp):
        assert_almost_equal(FitExp.parameters, [2.3078684])

    def test_fitting(self, FitExp):
        Y = FitExp.fit(self.ref_x)
        assert_allclose(Y, self.ref_y)

def test_FitGauss(gaussian_data):
    X, Y, _ = gaussian_data
    fit = numkit.fitting.FitGauss(X, Y, parameters=(-2, 1.0, 5.0))
    assert_almost_equal(fit.parameters, [-4.2093312,  0.4403894,  7.6803708])

