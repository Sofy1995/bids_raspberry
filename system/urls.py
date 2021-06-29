from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,  name='index'),
    path('bids/', views.BidListView.as_view(extra_context={'whose': 'all'}), name='bids'),
    path('bid/<int:pk>', views.BidDetailView.as_view(), name='bid-detail'),
    path('mybids/', views.MakingBidsByUserListView.as_view(extra_context={'whose': 'user'}), name='my-bids'),
]

urlpatterns += [
    path('bid/create/', views.bid_create, name='bid-create'),
    path('bid/<int:pk>/update/', views.bid_update, name='bid-update'),
    path('bid/<int:pk>/delete/', views.BidDelete.as_view(), name='bid-delete'),
    path('sticker/', views.sticker_create, name='sticker-create'),
    path('sticker/<int:pk>/update/', views.sticker_update, name='sticker-update'),
    path('sticker/delete<int:pk>', views.StickerDelete.as_view(), name='sticker-delete'),
    path('bid/search/', views.bid_search, name='bid-search'),
    path('bid/archive/', views.BidArchiveView.as_view(extra_context={'whose': 'past'}), name='bid-archive'),
    ]
