import matplotlib.pyplot as plt
# conda install matplotlib

x = [10,20,30,40,50,60,70,80,90]
y = [2, 3, 4, 9, 2, 5, 3, 4, 7]

plt.bar(x,y)
plt.title("AGES & PERSON")
plt.xlabel("나이")
plt.ylabel("숫자")

plt.show()
