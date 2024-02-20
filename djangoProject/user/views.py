from uuid import uuid4

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from forum.models import ForumForummsg
from user import models
from forum.serializers.IntroSerializer import IntroSerializer
from user.serializer.validate import CreateCode, MobileCodeSend
from user.serializer.account import MobileNumberserializer, Codeserializer, PassWordserializer, RecommendSerializer


# Create your views here.
# 用户注册
class PhoneRegister(APIView):
    def get(self, request, *args, **kwargs):
        """
        注册用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        ser = MobileNumberserializer(data={"Phone": request.query_params.get("Phone")})
        # 2.验证手机号格式
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 3.生成验证码
        Code = CreateCode()
        # 4. 保存手机号和验证码
        conn = get_redis_connection()
        conn.set(ser.validated_data.get("Phone"), Code, ex=60)
        # 5. 发送验证码
        if not MobileCodeSend("1484768", ser.validated_data.get("Phone"), Code):
            return Response({"status": False})
        return Response({"status": True, "message": "生成成功", "Code": Code})

    def post(self, request, *args, **kwargs):
        """
               手机号验证码验证结果
               :param request:
               :param args:
               :param kwargs:
               :return:
               """
        # 1.获取手机号和验证码
        ser = Codeserializer(data=request.data)
        # 2.验证手机号格式
        # 3.验证手机号、验证码是否匹配及超时
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 4.保存用户名、密码
        user = models.UserInfo.objects.create(Phone=ser.validated_data.get("Phone"),
                                              PassWord=ser.validated_data.get("PassWord"), token=str(uuid4()),
                                              UserName="hhhh1234")
        user.save()
        return Response({"status": True, "message": "创建成功", "Phone": ser.validated_data.get("Phone"),
                         "PassWord": ser.validated_data.get("PassWord")})


# 手机号密码登陆
class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        """
        密码登陆方法
        :param request:
        :return:
        """
        # 1.获取手机号、密码
        ser = PassWordserializer(data=request.data)
        # 2.校验手机号
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 3.校验密码
        user = models.UserInfo.objects.get(Phone=ser.validated_data.get("Phone"))
        # 4.返回结果
        user.token = str(uuid4())
        user.save()
        if ser.validated_data.get("PassWord") != user.PassWord:
            return Response({"status": False, "message": "密码错误"})
        return Response({"status": True, "message": "登陆成功",
                         "Phone": user.Phone, "token": user.token, "UserName": user.UserName,
                         "user_id": user.ID, 'resume': user.resume,
                         "AttentionNum": user.attentionnum})


# 手机号验证码登陆
class PhoneLogin(APIView):
    def get(self, request, *args, **kwargs):
        """
        手机号发送验证码
        :param args:
        :param kwargs:
        :param request:
        :return:
        """
        # 1.获取手机号和验证码信息
        ser = MobileNumberserializer(data={"Phone": request.query_params.get("Phone")})
        # 2.核验手机号
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 3.生成验证码
        try:
            user = models.UserInfo.objects.get(Phone=ser.data.get("Phone"))
            Code = CreateCode()
            # 4.验证码发送到手机
            if not MobileCodeSend("1484903", ser.data.get("Phone"), Code):
                return Response({"status": False, "message": "短信发送失败"})
            # 5.保存验证码
            # 5.1 搭建redis服务器(云redis)
            # 配置
            conn = get_redis_connection()
            conn.set(ser.data.get("Phone"), Code, ex=60)
            # .返回验证码信息
            return Response({"status": True, "Code": Code, "message": "发送成功"})
        except:
            return Response({"status": False, "message": "用户不存在"})

    def post(self, request, *args, **kwargs):
        """
        手机号验证码验证结果
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号和验证码
        ser = Codeserializer(data=request.data)
        # 2.验证手机号格式和验证码
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        user = models.UserInfo.objects.get(Phone=ser.validated_data.get("Phone"))
        user.token = uuid4()
        user.save()
        return Response({"status": True, "message": "登陆成功",
                         "Phone": user.Phone, "token": user.token, "UserName": user.UserName,
                         "user_id": user.ID, 'resume': user.resume,
                         "AttentionNum": user.attentionnum})


