import pytest
import blackjack21game


@pytest.fixture
def all_cards():
    # Test that all cards are within the valid range
    return [11,2,3,4,5,6,7,8,9,10,10,10,10]


#Basic assertion tests
def test_is_blackjack():
    # Test blackjack detection
    assert blackjack21game.is_blackjack([10, 11]) == True
    assert blackjack21game.is_blackjack([9, 10]) == False
    assert blackjack21game.is_blackjack([7, 4, 10]) == True
    assert blackjack21game.is_blackjack([5, 5, 10]) == False

def test_push_returns_valid_card(all_cards):
    for _ in range(100):
        card = blackjack21game.push()
        assert card in all_cards

@pytest.fixture
def winning_user_deck():
    return [10, 9]

def test_win_check_for_user(winning_user_deck, capsys):
    blackjack21game.computer_deck = [10, 6]
    blackjack21game.user_deck = winning_user_deck
    result = blackjack21game.win_check()
    captured = capsys.readouterr()
    assert "You win" in captured.out

@pytest.fixture(autouse=True, scope="function")
def reset_decks():
    yield
    blackjack21game.computer_deck = []
    blackjack21game.user_deck = []

# Parameterized test for blackjack

@pytest.mark.parametrize("deck, expected", [
    ([10, 11], True),
    ([9, 10], False),
    ([7, 4, 10], True),
    ([5, 5, 10], False),
])

def test_is_blackjack_parametrized(deck, expected):
    assert blackjack21game.is_blackjack(deck) == expected

# Multiple parameter test for blackjack
@pytest.mark.parametrize("user_sum, computer_sum, expected", [
    (20, 18, True),
    (19, 20, False),
    (21, 19, False),
    (18, 21, False),
])

def test_multiple_param_check(user_sum, computer_sum, expected, capsys):
    blackjack21game.user_deck = [user_sum]
    blackjack21game.computer_deck = [computer_sum]
    result = blackjack21game.win_check()
    captured = capsys.readouterr()
    if expected:
        assert "You win" in captured.out
    else:
        assert "Computer won" in captured.out

# Test with pytest.raise

def test_blacjack_with_empty_deck():
    with pytest.raises(ValueError):
        blackjack21game.is_blackjack([])

# pytest.xfail example 
@pytest.mark.xfail(reason="Deliberate failure for testing")
def test_deliberate_fail():
    assert blackjack21game.is_blackjack([10, 9]) == True

# pytest.skip example
@pytest.mark.skip(reason="Skipping this test for now")
def test_skipped():
    assert blackjack21game.push() in blackjack21game.cards

# Autouse fixture example
@pytest.fixture(autouse=True)
def setup_and_teardown():
    print("\nSetup: Starting test")
    yield
    print("\nTeardown: Test finished")