import time

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
# Create your views here.

from forum.models import ForumForummsg, ForumSpot, ForumComment
from user.models import UserInfo

from forum.serializers import IntroSerializer


class GetIntro(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        user_id = request.query_params.get('user_id')
        page = LimitOffsetPagination()
        page.page_size = request.query_params.get('limit')
        forumset = ForumForummsg.objects.all()
        if user_id:
            forumset = ForumForummsg.objects.filter(user_id=user_id)
        try:
            ret_page = page.paginate_queryset(forumset[::-1], request, self)
            result = IntroSerializer.IntroSerializer(instance=ret_page, many=True)
            msg = []
            try:
                for data in result.data:
                    user = UserInfo.objects.get(ID=data.get('user_id'))
                    msg.append({
                        "intro": data.get("intro"),
                        "forum_id": data.get("forum_id"),
                        "time": data.get('time'),
                        "UserName": user.UserName
                    })
                return Response({"Status": 1, "message": msg, "num":len(forumset)})
            except:
                return Response({"Status": 1, "message": "查询错误"})
        except:
            return Response({"Status": 1, "message": "数据不存在"})


class Forum(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        token = request.data.get('token')
        forum = request.data.get('forum')
        intro = request.data.get('intro')
        try:
            user = UserInfo.objects.get(token=token)
            date = str(time.time())  # 时间戳
            result = ForumForummsg.objects.create(user_id=user.ID, forum_msg=forum, intro=intro, time=date)
            result.save()
            return Response({"Status": 1, "message": "发布成功", "forum_id": result.forum_id})
        except:
            return Response({"Status": 0, "message": "发布失败"})

    def get(self, request, *args, **kwargs) -> Response:
        user_id = request.query_params.get('user_id')
        forum_id = request.query_params.get('forum_id')
        flag = 0
        if user_id:
            try:
                spot = ForumSpot.objects.get(spot_user_id=user_id, spot_forum_id=forum_id)
                flag = spot.spot_status
            except:
                flag = 0
        try:
            forum = ForumForummsg.objects.get(forum_id=forum_id)
            forum.pageview += 1
            forum.save()
            user = UserInfo.objects.get(ID=forum.user_id)
            return Response({
                "Status": 1,
                "message": {
                    "user_id": user.ID,
                    "UserName": user.UserName,
                    "forum": forum.forum_msg,
                    "intro": forum.intro,
                    "time": forum.time,
                    "forum_id": forum.forum_id,
                    "pageview": forum.pageview,
                    "spot": forum.spot,
                    "spot_status": flag
                }
            })
        except:
            return Response({"Status": 0, "message": "未找到文章"})


class Spot(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        forum_id = request.data.get('forum_id')
        user_id = request.data.get('user_id')
        try:
            spot = ForumSpot.objects.get(spot_user_id=user_id, spot_forum_id=forum_id)
            spot.spot_status = 0 if spot.spot_status else 1
            forum = ForumForummsg.objects.get(forum_id=forum_id)
            forum.spot += 1 if spot.spot_status else -1
            forum.save()
            spot.save()
            return Response({
                "Status": True,
                "message": "点赞成功" if spot.spot_status else "取消点赞成功",
                "data": forum.spot
            })
        except:
            ForumSpot.objects.create(spot_user_id=user_id, spot_forum_id=forum_id).save()
            forum = ForumForummsg.objects.get(forum_id=forum_id)
            forum.spot += 1
            forum.save()
            return Response({
                "Status": True,
                "message": "点赞成功",
                "data": forum.spot
            })


class Comment(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """获取评论"""
        forum_id = request.query_params.get('forum_id')
        page = LimitOffsetPagination()
        page.page_size = request.query_params.get('limit')
        parent_id = request.query_params.get('parent_id')
        commentset = ForumComment.objects.filter(forum_id=forum_id, parent_id=parent_id if parent_id else None)
        try:
            ret_page = page.paginate_queryset(commentset[::-1], request, self)
            result = IntroSerializer.CommentSerializer(instance=ret_page, many=True)
            msg = []
            for data in result.data:
                user = UserInfo.objects.get(ID=data.get('user_id'))
                msg.append({
                    'comment_id': data.get('comment_id'),
                    "user_id": user.ID,
                    "UserName": user.UserName,
                    "content": data.get('content'),
                    'time': data.get('time')
                })
            return Response({"Status": True, "message": msg, "num":len(commentset)})
        except:
            return Response({"Status": False, "message": "暂无评论"})

    def post(self, request, *args, **kwargs) -> Response:
        """回复/发布评论"""
        parent_id = request.data.get('parent_id') if request.data.get('parent_id') else None
        forum_id = request.data.get('forum_id')
        user_id = request.data.get('user_id')
        content = request.data.get('content')
        date = str(time.time())
        try:
            comment = ForumComment.objects.create(forum_id=forum_id, user_id=user_id, content=content,
                                                  parent_id=parent_id, time=date)
            comment.save()
            return Response({"Status": True, "message": {
                'comment_id': comment.comment_id,
                "user_id": comment.user_id,
                "UserName": UserInfo.objects.get(ID=comment.user_id).UserName,
                "content": comment.content,
                'time': comment.time
            }
                             })
        except:
            return Response({"Status": False, "message": "评论失败，请重新评论"})
