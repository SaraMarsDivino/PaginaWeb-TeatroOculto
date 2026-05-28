from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(username='admin').first()
if u:
    u.set_password('admin1234')
    u.save()
    print('password set for admin')
else:
    print('admin user not found')
