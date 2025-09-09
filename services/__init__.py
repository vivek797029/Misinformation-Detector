# This file initializes the 'services' directory as a Python package.

# By importing the main functions from our modules here, we can make them
# directly accessible from the 'services' package itself. This simplifies
# imports in other parts of our application, like app.py.

from .factcheck import fact_check
from .media_check import check_image
from .score import credibility_score
