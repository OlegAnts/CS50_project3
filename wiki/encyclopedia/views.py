from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(title),
        "title": title.capitalize()
    })


def search(request):
    entries = list(map(lambda x: x.lower(), util.list_entries()))
    find_entries = []

    search_box = request.GET.get('q').lower()

    if search_box in entries:
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(search_box),
            "title": search_box.capitalize()
        })
    else:
        for entry in entries:
            if search_box in entry:
                find_entries.append(entry)


    if find_entries:
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(find_entries[0]),
            "title": find_entries[0].capitalize()
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": util.list_entries()
        })





