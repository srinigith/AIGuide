"""
The flask application package.
"""

from decouple import config
from flask import Flask

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
# app.config.update(
#     #TESTING=True,
#     GROQ_API_KEY="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"
# )

import AIGuide.views
import AIGuide.pages.loanapp
import AIGuide.pages.analize