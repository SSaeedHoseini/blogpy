from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^contact$', views.ContactPage.as_view(), name='contact'),
    url(r'^article/all/$', views.AllArticleAPIView.as_view(), name='all_article'),

    url(r'^article/$', views.SingleArticleAPIView.as_view(), name='single'),
    url(r'^search/$', views.SearchArticleAPIView.as_view(), name='search'),

    url('^article/submit/$',views.SubmitArticleAPIView.as_view(), name='submit'),

    url('^article/update_cover/$', views.UpdateArticleCoverAPIView.as_view(), name='update_cover'),

    url('^article/delete/$', views.DeleteArticleAPIView.as_view(), name='delete'),

]

