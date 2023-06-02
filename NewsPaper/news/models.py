from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

POST_TYPE = [
    ("N", "News"),
    ("A", "Articles")
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username

    # Calculates the rating of an author based on:
    # 1 - posts written by an author * 3
    # 2 - rating of all author's comments
    # 3 - rating of all comments under author's posts
    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum']
        if posts_rating is None: posts_rating = 0
        posts_rating *= 3

        author_comment_rating = Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))['rating__sum']
        if author_comment_rating is None: author_comment_rating = 0

        post_commenters_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        if post_commenters_rating is None: post_commenters_rating = 0

        self.rating = posts_rating + author_comment_rating + post_commenters_rating


class Category(models.Model):
    tag = models.CharField(max_length=64, unique = True)

    def __str__(self):
        return self.tag


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPE)
    publication_date = models.DateField(auto_now_add = True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default = 0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.content[:124] + "..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_date = models.DateField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
