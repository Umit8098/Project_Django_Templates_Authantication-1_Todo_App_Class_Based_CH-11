from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from django.contrib import messages

# for class based views import;
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


class TodoList(ListView):
    model = Todo
    # default context_object_name: APP_Name_list (todo_list)
    context_object_name = 'todos'
    # template_name = "todo/home.html" or 
    # default template_name = "todo/todo_list.html"
    # ordering = ['priority', ]
    ordering = ['-priority', ]


class TodoCreate(CreateView):
    model = Todo
    form_class = TodoForm 
    template_name = 'todo/todo_add.html'
    # default todo/todo_form.html
    success_url = reverse_lazy('todo:list')


class TodoListCreate(CreateView):
    model = Todo
    form_class = TodoForm 
    template_name = 'todo/home.html'
    success_url = reverse_lazy('todo:home')

    def get_context_data(self, **kwargs):
        kwargs['todos'] = Todo.objects.order_by('-priority')
        kwargs['done_count'] = Todo.objects.filter(is_done=True).count()
        kwargs['priority_count'] = Todo.objects.filter(priority__gt=2).count()
        return super(TodoListCreate, self).get_context_data(**kwargs)

    
def is_completed(request, id):
    todo = Todo.objects.get(id=id)
    todo.is_done = not(todo.is_done)
    todo.save()
    return redirect('todo:home')

    
class TodoUpdate(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_update.html'
    # default temp_name "todo/todo_update_form.html"
    pk_url_kwarg = 'id'
    # default pk_url_kwargs = 'pk'
    success_url = reverse_lazy('todo:home')


class TodoDelete(DeleteView):
    model = Todo
    template_name = 'todo/todo_delete.html'
    # default temp_name "todo/todo_update_form.html"
    pk_url_kwarg = 'id'
    # default pk_url_kwargs = 'pk'
    success_url = reverse_lazy('todo:home')
