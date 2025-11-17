# test_coffeeMachine.py

import pytest
from unittest.mock import patch, MagicMock
import coffeeMachine

# ============================================================================
# 1. FIXTURES - Setup and Teardown
# ============================================================================

@pytest.fixture
def fresh_resources():
    """Fixture to provide fresh resource state for each test"""
    return {
        "Water": 300,
        "Milk": 200,
        "Coffee": 100,
        "Money": 0,
    }

@pytest.fixture
def sample_menu():
    """Fixture to provide menu data"""
    return {
        "espresso": {
            "Water": 50,
            "Milk": 0,
            "Coffee": 18,
            "Cost": 2
        },
        "latte": {
            "Water": 200,
            "Milk": 150,
            "Coffee": 24,
            "Cost": 3
        },
        "cappuccino": {
            "Water": 250,
            "Milk": 100,
            "Coffee": 24,
            "Cost": 4
        }
    }

@pytest.fixture
def low_resources():
    """Fixture for testing low resource scenarios"""
    return {
        "Water": 30,
        "Milk": 10,
        "Coffee": 5,
        "Money": 0,
    }

@pytest.fixture(autouse=True)
def reset_resources():
    """
    AUTO-USE FIXTURE: Automatically resets resources before each test
    This ensures each test starts with fresh state
    """
    # Setup: Reset resources to initial state
    coffeeMachine.resource = {
        "Water": 300,
        "Milk": 200,
        "Coffee": 100,
        "Money": 0,
    }
    
    print("\n[Setup] Resources reset to initial state")
    
    yield  # Test runs here
    
    # Teardown: Optional cleanup
    print("\n[Teardown] Test completed, resources cleaned up")


# ============================================================================
# 2. BASIC TESTS - Testing check_resource() function
# ============================================================================

def test_check_resource_sufficient_espresso():
    """Test that check_resource returns True when resources are sufficient for espresso"""
    result = coffeeMachine.check_resource("espresso")
    assert result is True

def test_check_resource_sufficient_latte():
    """Test that check_resource returns True when resources are sufficient for latte"""
    result = coffeeMachine.check_resource("latte")
    assert result is True

def test_check_resource_sufficient_cappuccino():
    """Test that check_resource returns True when resources are sufficient for cappuccino"""
    result = coffeeMachine.check_resource("cappuccino")
    assert result is True

def test_check_resource_insufficient(capsys):
    """Test that check_resource returns False when resources are insufficient"""
    # Set resources to low values
    coffeeMachine.resource["Water"] = 10
    coffeeMachine.resource["Milk"] = 5
    coffeeMachine.resource["Coffee"] = 2
    
    result = coffeeMachine.check_resource("latte")
    captured = capsys.readouterr()
    
    assert result is False
    assert "Out of stock" in captured.out


# ============================================================================
# 3. PARAMETRIZE - Testing multiple drink types
# ============================================================================

@pytest.mark.parametrize("drink,expected", [
    ("espresso", True),
    ("latte", True),
    ("cappuccino", True),
])
def test_check_resource_parametrized(drink, expected):
    """Parametrized test for checking resources for different drinks"""
    result = coffeeMachine.check_resource(drink)
    assert result == expected


# ============================================================================
# 4. TESTING cash_machine() function
# ============================================================================

def test_cash_machine_exact_payment():
    """Test cash_machine with exact payment amount"""
    # Espresso costs $2.00
    # Payment: 8 quarters = $2.00
    result = coffeeMachine.cash_machine(q=8, d=0, n=0, p=0, item="espresso")
    assert result is True
    assert coffeeMachine.resource["Money"] == 2

def test_cash_machine_overpayment(capsys):
    """Test cash_machine with overpayment and verify change is returned"""
    # Espresso costs $2.00
    # Payment: 12 quarters = $3.00
    result = coffeeMachine.cash_machine(q=12, d=0, n=0, p=0, item="espresso")
    captured = capsys.readouterr()
    
    assert result is True
    assert "balance amount" in captured.out

def test_cash_machine_insufficient_payment(capsys):
    """Test cash_machine with insufficient payment"""
    # Latte costs $3.00
    # Payment: 4 quarters = $1.00
    result = coffeeMachine.cash_machine(q=4, d=0, n=0, p=0, item="latte")
    captured = capsys.readouterr()
    
    assert result is False
    assert "Insufficient money" in captured.out

