import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# overage_charge

def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_zero_data_no_charge():
    assert overage_charge("basic", 0, False, False) == 0


def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0


def test_exactly_included_data_no_charge():
    # extra == 0 takes the "extra <= 0" branch
    assert overage_charge("standard", 5, False, False) == 0


def test_loyal_bonus_covers_usage():
    # basic 2 GB + 1 loyalty GB = 3 GB, so 3 GB used is free
    assert overage_charge("basic", 3, False, True) == 0


def test_loyal_premium_gets_no_bonus():
    # is_loyal is True but plan is premium, so no extra GB
    assert overage_charge("premium", 12, False, True) == 2 * 15


def test_home_overage_standard_rate():
    assert overage_charge("standard", 7, False, False) == 2 * 15


def test_roaming_overage_rate():
    assert overage_charge("standard", 7, True, False) == 2 * 40


def test_home_extra_exactly_10_no_heavy_rate():
    # extra == 10 is not > 10
    assert overage_charge("standard", 15, False, False) == 10 * 15


def test_home_heavy_overage():
    # extra > 10 and not roaming: 15 + 10 = 25 per GB
    assert overage_charge("standard", 20, False, False) == 15 * 25


def test_roaming_heavy_overage():
    # extra > 10 and roaming: 40 + 10 + 5 = 55 per GB
    assert overage_charge("standard", 16, True, False) == 11 * 55


def test_loyal_roaming_heavy_overage():
    assert overage_charge("basic", 20, True, True) == 17 * 55


# recharge_allowed

def test_kyc_pending_at_limit_allowed():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_over_limit_rejected():
    assert recharge_allowed(201, 0, True) is False


def test_recharge_at_max_amount_allowed():
    assert recharge_allowed(2000, 2, False) is True


def test_recharge_over_max_amount_rejected():
    assert recharge_allowed(2001, 0, False) is False


def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_too_many_pending_recharges_rejected():
    assert recharge_allowed(500, 3, False) is False


# validity_status

def test_prepaid_active_at_cutoff():
    # prepaid cutoff 0
    assert validity_status(0, True, False) == "active"


def test_prepaid_grace_just_below_cutoff():
    assert validity_status(-1, True, False) == "grace"


def test_prepaid_grace_at_lower_limit():
    assert validity_status(-15, True, False) == "grace"


def test_prepaid_expired():
    assert validity_status(-16, True, False) == "expired"


def test_prepaid_with_addon():
    # cutoff 0 + 2 = 2
    assert validity_status(2, True, True) == "active"
    assert validity_status(1, True, True) == "grace"


def test_postpaid_active_at_cutoff():
    # postpaid cutoff 3
    assert validity_status(3, False, False) == "active"


def test_postpaid_grace():
    assert validity_status(2, False, False) == "grace"
    assert validity_status(-12, False, False) == "grace"


def test_postpaid_expired():
    assert validity_status(-13, False, False) == "expired"


def test_postpaid_with_addon():
    # cutoff 3 + 2 = 5, grace down to -10
    assert validity_status(5, False, True) == "active"
    assert validity_status(-10, False, True) == "grace"
    assert validity_status(-11, False, True) == "expired"
