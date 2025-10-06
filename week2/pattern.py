def pattern(n):
    """
    Print a decreasing star pattern.

    For a given number n, it prints n stars in the first row, then
    decreases the count by 1 in each subsequent row.

    Returns:
        None
    """
    for i in range(n):
        print("*" * n)
        n = n - 1


def reverse(n):
    """
    Print an increasing star pattern.

    For a given number n, it prints 1 star in the first row, and increases
    the count by 1 each row up to n.

    Returns:
        None
    """
    for i in range(1, n + 1):
        print("*" * i)


n = int(input("Enter the number: "))
pattern(n)
reverse(n)
