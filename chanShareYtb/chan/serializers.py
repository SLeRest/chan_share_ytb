from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from taggit.serializers import TaggitSerializer, TagListSerializerField

from chan import models

class BaseSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(BaseSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)

class SongSerializer(TaggitSerializer, BaseSerializer):
    tags = TagListSerializerField()

    class Meta:
        models.Song
        fields = [  'id_ytb',
                    'title',
                    'channel_id',
                    'channel_url',
                    'channel_title',
                    'uploader_id',
                    'uploader_name',
                    'duration',
                    'thumbnail',
                    'description',
                    'upload_date_ytb',
                    'download_datetime',
                    'download_error',
                    'download_status']

class SongCreateSerializer(ModelSerializer):

    class Meta:
        models.Song
        fields = ['url_ytb']

    # TODO make youtube valid url check by trying to download
    # def validate_price(self, value):
    #     if value <= 1:
    #         raise ValidationError('Price must be greater than 1')
    #     return value

# class ArticleSerializer(BaseSerializer):
#
#     class Meta:
#         model = models.Article
#         fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
#
#     def validate_price(self, value):
#         if value <= 1:
#             raise ValidationError('Price must be greater than 1')
#         return value
#
#     def validate_product(self, value):
#         if value.active is False:
#             raise ValidationError('Inactive product')
#         return value
#
# class ProductListSerializer(BaseSerializer):
#
#     class Meta:
#         model = models.Product
#         fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecosore']
#
#
# class ProductDetailSerializer(BaseSerializer):
#     articles = SerializerMethodField()
#
#     class Meta:
#         model = models.Product
#         fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']
#
#     def get_articles(self, instance):
#         queryset = instance.articles.filter(active=True)
#         rf = ['product']
#         serializer = ArticleSerializer(queryset, remove_fields=rf, many=True)
#         return serializer.data
#
# class CategoryListSerializer(BaseSerializer):
#
#     class Meta:
#         model = models.Category
#         fields = ['id', 'name', 'date_created', 'date_updated', 'description']
#
#     def validate_name(self, value):
#         if models.Category.objects.filter(name=value).exists():
#             raise ValidationError('Category already exists')
#         return value
#
#     def validate(self, data):
#         if data['name'] not in data['description']:
#             raise ValidationError('NAme must be in description')
#         return data
#             
#
# class CategoryDetailSerializer(BaseSerializer):
#
#     products = SerializerMethodField()
#
#     class Meta:
#         model = models.Category
#         fields = ['id', 'name', 'date_created', 'date_updated', 'products']
#
#     def get_products(self, instance):
#         queryset = instance.products.filter(active=True)
#         rf = ['category']
#         serializer = ProductListSerializer(queryset, remove_fields=rf, many=True)
#         return serializer.data
