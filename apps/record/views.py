# from django
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#from record
from record.models import Record
from record.forms import RecordForm

def records(request):
    """ Return the all records list, ordered by added date. """
    records = Record.objects.all().order_by("-added")
    return render_to_response("record/records.html", {
        "records": records,
        "list": 'all',
        }, context_instance=RequestContext(request))

def user_records(request, username):
    """Return an user records list."""
    user = get_object_or_404(User, username=username)
    userrecords = Record.objects.filter(adder=user).order_by("-added")
    return render_to_response("record/records.html", {
        "records":userrecords,
        "list":'user',
        "username":username,
        }, context_instance=RequestContext(request))

def record(request, record_id):
    """ Return a record given its id."""
    isyours = False
    record = Record.objects.get(id=record_id)
    if request.user == record.adder:
        isyours = True
    return render_to_response("record/record.html", {
        "record": record,
        "isyours": isyours,
        }, context_instance=RequestContext(request))

@login_required
def your_records(request):
    """ Return the logged user record list. """
    yourrecord = Record.objects.filter(adder=request.user).order_by("-added")
    return render_to_response("record/records.html", {
        "records": yourrecords,
        "list": 'yours',
        }, context_instance=RequestContext(request))

@login_required
def add_record(request):
    """ Add a record to the web."""
    # POST request
    if request.method == "POST":
        record_form = RecordForm(request.POST, request.FILES)
        if record_form.is_valid():
            # from ipdb import set_trace; set_trace()
            new_record = record_form.save(commit=False)
            new_record.adder = request.user
            new_record.save()
            request.user.message_set.create(message=_("You have saved book '%(title)s'"))
            return HttpResponseRedirect(reverse("record.views.records"))
    # GET request
    else:
        record_form = RecordForm()
        return render_to_response("record/add.html", {
            "record_form":record_form,
            }, context_instance=RequestContext(request))
    # generic case
    return render_to_response("record/add.html", {
        "record_form": record_form,
        }, context_instance=RequestContext(request))

@login_required
def update_record(request, record_id):
    """ Update a record given its id. """
    record = Record.objects.get(id=record_id)
    if request.method == "POST":
        record_form = RecordForm(request.POST, request.FIFLES, instance=record)
        record_form.is_update = True
        if request.user == record.adder:
            # from ipdb import set_trace; set_trace()
            if record_form.save():
                record_form.save()
                request.user.message_set.create(message=_("You have updated record '%(title)s'") % {'title':record.title})
                return HttpResponseRedirect(reverse("record.views.records"))
    else:
        record_form = RecordForm(instance=record)
        return render_to_response("record/update.html", {
            "record_form":record_form,
            "record":record,
            }, context_instance=RequestContext(request))

@login_required
def delete_record(request, record_id):
    """ Delete a record given its id. """
    record = get_object_or_404(Record, id=record_id)
    if request.user == record.adder:
        record.delete()
        request.user.message_set.create(message="Record Deleted")

    return HttpResponseRedirect(reverse("record.views.records"))

