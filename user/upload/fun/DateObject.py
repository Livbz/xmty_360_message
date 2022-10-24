import copy


class DateObject:
    __year_list = set()

    @classmethod
    def __add_year(cls, year):
        cls.__year_list.add(int(year))

    @classmethod
    def reset_year_list(cls):
        """
        This is one critical function on this SHIT MOUNTAIN
        """
        cls.__year_list = set()

    @classmethod
    def get_yearlist(cls):
        return copy.deepcopy(cls.__year_list)

    @classmethod
    def get_first_Object_in_year(cls, year):
        time_repr = 12*year+1
        return DateObject(DateObject.to_period_string(time_repr))

    @staticmethod
    def to_period_string(time_repr):
        year = str(int(time_repr / 12))
        month = str(int(time_repr % 12))
        if month == 0:
            month = 12
        return "- " + year + "-" + month + "-"

    def __init__(self, period_string):
        self.period_string = period_string
        self.after_year = ""
        self.after_month = ""
        self.real = False
        self.__load_para(period_string)

    def get_year_month(self, period_string):
        year_month_day = period_string.split("-")
        return int(year_month_day[0]), int(year_month_day[1])

    def __load_para(self, period_string):
        if period_string.count("-") == 5:
            before_after = period_string.split(" - ")
            before = before_after[0]
            after = before_after[1]
            self.after_year, self.after_month = self.get_year_month(after)
            self.real = not before == after
        if period_string.count("-") == 3:
            after = period_string.split("- ")[1]
            self.after_year, self.after_month = self.get_year_month(after)
            self.real = True
        if period_string.count("-") == 6:
            print()
        DateObject.__add_year(self.after_year)

    def get_next(self):
        time_repr = self.get_time_repr() + 1
        new_period_string = self.to_period_string(time_repr)

        return DateObject(new_period_string)

    def get_time_repr(self):
        return int(self.after_year)*12+int(self.after_month)

    def __lt__(self, other):
        return self.get_time_repr() < other.get_time_repr()

    def __eq__(self, other):
        return self.get_time_repr() == other.get_time_repr()

    def __str__(self):
        return self.after_year + "_" + self.after_month + "_"


if __name__ == '__main__':
    print(DateObject.get_first_Object_in_year(11))
