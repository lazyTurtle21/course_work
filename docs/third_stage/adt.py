class Date:
    def __init__(self, data):
        """Creates an object instance for the specified Gregorian date."""
        self._julianDay = 0
        date = data[:10].split('-')
        time = data[11:].split(':')
        year, month, day = date[0], date[1], date[2]
        hour, mint, sec = time[0], time[1], time[2]

        assert all(len(x) == 2 for x in (day, month)), 'Invalid date'

        month = month[1] if month[0] == '0' else month
        day = day[1] if day[0] == '0' else day

        assert all(x.isdigit() for x in (day, month, year)), 'Invalid date'

        day, month, year = int(day), int(month), int(year)

        assert self._is_valid_gregorian(day, month, year),\
            "Invalid Gregorian date."

        tmp = -1 if month < 3 else 0
        self._julianDay = day - 32075 + (1461 * (year + 4800 + tmp) // 4) + \
                                        (367 * (month - 2 - tmp * 12) // 12)\
                          - (3 * ((year + 4900 + tmp) // 100) // 4)
# Extracts the appropriate Gregorian date component.

    def month(self):
        return (self._to_gregorian())[0]  # returning M from (M, d, y)

    def day(self):
        return (self._to_gregorian())[1]  # returning D from (m, D, y)

    def year(self):
        return (self._to_gregorian())[2]  # returning Y from (m, d, Y)

    def day_of_week(self):
        """Returns day of the week as an int between 0 (Mon) and 6 (Sun)."""
        month, day, year = self._to_gregorian()
        if month < 3:
            month = month + 12
        year = year - 1
        return ((13 * month + 3) // 5 + day + year + year // 4 -
                year // 100 + year // 400) % 7
# Returns the date as a string in Gregorian format.

    def _is_valid_gregorian(self, day, month, year):
        return True if 1 <= day <= 31 and 1 <= month <= 12 and \
                       0 <= year <= 3000 else False

    def __str__( self ):
        month, day, year = self._to_gregorian()
        return "%02d/%02d/%04d" % (month, day, year)

    # Logically compares the two dates.
    def __eq__( self, otherDate ):
        return self._julianDay == otherDate._julianDay

    def __lt__(self, otherDate):
        return self._julianDay < otherDate._julianDay

    def __le__(self, other):
        return self._julianDay <= other._julianDay

    def _to_gregorian(self):
        A = self._julianDay + 68569
        B = 4 * A // 146097
        A = A - (146097 * B + 3) // 4
        year = 4000 * (A + 1) // 1461001
        A = A - (1461 * year // 4) + 31
        month = 80 * A // 2447
        day = A - (2447 * month // 80)
        A = month // 11
        month = month + 2 - (12 * A)
        year = 100 * (B - 49) + year + A
        return month, day, year


if __name__ == '__main__':
    data = '2018-03-16T12:59:59.045'
    Date(data)
