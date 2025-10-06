def fibonacci(n):
    """
    Print the Fibonacci sequence up to n terms.

    Returns:
        None
    """
    a, b = 0, 1
    for i in range(n):
        print(a, end=" ")
        a, b = b, a + b


n = int(input("Enter how many terms you want: "))
fibonacci(n)
