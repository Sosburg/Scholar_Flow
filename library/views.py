import csv
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import PaperUploadForm, RegisterForm, StatementForm, ThemeForm
from .models import Paper, Statement, Theme, Workspace

DEFAULT_THEMES = [
    ("Methodological Gaps", "#ef4444"),
    ("Key Findings", "#3b82f6"),
    ("Future Research", "#10b981"),
]

def get_workspace(user):
    workspace, created = Workspace.objects.get_or_create(owner=user)
    if created and workspace.themes.count() == 0:
        for name, color in DEFAULT_THEMES:
            Theme.objects.create(workspace=workspace, name=name, color=color)
    return workspace

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        get_workspace(user)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    workspace = get_workspace(request.user)
    papers = workspace.papers.all()[:5]
    statements = Statement.objects.filter(paper__workspace=workspace)
    return render(request, 'library/dashboard.html', {
        'workspace': workspace, 'papers': papers,
        'paper_count': workspace.papers.count(),
        'statement_count': statements.count(),
        'theme_count': workspace.themes.count(),
    })

@login_required
def paper_list(request):
    workspace = get_workspace(request.user)
    form = PaperUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        paper = form.save(commit=False)
        paper.workspace = workspace
        if not paper.title:
            paper.title = request.FILES['pdf'].name.rsplit('.', 1)[0]
        paper.save()
        messages.success(request, 'Paper uploaded.')
        return redirect('paper_detail', paper_id=paper.id)
    return render(request, 'library/paper_list.html', {'papers': workspace.papers.all(), 'form': form})

@login_required
def paper_detail(request, paper_id):
    workspace = get_workspace(request.user)
    paper = get_object_or_404(Paper, id=paper_id, workspace=workspace)
    statements = paper.statements.prefetch_related('themes').all()
    form = StatementForm(request.POST or None, workspace=workspace)
    if request.method == 'POST' and form.is_valid():
        statement = form.save(commit=False)
        statement.paper = paper
        statement.save()
        statement.themes.set(form.cleaned_data['theme_ids'])
        messages.success(request, 'Statement saved.')
        return redirect('paper_detail', paper_id=paper.id)
    return render(request, 'library/paper_detail.html', {
        'paper': paper, 'statements': statements, 'form': form, 'themes': workspace.themes.all()
    })

@login_required
@require_POST
def delete_paper(request, paper_id):
    workspace = get_workspace(request.user)
    paper = get_object_or_404(Paper, id=paper_id, workspace=workspace)
    paper.delete()
    messages.success(request, 'Paper deleted.')
    return redirect('paper_list')

@login_required
def theme_list(request):
    workspace = get_workspace(request.user)
    form = ThemeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        theme = form.save(commit=False)
        theme.workspace = workspace
        theme.save()
        messages.success(request, 'Theme created.')
        return redirect('theme_list')
    return render(request, 'library/themes.html', {'themes': workspace.themes.all(), 'form': form})

@login_required
@require_POST
def delete_theme(request, theme_id):
    workspace = get_workspace(request.user)
    theme = get_object_or_404(Theme, id=theme_id, workspace=workspace)
    theme.delete()
    messages.success(request, 'Theme deleted.')
    return redirect('theme_list')

@login_required
@require_POST
def toggle_statement_theme(request, statement_id, theme_id):
    workspace = get_workspace(request.user)
    statement = get_object_or_404(Statement, id=statement_id, paper__workspace=workspace)
    theme = get_object_or_404(Theme, id=theme_id, workspace=workspace)
    if statement.themes.filter(id=theme.id).exists():
        statement.themes.remove(theme)
    else:
        statement.themes.add(theme)
    return redirect('paper_detail', paper_id=statement.paper_id)

@login_required
def synthesis(request):
    workspace = get_workspace(request.user)
    themes = workspace.themes.prefetch_related('statements__paper').all()
    return render(request, 'library/synthesis.html', {'themes': themes})

@login_required
def export_csv(request):
    workspace = get_workspace(request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scholarflow_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Theme', 'Statement', 'Paper', 'Author', 'Year', 'Page', 'Note', 'Created At'])
    for theme in workspace.themes.all():
        for statement in theme.statements.select_related('paper').all():
            writer.writerow([theme.name, statement.text, statement.paper.title, statement.paper.author, statement.paper.year, statement.page_number, statement.note, statement.created_at.isoformat()])
    return response
