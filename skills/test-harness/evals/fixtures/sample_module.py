from __future__ import annotations


def calculate_discount(price: float, percentage: float) -> float:
    """Apply a percentage discount to a price.

    Args:
        price: Original price (must be >= 0)
        percentage: Discount percentage (0-100)

    Returns:
        Discounted price

    Raises:
        ValueError: If price is negative or percentage is out of range
    """
    if price < 0:
        raise ValueError("Price must be non-negative")
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100")
    return round(price * (1 - percentage / 100), 2)


def find_duplicates(items: list[str]) -> list[str]:
    """Return items that appear more than once, in order of first duplicate occurrence."""
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in items:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates
