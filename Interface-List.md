# Interface

## Register

### GET

 Obtain the verification code

Method ：get

Path：user/register/phoneCode\?Phone="Phone"

Params：Phone

Result：Success：{"status": True, "message": "生成成功", "Code": Code} json

​					Failed：{"status": False, "message": ser.errors}/{"status": False, "Phone": Phone, "message": "用户已存在"}

### POST

Send data to the back end

Method：post

Path：user/register/phoneCode/

Params：Phone(required) Password(required) Code(required)

Result：Success：{"status": True, "message": "创建成功","Phone":Phone, "PassWord": PassWord} json

​					Failed：{"status": False, "message": ser.errors}

## Password Landing

### POST

Method：post

Path：user/login/password/

Params：Phone(required) Password(required)

Result：Success：{"status": True, "message": "登陆成功", "Phone": Phone, "token": token}} json

​					Failed：{"status": False, "message": "密码错误"}/{"status": False, "message": ser.errors}

## Mobile verification code login

### GET

Method：get

Path：user/login/phone/?Phone="Phone"

Params：Phone

Result：Success：{“status”: True,“message”: “发送成功”, “Code”: Code} json

​					Faild：{“status”: False, “message”: “手机格式错误”}/{“status”: False, “message”: “短信发送失败”}

### POST

Method：post

Path：user/login/phone/

Params：Phone(required) Code(required) 

Result：Success：{"status": True, "Phone": Phone, "token": user.token} json

​					Faild：{"status": False, "message": ser.errors}

## Forgot password

### GET

Method：get

Path：/user/forget/passwordchange//?Phone=“Phone”

Params：Phone(required) 

Result：Success：{"status": True, "message": "发送成功", "Code": Code}json

​					Faild：{"status": False, "message": "短信发送失败"}/{"status": False, "message": ser.errors}

### Upload

Method：put

Path：/user/forget/passwordchange/

Params：Phone(required) Code(required) Password(required)

Result：Success：{"status": True, "message": "修改成功" , "Phone": Phone,"Password":PassWord} json

​					Faild：{"status": False, "message": ser.errors}



## Change your password

Method：put

Path：/user/change/

Params：Phone(required) OldPassWord(required) NewPassWord(required)

Result：Success：{“status”: True, “message”: “修改成功” , “Password”:PassWord} json

​					Failed：{ "Status": false,  "message": "密码错误"}

## like

Method：put

Path：/postbar/like/pid

Params：pid

Result：{} json

## Posted

Method：post

Path：/postbar/

Params：ptitle(required), pwriter(required), pcontent(required)

Result：{pid, "ptitle", "pwriter", "pcontent"} json

## Comment

Method：post

Path：/postbar/pid

Params：pid(required),preview(required)

Result：{rid, "pid", "preview"} json

## Delete A Post

Method：delete

Path：/postbar/del/pid

Params：pid

Result：{"message":ok} json

## Modify A Post

Method：put 

Path：/postbar/up/pid

Params：ptitle, pcontent, pid

Result：{"pid", "ptitle", "pwriter", "pcontent"} json

## Collect

Method：post

Path：/postbar/collect/pid

Params：uid pid

Result：{"message":ok} json

## Get all posts

Method：get

Path：/index/postbar/

Params：

Result：[{pid, ptitle, pwriter, pcontent}] 

## Get a single post

Method：get

Path：/index/postbar/pid

Params：pid

Result：{pid, ptitle, pwriter, pcontent}json

## Get comments

Method：get

Path：/index/postbar/pid

Params：pid

Result：[{pid, rid, preview}]