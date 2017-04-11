
class StockDoesNotExist(Exception):
    def __init__(self, message, symbol):

        # Call the base class constructor with the parameters it needs
        super(StockDoesNotExist, self).__init__(message)