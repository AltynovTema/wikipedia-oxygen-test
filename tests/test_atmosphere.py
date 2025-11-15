import re
import pytest
from playwright.sync_api import Page

def test_earth_atmosphere_contains_exactly_20_95_percent_oxygen(page: Page):
    """Позитивный тест: в статье Earth указано значение 20.95% кислорода (с учётом точки/запятой и пробелов)."""
    page.goto("https://en.wikipedia.org/wiki/Earth")
    page.wait_for_selector("h1#firstHeading")
    assert "Earth" in page.locator("h1#firstHeading").inner_text()

    body_text = page.locator("div#bodyContent").inner_text()
    assert re.search(r"20[.,]95\s*%", body_text), "Expected to find '20.95%' or '20,95 %' in Earth article"


def test_earth_atmosphere_does_not_contain_20_94_or_20_96_percent_oxygen(page: Page):
    """Негативный тест: в статье Earth нет приближённых значений 20.94% и 20.96% (границы точности ±0.01%)."""
    page.goto("https://en.wikipedia.org/wiki/Earth")
    body_text = page.locator("div#bodyContent").inner_text()

    # Эти значения недопустимы как замена 20.95%
    forbidden_values = ["20.94%", "20.96%", "20,94 %", "20,96 %"]
    for val in forbidden_values:
        assert val not in body_text, f"Earth article must not contain inexact value: {val}"


def test_earth_atmosphere_does_not_contain_20_949_or_20_951_percent_oxygen(page: Page):
    """Негативный тест: в статье Earth нет значений с избыточной точностью: 20.949% и 20.951%."""
    page.goto("https://en.wikipedia.org/wiki/Earth")
    body_text = page.locator("div#bodyContent").inner_text()

    # Эти значения противоречат принятому значению 20.95%
    forbidden_values = ["20.949%", "20.951%", "20,949 %", "20,951 %"]
    for val in forbidden_values:
        assert val not in body_text, f"Earth article must not contain over-precise or incorrect value: {val}"