'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:12:05
 # @ Description:
    根据文本提取数字和金额并写入excel
 '''

# ！ /usr/local/bin/python3
import re

from src.color import color
from src.num import num
from src.progress import progress


class RecordData:
    def __init__(self, text, workbook, file_name):
        self.workbook = workbook
        self.file_name = file_name
        self.text = text
        self.error_text = ''
        self.text_type = '1'
        self.sheet_name = '统计'
        self.animals = ["兔", "虎", "牛", "鼠", "猪",
                        "狗", "鸡", "猴", "羊", "马", "蛇", "龙"]

    def animal_index(self, input_animal):  # 将生肖转换成对应的号码
        animals = self.animals
        numbers = list(range(1, 50))
        start_index = animals.index("兔")
        numbers = numbers[start_index:] + numbers[:start_index]
        for animal in input_animal:
            animal_index = animals.index(animal)
            result = [numbers[i]
                      for i in range(animal_index, len(numbers), 12)]
        return result

    def get_number(self, text):             # 获取数字和金额
        amount = 0
        rows = re.findall(r'\d+', text)
        rows = [int(row) for row in rows]
        # rows = [x for x in rows if x != 0]
        amount = rows[-1]
        rows.pop()
        return rows, amount

    def get_animals(self, text):           # 获取生肖和金额
        key_words = self.animals
        animals = []
        for keyword in key_words:
            if keyword in text:
                animals.append(keyword)
        amounts = re.findall(r"\d+", text)
        amount = amounts[-1]
        return animals, amount

    def get_tail(self, text):  # 获取尾数
        amounts = re.findall(r'\d+', text)
        amount = amounts[-1]
        pos = text.find('尾')
        if pos != -1:
            text = text[:pos]
        digits = re.findall(r'\d+', text)
        rows = []
        for digit in digits:
            if int(digit) >= 10:
                rows += [int(i)
                         for i in range(1, 50) if str(i)[-1] in digit[::-1]]
            else:
                rows += [int(i) for i in range(1, 50) if str(i)[-1] in digit]
        return rows, amount

    def get_head(self, text):  # 获取头数
        amounts = re.findall(r'\d+', text)
        amount = amounts[-1]
        pos = text.find('头')
        if pos != -1:
            text = text[:pos]
        digits = re.findall(r'\d+', text)
        rows = []
        for digit in digits:
            if int(digit) >= 10:
                rows += [int(i) for i in [str(s).zfill(2)
                                          for s in range(1, 50)] if str(i)[0] in digit[::-1]]
            else:
                rows += [int(i) for i in [str(s).zfill(2)
                                          for s in range(1, 50)] if str(i)[0] in digit]
        return rows, amount

    def record(self, rows, amount):         # 写入数据到excel
        color_str = ['红', '蓝', '绿']
        if len(rows) == 0:
            return "没有行数，无法录入！"
        for i in rows:
            if int(i) >= 50:
                return f'大于50行，无法录入！'
        if int(amount) == 0:
            return f"金额为0，无法录入！"
        rows = [int(row) for row in rows]
        rows = [x for x in rows if x != 0]
        self.worksheet = self.workbook.sheets[self.sheet_name]
        for row in rows:
            last_cell = self.worksheet.range(f'A{row}').end('right')
            next_cell = last_cell.offset(0, 1)
            if self.mode:
                next_cell.value = amount
            else:
                last_cell.clear_contents()
        for x in color_str:
            if x in self.text:
                self.worksheet = self.workbook.sheets["颜色"]
                for row in rows:
                    last_cell = self.worksheet.range(f'A{row}').end('right')
                    next_cell = last_cell.offset(0, 1)
                    if self.mode:
                        next_cell.value = amount
                    else:
                        last_cell.clear_contents()
        self.workbook.save(self.file_name)
        if self.mode:
            return "录入成功"
        else:
            return "撤回成功"

    def type_select(self):  # 识别文本类型
        self.text_type = '1'
        type2_str = self.animals
        type3_str = ['包', '肖']
        type4_str = ['红', '蓝', '绿']
        type5_str = ['大', '小']
        type6_str = ['尾']
        type7_str = ['头']
        animal_str = []
        for x in type2_str:
            if x in self.text:
                animal_str.append(x)
                self.text_type = '2'
                if '数' in self.text:
                    return
                for x in type3_str:
                    if x in self.text or len(animal_str) == 1:
                        self.text_type = '3'
        for x in type4_str:
            if x in self.text:
                self.text_type = '4'
                return
        for x in type5_str:
            if x in self.text:
                self.text_type = '5'
                return
        for x in type6_str:
            if x in self.text:
                self.text_type = '6'
                return
        for x in type7_str:
            if x in self.text:
                self.text_type = '7'
                return

    def sheet_select(self):  # 选择sheet
        self.sheet_name = '统计'
        name2_str = ['香', '港']
        for s in name2_str:
            if s in self.text:
                self.sheet_name = '港统'

    def type_input(self):  # 按类型获取位置和金额并写入到excel
        results = []
        match self.text_type:

            case "1":  # 数字特码
                rows, amount = self.get_number(text=self.text)
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "2":  # 生肖特码
                rows = []
                animals, amount = self.get_animals(self.text)
                for animal in animals:
                    rows += self.animal_index(animal)
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "3":  # 生肖包肖
                rows = []
                animals, amount = self.get_animals(self.text)
                for animal in animals:
                    rows = self.animal_index(animal)
                    if animal == "兔":
                        amount_1 = int(amount)/5
                        state = self.record(rows, amount_1)
                    else:
                        amount_1 = int(amount)/4
                        state = self.record(rows, amount_1)
                    results.append(
                        f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount_1} 元\n')
                return "\n".join(results)

            case "4":  # 红蓝绿波+单双
                rows = color(self.text).run()
                amounts = re.findall(r'\d+', self.text)
                amount = amounts[-1]
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "5":  # 大小
                rows = num(self.text).run()
                amounts = re.findall(r'\d+', self.text)
                amount = amounts[-1]
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "6":  # 尾
                rows, amount = self.get_tail(self.text)
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "7":  # 头
                rows, amount = self.get_head(self.text)
                state = self.record(rows, amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

    def type_output(self):  # 按类型获取位置和金额并写入到excel
        results = []
        match self.text_type:

            case "1":  # 数字特码
                rows, amount = self.get_number(text=self.text)
                state = self.record(rows, -amount)
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "2":  # 生肖特码
                rows = []
                animals, amount = self.get_animals(self.text)
                for animal in animals:
                    rows += self.animal_index(animal)
                state = self.record(rows, -int(amount))
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "3":  # 生肖包肖
                rows = []
                animals, amount = self.get_animals(self.text)
                for animal in animals:
                    rows = self.animal_index(animal)
                    if animal == "兔":
                        amount_1 = float(amount)/5
                        amount_1 = -amount_1
                        state = self.record(rows, amount_1)
                    else:
                        amount_1 = float(amount)/4
                        amount_1 = -amount_1
                        state = self.record(rows, amount_1)
                    results.append(
                        f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {-amount_1} 元\n')
                return "\n".join(results)

            case "4":  # 红蓝绿波+单双
                rows = color(self.text).run()
                amounts = re.findall(r'\d+', self.text)
                amount = amounts[-1]
                state = self.record(rows, -int(amount))
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "5":  # 大小
                rows = num(self.text).run()
                amounts = re.findall(r'\d+', self.text)
                amount = amounts[-1]
                state = self.record(rows, -int(amount))
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "6":  # 尾
                rows, amount = self.get_tail(self.text)
                state = self.record(rows, -int(amount))
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

            case "7":  # 头
                rows, amount = self.get_head(self.text)
                state = self.record(rows, -int(amount))
                results.append(
                    f'录入文本：  {self.text}\n录入表格：  {self.sheet_name}\n录入状态：  {state}\n录入位置：  第{",".join(map(str, rows))}行\n录入金额：  ￥ {amount} 元\n')
                return "\n".join(results)

    def run(self, mode=True):  # 运行程序
        self.mode = mode
        self.type_select()
        self.sheet_select()
        text = self.type_input()
        return text

    def callback(self, mode=True):
        self.mode = mode
        self.type_select()
        self.sheet_select()
        text = self.type_output()
        return text

    def end(self, save_path):  # 退出程序
        progress(self.workbook, save_path)
