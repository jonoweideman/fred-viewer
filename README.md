# fred-viewer

To run:

- Ensure NASDAQ_DATA_LINK_API_KEY environment variable is set to a valid API key for the Federal Reserve Economic Data API.
- Make sure all packages are installed in requirements.txt
- Execute: python3 fred_viewer.py to run the main app.
- Execute: pytest test.py to execute the GUI unit tests. 

Type in ticker you wish to view in the textbox and click "Fetch". If you type in "GDP", it will attempt to fetch "FRED/GDP", and so on. 

You can zoom in and navigate the graph using the buttons at the top of the screen. The table of monthly averages is in the second tab. You can switch between tabs at the tob of the window. 