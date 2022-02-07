import random
from django import forms
from encyclopedia import util
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponseRedirect
from django.core.files.storage import default_storage

# defining an index page that returns a list of all existing entries

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# defining a function that gets content and returns that title's entry

def get_by_title(request, title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/entries.html", {
        "content": util.remove_title(content), 
        "title": util.get_title(content)
    })

# defining a function that gives us a random entry from all entries

def random_entry(request):
    random_entry = util.get_entry(random.choice(util.list_entries()))
    title = ""
    potential_title = util.get_title(random_entry).split()[1:]
    for i in potential_title:
        if i != potential_title[-1]:
            title += i + " "
        else:
            title += i

    return redirect(reverse('title_name', kwargs={'title' : title}))
    

# defining form classes used in create_entry function

class NewTitle(forms.Form):
    title = forms.CharField(label="Title")

class NewContent(forms.Form):
    content = forms.CharField(label="Content")

# defining a function that lets us create a new entry

def create_entry(request):

    # if request method is POST, saving that value

    if request.method == "POST" :
        title = NewTitle(request.POST)
        content = NewContent(request.POST)
        if title.is_valid() and content.is_valid():
            title = title.cleaned_data["title"]
            content = "# " + title + f"\n\n" + content.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            prev_url = request.META.get('HTTP_REFERER').split('/')
            title = prev_url[-1]
            return get_by_title(title)

    #  if GET, giving us a form with no values

    return render(request, "encyclopedia/create.html", {
        "title": NewTitle(),
        "content": NewContent()
    })

# defining a search query

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
        
    # if query exist, return it

    if default_storage.exists(filename):
        content = util.get_entry(query)
        return render(request, "encyclopedia/entries.html", {
            "title": util.get_title(content),
            "content": util.remove_title(content)
            })

    # returns all entries where query occured

    else:
        all_entries = util.list_entries()
        search_result = []
        for i in map(find, all_entries):
            if len(i) > 0:
                search_result.append(i)

        # if empty search result, returns a message

        if len(search_result) == 0:
           return render(request, "encyclopedia/error.html", {
            "content": query
            })

        return render(request, "encyclopedia/searchbar.html", {
            "search_result": search_result
            })

# defining an edit page

def edit_entry(request):
    
    # getting a page that needs to be edited by taking the last part of the previous URL, which is a title of the last page visited

    prev_url =  request.META.get('HTTP_REFERER').replace("%20", " ").split("/")

    if request.method == 'GET':
        title = prev_url[-1]
        content = util.get_entry(title)
        content = util.remove_title(content)
        return render(request, "encyclopedia/edit.html", {
        "title": title, 
        "content": content
        })
    elif request.method == "POST" :
        new_title = request.POST.get('t')
        new_content = request.POST.get('c')
        new_content = "# " + new_title + f"\n\n" + new_content
        util.save_entry(new_title, new_content)
        return render(request, "encyclopedia/entries.html", {
        "title": util.get_title(new_content), 
        "content": util.remove_title(new_content)
        })

# defining a function that deletes entry

def delete_entry(request):
    prev_url =  request.META.get('HTTP_REFERER').replace("%20", " ").split("/")
    filename = f"entries/{prev_url[-1]}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))
    
    