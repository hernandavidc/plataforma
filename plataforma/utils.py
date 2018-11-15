from registration.models import Cliente, Veterinaria 

def get_rol(request):
    if Cliente.objects.filter(user=request.user).first():
        #print("cliente")
        rol= 'c'
    elif Veterinaria.objects.filter(user=request.user).first():
        #print("Veterinaria")
        rol = 'v'
    else:
        rol = 'n'
    return rol

def get_perfil(request):
    if Cliente.objects.filter(user=request.user).first():
        #print("cliente")
        rol= Cliente.objects.filter(user=request.user).first()
    elif Veterinaria.objects.filter(user=request.user).first():
        #print("Veterinaria")
        rol = Veterinaria.objects.filter(user=request.user).first()
    else:
        rol = 'n'
    return rol