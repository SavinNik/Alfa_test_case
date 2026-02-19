def get_first_sequence_elements(n: int) -> int:
    """ Выводит n первых элементов последовательности """
    if n <= 0:
        return 0

    result = ''
    for i in range(0, n + 1):
        result += str(i) * i
    return int(result[:n])

