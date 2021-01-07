# import graphene

# class Query(graphene.ObjectType):
#     hello = graphene.String(default_value="Hi!")

# schema = graphene.Schema(query=Query)

import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from graphene_django.forms.mutation import DjangoModelFormMutation

from django.forms import ModelForm

from items.models import Category, SubCategory, Product

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "subcategories")

class SubCategoryType(DjangoObjectType):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "notes", "category")

class ProductType(DjangoObjectType):
    category = graphene.Field(CategoryType)
    class Meta:
        model = Product
        fields = ("id", "name", "sub_category")

    def resolve_category(self, info):
        return self.sub_category.category

class Query(graphene.ObjectType):
    categories = DjangoListField(CategoryType)
    subcategories = graphene.List(SubCategoryType)
    all_categories = graphene.List(CategoryType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    items = DjangoListField(ProductType, name=graphene.String(required=False))

    def resolve_subcategories(root, info):
        # We can easily optimize query count in the resolve method
        return SubCategory.objects.select_related("category").all()

    def resolve_all_categories(root, info, **kwargs):
        qs = Category.objects.all()
        return qs

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

    def resolve_items(root, info, **kwargs):
        name = kwargs.get('name', '')
        qs = Product.objects.all()
        if name:
            qs = qs.filter(name__icontains=name)
        return qs


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class SubCategoryForm(ModelForm):
    class Meta:
        model = SubCategory
        fields = ('name', 'category',)

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sub_category')

class CategoryMutation(DjangoModelFormMutation):
    """
    mutation {
        createCategory (input: {
            name: "Category Name"
        }) {
            category {
                id
                name
                subcategories {
                    id
                }
            }
        }
    }
    """
    category = graphene.Field(CategoryType)

    class Meta:
        form_class = CategoryForm

class SubCategoryMutation(DjangoModelFormMutation):
    """
    mutation {
        createSubcategory (input: {
            category: 1
            name: "Sub Category Name"
        }) {
            subCategory {
                id
                name
                category {
                    id
                    name
                }
            }
        }
    }
    """
    subcategory = graphene.Field(SubCategoryType)

    class Meta:
        form_class = SubCategoryForm

class ProductMutation(DjangoModelFormMutation):
    item = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm
        return_field_name = 'item'


class Mutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()
    create_subcategory = SubCategoryMutation.Field()
    create_item = ProductMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)