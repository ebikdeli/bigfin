"""
To have a independent app, we defined our Generic serailizer here too.
We are following this document to define serializer for Generic serailizer:
https://www.django-rest-framework.org/api-guide/relations/#generic-relationships
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import FileUpload, Ticketing, Answer


class FileUploadRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `FileUpload_object` generic relationship.
    """
    def to_representation(self, value):
        if isinstance(value, Ticketing):
            serializer = TicketingSerializer(value)
        elif isinstance(value, Answer):
            serializer = AnswerSerializer(value)
        else:
            return {'error': 'This object is not Json serializer'}
        return serializer.data


# class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for FileUpload"""
    # url = serializers.HyperlinkedIdentityField(view_name='some view')
    content_object = FileUploadRelatedField(read_only=True)
    class Meta:
        model = FileUpload
        fields = '__all__'


# class TicketingSerializer(serializers.HyperlinkedModelSerializer):
class TicketingSerializer(serializers.ModelSerializer):
    """Serializer for Ticketing."""
    # url = serializers.HyperlinkedIdentityField(view_name='some view')

    class Meta:
        model = Ticketing
        fields = '__all__'


# class AnswerSerializer(serializers.HyperlinkedModelSerializer):
class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for Answer model
    https://www.django-rest-framework.org/api-guide/fields/#write_only
    """
    # url = serializers.HyperlinkedIdentityField(view_name='some view')
    """
    # This field used for ListField
    files = serializers.ListField(
                                  child=serializers.FileField(
                                                              max_length=100000,
                                                              allow_empty_file=False,
                                                              use_url=False)
                                 )
    """
    # file = serializers.FileField()
    # caption = serializers.CharField()
    # files = FileUploadRelatedField(queryset=FileUpload.objects.all())
    ticketing = TicketingSerializer(read_only=True)
    ticketing_obj = serializers.PrimaryKeyRelatedField(queryset=Ticketing.objects.all(),
                                                       many=False,
                                                       write_only=True,
                                                       allow_null=True)
    ticket_id = serializers.UUIDField(write_only=True,
                                      allow_null=True,
                                      help_text='For client_server architecture method')

    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):
        """Overriding 'create' method to support methods to create Answer object with DRF GUI or from
        client side technologies"""
        # 1- Create Answer with standard DRF GUI:
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            answer = Answer.objects.create(**validated_data)
            return answer

        # 2- Create Answer with ticket_id (client-server architecture)
        ticket_id = validated_data.pop('ticket_id', None)
        if ticket_id:
            queryset = Ticketing.objects.filter(ticket_id=ticket_id)
            if queryset.exists():
                ticketing = queryset.first()
                validated_data.update({'ticketing': ticketing})
                answer = Answer.objects.create(**validated_data)
                return answer
            else:
                raise ValidationError(detail=f'No ticket found with this id: {ticket_id}')

        raise ValidationError(detail={'error': 'No Ticket found'}, code=HTTP_400_BAD_REQUEST)
    
    def update(self, instance, validated_data):
        # 1- Update Answer with standard DRF GUI:
        ticketing_obj = validated_data.pop('ticketing_obj', None)
        if ticketing_obj:
            validated_data.update({'ticketing': ticketing_obj})
            Answer.objects.filter(id=instance.pk).update(**validated_data)
            # https://docs.djangoproject.com/en/4.0/ref/models/instances/#django.db.models.Model.refresh_from_db
            instance.refresh_from_db()
            return instance

        # 2- Update Answer with ticket_id (client-server architecture)
        ticket_id = validated_data.pop('ticket_id', None)
        if ticket_id:
            queryset = Ticketing.objects.filter(ticket_id=ticket_id)
            if queryset.exists():
                ticketing = queryset.first()
                validated_data.update({'ticketing': ticketing})
                Answer.objects.filter(id=instance.pk).update(**validated_data)
                instance.refresh_from_db()
                return instance
            else:
                raise ValidationError(detail=f'No ticket found with this id: {ticket_id}')

        raise ValidationError(detail={'error': 'No Ticket found'}, code=HTTP_400_BAD_REQUEST)

    """
    # This method used for ListField
    def create(self, validated_data):
        files=validated_data.pop('files')
        answer=Answer.objects.create(**validated_data)
        for f in files:
            file=FileUpload.objects.create(f)
            answer.files.add = file
        answer.save()
        return answer
    """