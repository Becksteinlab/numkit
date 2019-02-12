# -*- coding: utf-8 -*-
# numkit.integration test cases
# Part of GromacsWrapper
# Copyright (c) Oliver Beckstein <orbeckst@gmail.com>
# Published under the Modified BSD Licence.

import numkit.timeseries

import numpy as np
from numpy.testing import assert_almost_equal, assert_equal

import pytest

@pytest.fixture(scope="module")
def data():
    X = np.linspace(-10,10,50000)
    yerr = np.random.randn(len(X))*0.05
    return np.vstack((X, np.sin(X) + yerr))

binsizes = (5, 100, 1000, 10000)

class TestRegularizedFunction(object):
    @pytest.mark.parametrize("bins", binsizes)
    def test_max(self, data, bins):
        Y, X = numkit.timeseries.max_histogrammed_function(data[0], data[1], bins=bins)
        assert len(X) == bins
        assert_almost_equal(np.max(Y), np.max(data[1]))

    @pytest.mark.filterwarnings("ignore:tcorrel")
    @pytest.mark.parametrize("func", (
        "rms_histogrammed_function",
        "mean_histogrammed_function",
        "std_histogrammed_function",
        "min_histogrammed_function",
        "max_histogrammed_function",
        "median_histogrammed_function",
        "percentile_histogrammed_function",
        "error_histogrammed_function",
        "circmean_histogrammed_function",
        "circstd_histogrammed_function",
        "tc_histogrammed_function",
        ))
    @pytest.mark.parametrize("bins", binsizes)
    def test_func(self, func, data, bins):
        function = getattr(numkit.timeseries, func)
        Y, X = function(data[0], data[1], bins=bins)
        assert len(X) == bins
        # assert_almost_equal(np.max(Y), np.max(data[1]))
        # add test for Y data (but has randomness)

    @pytest.mark.parametrize("func", (
        "error_histogrammed_function",
        "tc_histogrammed_function",
        ))
    @pytest.mark.parametrize("bins", [1000, 10000])
    def test_func_warns(self, func, data, bins):
        function = getattr(numkit.timeseries, func)
        with pytest.warns(numkit.LowAccuracyWarning):
            Y, X = function(data[0], data[1], bins=bins)


@pytest.mark.parametrize('window', (
    'flat', 'hanning', 'hamming', 'bartlett', 'blackman'))
def test_smooth(data, window):
    a = numkit.timeseries.smooth(data[1], window=window)
    assert len(a) == len(data[1])
