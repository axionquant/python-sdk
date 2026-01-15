from axion import Axion, ta, visualize, utils as axion_utils


def main():
    client = Axion(api_key="axn_599562c192e86a7818ac656499adee21")
    # esg_data = client.get_esg_data("AAPL")
    # print(esg_data)
    prices = client.get_stock_prices('ABEQ')
    test = axion_utils.df(prices)

    t2 = ta.roc(test, 'close')

    print(t2)
    visualize.candles(test)


if __name__ == "__main__":
    main()
