from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from bonanzamall import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="Home"),
    path('login/', views.user_login, name="userLogin"),
    path('registration/', views.registration, name="userReg"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='userLogout'),
    path('shop/', views.shop, name="Shop"),
    # path('detail/', views.detail, name="Detail"),
    path('contact/', views.contact, name="Contact"),
    path('cart/', views.view_cart, name="Cart"),
    path('checkout/', views.view_checkout, name="Checkout"),

    path('save-billing-info/', views.place_order, name="SaveBilling"),
    # path('download-details/', views.download_checkout_details, name="DownloadCheckoutDetails"),
    path('orders-history/', views.orders_history, name="OrdersHistory"),
    path('order-details/<int:invoice_number>', views.order_details, name='OrderDetails'),


    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('help/', views.help, name="Help"),
    path('FAQs/', views.FAQ, name="FAQ"),
    path('about/', views.about, name="About"),
    path('top-products-details/<top_products_name_ref>', views.top_products_details, name="TopProductsDetails"),
    path('special-offers-details/<special_offers_name_ref>', views.special_offers_details, name="SpecialOffersDetails"),
    path('store-products-details/<store_products_name_ref>', views.store_products_details, name="StoreProductsDetails"),

    
    # Categories
    path('usb-flash-drives/<int:category_id>/', views.product_category, name="USBDrives"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('earbuds/<int:category_id>/', views.product_category, name="EarBuds"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('men-watches/<int:category_id>/', views.product_category, name="MenWatches"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('men-smart-watches/<int:category_id>/', views.product_category, name="MenSmartWatches"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('men-rings/<int:category_id>/', views.product_category, name="MenRings"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('men-wallets/<int:category_id>/', views.product_category, name="MenWallets"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('men-smart-wallets/<int:category_id>/', views.product_category, name="MenSmartWallets"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('women-jewelry-sets/<int:category_id>/', views.product_category, name="WomenJewelrySet"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('women-fashion-watches/<int:category_id>/', views.product_category, name="WomenFashionWatches"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('women-fashion-rings/<int:category_id>/', views.product_category, name="WomenFashionRings"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('women-fashion-neclace/<int:category_id>/', views.product_category, name="WomenFashionNeclace"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),

    path('women-fashion-bags/<int:category_id>/', views.product_category, name="WomenFashionBags"),
    path('product-details/<all_products_name_ref>', views.product_category_details, name="ProductDetails"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
