import random

a = ["一班", "二班", "三班", "四班"]

result = list()

for i in range(200):
    index = int(random.random()/0.25)
    result.append(a[index])

with open("r.csv", "w", encoding="utf-8") as f:
    for i in result:
        f.write(i)
        f.write("\n")
