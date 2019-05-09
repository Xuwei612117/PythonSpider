import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd


def main():
    df = pd.read_csv("微医在线问诊医生数据.csv")
    name = df['姓名']
    title = df['医生职称']
    print("数据行数:", len(df))
    plt.scatter(name, title)
    plt.title('医生职称图')
    plt.xlabel("name")
    plt.ylabel("title")
    plt.show()


if __name__ == '__main__':
    main()
