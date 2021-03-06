#!/usr/bin/env python3

import matplotlib  # Install PYQT5 manually if you want to test this helper function
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

from freqtrade import exchange, analyze


def plot_analyzed_dataframe(pair: str) -> None:
    """
    Calls analyze() and plots the returned dataframe
    :param pair: pair as str
    :return: None
    """

    # Init Bittrex to use public API
    exchange._API = exchange.Bittrex({'key': '', 'secret': ''})
    dataframe = analyze.analyze_ticker(pair)

    dataframe.loc[dataframe['buy'] == 1, 'buy_price'] = dataframe['close']
    dataframe.loc[dataframe['sell'] == 1, 'sell_price'] = dataframe['close']

    # Two subplots sharing x axis
    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    fig.suptitle(pair, fontsize=14, fontweight='bold')
    ax1.plot(dataframe.index.values, dataframe['close'], label='close')
    # ax1.plot(dataframe.index.values, dataframe['sell'], 'ro', label='sell')
    ax1.plot(dataframe.index.values, dataframe['sma'], '--', label='SMA')
    ax1.plot(dataframe.index.values, dataframe['tema'], ':', label='TEMA')
    ax1.plot(dataframe.index.values, dataframe['blower'], '-.', label='BB low')
    ax1.plot(dataframe.index.values, dataframe['buy_price'], 'bo', label='buy')
    ax1.legend()

    ax2.plot(dataframe.index.values, dataframe['adx'], label='ADX')
    ax2.plot(dataframe.index.values, dataframe['mfi'], label='MFI')
    # ax2.plot(dataframe.index.values, [25] * len(dataframe.index.values))
    ax2.legend()

    ax3.plot(dataframe.index.values, dataframe['fastk'], label='k')
    ax3.plot(dataframe.index.values, dataframe['fastd'], label='d')
    ax3.plot(dataframe.index.values, [20] * len(dataframe.index.values))
    ax3.legend()

    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    fig.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
    plt.show()


if __name__ == '__main__':
    plot_analyzed_dataframe('BTC_ETH')

