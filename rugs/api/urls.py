from django.urls import path
from .views import RugFinderAPI, RugPartListAPI, RugTypListAPI, UserRugListAPI, UserRugDetailAPI, RugSellersListAPI, \
    RugLogCreateAPI, NewRugPartsListAPI, RugBrandsListAPI, RugYarnsListAPI, RugColorsListAPI, RugCitiesListAPI, \
    RugListAPI, RugReplacementFormAPI, CustomRugSizeListAPI, CustomRugRequestAPI, RugDensitiesListAPI, RugShanehsListAPI

app_name = "rug-api"
urlpatterns = [
    path('find/', RugFinderAPI.as_view(), name="rug-finder"),
    path('rugs/', RugListAPI.as_view(), name="rug-list"),
    path('brands/', RugBrandsListAPI.as_view(), name="rug-brands"),
    path('yarns/', RugYarnsListAPI.as_view(), name="rug-yarns"),
    path('densities/', RugDensitiesListAPI.as_view(), name="rug-densities"),
    path('shanehs/', RugShanehsListAPI.as_view(), name="rug-shanehs"),
    path('colors/', RugColorsListAPI.as_view(), name="rug-colors"),
    path('cities/', RugCitiesListAPI.as_view(), name="rug-cities"),
    path('parts/', RugPartListAPI.as_view(), name="rug-parts"),
    path('parts/new/', NewRugPartsListAPI.as_view(), name="rug-parts-new"),
    path('types/', RugTypListAPI.as_view(), name="rug-types"),
    path('user-rugs/', UserRugListAPI.as_view(), name="user-rug-list"),
    path('rug-replacement/', RugReplacementFormAPI.as_view(), name="rug-replacement"),
    path('custom-rug/sizes/', CustomRugSizeListAPI.as_view(), name="custom-rug-sizes"),
    path('custom-rug/', CustomRugRequestAPI.as_view(), name="custom-rug-request"),
    path('user-rug/<int:pk>', UserRugDetailAPI.as_view(), name="user-rug-detail"),
    path('rug/<int:pk>/sellers', RugSellersListAPI.as_view(), name="rug-sellers"),
    path('log/', RugLogCreateAPI.as_view(), name="rug-log"),
]
