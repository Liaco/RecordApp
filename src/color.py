'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:12:20
 # @ Description:
    红蓝绿波
 '''

class color:  
    
    def __init__(self,text):
        self.text = text
    
    def add(self):
        red = [1, 2, 7, 8, 12, 13, 18, 19, 23, 24, 29, 30, 34, 35, 40, 45, 46]
        blue = [3, 4, 9, 10, 14, 15, 20, 25, 26, 31, 37, 42, 36, 41, 47, 48]
        green = [5, 6, 11, 16, 17, 21, 22, 27, 28, 32, 33, 38, 39 ,43, 44, 49]
        rows = []

        if "红" in self.text:
            rows += red
        if "蓝" in self.text:
            rows += blue
        if "绿" in self.text:
            rows += green
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
    rows = color(x).run()
    print(rows)


