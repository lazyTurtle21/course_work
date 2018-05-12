import math


class Date:
    def __init__(self, data):
        """Creates an object instance for the specified Gregorian date."""
        self._julianDay = 0
        date = data[:10].split('-')
        time = data[11:].split(':')
        year, month, day = date[0], date[1], date[2]
        hour, mint, sec = time[0], time[1], time[2]

        month = month[1] if month[0] == '0' else month
        day = day[1] if day[0] == '0' else day

        assert all(x.isdigit() for x in (day, month, year, hour,
                                         mint)), 'Invalid date'

        hour, mint, sec, year, month, day = int(hour), int(mint), float(sec), \
                                            int(year), int(month), int(day)

        assert self._is_valid_gregorian(day, month, year), \
            "Invalid Gregorian date."

        tmp = -1 if month < 3 else 0
        self._julianDay = day - 32075 + (1461 * (year + 4800 + tmp) // 4) +\
                                        (367 * (month - 2 - tmp * 12) // 12)\
                              - (3 * ((year + 4900 + tmp) // 100) // 4)
        self._seconds = sec + mint * 60 + hour * 3600

    def month(self):
        """Extracts the appropriate Gregorian date component."""
        return (self._to_gregorian())[1]  # returning M from (M, d, y)

    def day(self):
        """Extracts the appropriate Gregorian date component."""
        return (self._to_gregorian())[0]  # returning D from (m, D, y)

    def year(self):
        """Extracts the appropriate Gregorian date component."""
        return (self._to_gregorian())[2]  # returning Y from (m, d, Y)

    def hour(self):
        """Extracts the appropriate time component."""
        return self._to_clock()[0]

    def minutes(self):
        """Extracts the appropriate time component."""
        return self._to_clock()[1]

    def seconds(self):
        """Extracts the appropriate time component."""
        return self._to_clock()[2]

    def _to_clock(self):
        """Return time in format (hours, minutes, seconds)"""
        hour = self._seconds // 3600
        minutes = math.floor((self._seconds / 3600 - hour) * 60)
        seconds = round(self._seconds - ((hour * 3600) + (minutes * 60)), 2)
        return hour, minutes, seconds

    def day_of_week(self):
        """Returns day of the week as an int between 0 (Mon) and 6 (Sun)."""
        day, month, year = self._to_gregorian()
        if month < 3:
            month = month + 12
        year = year - 1
        return ((13 * month + 3) // 5 + day + year + year // 4 -
                year // 100 + year // 400) % 7

    def _is_valid_gregorian(self, day, month, year):
        """Returns the date as a string in Gregorian format."""
        return True if 1 <= day <= 31 and 1 <= month <= 12 and \
                       0 <= year <= 3000 else False

    def __str__(self):
        """Return Date as a string"""
        day, month, year = self._to_gregorian()
        hour, minutes, second = self._to_clock()
        return "%02d/%02d/%04d %02d:%02d:%.2f" % (day, month, year, hour,
                                                  minutes, second)

    def __eq__(self, otherdate):
        """Logically compares the two dates."""
        return self._julianDay == otherdate._julianDay

    def __lt__(self, other):
        """Logically compares the two dates."""
        return self._julianDay < other._julianDay

    def __le__(self, other):
        """Logically compares the two dates."""
        return self._julianDay <= other._julianDay

    def _to_gregorian(self):
        """Turn julian date into gregorian"""
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
        return day, month, year


if __name__ == '__main__':
    data = '2018-03-16T12:59:59.045'
    data = Date('2018-03-16T12:59:59.045')
    print(data)
