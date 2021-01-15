from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,  name='index'),
    path('bids/', views.BidListView.as_view(), name='bids'),
    path('bid/<int:pk>', views.BidDetailView.as_view(), name='bid-detail'),
    path('mybids/', views.MakingBidsByUserListView.as_view(), name='my-bids'),
]

urlpatterns += [
    # path('bid/create/', views.BidCreate.as_view(), name='bid-create'),
    path('bid/create/', views.bid_create, name='bid-create'),
    path('bid/<int:pk>/update/', views.bid_update, name='bid-update'),
    path('bid/<int:pk>/delete/', views.BidDelete.as_view(), name='bid-delete'),
    path('sticker/', views.sticker_create, name='sticker-create'),
    path('sticker/delete<int:pk>', views.StickerDelete.as_view(), name='sticker-delete'),
    # path('bid/<int:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
