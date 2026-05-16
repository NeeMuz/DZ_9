import graphene
from graphene_django import DjangoObjectType
from .models import Article, Category, Tag


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "image",
            "category",
            "tags",
            "created_date",
        )


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        category_id = graphene.ID(required=False)
        tag_ids = graphene.List(graphene.ID, required=False)

    article = graphene.Field(ArticleType)

    @classmethod
    def mutate(cls, root, info, title, content, category_id=None, tag_ids=None):
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None

        article = Article.objects.create(
            title=title,
            content=content,
            category=category,
        )

        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            article.tags.set(tags)

        return CreateArticle(article=article)


class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType)
    article = graphene.Field(ArticleType, id=graphene.ID(required=True))

    def resolve_all_articles(root, info):
        return Article.objects.all()

    def resolve_article(root, info, id):
        return Article.objects.get(id=id)


class Mutation(graphene.ObjectType):
    create_article = CreateArticle.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
