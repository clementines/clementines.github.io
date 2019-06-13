import timeit #timer library
start = timeit.default_timer() # start timer
import pandas as pd # data munging library
import numpy as np # data munging library
from datetime import date, datetime # date preprocessing library
import requests # web request library
import re # regular expressions
from bs4 import BeautifulSoup # HTML parsing library
from bokeh.io import output_file, show
from bokeh.layouts import layout
from bokeh.plotting import figure, ColumnDataSource
from bokeh.palettes import Plasma256, Category10
from bokeh.models import NumeralTickFormatter,LinearColorMapper,BasicTicker,ColorBar

import time
import pandas.io.formats.excel # expose defaults for excel output headers
pandas.io.formats.excel.header_style = None # delete original header formatting

stop = timeit.default_timer()
print(stop-start,' seconds for import and function compile')
# main execution ##############################################################