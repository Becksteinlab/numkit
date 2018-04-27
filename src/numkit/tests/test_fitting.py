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
from numpy.testing import assert_equal, assert_almost_equal

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

