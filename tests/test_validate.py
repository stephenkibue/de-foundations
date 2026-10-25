import pytest
from datetime import date
from src.kuku.validate import parse_date, parse_count, parse_flock, validate_row, ProductionRecord

GOOD_ROW = {
    "date": "01/10/2026",
    "flock": "b ",
    "eggs": "641",
    "birds": "800",
    "recorded_by": "Otieno"
}

@pytest.mark.parametrize("text", [
    "2026-10-01",
    "01/10/2026",
    " 2026-10-01 ",
])
def test_parse_date_valid(text):
    assert parse_date(text) == date(2026, 10, 1)

@pytest.mark.parametrize("text", [
    "2026-02-31",
    "1 Oct",
    "",
])
def test_parse_date_invalid(text):
    with pytest.raises(ValueError, match="not a real date"):
        parse_date(text)

@pytest.mark.parametrize("text, expected", [
    ("970", 970),
    (" 405 ", 405),
    ("1,010", 1010),
    ("0", 0),
])
def test_parse_count_valid(text, expected):
    assert parse_count(text, "eggs") == expected

@pytest.mark.parametrize("text, match_msg", [
    ("", "eggs is missing"),
    ("n/a", "eggs is not a number"),
    ("twelve hundred", "eggs is not a number"),
    ("-40", "eggs is negative"),
])
def test_parse_count_rejects(text, match_msg):
    with pytest.raises(ValueError, match=match_msg):
        parse_count(text, "eggs")

@pytest.mark.parametrize("text, expected", [
    ("A", "A"),
    ("b", "B"),
    ("C ", "C"),
])
def test_parse_flock_valid(text, expected):
    assert parse_flock(text) == expected

def test_parse_flock_invalid():
    with pytest.raises(ValueError, match="unknown flock"):
        parse_flock("D")

def test_validate_row_good():
    validated = validate_row(GOOD_ROW)
    assert validated.flock == "B"
    assert validated.date == date(2026, 10, 1)
    assert validated.eggs == 641
    assert validated.laying_rate() == pytest.approx(0.80125)

def test_validate_row_eggs_exceed_birds():
    row = {**GOOD_ROW, "eggs": "900"}
    with pytest.raises(ValueError, match="more eggs than birds"):
        validate_row(row)

def test_validate_row_birds_zero():
    row = {**GOOD_ROW, "eggs": "0", "birds": "0"}
    with pytest.raises(ValueError, match="birds is zero"):
        validate_row(row)