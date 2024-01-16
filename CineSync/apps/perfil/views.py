from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def mostrar_perfil(request):
    user_profile = getattr(request.user, 'userprofile', None)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('mostrar_perfil')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'perfil.html', {'form': form, 'user_profile': user_profile})