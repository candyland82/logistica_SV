import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica_SV.settings')
django.setup()

def test_email():
    print("--- Probando Configuración de Correo ---")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"User: {settings.EMAIL_HOST_USER}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    
    try:
        print("\nIntentando enviar correo de prueba...")
        send_mail(
            'Prueba de Configuración Logística SV',
            'Si lees esto, el archivo .env y la configuración SMTP funcionan correctamente. 🚀',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER], # Se envía a sí mismo
            fail_silently=False,
        )
        print("✅ ¡ÉXITO! Correo enviado correctamente.")
        print(f"Revisa la bandeja de entrada de {settings.EMAIL_HOST_USER}")
    except Exception as e:
        print("❌ ERROR: No se pudo enviar el correo.")
        print(f"Detalle del error: {e}")

if __name__ == "__main__":
    test_email()
