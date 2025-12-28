from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import VIPClient, Organization, Interaction, User, Role


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    """Главная страница (дашборд)"""
    total_clients = VIPClient.objects.count()
    active_clients = VIPClient.objects.filter(status='active').count()
    total_organizations = Organization.objects.count()
    recent_interactions = Interaction.objects.select_related('vip_client', 'user').order_by('-date')[:10]
    
    context = {
        'total_clients': total_clients,
        'active_clients': active_clients,
        'total_organizations': total_organizations,
        'recent_interactions': recent_interactions,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def users_list(request):
    """Список пользователей"""
    users = User.objects.select_related('role').all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/users_list.html', context)


@login_required
def vip_clients_list(request):
    """Список VIP-клиентов"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    clients = VIPClient.objects.select_related('organization').all()
    
    if search_query:
        clients = clients.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(position__icontains=search_query)
        )
    
    if status_filter:
        clients = clients.filter(status=status_filter)
    
    context = {
        'clients': clients,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': VIPClient.STATUS_CHOICES,
    }
    return render(request, 'projects/vip_clients_list.html', context)


@login_required
def vip_client_detail(request, pk):
    """Детальная информация о VIP-клиенте"""
    client = get_object_or_404(VIPClient.objects.select_related('organization'), pk=pk)
    interactions = Interaction.objects.filter(vip_client=client).select_related('user').order_by('-date')
    
    context = {
        'client': client,
        'interactions': interactions,
    }
    return render(request, 'projects/vip_client_detail.html', context)


@login_required
def vip_client_add(request):
    """Добавление нового VIP-клиента"""
    if request.method == 'POST':
        try:
            client = VIPClient.objects.create(
                full_name=request.POST.get('full_name'),
                position=request.POST.get('position'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                organization_id=request.POST.get('organization') or None,
                status=request.POST.get('status', 'active'),
                notes=request.POST.get('notes', ''),
            )
            messages.success(request, f'VIP-клиент {client.full_name} успешно добавлен')
            return redirect('vip_client_detail', pk=client.pk)
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении клиента: {str(e)}')
    
    organizations = Organization.objects.all()
    context = {
        'organizations': organizations,
        'status_choices': VIPClient.STATUS_CHOICES,
    }
    return render(request, 'projects/vip_client_add.html', context)


@login_required
def vip_client_edit(request, pk):
    """Редактирование VIP-клиента"""
    client = get_object_or_404(VIPClient, pk=pk)
    
    if request.method == 'POST':
        try:
            client.full_name = request.POST.get('full_name')
            client.position = request.POST.get('position')
            client.phone = request.POST.get('phone')
            client.email = request.POST.get('email')
            client.organization_id = request.POST.get('organization') or None
            client.status = request.POST.get('status', 'active')
            client.notes = request.POST.get('notes', '')
            client.save()
            messages.success(request, f'VIP-клиент {client.full_name} успешно обновлен')
            return redirect('vip_client_detail', pk=client.pk)
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении клиента: {str(e)}')
    
    organizations = Organization.objects.all()
    context = {
        'client': client,
        'organizations': organizations,
        'status_choices': VIPClient.STATUS_CHOICES,
    }
    return render(request, 'projects/vip_client_edit.html', context)


@login_required
def vip_client_delete(request, pk):
    """Удаление VIP-клиента"""
    client = get_object_or_404(VIPClient, pk=pk)
    
    if request.method == 'POST':
        client_name = client.full_name
        client.delete()
        messages.success(request, f'VIP-клиент {client_name} успешно удален')
        return redirect('vip_clients_list')
    
    context = {
        'client': client,
    }
    return render(request, 'projects/vip_client_delete.html', context)


@login_required
def organizations_list(request):
    """Список организаций"""
    organizations = Organization.objects.all()
    context = {
        'organizations': organizations,
    }
    return render(request, 'projects/organizations_list.html', context)


@login_required
def interaction_add(request, client_pk):
    """Добавление взаимодействия с VIP-клиентом"""
    client = get_object_or_404(VIPClient, pk=client_pk)
    
    if request.method == 'POST':
        try:
            interaction = Interaction.objects.create(
                vip_client=client,
                user=request.user,
                date=request.POST.get('date'),
                type=request.POST.get('type'),
                channel=request.POST.get('channel') or None,
                description=request.POST.get('description'),
                result=request.POST.get('result', ''),
            )
            messages.success(request, 'Взаимодействие успешно добавлено')
            return redirect('vip_client_detail', pk=client.pk)
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении взаимодействия: {str(e)}')
    
    context = {
        'client': client,
        'type_choices': Interaction.TYPE_CHOICES,
        'channel_choices': Interaction.CHANNEL_CHOICES,
    }
    return render(request, 'projects/interaction_add.html', context)
