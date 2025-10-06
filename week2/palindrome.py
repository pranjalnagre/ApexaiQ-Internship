def palindrome_string(s):
    """
    Check if a given string is a palindrome and print the result.

    Returns:
        None
    """
    cleaned_text = s.replace(" ", "").lower()
    if cleaned_text == cleaned_text[::-1]:
        print(f"'{s}' is a palindrome")
    else:
        print(f"'{s}' is not a palindrome")


def palindrome_series(n):
    """
    Print all palindrome numbers from 0 to n.

    Returns:
        None
    """
    print(f"Palindrome numbers from 0 to {n}:")
    for i in range(n + 1):
        if str(i) == str(i)[::-1]:
            print(i, end=" ")


limit = int(input("Enter the limit: "))
palindrome_series(limit)

text = input("\nEnter a string: ")
palindrome_string(text)
