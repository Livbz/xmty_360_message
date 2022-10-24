from .DateObject import DateObject


class RecordObject(DateObject):
    def __init__(self, period_string, electricity_amount, electricity_bill):
        super().__init__(period_string)
        self.electricity_amount = electricity_amount
        self.electricity_bill = electricity_bill

    def get_next(self):
        t = (self.get_time_repr()+1)
        next_period_string = DateObject.to_period_string(t)
        return RecordObject(next_period_string, "???", "???")

    def __str__(self):
        return self.period_string+"//"+str(self.electricity_amount)+"//"+str(self.electricity_bill)


    @classmethod
    def get_yearlist(cls):
        return DateObject.get_yearlist()

    @classmethod
    def get_first_Object_in_year(cls, year):
        time_repr = 12 * int(year) + 1
        return RecordObject(RecordObject.to_period_string(time_repr), "???", "???")


if __name__ == '__main__':
    a = RecordObject("2021-05-20 - 2021-06-20", 424244, 12323)
    print(RecordObject.get_first_Object_in_year(42))
