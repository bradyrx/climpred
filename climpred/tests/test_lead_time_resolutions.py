import numpy as np
import pandas as pd
import pytest
import xarray as xr

from climpred.prediction import compute_hindcast, compute_perfect_model

#  VALID_LEAD_UNITS = ['seasons']


@pytest.fixture()
def daily_initialized():
    init = pd.date_range('1990-01', '1990-03', freq='D')
    lead = np.arange(5)
    member = np.arange(5)
    return xr.DataArray(
        np.random.rand(len(init), len(lead), len(member)),
        dims=['init', 'lead', 'member'],
        coords=[init, lead, member],
    )


@pytest.fixture()
def daily_reference():
    time = pd.date_range('1990-01', '1990-03', freq='D')
    return xr.DataArray(np.random.rand(len(time)), dims=['time'], coords=[time])


@pytest.fixture()
def monthly_initialized():
    init = pd.date_range('1990-01', '1996-01', freq='MS')
    lead = np.arange(5)
    member = np.arange(5)
    return xr.DataArray(
        np.random.rand(len(init), len(lead), len(member)),
        dims=['init', 'lead', 'member'],
        coords=[init, lead, member],
    )


@pytest.fixture()
def monthly_reference():
    time = pd.date_range('1990-01', '1996-01', freq='MS')
    return xr.DataArray(np.random.rand(len(time)), dims=['time'], coords=[time])


def test_daily_resolution_hindcast(daily_initialized, daily_reference):
    """Tests that daily resolution hindcast predictions work."""
    daily_initialized.lead.attrs['units'] = 'days'
    assert compute_hindcast(daily_initialized, daily_reference).all()


def test_daily_resolution_perfect_model(daily_initialized, daily_reference):
    """Tests that daily resolution perfect model predictions work."""
    daily_initialized.lead.attrs['units'] = 'days'
    assert compute_perfect_model(daily_initialized, daily_reference).all()


def test_pentadal_resolution_hindcast(daily_initialized, daily_reference):
    """Tests that pentadal resolution hindcast predictions work."""
    pentadal_hindcast = daily_initialized.resample(init='5D').mean()
    pentadal_reference = daily_reference.resample(time='5D').mean()
    pentadal_hindcast.lead.attrs['units'] = 'pentads'
    assert compute_hindcast(pentadal_hindcast, pentadal_reference).all()


def test_pentadal_resolution_perfect_model(daily_initialized, daily_reference):
    """Tests that pentadal resolution perfect model predictions work."""
    pentadal_pm = daily_initialized.resample(init='5D').mean()
    pentadal_reference = daily_reference.resample(time='5D').mean()
    pentadal_pm.lead.attrs['units'] = 'pentads'
    assert compute_hindcast(pentadal_pm, pentadal_reference).all()


def test_weekly_resolution_hindcast(daily_initialized, daily_reference):
    """Tests that weekly resolution hindcast predictions work."""
    weekly_hindcast = daily_initialized.resample(init='W').mean()
    weekly_reference = daily_reference.resample(time='W').mean()
    weekly_hindcast.lead.attrs['units'] = 'weeks'
    assert compute_hindcast(weekly_hindcast, weekly_reference).all()


def test_weekly_resolution_perfect_model(daily_initialized, daily_reference):
    """Tests that weekly resolution perfect model predictions work."""
    weekly_pm = daily_initialized.resample(init='W').mean()
    weekly_reference = daily_reference.resample(time='W').mean()
    weekly_pm.lead.attrs['units'] = 'weeks'
    assert compute_hindcast(weekly_pm, weekly_reference).all()


def test_monthly_resolution_hindcast(monthly_initialized, monthly_reference):
    """Tests that monthly resolution hindcast predictions work."""
    monthly_initialized.lead.attrs['units'] = 'months'
    assert compute_hindcast(monthly_initialized, monthly_reference).all()


def test_monthly_resolution_perfect_model(monthly_initialized, monthly_reference):
    """Tests that monthly resolution perfect model predictions work."""
    monthly_initialized.lead.attrs['units'] = 'months'
    assert compute_perfect_model(monthly_initialized, monthly_reference).all()


def test_yearly_resolution_hindcast(monthly_initialized, monthly_reference):
    """Tests that yearly resolution hindcast predictions work."""
    yearly_hindcast = monthly_initialized.resample(init='YS').mean()
    yearly_reference = monthly_reference.resample(time='YS').mean()
    yearly_hindcast.lead.attrs['units'] = 'years'
    assert compute_hindcast(yearly_hindcast, yearly_reference).all()


def test_yearly_resolution_perfect_model(monthly_initialized, monthly_reference):
    """Tests that yearly resolution perfect model predictions work."""
    yearly_pm = monthly_initialized.resample(init='YS').mean()
    yearly_reference = monthly_reference.resample(time='YS').mean()
    yearly_pm.lead.attrs['units'] = 'years'
    assert compute_hindcast(yearly_pm, yearly_reference).all()
