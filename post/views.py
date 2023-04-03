from django.shortcuts import redirect
from django.views.generic import (ListView, CreateView, UpdateView,
								  DeleteView, DetailView)
from .models import Image, Post
from django.urls import reverse_lazy
from django.views import View
from .mixins import PostMixin, ImageMixin
from accounts.mixins import MyLoginRequiredMixin


class PostListView(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'post/PostList.html'

    def get_queryset(self):
        return self.model.objects.all()


class PostDetailView(MyLoginRequiredMixin, DetailView):
	model = Post
	template_name = 'post/PostDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['coments'] = self.model.objects.get(id=self.kwargs['pk']).comments.all()
		return context
	
	def blog_view(self):
		user = self.request.user
		if user not in self.model.views.all():
			self.model.views.add(user)
		else:
			self.model.views.remove(user)


class PostCreateView(MyLoginRequiredMixin, CreateView):
	model = Post
	fields = ('body',)
	template_name = "post/PostCreate.html"

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form['body'].field.widget.attrs.update({'class' : 'btn btn-outline-light'})
		return form    

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class PostUpdateView(PostMixin, UpdateView):
	model = Post
	fields = ('body',)
	template_name = "post/PostUpdate.html"

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form['body'].field.widget.attrs.update({'class' : 'btn btn-outline-light'})
		return form    


class PostDeleteView(PostMixin, DeleteView):
    model = Post
    template_name = 'post/PostDelete.html'
    success_url = reverse_lazy('blog:BlogList')


class PostLikesView(View):
	def dispatch(self, request, pk, *args, **kwargs):
		user = request.user
		post = Post.objects.get(id=pk)
		if user.is_authenticated:
			if user in post.unlikes.all():
				post.unlikes.remove(user)
			if user not in post.likes.all():
				post.likes.add(user)
			else:
				post.likes.remove(user)			
		else:
			return redirect('accounts:Login')


		return redirect('blog:PostDetail', post.id)


class PostUnLikesView(View):
	def dispatch(self, request, pk, *args, **kwargs):
		user = request.user
		post = Post.objects.get(id=pk)
		if user.is_authenticated:
			if user in post.likes.all():
				post.likes.remove(user)
			if user not in post.unlikes.all():
				post.unlikes.add(user)
			else:
				post.unlikes.remove(user)			
		else:
			return redirect('accounts:Login')

		return redirect('blog:PostDetail', post.id)


class ImageCreateView(MyLoginRequiredMixin, CreateView):
	model = Image
	fields = ('image',)
	template_name = "image/ImageCreate.html"

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.post = Post.objects.get(id=self.kwargs['pk'])
		return super(ImageCreateView, self).form_valid(form)


class ImageUpdateView(ImageMixin, UpdateView):
	model = Image
	fields = ('image',)
	template_name = "image/ImageUpdate.html"


class ImageDeleteView(ImageMixin, DeleteView):
    model = Image
    template_name = 'image/ImageDelete.html'
    success_url = reverse_lazy('blog:BlogList')
