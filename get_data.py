from vnstock import Vnstock

class DataSource:
    def __init__(self, symbol='VCI', start='2024-01-02', end='2024-06-10', interval='1D', source='VCI'):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.source = source
        self.quote = Vnstock().stock(symbol=symbol, source=source).quote
        self.data = self.get_data()

    def get_data(self):
        df = self.quote.history(start=self.start, end=self.end, interval=self.interval)
        df = df.set_index('time')
        return df