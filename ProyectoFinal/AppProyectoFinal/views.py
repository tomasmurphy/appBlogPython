from tkinter.filedialog import SaveAs
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from itsdangerous import Serializer
from AppProyectoFinal.models import *
from AppProyectoFinal.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, BaseUpdateView


#PAGINA PRINCIPAL
def inicio(request):
      return render(request, "AppProyectoFinal/inicio.html")

def login_request(request):
      if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)
            if form.is_valid():
                  usuario = form.cleaned_data.get("username")
                  contraseña = form.cleaned_data.get("password")
                  user = authenticate(username=usuario, password=contraseña)
                  if user is not None:
                        login(request, user)
                        return redirect("inicio")
                  else:
                        return render(request, "AppProyectoFinal/login.html",{"bienvenido":"Error, datos incorrectos"})
            else:
                  form = AuthenticationForm()
                  return render(request, "AppProyectoFinal/login.html", {"bienvenido":"Error, datos incorrectos","form":form})
      form = AuthenticationForm()
      return render(request, "AppProyectoFinal/login.html", {"form":form})

def register(request):
      if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                  informacion = form.cleaned_data
                  form.save()
                  return redirect('login')
      else:
           form = UserRegisterForm()
      return render(request, "AppProyectoFinal/register.html", {"form":form})     

def acerca_de_mi(request):
      return render(request, "AppProyectoFinal/acerca_de_mi.html")
     
def error404(request, exception):
    
    return render(request, "AppProyectoFinal/404.html", status=404)

def error500(request):
    
    return render(request, "AppProyectoFinal/500.html", status=500)

#BLOG
class GaleriaListView(ListView):
      model = Blog
      template_name = "AppProyectoFinal/galeria.html"
      
class GaleriaDetailView(DetailView):
      model = Blog
      template_name = "AppProyectoFinal/ver_blog.html"
            
class BlogListView(ListView):
      model = Blog
      template_name = "AppProyectoFinal/Blog.html"

class BlogDetailView(DetailView):
      model = Blog
      template_name = "AppProyectoFinal/ver_blog.html"
        
class BlogCreateView(CreateView):
      model = Blog
      fields = ["titulo", "autor","texto","portada"]
      success_url = reverse_lazy('blog')
      template_name = "AppProyectoFinal/form_blog.html"
      
      def form_valid(self, form):
            try:
                  user = User.objects.get(username = self.request.user)
            except ObjectDoesNotExist:
                  user = "Anonimo"

            Blog.objects.create(titulo = self.request.POST['titulo'],
                            autor = self.request.POST['autor'], 
                            texto = self.request.POST['texto'],
                            portada = self.request.FILES['portada'],
                            usuario = user)
            return redirect(self.success_url)

def buscar_blog(request):
      if request.GET["titulo"]:
            titulo = request.GET["titulo"]
            texto = Blog.objects.filter(titulo__icontains=titulo)
            foro_list = {"titulo":titulo,"blog_list":texto}
            return render(request, "AppProyectoFinal/blog.html",foro_list)
      else:
            return render(request, "AppProyectoFinal/blog.html")

#FORO
class ForoListView(ListView):
      model = Foro
      template_name = "AppProyectoFinal/foro.html"
       
class ForoCreateView(CreateView):
      model = Foro
      fields = ["mensaje"]
      success_url = reverse_lazy('foro')
      template_name = "AppProyectoFinal/mensajes.html"
      
      
      def form_valid(self, form):
            try:
                  user = User.objects.get(username = self.request.user)
            except ObjectDoesNotExist:
                  user = "Anonimo"
        
            Foro.objects.create(mensaje = self.request.POST['mensaje'], usuario = user)
            return redirect(self.success_url)
      
