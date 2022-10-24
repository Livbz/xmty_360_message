import xlwt


def generate_excel_col_indexs(length):
    alphabetic = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if length <= 26:
        for i in range(length):
            yield alphabetic[i]
    else:
        for i in range(26):
            yield alphabetic[i]
        for i in range(length - 26):
            prefix = int(i / 26)
            suffix = i % 26
            yield alphabetic[prefix] + alphabetic[suffix]


def concate(l, join="+"):
    result = join.join(l)
    return result


def transform(row, col):
    row_name = row + 1
    return LineObject.year_transformer[col] + str(row_name)


def generate_divison_formula(a, b):
    return a + "/" + b


class LineObject:
    year_max_object = dict()
    year_transformer = dict()

    def __init__(self, year, month):
        self.content = list()
        self.year = year
        self.month = month
        self.__length = 0
        self.year_max_object[year] = 0

    @classmethod
    def computer_year_max(cls, year, length):
        cls.year_max_object[year] = max(cls.year_max_object[year], length)

    @classmethod
    def generate_transformer(cls, year_list, shift):
        max_length = max([cls.year_max_object[year]*4 for year in year_list]) + shift + 100
        indexs = list(generate_excel_col_indexs(max_length))
        cls.year_transformer = {i: index for i, index in zip(range(max_length), indexs)}

    def append(self, o):
        self.content.append(o)
        self.__length = self.__length + 1
        self.computer_year_max(self.year, self.__length)

    def sheet_write(self, sheet, row, col):
        n = 0
        amount_list = list()
        bill_list = list()

        for record in self.content:
            sheet.write(row, col + n*4, record.electricity_amount)
            sheet.write(row, col+1 + n*4, record.electricity_bill)
            amount = transform(row, col + n*4)
            bill = transform(row, col+1 + n*4)
            formula = generate_divison_formula(bill, amount)
            sheet.write(row, col+2 + n*4, xlwt.Formula(formula))
            n = n + 1
            amount_list.append(amount)
            bill_list.append(bill)

        # Add additional cells into the formula
        for a in range(10):
            amount = transform(row, col + n * 4)
            bill = transform(row, col + 1 + n * 4)
            n = n + 1
            amount_list.append(amount)
            bill_list.append(bill)
        try:
            sheet.write(row, col - 4-1, xlwt.Formula(concate(amount_list)))
            sheet.write(row, col - 2-1-1, xlwt.Formula(concate(bill_list)))
            sheet.write(row, col - 2-1, xlwt.Formula("B"+str(row+1)+"/A"+str(row+1)))
        except:
            print()


if __name__ == '__main__':
    for i in generate_excel_col_indexs(30):
        print(i)
