from .accounts.user import urlpatterns as user_urlpatterns
from .summary.thesis import urlpatterns as thesis_urlpatterns


urlpatterns = [
    *user_urlpatterns,
    *thesis_urlpatterns,
]
