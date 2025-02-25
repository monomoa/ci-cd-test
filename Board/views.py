from django.shortcuts import get_object_or_404, render, redirect
from Board.models import Board
from Board.forms import BoardCreateForm, BoardUpdateForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
from config import settings
import os

from django.core.exceptions import PermissionDenied
class BoardUpdate(UpdateView):
    model = Board
    form_class = BoardUpdateForm
    template_name = 'Board/board_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        if self.get_object().file_upload.name != '':
            if self.object.file_upload != self.get_object().file_upload.name:
                file_upload_path=os.path.join(settings.MEDIA_ROOT, self.get_object().file_upload.path)
                if os.path.exists(file_upload_path):
                    os.remove(file_upload_path)
            if 'upload_clear' in self.request.POST:
                file_upload_path=os.path.join(settings.MEDIA_ROOT, self.get_object().file_upload.path)
                if os.path.exists(file_upload_path):
                    os.remove(file_upload_path)
                    self.object.file_upload = ''
        return super().form_valid(form)


class BoardList(ListView):
    model = Board
    template_name = 'Board/board_list.html'
    ordering = '-pk'
    paginate_by = 10

class BoardDetail(DetailView):
    model = Board
    template_name = 'Board/board_detail.html'

class BoardCreate(CreateView):
    model = Board
    form_class = BoardCreateForm
    template_name = 'Board/board_form.html'
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            if self.request.FILES:
                form.instance.filename = self.request.FILES['file_upload']
            return super().form_valid(form)
        else:
            return redirect('/Board')

@login_required(login_url='common:login')
def BoardDelete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user != board.author:
        return redirect('Board:detail', pk=pk)
    if board.file_upload:
        file_upload_path = os.path.join(settings.MEDIA_ROOT, board.file_upload.path)
        if os.path.exists(file_upload_path):
            os.remove(file_upload_path)
    board.delete()
    return redirect('Board:list')

import mimetypes,urllib
from django.http import HttpResponse, Http404
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

@login_required(login_url='common:login')
def Board_download(request, pk):
    file = get_object_or_404(Board, pk=pk)
    url = file.file_upload.url[1:]
    url = os.path.join(BASE_DIR, url)

    if os.path.exists(url):
        with open(url, 'rb') as f:
            quote_file_url = urllib.parse.quote(file.filename.encode('utf-8'))
            response = HttpResponse(f.read(), content_type=mimetypes.guess_type(url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
    raise Http404
