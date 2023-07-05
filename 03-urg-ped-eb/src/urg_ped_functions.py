
def get_number_of_hours(s) -> float:
    d = {
        'o': 0,
        'D': 12,
        'C': 7.5
    }
    return sum(d[val] for val in s)


def is_a_working_day(l):
    return l in ['D','C']