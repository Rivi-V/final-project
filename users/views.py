from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from users.forms import LoginForm, ProfileForm, RegisterForm, UserPasswordChangeForm
from users.models import User
from users.service import apply_variant_one_filter, paginate_queryset


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request, request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('projects:list')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('projects:list')


def user_detail_view(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related('owned_projects__participants', 'skills'),
        pk=user_id,
    )
    return render(request, 'users/user-details.html', {'user': profile_user})


@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('users:detail', user_id=request.user.id)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def change_password_view(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('users:detail', user_id=request.user.id)
    return render(request, 'users/change_password.html', {'form': form})


def users_list_view(request):
    participants = User.objects.all()
    context = {}
    if request.user.is_authenticated:
        active_filter = request.GET.get('filter')
        context['active_filter'] = active_filter
        participants = apply_variant_one_filter(participants, request.user, active_filter)

    context['participants'] = paginate_queryset(
        participants.distinct().order_by('-date_joined', '-id'),
        request,
    )
    return render(request, 'users/participants.html', context)