@pytest.mark.parametrize("quarters,dimes,nickels,pennies,item,expected", [
    (8, 0, 0, 0, "espresso", True),    # Exact: $2.00
    (12, 0, 0, 0, "latte", True),      # Exact: $3.00
    (16, 0, 0, 0, "cappuccino", True), # Exact: $4.00
    (4, 0, 0, 0, "latte", False),      # Insufficient: $1.00 for $3.00 item
    (10, 5, 10, 25, "cappuccino", False), # Mixed coins: $3.75 for $4.00
])
def test_cash_machine_various_payments(quarters, dimes, nickels, pennies, item, expected):
    """Parametrized test for various payment scenarios"""
    result = coffeeMachine.cash_machine(q=quarters, d=dimes, n=nickels, p=pennies, item=item)
    assert result == expected


# ============================================================================
# 5. TESTING update_resource() function
# ============================================================================

def test_update_resource_espresso(fresh_resources):
    """Test that resources are correctly updated after making espresso"""
    coffeeMachine.resource = fresh_resources.copy()
    
    initial_water = coffeeMachine.resource["Water"]
    initial_coffee = coffeeMachine.resource["Coffee"]
    
    coffeeMachine.update_resource("espresso")
    
    assert coffeeMachine.resource["Water"] == initial_water - 50
    assert coffeeMachine.resource["Coffee"] == initial_coffee - 18
    assert coffeeMachine.resource["Milk"] == 200  # Should not change

def test_update_resource_latte(fresh_resources):
    """Test that resources are correctly updated after making latte"""
    coffeeMachine.resource = fresh_resources.copy()
    
    initial_water = coffeeMachine.resource["Water"]
    initial_milk = coffeeMachine.resource["Milk"]
    initial_coffee = coffeeMachine.resource["Coffee"]
    
    coffeeMachine.update_resource("latte")
    
    assert coffeeMachine.resource["Water"] == initial_water - 200
    assert coffeeMachine.resource["Milk"] == initial_milk - 150
    assert coffeeMachine.resource["Coffee"] == initial_coffee - 24

def test_update_resource_cappuccino(fresh_resources):
    """Test that resources are correctly updated after making cappuccino"""
    coffeeMachine.resource = fresh_resources.copy()
    
    coffeeMachine.update_resource("cappuccino")
    
    assert coffeeMachine.resource["Water"] == 50   # 300 - 250
    assert coffeeMachine.resource["Milk"] == 100   # 200 - 100
    assert coffeeMachine.resource["Coffee"] == 76  # 100 - 24

@pytest.mark.parametrize("drink,water_used,milk_used,coffee_used", [
    ("espresso", 50, 0, 18),
    ("latte", 200, 150, 24),
    ("cappuccino", 250, 100, 24),
])
def test_update_resource_parametrized(drink, water_used, milk_used, coffee_used):
    """Parametrized test for resource updates"""
    initial_water = coffeeMachine.resource["Water"]
    initial_milk = coffeeMachine.resource["Milk"]
    initial_coffee = coffeeMachine.resource["Coffee"]
    
    coffeeMachine.update_resource(drink)
    
    assert coffeeMachine.resource["Water"] == initial_water - water_used
    assert coffeeMachine.resource["Milk"] == initial_milk - milk_used
    assert coffeeMachine.resource["Coffee"] == initial_coffee - coffee_used


# ============================================================================
# 6. TESTING EDGE CASES with pytest.raises()
# ============================================================================

def test_check_resource_invalid_item():
    """Test that check_resource handles invalid menu items"""
    with pytest.raises(KeyError):
        coffeeMachine.check_resource("mocha")  # Item not in menu

def test_cash_machine_negative_coins():
    """Test cash_machine behavior with negative coin values"""
    # This should be handled but currently isn't - good test for future improvement
    result = coffeeMachine.cash_machine(q=-5, d=0, n=0, p=0, item="espresso")
    # Currently this will calculate negative payment
    assert result is False


# ============================================================================
# 7. TESTING WITH FIXTURES - Complex scenarios
# ============================================================================

def test_multiple_orders_deplete_resources(fresh_resources):
    """Test making multiple drinks until resources run low"""
    coffeeMachine.resource = fresh_resources.copy()
    
    # Make 3 lattes (each uses 200 water, 150 milk, 24 coffee)
    coffeeMachine.update_resource("latte")
    coffeeMachine.update_resource("latte")
    
    # After 2 lattes: Water should be low
    # 300 - (200*2) = -100 (which is impossible, but update doesn't check)
    assert coffeeMachine.resource["Water"] < 200

def test_resource_check_after_multiple_drinks(low_resources):
    """Test resource checking with low initial resources"""
    coffeeMachine.resource = low_resources.copy()
    
    # Should fail for any drink due to low resources
    result = coffeeMachine.check_resource("espresso")
    assert result is False


# ============================================================================
# 8. INTEGRATION TESTS - Testing full workflow
# ============================================================================

