import math


class Calendar:
    __slots__ = 'years', 'months', 'days', 'hours'

    NUM_MONTHS_IN_YEAR = 12
    NUM_DAYS_IN_MONTH = 30
    NUM_DAYS_IN_WEEK = 8
    NUM_HOURS_IN_DAY = 24

    NUM_DAYS_IN_YEAR = NUM_MONTHS_IN_YEAR * NUM_DAYS_IN_MONTH
    NUM_WEEKS_IN_YEAR = math.ceil(NUM_DAYS_IN_YEAR / NUM_DAYS_IN_WEEK)

    MONTH_NAMES = ('Botehr', 'Quxuns', 'Kleisk', 'Mowohs', 'Blosont', 'Newird', 'Flilu', 'Criwa', 'Pleguht', 'Quihn', 'Klibelm', 'Srabuph')

    def __init__(self, years: int, months: int, days: int, hours: int):
        """NOTE: The Calendar class counts months starting from zero for internal logic. Externally, months start at one.
        Constructor takes data in human format (i.e., first month/day is month/day 1 not 0).
        Methods making use of constructor should act accordingly. Developers adjusting this class should clearly distinguish
        usage of fields (e.g. self.years, self.months), which are internal, vs usage of methods (e.g. self.year(), self.month()), which are external."""

        if months == 0 or days == 0:
            raise ValueError("Invalid date: neither month nor day can be zero")

        self.years = years
        self.months = months - 1
        self.days = days - 1
        self.hours = hours

        self.recalculate()  # weekday and week_number initialized here

    def __str__(self):
        return (f"{'-' if self.years<0 else ''}{str(abs(self.years)).rjust(3, '0')}/"
                f"{str(self.months + 1).rjust(2, '0')}/"
                f"{str(self.days + 1).rjust(2, '0')} "
                f"{self.hours}:00")

    def recalculate(self):
        excess_days = math.floor(self.hours / Calendar.NUM_HOURS_IN_DAY)
        self.hours = self.hours % Calendar.NUM_HOURS_IN_DAY
        self.days += excess_days

        excess_months = math.floor(self.days / Calendar.NUM_DAYS_IN_MONTH)  # number of months gained from excess days
        self.days = self.days % Calendar.NUM_DAYS_IN_MONTH                  # number of days when months have been accounted for
        self.months += excess_months                                        # add excess days to months

        excess_years = math.floor(self.months / Calendar.NUM_MONTHS_IN_YEAR)
        self.months = self.months % Calendar.NUM_MONTHS_IN_YEAR
        self.years += excess_years

    def __add__(self, other) -> 'Calendar':
        if isinstance(other, Calendar):
            y = self.years + other.years
            m = self.month() + other.month()
            d = self.day() + other.day()
            h = self.hours + other.hours
            cal = Calendar(y, m, d, h)
        elif isinstance(other, Year):
            cal = Calendar(self.year() + int(other), self.month(), self.day(), self.hour())
        elif isinstance(other, Month):
            cal = Calendar(self.year(), self.month() + int(other), self.day(), self.hour())
        elif isinstance(other, Day):
            cal = Calendar(self.year(), self.month(), self.day() + int(other), self.hour())
        elif isinstance(other, Hour):
            cal = Calendar(self.year(), self.month(), self.day(), self.hour() + int(other))
        else:
            raise NotImplementedError(f"Unsupported type for addition to Calendar: {type(other)}")

        cal.recalculate()

        return cal

    def __sub__(self, other) -> 'Calendar':
        if isinstance(other, Calendar):
            return self + Calendar(-other.years, -other.months, -other.days, -other.hours)
        elif isinstance(other, Year):
            return self + Year(-int(other))
        elif isinstance(other, Month):
            return self + Month(-int(other))
        elif isinstance(other, Day):
            return self + Day(-int(other))
        elif isinstance(other, Hour):
            return self + Hour(-int(other))
        else:
            raise NotImplementedError(f"Unsupported type for subtraction from Calendar: {type(other)}")

    def __lt__(self, other):
        # Only __lt__ is implemented because < and > operators need only one of these functions to be implemented and defining __gt__ would in essence be duplicate code.
        if not isinstance(other, Calendar):
            raise NotImplementedError(f"Calendar objects should only be compared to other calendar objects, not to {type(other)} objects.")
        if self.years == other.years:
            if self.months == other.months:
                if self.days == other.days:
                    return self.hours < other.hours
                else:
                    return self.days < other.days
            else:
                return self.months < other.months
        else:
            return self.years < other.years

    def month_name(self) -> str:
        return Calendar.MONTH_NAMES[self.months]

    def year(self) -> int:
        return self.years

    def month(self) -> int:
        return self.months + 1

    def day(self) -> int:
        return self.days + 1

    def hour(self) -> int:
        return self.hours

    def week_number(self) -> int:
        return (self.days + self.months * Calendar.NUM_DAYS_IN_MONTH) // Calendar.NUM_DAYS_IN_WEEK

    def weekday(self) -> int:
        return (self.days + self.months * Calendar.NUM_DAYS_IN_MONTH) % Calendar.NUM_DAYS_IN_WEEK

    def total_hours(self) -> int:
        return ((self.years * Calendar.NUM_MONTHS_IN_YEAR + self.months) * Calendar.NUM_DAYS_IN_MONTH + self.days) * Calendar.NUM_HOURS_IN_DAY + self.hours


class Year:
    __slots__ = "_years"

    def __init__(self, years: int):
        self._years = years

    def __int__(self) -> int:
        return self._years


class Month:
    __slots__ = "_months"

    def __init__(self, months: int):
        self._months = months

    def __int__(self) -> int:
        return self._months


class Day:
    __slots__ = "_days"

    def __init__(self, days: int):
        self._days = days

    def __int__(self) -> int:
        return self._days


class Hour:
    __slots__ = "_hours"

    def __init__(self, hours: int):
        self._hours = hours

    def __int__(self) -> int:
        return self._hours
