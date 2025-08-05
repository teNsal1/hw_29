from django import forms
from .models import Review, Order, Master, Service

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['master', 'rating', 'client_name', 'text', 'photo']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['services'].queryset = Service.objects.filter(masters__id=master_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.master:
            self.fields['services'].queryset = self.instance.master.services_offered.all()
        else:
            self.fields['services'].queryset = Service.objects.none()

    class Meta:
        model = Order
        fields = ['master', 'services', 'client_name', 'phone', 'comment', 'appointment_date']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-select'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')

        if master and services:
            invalid_services = [
                service for service in services 
                if not service.masters.filter(id=master.id).exists()
            ]
            if invalid_services:
                raise forms.ValidationError(
                    f"Мастер {master.name} не предоставляет: " +
                    ", ".join([s.name for s in invalid_services])
                )
        return cleaned_data