def buscar_mensaje(request):
      if request.GET["usuario"]:
            usuario = request.GET["usuario"]
            mensaje = Foro.objects.filter(usuario__icontains=usuario)
            foro_list = {"usuario":usuario,"foro_list":mensaje}
            return render(request, "AppProyectoFinal/foro.html",foro_list)
      else:
            return render(request, "AppProyectoFinal/foro.html")

#PODCAST

class PodcastListView(ListView):
      model = Podcast
      template_name = "AppProyectoFinal/podcast.html"
        
class PodcastCreateView(CreateView):
      model = Podcast
      fields = ["link"]
      success_url = reverse_lazy('podcast')
      template_name = "AppProyectoFinal/form_podcast.html"
      
      def form_valid(self, form):
            try:
                  user = User.objects.get(username = self.request.user)
            except ObjectDoesNotExist:
                  user = "Anonimo"

            Podcast.objects.create(link = self.request.POST['link'],
                            usuario = user)
            return redirect(self.success_url)

def buscar_podcast(request):
      if request.GET["usuario"]:
            usuario = request.GET["usuario"]
            mensaje = Podcast.objects.filter(usuario__icontains=usuario)
            foro_list = {"usuario":usuario,"podcast_list":mensaje}
            return render(request, "AppProyectoFinal/podcast.html",foro_list)
      else:
            return render(request, "AppProyectoFinal/podcast.html")

#ADMINISTRADOR-
@staff_member_required
def administrador(request):
      return render(request, "AppProyectoFinal/administrador.html")

#foro
@method_decorator (staff_member_required, name="dispatch")
class AdminstradorForoListView(ListView):
      model = Foro
      template_name = "AppProyectoFinal/foro_lista_administrador.html"

@staff_member_required
def buscar_mensaje_administrador(request):
      if request.GET["usuario"]:
            usuario = request.GET["usuario"]
            mensaje = Foro.objects.filter(usuario__icontains=usuario)
            foro_list = {"usuario":usuario,"foro_list":mensaje}
            return render(request, "AppProyectoFinal/foro_lista_administrador.html",foro_list)
      else:
            return render(request, "AppProyectoFinal/foro_lista_administrador.html")

@method_decorator (staff_member_required, name="dispatch")            
class AdministradorForoDeleteView(DeleteView):
      model = Foro
      template_name = "AppProyectoFinal/foro_confirm_delete.html"
      success_url = reverse_lazy('foro_lista_administrador')
      
@method_decorator (staff_member_required, name="dispatch")
class AdministradorForoUpdateView(UpdateView):
      model = Foro
      fields = ["mensaje"]
      success_url = reverse_lazy('foro_lista_administrador')
      template_name = "AppProyectoFinal/foro_editar_administrador.html"

#blog
@method_decorator (staff_member_required, name="dispatch")
class AdminstradorBlogListView(ListView):
      model = Blog
      template_name = "AppProyectoFinal/blog_lista_administrador.html"

@staff_member_required
def buscar_blog_administrador(request):
      if request.GET["titulo"]:
            titulo = request.GET["titulo"]
            texto = Blog.objects.filter(titulo__icontains=titulo)
            foro_list = {"titulo":titulo,"blog_list":texto}
            return render(request, "AppProyectoFinal/blog_lista_administrador.html",foro_list)
      else:
            return render(request, "AppProyectoFinal/blog_lista_administrador.html")

@method_decorator (staff_member_required, name="dispatch")
class AdministradorBlogDeleteView(DeleteView):
      model = Blog
      template_name = "AppProyectoFinal/blog_confirm_delete.html"
      success_url = reverse_lazy('blog_lista_administrador')

@method_decorator (staff_member_required, name="dispatch")      
class AdministradorBlogUpdateView(UpdateView):
      model = Blog
      fields = ["titulo","autor","portada","texto"]
      success_url = reverse_lazy('blog_lista_administrador')
      template_name = "AppProyectoFinal/blog_editar_administrador.html"  

#podcast
@method_decorator (staff_member_required, name="dispatch")
class AdminstradorPodcastListView(ListView):
      model = Podcast
      template_name = "AppProyectoFinal/podcast_lista_administrador.html"

