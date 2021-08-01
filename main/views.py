from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib import messages
import wikipedia as wiki
import wikipediaapi
import requests
from math import gcd
import googletrans
from googletrans import Translator

Todo = apps.get_model("main", "ToDo")
Notebook = apps.get_model("main", "Notebook")

wikiapi = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI
)


def home(request):
    return render(request, "index.html")


class ToDo:
    def __init__(self):
        pass

    def todo(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                todo = request.POST["todo"]

                Todo.objects.create(
                    user=request.user,
                    todo=todo,
                )

                return redirect("/todo-list")
            else:
                todo = Todo.objects.filter(user=request.user).order_by("-created")
                try:
                    print(todo.values()[0])
                except IndexError:
                    messages.info(request, "You haven't created any to-do. Please create some to show here")

                data = {
                    "todo_list": todo,
                }
                return render(request, "main/todo/todo.html", data)
        else:
            data = {
                "error": "You cannot view this unless you login or register yourself.",
                "error_message": "Please register or login to this site to view or create your to-do"
            }
            return render(request, "main/error.html", data)

    def edit_todo(self, request, todo_id):
        if request.user.is_authenticated:
            if request.method == "POST":
                todo = request.POST['todo']

                todo_list = Todo.objects.get(id=todo_id)
                todo_list.todo = todo
                todo_list.save()

                return redirect("/todo-list")
            else:
                todo = Todo.objects.get(id=todo_id)
                data = {
                    "todo": todo
                }
                return render(request, "main/todo/add_todo.html", data)
        else:
            data = {
                "error": "You cannot edit this unless you login or register yourself.",
                "error_message": "Please register or login to this site to edit or create your to-do"
            }
            return render(request, "main/error.html", data)

    def delete_todo(self, request, todo_id):
        if request.user.is_authenticated:
            todo = Todo.objects.filter(id=todo_id)
            todo.delete()

            return redirect("/todo-list")
        else:
            data = {
                "error": "You cannot delete this unless you login or register yourself.",
                "error_message": "Please register or login to this site to delete your to-do"
            }
            return render(request, "main/error.html", data)


class NoteBook:
    def __init__(self):
        pass

    def notebook(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                notebook_name = request.POST["notebook_name"]
                notebook_content = request.POST["notebook_content"]

                Notebook.objects.create(
                    user=request.user,
                    notebook_name=notebook_name,
                    notebook_content=notebook_content
                )

                return redirect("/notebook")
            else:
                notebook = Notebook.objects.filter(user=request.user).order_by("-created")
                try:
                    print(notebook.values()[0])
                except IndexError:
                    messages.info(request, "You haven't created any notebooks. Please create some to show here")

                data = {
                    "notebook_list": notebook,
                }
                return render(request, "main/notebook/notebook.html", data)
        else:
            data = {
                "error": "You cannot view this unless you login or register yourself.",
                "error_message": "Please register or login to this site to view or create your notebook"
            }
            return render(request, "main/error.html", data)

    def edit_notebook(self, request, notebook_id):
        if request.user.is_authenticated:
            if request.method == "POST":
                notebook_name = request.POST['notebook_name']
                notebook_content = request.POST["notebook_content"]

                notebook_list = Notebook.objects.get(id=notebook_id)
                notebook_list.notebook_name = notebook_name
                notebook_list.notebook_content = notebook_content
                notebook_list.save()

                return redirect("/notebook")
            else:
                notebook = Notebook.objects.get(id=notebook_id)
                data = {
                    "notebook": notebook
                }
                return render(request, "main/notebook/add_notebook.html", data)
        else:
            data = {
                "error": "You cannot edit this unless you login or register yourself.",
                "error_message": "Please register or login to this site to edit or create your notebook"
            }
            return render(request, "main/error.html", data)

    def delete_notebook(self, request, notebook_id):
        if request.user.is_authenticated:
            notebook = Notebook.objects.filter(id=notebook_id)
            notebook.delete()

            return redirect("/notebook")
        else:
            data = {
                "error": "You cannot delete this unless you login or register yourself.",
                "error_message": "Please register or login to this site to delete your notebook"
            }
            return render(request, "main/error.html", data)


class Wikipedia:
    def __init__(self):
        pass

    def wikipedia(self, request):
        if request.method == "POST":
            search = request.POST["search"]
            search_list = wiki.search(search)
            search_list_lower = []

            for i in range(len(search_list)):
                lower_case = str(search_list[i]).lower()
                search_list_lower.append(lower_case)

            if str(search).lower() in search_list_lower:
                print(f"{search = } is present")
                index_no = search_list_lower.index(str(search).lower())
                search_content = wikiapi.page(search_list[index_no]).summary

                data = {
                    "search_name": search,
                    "search_content": search_content,
                }

                return render(request, "main/wikipedia/wikipedia.html", data)
            else:
                print(f"{search = } is not present")
                data = {
                    "search_list": search_list,
                }

                return render(request, "main/wikipedia/wikipedia_list.html", data)
        else:
            return render(request, "main/wikipedia/wikipedia.html")


class Dictionary:
    def __init__(self):
        pass

    def dictionary(self, request):
        if request.method == "POST":
            word = request.POST['word']

            data = self.get_json(word)

            return render(request, "main/dictionary/dictionary.html", data)
        else:
            return render(request, "main/dictionary/dictionary.html")

    def get_json(self, word, language_code='en_GB'):
        word_lower = str(word).lower()
        URL = f"https://api.dictionaryapi.dev/api/v2/entries/{language_code}/{word_lower}"
        print(URL)

        r = requests.get(url=URL)
        data = r.json()
        data = data[0]

        try:
            phonetics_text = data['phonetics'][0]['text']
            phonetics_audio_url = data['phonetics'][0]['audio']
            meanings_parts_of_speech = data['meanings'][0]['partOfSpeech']
            meanings_definition = data['meanings'][0]['definitions'][0]['definition']
            meanings_definition_example = data['meanings'][0]['definitions'][0]['example']

            data_dict = {
                "word": word,
                "phonetics": phonetics_text,
                "audio_url": phonetics_audio_url,
                "parts_of_speech": meanings_parts_of_speech,
                "definition": meanings_definition,
                "example": meanings_definition_example,
            }

            return data_dict
        except KeyError:
            data = {
                "error:": "No definitions found. Please try another search or use our Wikipedia page."
            }

            return data


class Youtube:
    def __init__(self):
        self.api_key = "AIzaSyAppLBsMm7C9ZuFWO-9TCxlqGo8ECbDT6M"
        self.id, self.titles, self.descriptions = [], [], []

    def youtube(self, request):
        if request.method == 'POST':
            youtube_query = request.POST['youtube_query']
            data = self.get_videos(self.api_key, youtube_query, 20)

            return render(request, "main/youtube/youtube.html", data)
        else:
            return render(request, "main/youtube/youtube.html")

    def get_videos(self, api_key, query, max_results):
        request_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&key={api_key}&type=video&q={query}&maxResults={max_results}"
        r = requests.get(url=request_url)
        data = r.json()

        data = data['items']
        video_ids, titles, descriptions, img_urls = [], [], [], []
        self.id, self.titles, self.descriptions = video_ids, titles, descriptions
        for result in data:
            video_ids.append(result['id']['videoId'])
            titles.append(result['snippet']['title'])
            descriptions.append(result['snippet']['description'])
            img_urls.append(result['snippet']['thumbnails']['high']['url'])

        all_videos = zip(video_ids, titles, descriptions, img_urls)

        data = {
            'query': query,
            'all': all_videos
        }

        return data

    def show_youtube_video(self, request, video_id):
        video_index_no = self.id.index(video_id)
        video_title = self.titles[video_index_no]
        video_desc = self.descriptions[video_index_no]
        print(gcd(350, 625))
        print(350/25, 625/25)
        print(gcd(700, 1250))
        print(700/50, 1250/50)
        data = {
            "title": video_title,
            "url": f'https://www.youtube.com/embed/{video_id}',
            "description": video_desc,
        }

        return render(request, "main/youtube/youtube_video.html", data)


class Translate:
    def __init__(self):
        pass

    def translate(self, request):
        languages = googletrans.LANGUAGES
        languages = {k: v.capitalize() for k, v in languages.items()}
        if request.method == 'POST':
            translator = Translator()

            language_from = request.POST["language_from"]
            language_to = request.POST['language_to']
            text_to_translate = request.POST['text_to_translate']
            translated_text = translator.translate(text_to_translate, src=language_from, dest=language_to)

            data = {
                "languages": languages,
                "translated_text": translated_text.text,
                "pronunciation": translated_text.pronunciation,
                "text_to_translate": text_to_translate
            }

            return render(request, "main/translate/translate.html", data)
        else:
            data = {
                "languages": languages,
            }
            return render(request, "main/translate/translate.html", data)

# TODO: Create the following features
# Translate
