import glob

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import File
from project.models import Project
from task.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from guardian.core import ObjectPermissionChecker
from django.core.exceptions import PermissionDenied
import asyncio
import bugsnag


class DocumentProjectView(LoginRequiredMixin, View):
    def get(self, request, pk):
        checker = ObjectPermissionChecker(request.user)
        project = get_object_or_404(Project, id=pk)
        files = File.objects.filter(project=project)
        tasks = Task.objects.filter(project=project)
        if checker.has_perm('olp_view_project', project):
            return render(request, 'projectdetails/files.html', {'project': project, 'files': files, 'tasks': tasks})
        else:
            raise PermissionDenied


class DownloadFile(LoginRequiredMixin, View):
    async def get(self, request, pk):
        file = await sync_to_async(File.objects.get)(pk=pk)
        with open('.' + file.url(), 'rb') as f:
            data = f.read()
            f.close()
        response = HttpResponse(data, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file.filename())
        return response


class DeleteFile(LoginRequiredMixin, View):
    def post(self, request):
        print("Delete file")
        try:
            delete_files = [int(x) for x in request.POST.get('delete_files').split(',')]
            files = File.objects.filter(id__in=delete_files)
            for file in files:
                print('.' + file.url())
                os.remove('.' + file.url())
                file.delete()
            return HttpResponse('Ok', status=200)
        except Exception as e:
            bugsnag.notify(e)
            return HttpResponse('Bad Request', status=400)


class UploadFile(LoginRequiredMixin, View):
    def post(self, request):
        files = request.FILES
        project_id = request.POST.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
            for _, file in dict(files).items():
                File.objects.create(project=project, file=file[0])
            return HttpResponse('Success', status=200)
        except Project.DoesNotExist as e:
            bugsnag.notify(e)
            return HttpResponse('Not Found', status=404)


class RenameFile(LoginRequiredMixin, View):
    def post(self, request):
        file_id = request.POST.get('file_id')
        new_name = request.POST.get('new_name')
        try:
            file = File.objects.get(id=file_id)
            list_path = file.file.url.split('/')[:-1][1:]
            path = os.path.join(*list_path)
            all_files = glob.glob(path + '/*')
            new_path = path + '/' + new_name
            if new_path in all_files:
                return HttpResponse('Bad request', status=400)
            else:
                os.rename('.' + file.file.url, './' + new_path)
                file.file.name = new_path.replace('media/', '')
                file.save()
                return HttpResponse('Successful', status=200)
        except File.DoesNotExist as e:
            bugsnag.notify(e)
            return HttpResponse('Not Found', status=404)
