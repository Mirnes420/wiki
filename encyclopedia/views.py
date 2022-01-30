from http.client import HTTPResponse
import random
from django import forms
from encyclopedia import util
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#done

def get_by_title(request, title):
    entry = util.get_entry(title)
    content = ""
    """for i in entry:
        if i[0] == '#':
            content +=  ' </h5> <h3> '+ i + ' </h3> <h5 style="color:white">'
        else:
            content += i"""
    return render(request, "encyclopedia/entries.html", {
        "entry": util.remove_title(entry), 
        "title": util.get_title(entry)
    })
#done

def random_entry(request):
    entry = util.get_entry(random.choice(util.list_entries()))
    title = util.get_title(entry)
    return render(request, "encyclopedia/entries.html", {
        "entry": util.remove_title(entry), 
        "title": title
    })
#done
class NewTitle(forms.Form):
    title = forms.CharField(label="Title")

class NewContent(forms.Form):
    entry = forms.CharField(label="Content")
#done

def create_entry(request):
    if request.method == "POST" :
        title = NewTitle(request.POST)
        entry = NewContent(request.POST)
        if title.is_valid() and entry.is_valid():
            title = title.cleaned_data["title"]
            entry = "# " + title + f"\n\n" + entry.cleaned_data["entry"]
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("index"))
        else:
            prev_url = request.META.get('HTTP_REFERER').split('/')
            title = prev_url[-1]
            return get_by_title(title)

    return render(request, "encyclopedia/create.html", {
        "title": NewTitle(),
        "entry": NewContent()
    })
#done

def search(request):
    query = request.GET.get('q')
    filename = f"entries/{query}.md"
    # Defining a function for map() function above
    def find(result):
        # Making a search case insesnitive
        if query.lower() in result.lower():
            return result
        else:
            return ''

    if default_storage.exists(filename):
        entry = util.get_entry(query)
        return render(request, "encyclopedia/entries.html", {
            "title": util.get_title(entry),
            "entry": util.remove_title(entry)
            })
    else:
        all_entries = util.list_entries()
        search_result = []
        for i in map(find, all_entries):
            if len(i) > 0:
                search_result.append(i)
        if len(search_result) == 0:
            search_result.append(f'No items matched for"{query}"!')
            
        return render(request, "encyclopedia/searchbar.html", { 
            "search_result": search_result
            })
#done
def edit_entry(request):
    prev_url =  request.META.get('HTTP_REFERER').replace("%20", " ").split("/")

    if request.method == 'GET':
        title = prev_url[-1]
        entry = util.get_entry(title)
        entry = util.remove_title(entry)
        return render(request, "encyclopedia/edit.html", {
        "title": title, 
        "entry": entry
        })
    else:
        title = request.GET.get('t')
        entry = request.GET.get('e')
        util.save_entry(title, entry)
        return HttpResponseRedirect(reverse("index"))


"""class AddPageForm(forms.Form):
    title = forms.CharField(max_length=20)
    entry = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Tell us more!"
            })

     
def edit_page(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        form = AddPageForm(request.POST, initial={
                "title": NewTitle,
                "entry": NewContent
                })
        
        if form.is_valid():
            util.save_entry(title, entry)
            return render(request, "encyclopedia/edit.html", {
            "title":title
            )}

        else:
            form = AddPageForm()
            return render(request, "encyclopedia/editpage.html", {"form":form})"""

def delete_entry(request):
    prev_url =  request.META.get('HTTP_REFERER').replace("%20", " ").split("/")
    filename = f"entries/{prev_url[-1]}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return HttpResponseRedirect(reverse("index"))
    