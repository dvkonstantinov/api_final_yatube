from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # group = SlugRelatedField(slug_field='slug',
    #                          queryset=Group.objects.all(), required=False)
    comments = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    text = serializers.CharField()

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    def validate_following(self, follower_name):
        user = self.context.get('request').user
        if user == follower_name:
            raise serializers.ValidationError('Вы не можете подписаться на '
                                              'самого себя')
        return follower_name

    class Meta:
        fields = ('user', 'following')
        model = Follow
