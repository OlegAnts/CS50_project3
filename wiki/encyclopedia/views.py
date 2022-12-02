from django.shortcuts import render
from . import util
from django.contrib import messages
from random import randint
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(title)),
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


def create(request):
    entries = list(map(lambda x: x.lower(), util.list_entries()))

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and title.lower() not in entries:
            util.save_entry(title=title, content=str(content))
            messages.success(request, 'New entry added to encyclopedia!!!!')
        elif title.lower() in entries:
            messages.error(request, f'Entry with name "{title}" already exist')

    return render(request, "encyclopedia/create.html")



def edit(request, title):
    if request.method == "POST":
        print()
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title=title, content=str(content))
        return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(title),
            "title": title
        })

    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(title),
        "title": title
    })


def random(request):
    entries = util.list_entries()
    random_entry = entries[randint(0, len(entries)-1)]

    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(random_entry),
        "title": random_entry
    })
