import yfinance as yf

class Stock:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        # --- Core Financial Data ---
        self.price = info.get('currentPrice') or info.get('regularMarketPrice')
        self.outstanding_shares = info.get('sharesOutstanding')
        dividend_per_share = info.get('dividendRate', 0)

        # Dividend yield (%)
        self.dividend_yield = (dividend_per_share / self.price) * 100 if self.price else None

        # Ratios and returns
        self.trailing_eps = info.get('trailingEps')
        self.forward_eps = info.get('forwardEps')
        self.price_to_book_ratio = info.get('priceToBook')
        self.return_on_equity = info.get('returnOnEquity')
        self.debt_to_equity = info.get('debtToEquity')

    # --- Core Metric Methods ---
    def market_cap(self):
        """Calculate Market Capitalization."""
        if self.price and self.outstanding_shares:
            cap = self.price * self.outstanding_shares
            return f"Market Cap: ₹{cap:,.2f}"
        return "Market Cap data not available."

    def dividend_info(self):
        """Display dividend yield."""
        if self.dividend_yield:
            return f"Dividend Yield: {self.dividend_yield:.2f}%"
        return "Dividend data not available."

    def eps_info(self):
        """Display EPS (Earnings Per Share)."""
        if self.trailing_eps or self.forward_eps:
            out = []
            if self.trailing_eps:
                out.append(f"EPS Trailing 12M: {self.trailing_eps}")
            if self.forward_eps:
                out.append(f"EPS Forward 12M: {self.forward_eps}")
            return "\n".join(out)
        return "EPS data not available."

    def pe_ratio(self):
        """Calculate Price-to-Earnings ratios."""
        trailing_pe = self.price / self.trailing_eps if self.price and self.trailing_eps else None
        forward_pe = self.price / self.forward_eps if self.price and self.forward_eps else None

        if trailing_pe and forward_pe:
            return f"P/E (Trailing): {trailing_pe:.2f} | P/E (Forward): {forward_pe:.2f}"
        elif trailing_pe:
            return f"P/E (Trailing): {trailing_pe:.2f}"
        elif forward_pe:
            return f"P/E (Forward): {forward_pe:.2f}"
        return "P/E ratio data not available."

    def pb_ratio(self):
        """Display Price-to-Book ratio."""
        if self.price_to_book_ratio:
            return f"P/B Ratio: {self.price_to_book_ratio:.2f}"
        return "P/B data not available."

    def roe_ratio(self):
        """Display Return on Equity."""
        if self.return_on_equity:
            return f"ROE: {self.return_on_equity:.2f}"
        return "ROE data not available."

    def de_ratio(self):
        """Display Debt-to-Equity ratio."""
        if self.debt_to_equity:
            return f"D/E Ratio: {self.debt_to_equity:.2f}"
        return "D/E ratio data not available."
