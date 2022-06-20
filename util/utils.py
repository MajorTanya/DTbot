def rint(flt: float) -> int | float:
    """Round to 2 digits. Returns int if rounded float has only zeroes after the decimal point."""
    return int(rounded) if (rounded := round(flt, 2)).is_integer() else rounded
