import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error


def getdata():
    print("Which dataset would you like to use?")
    file = "data\\" + (str(input("FILE> ")) or "GE") + ".csv"
    return file, pd.read_csv("" + file, parse_dates=True)


def pickcol(data):
    cols = data.columns
    print("Which column do you want to plot? [0-", str(len(cols)))
    for i in range(len(cols) - 1):
        print(str(i), ":", cols[i + 1])
    index = int(input()) + 1
    return cols[index]


def pickyear():
    print("What year would you like to plot? [2009-2019]")
    yr = int(input())
    return yr


def time_series():
    def f(x):
        return 250 * (x - 2009)

    file, dat = getdata()
    dat['Date'] = pd.to_datetime(dat['Date'])
    col = 'Open'
    yr = 2010
    yr = pickyear()
    data = dat[dat['Date'].dt.year == yr]
    data.set_index('Date')
    col = pickcol(data)
    data[col].rolling(14).mean().plot(label='mean prices')
    data[col].rolling(14).max().plot(label='max prices')
    data[col].rolling(14).min().plot(label='min prices')
    data[col].plot(label='daily')
    m = ["Jan ", "Feb ", "Mar ", "Apr ", "May ", "Jun ", "Jul ", "Aug ", "Sep ", "Oct ", "Nov ", "Dec "]
    upper = f(yr + 1)
    lower = f(yr)
    rang = upper - lower
    plt.xticks([(i / 12) * rang + lower for i in range(12)], [j + str(yr) for j in m])
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.xlabel("Month")
    plt.ylabel(col + " Price")
    plt.title(col + " Prices for " + file.split("\\")[-1].split(".")[0].split("/")[-1] + " in " + str(yr))
    plt.tight_layout()
    plt.legend()
    plt.show()


def scatterplot():
    file, data = getdata()
    year = pickyear()
    data = data.loc[data["Date"].astype("datetime64").dt.year == year]
    data.plot.scatter("Open", "Close")
    print(f"Correlation Coefficient: {data.corr()['Open']['Close']: .4f}")

    # Regression
    model = linear_model.LinearRegression()

    X = data.loc[:, "Open"].values.reshape(-1, 1)
    Y = data[["Open", "Close"]].values
    model.fit(X, Y)  # perform linear regression
    Y_pred = model.predict(X)  # make predictions
    plt.plot(X, Y_pred, color='red')

    print('Regression Coefficients: \n', model.coef_)
    print(f"Mean squared error: {mean_squared_error(Y, Y_pred):.3f}")

    plt.title(f"Open vs Close Prices for {file[5:-4]} {year}")
    plt.show()


def box_plot():
    file, dat = getdata()
    year = pickyear()
    col = pickcol(dat)
    dat['Date'] = pd.to_datetime(dat['Date'])
    data = dat[dat['Date'].dt.year == year]
    data.set_index('Date')
    plt.boxplot(data[col])
    plt.ylabel(col + " Price")
    plt.xlabel(col)
    plt.title(col + " Prices for " + file.split("\\")[-1].split(".")[0].split("/")[-1] + " in " + str(year))
    plt.xticks([])
    plt.show()


if __name__ == "__main__":
    box_plot()
    time_series()
    scatterplot()
