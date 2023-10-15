'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:13:40
 # @ Description:
    大小波
 '''

class num:      #大小
    def __init__(self,text):
        self.text = text
    
    def add(self):
        rows = []
        if "小" in self.text:
            rows = range(1,25)
        if "大" in self.text:
            rows = range(25,50)

        return rows
    
    def sub(self,rows):
        if "单" in self.text:
            rows = [x for x in rows if x % 2 != 0]
        elif "双" in self.text:
            rows = [x for x in rows if x % 2 == 0]
        elif "偶" in self.text:
            rows = [x for x in rows if x % 2 == 0]
        else:
            rows = rows
        return rows

    def run(self):
        rows = self.add()
        return self.sub(rows)


if __name__ == '__main__':
    x = input("请输入：\n")
    rows = num(x).run()
    print(rows)


