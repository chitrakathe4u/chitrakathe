"""
URL configuration for chitrakathe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),
    path('', views.index, name="index" ),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('login/', views.login_view, name="login" ),
    path('admin-members/', views.admin_members, name="admin_members" ),
    path('admin-members/<int:id>/', views.admin_members_profile, name="admin_members_profile" ),
    path('admin-posts/', views.admin_posts, name="admin_posts" ),
    path('delete-post/<int:id>/', views.delete_post, name="delete_posts" ),
    path('delete-member/<int:id>/', views.delete_member, name="delete_member" ),
    path('edit-post/<int:pk>/', views.edit_post, name="edit_post" ),
    path('add-post/', views.add_post, name="add_post" ),
    path('add-member/', views.add_member, name="add_members" ),
   path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
   path('logout/', views.logout_view, name='logout'),
   path('team/', views.team, name='team'),
   path('about/', views.about, name='about'),
   path('donate/', views.donate, name='donate'),
   path('team/<int:pk>', views.team_profile, name='team_profile'),
    path('category/', views.category, name='category'),
   path('submit-article/', views.submit_article, name='submit_article'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
