from django.shortcuts import render, redirect
from .forms import ContactForm
from .tasks import send_contact_email

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_contact_email.delay(
                "New Message",
                form.cleaned_data['message'],
                form.cleaned_data['email']
            )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
