from django import forms
from django.shortcuts import render, redirect
from . import util
from random import choice
import markdown2
import re

class NewPageForm(forms.Form):
    title = forms.CharField(label="New Page Title", widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    markdown = forms.CharField(label="New Page Content", widget=forms.Textarea(attrs={'class': "form-control"}), required=False)

class EditPageForm(forms.Form):
    markdown = forms.CharField(label="Edit Page Content", widget=forms.Textarea(attrs={'class': "form-control"}), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikipage(request, title):
    page_md = util.get_entry(title.capitalize())

    if page_md == None:
        return render(request, "encyclopedia/error.html")

    return render(request, "encyclopedia/wikipage.html", {
        "title": title,
        "page_md": markdown2.markdown(page_md)
    })

def search(request):
    if request.method == 'POST':
        q = request.POST.get('q')
        if q.lower() in [page.lower() for page in util.list_entries()]:
            return redirect('wikipage', title = q)
        matches = []
        for page in util.list_entries():
            if q.lower() in page.lower():
                matches.append(page)
        return render(request, "encyclopedia/search.html", {
            "matches": matches
        })

def new(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new.html', {
            "form": NewPageForm(),
            "error": None
        })

    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        markdown = form.cleaned_data["markdown"]
        if title.lower() in [page.lower() for page in util.list_entries()] or title == "":
            if title == "":
                error = "Please fill in a title."
            else:
                error = "Page already exists."
            return render(request, 'encyclopedia/new.html', {
                "form": form,
                "error": error
            })
        else:
            util.save_entry(title, markdown)
            return redirect('wikipage', title = title)
    return redirect('index')

def edit(request, title):
    if request.method == 'GET':
        initial = {"markdown":re.sub("\r", "", util.get_entry(title.capitalize()))}
        return render(request, 'encyclopedia/edit.html', {
            "title": title.capitalize(),
            "form": EditPageForm(initial = initial),
            "error": None
        })
    form = EditPageForm(request.POST)
    if form.is_valid():
        markdown = form.cleaned_data["markdown"]
        util.save_entry(title, markdown)
        return redirect('wikipage', title = title)
    else:
        return render(request, 'encyclopedia/edit.html', {
            "form": form,
            "error": "Something went wrong."
            })

def random(request):
    return redirect('wikipage', title = choice(util.list_entries()))
