from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .forms import AdvertisementForm, ResponseForm
from .models import Advertisement, Response
import random


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisement_list.html'
    context_object_name = 'advertisements'
    ordering = ['-created_at']
    paginate_by = 3


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisement_detail.html'
    context_object_name = 'advertisement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'advertisement_create.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {'error': 'Этот email уже зарегистрирован'})

        code = str(random.randint(100000, 999999))
        request.session['registration_code'] = code
        request.session['registration_email'] = email

        send_mail(
            'Код подтверждения регистрации',
            f'Ваш код подтверждения: {code}\n'
            f'Этот код будет использоваться для входа в систему',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('verify_email')
    return render(request, 'registration/register.html')


def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session.get('registration_code'):
            email = request.session.get('registration_email')
            user = User.objects.create_user(username=email, email=email, password=code)
            login(request, user)
            del request.session['registration_code']
            del request.session['registration_email']
            return redirect('advertisement_list')
        else:
            return render(request, 'registration/verify_email.html', {'error': 'Неверный код'})
    return render(request, 'registration/verify_email.html')


@login_required
def create_response(request, ad_id):
    advertisement = get_object_or_404(Advertisement, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.author = request.user
            response.save()

            send_mail('Новый отклик на ваше объявление',
                      f'Пользователь {request.user.username} оставил отклик на ваше объявление '
                      f'"{advertisement.title}":\n\n"{response.content}"',
                      settings.DEFAULT_FROM_EMAIL,
                      [advertisement.author.email],
                      fail_silently=False,
                      )

            messages.success(request, 'Ваш отклик успешно отправлен.')
            return redirect('advertisement_detail', pk=ad_id)
        else:
            form = ResponseForm()
    return render(request, 'responses/create_response.html', {'form': form, 'advertisement': advertisement})


@login_required
def my_responses(request):
    responses = Response.objects.filter(advertisement__author=request.user).order_by('-created_at')
    response_filter = request.GET.get('response_filter')
    if response_filter:
        responses = responses.filter(advertisement_id=response_filter)

    user_advertisements = Advertisement.objects.filter(author=request.user)

    context = {
        'responses': responses,
        'user_advertisements': user_advertisements,
        'selected_ad': response_filter
    }
    return render(request, 'responses/my_responses.html', context)


@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, advertisement__author=request.user)
    response.adopted = True
    response.save()

    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{response.advertisement.title}" был принят автором.',
        settings.DEFAULT_FROM_EMAIL,
        [response.author.email],
        fail_silently=False,
    )

    messages.success(request, 'Отклик успешно принят.')
    return redirect('my_responses')


@login_required
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, advertisement__author=request.user)
    response.delete()
    messages.success(request, 'Отклик успешно удален.')
    return redirect('my_responses')
