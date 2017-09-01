# coding=utf-8
from __future__ import print_function


class NumberService(object):
    def __init__(self):
        self.singles_and_doubles = {
            '0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine',
            '10': 'ten',
            '11': 'eleven',
            '12': 'twelve',
            '13': 'thirteen',
            '14': 'fourteen',
            '15': 'fifteen',
            '16': 'sixteen',
            '17': 'seventeen',
            '18': 'eighteen',
            '19': 'nineteen',
            '20': 'twenty',
            '30': 'thirty',
            '40': 'forty',
            '50': 'fifty',
            '60': 'sixty',
            '70': 'seventy',
            '80': 'eighty',
            '90': 'ninety'
        }

        self.trailing_zeroes = {
            '100': 'hundred',
            '1000': 'thousand',
            '1000000': 'million',
            '1000000000': 'billion',
            '1000000000000': 'trillion',
        }

        self.weishu = [1000000000000, 1000000000, 1000000, 1000]

        # set for keywords
        self.addition_keywords = ['and', 'plus']

    def parse_number_less_than_1000(self, num):
        result = []
        qian = num / 1000
        if qian > 0:
            result.append(self.singles_and_doubles[str(qian)] + ' thousand ')
            num = num - 1000 * qian
        bai = num / 100
        if bai > 0:
            result.append(self.singles_and_doubles[str(bai)] + ' hundred ')
            num = num - 100 * bai
        if self.singles_and_doubles.has_key(str(num)):
            result.append(self.singles_and_doubles[str(num)])
        else:
            result.append(self.singles_and_doubles[str(num)[0]+'0'] +' ' + self.singles_and_doubles[str(num)[1]] + ' ')
        str_result = ''
        for i in result:
            str_result = str_result + i
        return str_result

    def parse_numer(self, num):
        final_list = []
        for item in self.weishu:
            result = num / item
            if result > 0:
                temp = self.parse_number_less_than_1000(result)
                final_list.append(temp + self.trailing_zeroes[str(item)] + ' ')
                num = num - item * result
        final_list.append(self.parse_number_less_than_1000(num))
        final_result = ''
        for i in final_list:
            final_result = final_result + i
        return final_result
