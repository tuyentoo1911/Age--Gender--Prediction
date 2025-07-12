from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import ContactForm
from .models import ContactMessage


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ContactView(View):
    """Contact form view"""
    
    def get(self, request):
        form = ContactForm()
        context = {
            'form': form,
            'page_title': 'Liên hệ'
        }
        return render(request, 'contact/contact.html', context)
    
    def post(self, request):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                # Save contact message
                contact_message = form.save(commit=False)
                contact_message.ip_address = get_client_ip(request)
                contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
                contact_message.save()
                
                messages.success(
                    request, 
                    'Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.'
                )
                return redirect('contact')
                
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        
        else:
            # Form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        
        context = {
            'form': form,
            'page_title': 'Liên hệ'
        }
        return render(request, 'contact/contact.html', context)


class ContactSuccessView(View):
    """Contact success page"""
    
    def get(self, request):
        context = {
            'page_title': 'Gửi thành công'
        }
        return render(request, 'contact/success.html', context) 