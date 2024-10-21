from django.urls import path
from .views import (
    TodoList,
    TodoCreate,
    TodoListCreate,
    is_completed,
    TodoUpdate,
    TodoDelete,
)

# views'e uğramadan direkt List:
from django.views.generic import ListView
from .models import Todo

app_name = 'todo'

urlpatterns = [
    
    # views'e uğramadan direkt List:
    path('list_direct/', ListView.as_view(model=Todo, context_object_name='todos'), name='list_direct'),

    # class_base home List;
    path('list/', TodoList.as_view(), name='list'),

    # class_base home Create;
    path('add/', TodoCreate.as_view(), name='add'),

    # class_base home (List/Create);
    path('', TodoListCreate.as_view(), name='home'),
    
    path('isdone/<int:id>', is_completed, name='done'),
    
    # path('update/<int:id>', todo_update, name='update'),
    path('update/<int:id>', TodoUpdate.as_view(), name='update'),
    
    # path('delete/<int:id>', todo_delete, name='delete'),
    path('delete/<int:id>', TodoDelete.as_view(), name='delete'),
]
