from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class IndexPage(TemplateView):

    def get(self, request, *args, **kwargs):

        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'created_at': article.created_at.date(),
                'category': article.category.title,
            })

        promote_data = []
        all_promote_articles = Article.objects.filter(promote=True)
        for promote_article in all_promote_articles:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'auther': promote_article.auther.user.first_name + ' ' + promote_article.auther.user.last_name,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'avatar': promote_article.auther.avatar.url if promote_article.auther.avatar else None,
                'created_at': promote_article.created_at.date()
            })

        context = {'article_data': article_data,
                   'promote_article_data': promote_data}

        return render(request, 'index.html', context=context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'


class AllArticleAPIView(APIView):

    def get(self, request):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:10]
            data = []

            for article in all_articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at.date(),
                    'category': article.category.title,
                    'auther': article.auther.user.first_name + ' ' + article.auther.user.last_name,
                    'promote': article.promote,
                })
            return Response(data={'data': data}, status=status.HTTP_200_OK)

        except:
            return Response(data={'message': 'soneting wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
