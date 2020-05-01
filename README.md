# stronks

A `streamlit` app to view `yfinance` data.

```bash
git clone https://github.com/tjduigna/stronks.git
cd stronks
pip install -r requirements.txt
cd stronks
streamlit run app.py
```

No need to install `stronks` as a python package
as `app.py` is a stand-alone script run by `streamlit`.


Features
########

Supports viewing multiple tickers at the same time.
Also supports the same time intervals that the `yfinance`
API supports. Some quick heuristics based on the
co-dependence of time intervals and windows are
undoubtedly buggy. But it all works surprisingly well.
