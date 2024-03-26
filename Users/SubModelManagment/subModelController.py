from ..serializers import SubModelSerializer

def createSubmodel(subModelData):
    serializer = SubModelSerializer(data=subModelData)
    serializer.is_valid(raise_exception=True)
    serializer.save()