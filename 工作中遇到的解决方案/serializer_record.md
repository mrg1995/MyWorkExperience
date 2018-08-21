#Serializer 序列化器

- 序列化器   (序列化器,以及各种字段实际上是Python中的描述符,这也就解释了嵌套序列化的原理)

  - 序列化    

    ```
    # 将对象序列化成Python对象
    obj = User.objects.get(id=1)
    serializer = serializer1(instance=obj[,many=True])
    response_data = serializer.data  # 序列化出来的对象 ,一般直接就可以response

    #如果要进行修改
    response_data["status"] == True
    response_data["msg"] == "查找成功"
    ```

  - 反序列化

    ```
    # 将Python对象反序列化
    serializer = serializer1(data=request.data)
    serializer.is_valid(raise_exception=True)  # 将serializer对象进行验证  
    serializer.valideted_data   # 验证过滤后serializer对象
    serializer.save()
    ```

- 情况1 某个字段  不要前端传入  后端自动生成数值   

  - 将该字段设置成read_only    (这样序列化器会过滤掉前端传回的该字段数据)
  - 重写validate函数, 将你要生成数值的逻辑写入即可

  创建店铺时  生成店铺专属key

  ```
  import uuid
  import hashlib
  from django.conf import settings
  from rest_framework import serializers
  from shop.models import Shop

  def getKey():
      '''
      生成店铺唯一标志
      :return: 返回hash值
      '''
      hash = hashlib.md5(settings.SECRET_KEY.encode())
      hash.update(str(uuid.uuid1()).encode())
      return hash.hexdigest()

  class ShopSerializer(serializers.ModelSerializer):
      shopKey = serializers.CharField(max_length=50, read_only=True)
      isDelete = serializers.HiddenField(default=False, write_only=True)

      def validate(self, attrs):
          attrs['shopKey'] = getKey()
          return attrs

      class Meta:
          model = Shop
          fields = '__all__'
  ```

  ​