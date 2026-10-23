"""Development overrides without replacing environment-configured database/secrets."""

import os

from untitled2.settings import *

DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
if DEBUG and "debug_toolbar" not in INSTALLED_APPS:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = [*MIDDLEWARE, "debug_toolbar.middleware.DebugToolbarMiddleware"]
