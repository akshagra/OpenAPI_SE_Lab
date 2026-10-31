import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# overage_charge

def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0


def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_home_overage_standard_rate():
    # 7 GB on standard (5 GB included) -> 2 GB extra at 15
    assert overage_charge("standard", 7, False, False) == 30


def test_loyal_roaming_heavy_overage():
    # basic 2 GB + 1 loyalty GB = 3 GB included, 20 GB used -> 17 GB extra
    # roaming 40 + heavy-use 10 + roaming surcharge 5 = 55 per GB
    assert overage_charge("basic", 20, True, True) == 17 * 55


# recharge_allowed

def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_recharge_kyc_pending_small_amount():
    assert recharge_allowed(150, 0, True) is True


def test_recharge_over_limit_rejected():
    assert recharge_allowed(2500, 0, False) is False


# validity_status

def test_prepaid_active():
    assert validity_status(5, True, False) == "active"


def test_postpaid_with_addon_grace():
    # cutoff 3 + 2 = 5, grace down to -10
    assert validity_status(-5, False, True) == "grace"


def test_postpaid_expired():
    # cutoff 3, grace down to -12
    assert validity_status(-20, False, False) == "expired"