def test_full_espresso_workflow(capsys):
    """Integration test: Full workflow for ordering an espresso"""
    # Step 1: Check resources
    assert coffeeMachine.check_resource("espresso") is True
    
    # Step 2: Process payment
    assert coffeeMachine.cash_machine(q=8, d=0, n=0, p=0, item="espresso") is True
    
    # Step 3: Update resources
    initial_water = coffeeMachine.resource["Water"]
    coffeeMachine.update_resource("espresso")
    
    # Step 4: Verify resources updated
    assert coffeeMachine.resource["Water"] == initial_water - 50
    assert coffeeMachine.resource["Money"] == 2

def test_full_failed_workflow_insufficient_funds(capsys):
    """Integration test: Full workflow with insufficient payment"""
    # Check resources (should pass)
    assert coffeeMachine.check_resource("cappuccino") is True
    
    # Try to pay with insufficient funds
    result = coffeeMachine.cash_machine(q=4, d=0, n=0, p=0, item="cappuccino")
    captured = capsys.readouterr()
    
    assert result is False
    assert "Insufficient money" in captured.out
    
    # Resources should NOT be updated
    assert coffeeMachine.resource["Water"] == 300

def test_full_failed_workflow_out_of_stock():
    """Integration test: Full workflow with insufficient resources"""
    # Deplete resources
    coffeeMachine.resource["Water"] = 10
    
    # Check resources (should fail)
    assert coffeeMachine.check_resource("latte") is False
    
    # Payment should not be processed if resources check fails
    # (In actual code flow, this wouldn't be reached)


# ============================================================================
# 9. TESTING WITH pytest.approx() - For floating point calculations
# ============================================================================

def test_cash_machine_float_precision():
    """Test cash machine with floating point precision"""
    # Payment: 2 quarters (0.50) + 15 dimes (1.50) = $2.00
    result = coffeeMachine.cash_machine(q=2, d=15, n=0, p=0, item="espresso")
    assert result is True
    assert coffeeMachine.resource["Money"] == pytest.approx(2.0, abs=0.01)


# ============================================================================
# 10. ADDITIONAL TESTS - Testing menu structure
# ============================================================================

def test_menu_structure(sample_menu):
    """Test that menu has correct structure"""
    for drink in ["espresso", "latte", "cappuccino"]:
        assert drink in coffeeMachine.menu
        assert "Water" in coffeeMachine.menu[drink]
        assert "Milk" in coffeeMachine.menu[drink]
        assert "Coffee" in coffeeMachine.menu[drink]
        assert "Cost" in coffeeMachine.menu[drink]

def test_menu_costs_are_positive():
    """Test that all menu items have positive costs"""
    for drink, details in coffeeMachine.menu.items():
        assert details["Cost"] > 0

def test_resource_keys_exist():
    """Test that all required resource keys exist"""
    required_keys = ["Water", "Milk", "Coffee", "Money"]
    for key in required_keys:
        assert key in coffeeMachine.resource


# ============================================================================
# 11. MARKS - Categorizing tests
# ============================================================================

@pytest.mark.slow
def test_resource_depletion_simulation():
    """Slow test: Simulate multiple orders until resources depleted"""
    orders = 0
    while coffeeMachine.check_resource("espresso") and orders < 5:
        coffeeMachine.update_resource("espresso")
        orders += 1
    
    assert orders > 0
    assert coffeeMachine.resource["Water"] < 300

@pytest.mark.integration
def test_complete_coffee_shop_day():
    """Integration test: Simulate a day at the coffee shop"""
    # Morning rush: 2 espressos
    coffeeMachine.update_resource("espresso")
    coffeeMachine.update_resource("espresso")
    
    # Afternoon: 1 latte
    coffeeMachine.update_resource("latte")
    
    # Check remaining resources
    assert coffeeMachine.resource["Water"] < 300
    assert coffeeMachine.resource["Coffee"] < 100


# ============================================================================
# RUNNING INSTRUCTIONS
# ============================================================================
"""
To run these tests:

1. Basic run:
   pytest test_coffeeMachine.py

2. Verbose output:
   pytest test_coffeeMachine.py -v

3. Run with print statements:
   pytest test_coffeeMachine.py -s

4. Run specific test:
   pytest test_coffeeMachine.py::test_check_resource_sufficient_espresso

5. Run parametrized tests only:
   pytest test_coffeeMachine.py -k "parametrized"

6. Run slow tests only:
   pytest test_coffeeMachine.py -m slow

7. Run integration tests:
   pytest test_coffeeMachine.py -m integration

8. Run with coverage:
   pytest test_coffeeMachine.py --cov=coffeeMachine
"""