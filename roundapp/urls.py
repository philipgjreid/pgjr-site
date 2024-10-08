from django.urls import path
from .import views

# urlpatterns = [
#     path('round/', views.round_home, name="round-home"),
#     path('new_round/', views.new_round, name="new-round"),
#     path('ajax/load_tees/', views.load_tees, name="ajax-load-tees"),
#     path('round_stats/', views.round_stats, name="round-stats"),
#     #path('round_stats/<int:round_id>/', views.round_stats, name="round-stats"),
#     path('round/<int:round_id>/stats/<int:hole_number>/', views.round_stats, name='round-stats-holes'),
#     path('round/<int:round_id>/summary/', views.round_summary, name='round-summary'),
# ]

urlpatterns = [
    path('golf_home/', views.golf_home, name="golf-home"),
    # path('round/', views.round_home, name="round-home"),
    path('new_round/', views.new_round, name='new-round'),
    path('ajax/load_tees/', views.load_tees, name="ajax-load-tees"),
    path('round/<int:round_number_id>/stats/<int:hole_number>/', views.round_stats, name='round-stats'),
    #path('round_stats/', views.round_stats, name='round-stats'),
    path('round_summary/<int:round_number_id>/summary/', views.round_summary, name='round-summary'),
    path('review_data/', views.review_data, name='review-data'),
    path('save-round/', views.save_round, name='save-round'),

    path('stats_test/<int:round_number_id>/<int:hole_number>/', views.stats_test, name='stats-test'),
    path('round_csv/<int:round_number_id>', views.round_csv, name="round-csv"),

    path('check_incomplete_rounds/', views.check_incomplete_rounds, name="check-incomplete-rounds"),
    path('continue_round/<int:round_number_id>', views.continue_round, name="continue-round"),
]