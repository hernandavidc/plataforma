from registration.models import Cliente, Veterinaria 

def rol_data(request):
    if not (request.user.is_anonymous):
        if Cliente.objects.filter(user=request.user).first():
            #print("cliente")
            rol= 'c'
        elif Veterinaria.objects.filter(user=request.user).first():
            #print("Veterinaria")
            rol = 'v'
        else:
            rol = 'n'
        return {'rol': rol}
    else:
        return {}