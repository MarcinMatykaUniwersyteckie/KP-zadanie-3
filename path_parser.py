from pathlib import Path

ERROR_MESSAGE = 'Zły format danych!'

ALLOWED_MONTHS = [
    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
    'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
]

ALLOWED_DAYS = [
    'poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela',
    'pn', 'wt', 'śr', 'cz', 'pt', 'sb', 'nd'
]
DAYS_IN_WEEK = 7

ALLOWED_TIMES = [
    'rano', 'wieczorem', 'r', 'w'
]
TIMES_PER_DAY = 2
DEFAULT_TIME = 'rano'

# Creates a path object from a list of consecutive folders
# e.g. ['A', 'B', 'C'] -> A/B/C
def create_path(*args):
    path_string = ''
    for folder in args:
        assert isinstance(folder, str), ERROR_MESSAGE
        if path_string != '':
            path_string += '/'
        path_string += folder
    return Path(path_string)

# Creates a list of path from a list of lists of consecutive folders
# e.g. [['A', 'B'], 'C'] -> [A/B, C]
def strings_to_paths(*args):
    paths = []
    for to_be_path in args:
        paths.append(create_path(*to_be_path))
    return paths

# Reformats the array storing months to be suitable for path creation
def parse_months(*args):
    months = []
    for month in args:
        assert isinstance(month, str), ERROR_MESSAGE
        month = month.capitalize()
        assert month in ALLOWED_MONTHS, ERROR_MESSAGE
        months.append(month)

    return months

# Reformats the array storing days to be suitable for path creation
# Gives out all the days together with their respective months
def parse_days(**kwargs):
    # One argument stores previously reformatted information about months
    # The other one stores raw information about days

    assert len(kwargs) == 2, ERROR_MESSAGE
    assert 'months' in kwargs, ERROR_MESSAGE
    assert 'days' in kwargs, ERROR_MESSAGE

    months = kwargs['months']
    current_month = 0
    months_count = len(months)

    days_raw = kwargs['days']
    days = []

    for day in days_raw:
        assert isinstance(day, str), ERROR_MESSAGE
        day = day.lower()

        assert current_month < months_count, ERROR_MESSAGE
        assert isinstance(months[current_month], str), ERROR_MESSAGE

        ends = day.split('-')
        number_of_ends = len(ends)
        assert number_of_ends <= 2, ERROR_MESSAGE

        start = ALLOWED_DAYS.index(ends[0]) % DAYS_IN_WEEK
        end = (ALLOWED_DAYS.index(ends[number_of_ends - 1]) + 1) % DAYS_IN_WEEK
        current_day = start

        if start == end:
            days.append([months[current_month], ALLOWED_DAYS[current_day], DEFAULT_TIME])
            current_day = (current_day + 1) % DAYS_IN_WEEK

        while current_day != end:
            days.append([months[current_month], ALLOWED_DAYS[current_day], DEFAULT_TIME])
            current_day = (current_day + 1) % DAYS_IN_WEEK

        current_month += 1

    return days

# Corrects information about times of the day from default one to the actual one
def correct_times(**kwargs):
    # One argument stores previously reformatted information about days,
    # along with their respective months
    # The other one stores information about times of day

    assert len(kwargs) == 2, ERROR_MESSAGE
    assert 'days' in kwargs, ERROR_MESSAGE
    assert 'times' in kwargs, ERROR_MESSAGE

    days = kwargs['days']
    days_size = len(days)
    current_day = 0

    times = kwargs['times']

    for time in times:
        assert isinstance(time, str), ERROR_MESSAGE
        time = time.lower()

        assert time in ALLOWED_TIMES, ERROR_MESSAGE
        time = ALLOWED_TIMES[ALLOWED_TIMES.index(time) % TIMES_PER_DAY]

        assert current_day < days_size, ERROR_MESSAGE
        assert len(days[current_day]) == 3, ERROR_MESSAGE
        for i in range(3):
            assert isinstance(days[current_day][i], str), ERROR_MESSAGE
        days[current_day][2] = time

        current_day += 1

# Main function of the program
# Reads raw data about months, days and times of day, gives out path
def parse_paths(**kwargs):
    assert len(kwargs) == 3, ERROR_MESSAGE
    assert 'months' in kwargs, ERROR_MESSAGE
    assert 'days' in kwargs, ERROR_MESSAGE
    assert 'times' in kwargs, ERROR_MESSAGE

    months = parse_months(*kwargs['months'])
    days = parse_days(months = months, days = kwargs['days'])
    correct_times(days = days, times = kwargs['times'])

    return strings_to_paths(*days)

#
# Example usage:
#
# mypaths = parse_paths(months = ['styczeń', 'luty'], days = ['pn-wt', 'pt'], times = ['r', 'w'])
# returns: [Styczeń/poniedziałek/rano,
# Styczeń/wtorek/wieczorem,
# Luty/piątek/rano]
#
# You can mess with the letter size, write out whole day or time of day names
# and go around the week (through Sunday back to Monday):
# mypaths2 = parse_paths(months = ['mARzEc', 'KwIEcieŃ'], days=['poNIeDziałEK-CZ','Sb-WTorek'], times = ['RaNO', 'wieCZoReM', 'W', 'r', 'WieczoREM'])
# returns: [Marzec/poniedziałek/rano,
# Marzec/wtorek/wieczorem,
# Marzec/środa/wieczorem,
# Marzec/czwartek/rano,
# Kwiecień/sobota/wieczorem,
# Kwiecień/niedziela/rano,
# Kwiecień/poniedziałek/rano,
# Kwiecień/wtorek/rano]
#
