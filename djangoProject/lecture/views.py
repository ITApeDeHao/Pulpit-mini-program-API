import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from lecture.models import UniversityLecture
from lecture.serializer import LectureSerializer
# Create your views here.

class Lecture(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        page = LimitOffsetPagination()
        page.page_size = request.query_params.get('limit')
        lecture_set = UniversityLecture.objects.filter(course_data__gt=str(time.time()))
        result_set = page.paginate_queryset(lecture_set[::-1],request,self)
        result = LectureSerializer.LectureSerializer(instance=result_set,many=True)
        print(result.data)
        return Response({"Status":True,"message":result.data,"num":len(lecture_set)})