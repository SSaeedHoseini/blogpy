from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *


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


class SingleArticleAPIView(APIView):

    def get(self, request):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serializer_data = SingleArticleSerializer(article, many=True)
            return Response({'data': serializer_data.data}, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response({'message': exc}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):

    def get(self, request):
        try:
            from django.db.models import Q
            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            article_data = []
            for article in articles:
                article_data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at.date(),
                    'category': article.category.title,
                    'auther': article.auther.user.first_name + ' ' + article.auther.user.last_name,
                    'promote': article.promote,
                })
            return Response(data={'data': article_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'data': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitArticleAPIView(APIView):

    def post(self, request):
        try:
            serialized_data = SubmitArticleSerializer(data=request.data)
            if serialized_data.is_valid():
                title = serialized_data.data.get('title')
                cover = request.FILES['cover']
                content = serialized_data.data.get('content')
                category_id = serialized_data.data.get('category_id')
                auther_id = serialized_data.data.get('auther_id')
                promote = serialized_data.data.get('promote')
            else:
                return Response(data={'message': serialized_data.errors()}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=auther_id)
            # if user.DoesNotExist:
            #     return Response(data={'message': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

            user_profile = UserProfile.objects.get(user=user)
            # if user_profile.DoesNotExist:
            #     return Response(data={'message': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

            categoty = Category.objects.get(id=category_id)
            # if categoty.DoesNotExist:
            #     return Response(data={'message': 'categoty not found.'}, status=status.HTTP_404_NOT_FOUND)

            article = Article()
            article.title = title
            article.auther = user_profile
            article.category = categoty
            article.content = content
            article.cover = cover
            article.promote = promote
            article.save()

            return Response(data={'id': article.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data={'data': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateArticleCoverAPIView(APIView):

    def post(self, request):
        try:
            serializer = UpdateArticleCoverSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response(data={'message':'bad request.'},status=status.HTTP_404_NOT_FOUND)

            Article.objects.filter(id=article_id).update(cover=cover)
            return Response(data={'id':article_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'message': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):

    def post(self, request):
        try:
            serializer = DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response(data={'message': 'bad request.'}, status=status.HTTP_404_NOT_FOUND)

            Article.objects.filter(id=article_id).delete()
            return Response(data={'id': article_id}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={'message': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)