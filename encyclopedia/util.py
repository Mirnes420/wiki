import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import request


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns error.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return f'Error 404. "{title}" not found!'

def get_title(entry):
    title = []
    for i in entry.split("\n"):
        title.append(i) 
    return title[0]

def remove_title(entry):
    content = ""
    for i in [entry]:
       content += i +'hi'
    return content


def prev_url():
    url = request.META.get('HTTP_REFERER').split('/')
    title = url[-1]
    try:
        default_storage.open(f"entries/{title}.md")
    except FileNotFoundError:
        return None
    return title
