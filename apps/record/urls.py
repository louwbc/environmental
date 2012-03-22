# from django
from django.conf.urls.defaults import *

# from record
from record.models import Record

urlpatterns = patterns("",
    url(r"^$","record.views.records", name="all_records"),
    url(r"^(\d+)/record/$", "record.views.record", name="describe_record"),
    url(r"^your_records/$", "record.views.your_records", name="your_records"),
    url(r"^user_records/(?P<username>\w+)/$", "record.views.user_records", name="user_records"),
    # CRUD urls
    url(r"^add/$", "record.views.add_record", name="add_record"),
    url(r"^(\d+)/update/$", "record.views.update_record", name="update_record"),
    url(r"^(\d+)/delete/$", "record.views.delete_record", name="delete_record"),

)


