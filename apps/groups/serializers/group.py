from django.forms import model_to_dict
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from groups.models import Group, Room
from users.models import Comment


class GroupRoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')


class GroupListCommentModelSerializer(ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, obj: Comment):  # noqa
        return model_to_dict(obj.author, ('id', 'phone', 'first_name'))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author')


class GroupListModelSerializer(ModelSerializer):
    # course = SerializerMethodField()
    # teacher = SerializerMethodField()
    #
    # def get_course(self, obj: Group):  # noqa
    #     if obj.course:
    #         return model_to_dict(obj.course,
    #                              ('id', 'name', 'description', 'lesson_duration', 'course_duration', 'price'))
    #     return None
    #
    # def get_teacher(self, obj: Group):  # noqa
    #     if obj.teacher:
    #         return model_to_dict(obj.teacher, ('id', 'first_name', 'phone'))
    #     return None

    class Meta:
        model = Group
        fields = (
            'id', 'name', 'branch', 'days', 'room', 'status', 'course', 'teacher', 'start_date', 'end_date',
            'start_time',
            'end_time', 'students_count',
            'created_at', 'updated_at', 'tags')

    def to_representation(self, instance: Group):
        data = super().to_representation(instance)
        data['students_count'] = instance.students_count
        data['course'] = model_to_dict(instance.course,
                                       ('id', 'name', 'description', 'lesson_duration', 'course_duration', 'price'))
        data['teacher'] = model_to_dict(instance.teacher, ('id', 'first_name', 'phone'))
        data['rooms'] = GroupRoomListModelSerializer(instance.room).data
        data['comment'] = GroupListCommentModelSerializer(instance.comment, many=True).data
        return data


class GroupAddStudentModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = 'start_date',