@staff_member_required
def buscar_podcast_administrador(request):
      if request.GET["usuario"]:
            usuario = request.GET["usuario"]
            mensaje = Podcast.objects.filter(usuario__icontains=usuario)
            podcast_list = {"usuario":usuario,"podcast_list":mensaje}
            return render(request, "AppProyectoFinal/podcast_lista_administrador.html",podcast_list)
      else:
            return render(request, "AppProyectoFinal/podcast_lista_administrador.html")

@method_decorator (staff_member_required, name="dispatch")            
class AdministradorPodcastDeleteView(DeleteView):
      model = Podcast
      template_name = "AppProyectoFinal/podcast_confirm_delete.html"
      success_url = reverse_lazy('podcast_lista_administrador')
      
@method_decorator (staff_member_required, name="dispatch")
class AdministradorPodcastUpdateView(UpdateView):
      model = Podcast
      fields = ["link"]
      success_url = reverse_lazy('podcast_lista_administrador')
      template_name = "AppProyectoFinal/podcast_editar_administrador.html"

#usuario
@method_decorator (staff_member_required, name="dispatch")
class AdminstradorUserListView(ListView):
      model = User
      template_name = "AppProyectoFinal/usuario_lista_administrador.html"

@staff_member_required
def buscar_user_administrador(request):
      if request.GET["username"]:
            username = request.GET["username"]
            texto = User.objects.filter(username__icontains=username)
            user_list = {"username":username,"user_list":texto}
            return render(request, "AppProyectoFinal/usuario_lista_administrador.html",user_list)
      else:
            return render(request, "AppProyectoFinal/usuario_lista_administrador.html")
            
@method_decorator (staff_member_required, name="dispatch")
class AdministradorUserDeleteView(DeleteView):
      model = User
      template_name = "AppProyectoFinal/User_confirm_delete.html"
      success_url = reverse_lazy('usuario_lista_administrador')
      
@method_decorator (staff_member_required, name="dispatch")
class AdministradorUserUpdateView(UpdateView):
      model = User
      fields = ["username","email","first_name","last_name", "is_active","is_staff"]
      success_url = reverse_lazy('usuario_lista_administrador')
      template_name = "AppProyectoFinal/usuario_editar_administrador.html"

@staff_member_required
def change_password_administrador(request, id):

      usuario = User.objects.get(id=id)
     
      if request.method == 'POST':
            miFormulario = UserEditForm(request.POST) 
            if miFormulario.is_valid():

                  informacion = miFormulario.cleaned_data
                  usuario.set_password(informacion['password1'])
                  usuario.save()

                  return render(request, "AppProyectofinal/inicio.html") 
      else: 
            miFormulario= UserEditForm() 

      return render(request, "AppProyectoFinal/change_password_administrador.html", {"form":miFormulario, "usuario":usuario})

      
#PERFIL DE USUARIO
@method_decorator (login_required, name="dispatch")
class UserAutoUpdateView(UpdateView):
      model = User
      fields = ["email","first_name","last_name"]
      success_url = reverse_lazy('mi_usuario')
      template_name = "AppProyectoFinal/editar_usuario.html"

      def get_object(self, queryset = None):
          return self.request.user
      
@login_required
def mi_usuario(request):
      return render(request, "AppProyectoFinal/mi_usuario.html")

@login_required
def change_password(request):
      usuario = request.user
      if request.method == 'POST':
            miFormulario = UserEditForm(request.POST) 
            if miFormulario.is_valid():

                  informacion = miFormulario.cleaned_data
                  usuario.set_password(informacion['password1'])
                  usuario.save()

                  return redirect("login") 
      else: 
            
            miFormulario= UserEditForm(initial={ 'email':usuario.email}) 

      return render(request, "AppProyectoFinal/change_password.html", {"form":miFormulario, "usuario":usuario})



