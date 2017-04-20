from rest_framework import serializers

from users.models import Profile


class GenderAgeBaseSerializer(serializers.Serializer):
    count_males = Profile.objects.filter(gender=Profile.GENDER_MALE).count()
    count_females = Profile.objects.filter(
        gender=Profile.GENDER_FEMALE).count()
    count_all = count_males + count_females


class GenderStatSerializer(GenderAgeBaseSerializer):
    male_percentage = serializers.SerializerMethodField()
    female_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('gender',)

    def get_male_percentage(self):
        return 100 * float(self.count_males)/float(self.count_all)

    def get_female_percentage(self):
        return 100 * float(self.count_females)/float(self.count_all)


class ProfileStatSerializer(serializers.ModelSerializer):
    gender = GenderStatSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
