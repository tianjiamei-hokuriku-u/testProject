from django.shortcuts import render,redirect,get_object_or_404
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    status = request.GET.get("status", "all")

    qs = Todo.objects.all()
    if status == "active":
        qs = qs.filter(is_done=False)
    elif status == "done":
        qs = qs.filter(is_done=True)
    else:
        status = "all"

    todos = qs.order_by("is_done", "due_date", "-created_at")

    total = Todo.objects.count()
    done_count = Todo.objects.filter(is_done=True).count()
    active_count = total - done_count

    return render(request, "testApp/todo_list.html", {
        "todos": todos,
        "status": status,
        "total": total,
        "done_count": done_count,
        "active_count": active_count,
    })

def todo_create(request):
    if request.method=="POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoForm()

    return render(request, "testApp/todo_form.html", {"form": form})

def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect("todo_list")

def todo_delete(request,pk):
    todo = get_object_or_404(Todo,pk=pk)
    if request.method == "POST":
        todo.delete()
        return redirect("todo_list")
    return render(request, "testApp/todo_confirm_delete.html", {"todo": todo})

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoForm(instance=todo)

    return render(request, "testApp/todo_form.html", {"form": form, "is_edit": True, "todo": todo})

