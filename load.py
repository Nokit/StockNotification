from edinet_xbrl.edinet_xbrl_downloader import EdinetXbrlDownloader

## init downloader
xbrl_downloader = EdinetXbrlDownloader()

## set a ticker you want to download xbrl file
ticker = "1234"
target_dir = "/"
xbrl_downloader.download_by_ticker(ticker, target_dir)