# 用户忘记密码
class ForgetPassword(APIView):
    def get(self, request, *args, **kwargs):
        """
        获取忘记密码验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        ser = MobileNumberserializer(data=request.data)
        # 2.验证手机号格式
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 3.生成验证码
        Code = CreateCode()
        # 4. 保存手机号和验证码
        conn = get_redis_connection()
        conn.set(ser.validated_data.get("Phone"), Code, ex=60)
        # 5. 发送验证码
        if not MobileCodeSend("1484902", ser.validated_data.get("Phone"), Code):
            return Response({"status": False, "message": "短信发送失败"})
        return Response({"status": True, "message": "生成成功", "Code": Code})

    def put(self, request, *args, **kwargs):
        """
               手机号验证码验证结果
               :param request:
               :param args:
               :param kwargs:
               :return:
               """
        # 1.获取手机号和验证码
        ser = Codeserializer(data=request.data)
        # 2.验证手机号格式
        # 3.验证手机号、验证码是否匹配及超时
        if not ser.is_valid():
            return Response({"status": False, "message": ser.errors})
        # 4.更新密码
        # Todo Update()
        user = models.UserInfo.objects.get(Phone=ser.validated_data.get("Phone"))
        user.PassWord = ser.validated_data.get("PassWord")
        user.token = uuid4()
        user.save()
        return Response({"status": True, "message": "修改成功", "Phone": ser.validated_data.get("Phone"),
                         "Password": ser.validated_data.get("PassWord"), "token": user.token,
                         "UserName": user.UserName})


# 用户修改密码
class ChangePassWord(APIView):
    def put(self, request, *args, **kwargs):
        Phone = request.data.get("Phone")
        OldPassWord = request.data.get("OldPassWord")
        NewPassWord = request.data.get("NewPassWord")
        user = models.UserInfo.objects.get(Phone=Phone)
        if OldPassWord != user.PassWord:
            return Response({"Status": False, "message": "密码错误"})
        user.PassWord = NewPassWord
        user.token = uuid4()
        user.save()
        return Response({"Status": True, "message": "修改成功", "token": user.token, "UserName": user.UserName})


# 用户进行实名认证
class NameAuthenticate(APIView):
    def put(self, request, *args, **kwargs):
        Token = request.data.get("Token")
        Name = request.data.get("Name")
        UserNum = request.data.get("UserNum")
        try:
            user = models.UserInfo.objects.get(token=Token)
        except:
            return Response({"Status": 0, "message": "登录信息有误"})


# 关注
class Attention(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        """
        添加/取消关注
        :param request: request.data.func(0(取消关注),1(关注))
        :param args:
        :param kwargs:
        :return:
        """
        status = request.data.get('func')
        if status == 1:
            token = request.data.get('token')
            attention_id = request.data.get('attention_id')
            try:
                user = models.UserInfo.objects.get(token=token)
                attention_user = models.UserInfo.objects.get(ID=attention_id)
                if user.ID == attention_user.ID:
                    return Response({"Status": False, 'message': "不可以关注自己哦"})
                try:
                    models.UserAttention.objects.get(user_id=user.ID, attention_id=attention_user.ID,
                                                     attention_status=1)
                    return Response({"Status": False, "message": "请勿重复关注"})
                except:
                    try:
                        attention = models.UserAttention.objects.get(user_id=user.ID, attention_id=attention_user.ID,
                                                                     attention_status=0)
                        attention.attention_status = 1
                        attention.save()
                    except:
                        attention = models.UserAttention.objects.create(user_id=user.ID, attention_id=attention_user.ID,
                                                                        attention_status=1)
                        attention.save()
                    finally:
                        return Response({"Status": True, "message": "关注成功"})
            except:
                return Response({"Status": False, "message": "请先登录哦"})
        elif status == 0:
            token = request.data.get('token')
            attention_id = request.data.get('attention_id')
            user = models.UserInfo.objects.get(token=token)
            attention_user = models.UserInfo.objects.get(ID=attention_id)
            try:
                attention = models.UserAttention.objects.get(user_id=user.ID, attention_id=attention_user.ID)
                attention.attention_status = 0
                attention.save()
                return Response({"Status": True, "message": "取消关注成功"})
            except:
                return Response({"Status": False, "message": "您还未关注"})

    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token")
        user = models.UserInfo.objects.get(token=token)
        attentions = models.UserAttention.objects.filter(user_id=user.ID, attention_status=1)
        result = []
        if not attentions:
            return Response({"Status": True, "message": "该用户无关注"})
        for attention in attentions:
            user = models.UserInfo.objects.get(ID=attention.attention_id)
            result.append({
                "UserName": user.UserName,
                "resume": user.resume,
                'user_id': user.ID
            })
        return Response({"Status": True, "message": result})


# 推荐的人
class Recommend(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        page = LimitOffsetPagination()
        page.page_size = request.query_params.get('limit')
        userset = models.UserInfo.objects.filter(grade__gte=5)
        res_pag = page.paginate_queryset(userset[::-1], request, self)
        results = RecommendSerializer(instance=res_pag, many=True)
        msg = []
        for data in results.data:
            msg.append({
                "user_id": data.get("ID"),
                "user_name": data.get("UserName"),
                "is_attention": "",
                'resume': data.get('resume')
            })
        return Response({"result": msg, 'num': len(msg)})


# 未完成的
# 修改用户名
class ChangeUserName(APIView):
    def put(self, request, *args, **kwargs) -> Response:
        UserName = request.data.get('UserName')
        resume = request.data.get('resume')
        token = request.data.get('token')
        if not token:
            return Response({"Status": 0, "message": "用户未登录"})
        try:
            user = models.UserInfo.objects.get(token=token)
            if UserName:
                user.UserName = UserName
            if resume:
                user.resume = resume
            user.save()
            return Response({"Status": 1, "message": "修改成功"})
        except:
            return Response({"Status": 0, "message": "登录信息有误"})


# 展示个人主页面
class Personal(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        user_id = request.query_params.get('user_id')
        try:
            user = models.UserInfo.objects.get(ID=user_id)
            forumset = ForumForummsg.objects.filter(user_id=user_id)
            result = IntroSerializer(instance=forumset, many=True)
            return Response({
                "Status": True,
                "message": {
                    "UserName": user.UserName,
                    "data":result.data
                }
            })
        except:
            return Response({"Status": False, "message":"该用户不存在"})
