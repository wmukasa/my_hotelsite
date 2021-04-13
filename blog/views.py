from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
								DetailView,
								CreateView,
								UpdateView,
								DeleteView)

def home(request):
	return render(request,'blog/home.html')

def about(request):
	return render(request,'blog/about.html',{'title':'about'})

def accomodation(request):
	return render(request,'blog/accomodation.html',{'title':'accomodation'})

def gallery(request):
	return render(request,'blog/gallery.html',{'title':'gallery'})

def contact(request):
	return render(request,'blog/contact.html',{'title':'contact'})	

def blog(request):
	context = {
		'posts':Post.objects.all()
	}
	return render(request,'blog/blog.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/blog.html'
	context_object_name ='posts'
	ordering = ['-date_posted']
	paginate_by=3

class PostDetailView(DetailView):
	model = Post
class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post 
	fields =['title','content']
	
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

	model = Post 
	fields =['title','content']
	
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user ==post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	success_url = '/'
	model = Post
	def test_func(self):
		post = self.get_object()
		if self.request.user ==post.author:
			return True
		return False
class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_post.html'
	context_object_name ='posts'
	paginate_by=3
	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')