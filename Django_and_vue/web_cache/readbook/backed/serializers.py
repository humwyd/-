from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from account.models import *
from .models import *
from django.utils import timezone

# 注册的序列化
class RegSerializer(serializers.ModelSerializer):
    checkpass = serializers.CharField(max_length=256, write_only=True)
    # gender = serializers.CharField(max_length=256)

    class Meta:
        model = Account
        fields = ('username', 'password', 'checkpass', 'email')
        extra_kwargs = {'checkpass': {'required': False}}
    
    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        del attrs['checkpass']
        return attrs

# 这个用于login验证
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'password')

# book全部信息
class BookSerializer(serializers.ModelSerializer):
    # collections = CollectionSerializer(many=True,require = False)
    # avg_rating = serializers.SerializerMethodField('avg_rating_edit',required=False)
    class Meta:
        model = Book
        fields = ('__all__')
        extra_kwargs = {'collection':{'required':False}}
    


# collection全部信息，包括有哪些书
class CollectionSerializer(serializers.ModelSerializer):
    # books = BookSerializer(many=True, required = False, read_only=True)
    books=serializers.SerializerMethodField('book_list_edit',required=False)
    class Meta:
        model = Collection
        fields = ('id','name','user','books')
    
    def book_list_edit(self,obj):
        books_relation_set = Collection_Book.objects.filter(collection=obj.id)
        res=[]
        if(books_relation_set.exists()):
            for i in books_relation_set:
                temp=Book.objects.get(id=i.book.id)
                ser=BookSerializer(instance=temp)
                res.append(ser.data)
                res[-1]['join_time']=str(i.create_time)
                res[-1]['join_time']=res[-1]['join_time'][:10]
            res.sort(key=lambda i:i['join_time'],reverse=True)
            return res
        else:
            return res
         


# 这个用于访问用户账户页面以及添加图书等
class AccountDetailSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(many=True, required = False)
    class Meta:
        model = Account
        fields = ['id','username','email','gender','uimg','date_of_birth','join_date','collections']
        # fields = "__all__"
        # exclude = ('password',)

class OtherAccountDetailSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(many=True, required = False)
    class Meta:
        model = Account
        fields = ['username','collections']

# 评论的信息，
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id','content','user','book','like_count_num','create_time']

# 点赞信息，
class LikeItSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeIt
        fields = ('__all__')

# 打分信息
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('__all__')

# 每月目标

class MonthlyGoalBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('__all__')

# 每月记录
class MonthRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthRecord
        fields = ('__all__')

# 统计记录
class HistorySerializer(serializers.ModelSerializer):
    this_year_rec=serializers.SerializerMethodField('this_year_rec_edit',required=False)
    other_year_rec=serializers.SerializerMethodField('other_year_rec_edit',required=False)
    class Meta:
        model = Account
        fields=['id','username','this_year_rec','other_year_rec']
    
    def this_year_rec_edit(self,obj):
        time_now = timezone.now()
        this_year=time_now.year
        this_month = int(time_now.month)
        start_year=obj.join_date.year
        start_month = obj.join_date.month
        records={}
        if(this_year==start_year):
            for i in range(start_month,this_month+1):
                records[i]=[0,0]
        else:
            for i in range(1,this_month+1):
                records[i]=[0,0]
        # (0,0)-->(goal,accomplish)
        this_year_rec_set=MonthRecord.objects.filter(user=obj.id,year=this_year)
        if(this_year_rec_set.exists()):
            for i in this_year_rec_set:
                records[i.month][1]=i.total_nums
        this_year_goal_set = Goal.objects.filter(user=obj.id,year=this_year)
        if(this_year_goal_set.exists()):
            for i in this_year_goal_set:
                records[i.month][0]=i.target
        return {this_year:records}
    
    def other_year_rec_edit(self,obj):
        time_now = timezone.now()
        this_year=time_now.year
        start_year=obj.join_date.year
        records={}
        if(this_year==start_year):
            return {"other_year":records}
        for i in range(start_year,this_year):
            records[i]=[0,0]
        other_year_rec_set = MonthRecord.objects.filter(user=obj.id).exclude(year=this_year)
        if(other_year_rec_set.exists()):
            for i in other_year_rec_set:
                records[i.year][1]+=i.total_nums
        this_year_goal_set = Goal.objects.filter(user=obj.id).exclude(year=this_year)
        if(this_year_goal_set.exists()):
            for i in this_year_goal_set:
                records[i.year][0]+=i.target
        
        return {"other_year":records}



        
        


# 用户对哪些评论点赞了


# serializer = DeviceByTypeSerializer(device_type, many=True, context={'request': request})
# 书籍详细信息（包含打分，评论，点赞，赞数，评论排序按时间来）
class BookDetailPageSerializer(serializers.ModelSerializer):
    user_rating_review=serializers.SerializerMethodField('user_rating_review_edit',required=False)
    rating_analyse = serializers.SerializerMethodField('rating_analyse_edit',required=False)
    review_book =serializers.SerializerMethodField('review_edit',required=False)
    class Meta:
        model = Book
        fields = ['id','title','user_rating_review','rating_analyse','review_book']
    
    def user_rating_review_edit(self,obj):
        user_id = self.context['user_id']
        book_id = obj.id
        user_rating=0
        user_review=""
        rating_count_set = Rating.objects.filter(book=book_id,user=user_id)
        review_set = Review.objects.filter(book=book_id,user=user_id)
        if(rating_count_set.exists() and review_set.exists()):
            user_rating=rating_count_set[0].rating
            user_review=review_set[0].content
            return {"user_rating":user_rating, "user_review":user_review}
        elif(rating_count_set.exists()):
            user_rating=rating_count_set[0].rating
            return {"user_rating":user_rating, "user_review":user_review}
        elif(review_set.exists()):
            user_review=review_set[0].content
            return {"user_rating":user_rating, "user_review":user_review}
        else:
            return {"user_rating":user_rating, "user_review":user_review}

    def rating_analyse_edit(self,obj):
        user_id = self.context['user_id']
        book_id = obj.id
        rating_count_set = Rating.objects.filter(book=book_id)
        count_num=rating_count_set.count()
        five_nums=0
        four_nums=0
        three_nums=0
        two_nums=0
        one_nums=0
        five_percentage=0
        four_percentage=0
        three_percentage=0
        two_percentage=0
        one_percentage=0
        # 这一步获取了均分和评分人数
        # 以及各分段人数
        if(rating_count_set.exists()):
            for i in rating_count_set:
                if(i.rating==5):
                    five_nums+=1
                elif(i.rating==4):
                    four_nums+=1
                elif(i.rating==3):
                    three_nums+=1
                elif(i.rating==2):
                    two_nums+=1
                elif(i.rating==1):
                    one_nums+=1
            five_percentage=round(five_nums/count_num,3)
            four_percentage=round(four_nums/count_num,3)
            three_percentage=round(three_nums/count_num,3)
            two_percentage=round(two_nums/count_num,3)
            one_percentage=round(one_nums/count_num,3)
        return {"how_many_user_scored":count_num,'average_rating':obj.avg_rating,"five":five_percentage,"four":four_percentage,"three":three_percentage,"two":two_percentage,"one":one_percentage}


    def review_edit(self,obj):
        user_id = self.context['user_id']
        book_id = obj.id
        # 检索所有非当前用户的评论
        # exclude(user=user_id)
        review_set = Review.objects.filter(book=book_id)
        if(review_set.exists()):
            # 评论的主体
            rev_ser = ReviewSerializer(instance=review_set,many=True)
            res=[]
            for i in rev_ser.data:
                res.append(i)
            # 因为现在用户可以多评论了，所以需要单独搜索一个用户的集合
            review_user_info=[]
            for i in res:
                if(i['user'] not in review_user_info):
                    review_user_info.append(i)
            # 提前赋值为0
            for i in res:
                i['rating']=0

            user_rating_dict={}
            for i in review_user_info:
                rating_temp_set=Rating.objects.filter(user=i['user'],book=i['book'])
                if(rating_temp_set.exists()):
                    for j in rating_temp_set:
                        user_rating_dict[i['user']]=j.rating
            
            if(user_rating_dict!={}):
                for i in res:
                    # 给每一条评论加上分数。
                    if(i['user'] in user_rating_dict.keys()):
                        i['rating']=user_rating_dict[i['user']]

            like_status_set = LikeIt.objects.filter(user=user_id,belongto_book=book_id)
            like_status_list=[]
            # 获取所有用户点赞的评论的id
            if(like_status_set.exists()):
                for i in like_status_set:
                    if(i.status==True):
                        like_status_list.append(i.review.id)
            
            print(like_status_list)
            # 要让每条评论的obj包含当前用户是否处于点赞状态
            # 循环遍历列表，还会有个点过赞的列表
            for i in res:
                i['like_status']=0
                if(i['id'] in like_status_list):
                    i['like_status']=1
            
            # 按照时间顺序排列，最新的在上面
            res.sort(key=lambda i:i['create_time'],reverse=True)

            for i in res:
                i['create_time']=i['create_time'][:10]

            for i in res:
                i['user']=(Account.objects.get(id=i['user'])).username
            return res
        else:
            return [] 

#
class BookDetailPageNoUserSerializer(serializers.ModelSerializer):
    rating_analyse = serializers.SerializerMethodField('rating_analyse_edit',required=False)
    review_book =serializers.SerializerMethodField('review_edit',required=False)
    class Meta:
        model = Book
        fields = ['id','title','rating_analyse','review_book']
    
    def rating_analyse_edit(self,obj):
        book_id = obj.id
        rating_count_set = Rating.objects.filter(book=book_id)
        count_num=rating_count_set.count()
        five_nums=0
        four_nums=0
        three_nums=0
        two_nums=0
        one_nums=0
        five_percentage=0
        four_percentage=0
        three_percentage=0
        two_percentage=0
        one_percentage=0
        # 这一步获取了均分和评分人数
        # 以及各分段人数
        if(rating_count_set.exists()):
            for i in rating_count_set:
                if(i.rating==5):
                    five_nums+=1
                elif(i.rating==4):
                    four_nums+=1
                elif(i.rating==3):
                    three_nums+=1
                elif(i.rating==2):
                    two_nums+=1
                elif(i.rating==1):
                    one_nums+=1
            five_percentage=round(five_nums/count_num,3)
            four_percentage=round(four_nums/count_num,3)
            three_percentage=round(three_nums/count_num,3)
            two_percentage=round(two_nums/count_num,3)
            one_percentage=round(one_nums/count_num,3)
        return {"how_many_user_scored":count_num,'average_rating':obj.avg_rating,"five":five_percentage,"four":four_percentage,"three":three_percentage,"two":two_percentage,"one":one_percentage}
    
    def review_edit(self,obj):
        book_id = obj.id
        review_set = Review.objects.filter(book=book_id)
        if(review_set.exists()):
            # 评论的主体
            rev_ser = ReviewSerializer(instance=review_set,many=True)
            res=[]
            for i in rev_ser.data:
                res.append(i)
            # 因为现在用户可以多评论了，所以需要单独搜索一个用户的集合
            review_user_info=[]
            for i in res:
                if(i['user'] not in review_user_info):
                    review_user_info.append(i)
            
                        # 提前赋值为0
            for i in res:
                i['rating']=0

            user_rating_dict={}
            for i in review_user_info:
                rating_temp_set=Rating.objects.filter(user=i['user'],book=i['book'])
                if(rating_temp_set.exists()):
                    for j in rating_temp_set:
                        user_rating_dict[i['user']]=j.rating
            
            if(user_rating_dict!={}):
                for i in res:
                    # 给每一条评论加上分数。
                    if(i['user'] in user_rating_dict.keys()):
                        i['rating']=user_rating_dict[i['user']]
            
            # 要让每条评论的obj包含当前用户是否处于点赞状态
            # 循环遍历列表，还会有个点过赞的列表
            for i in res:
                i['like_status']=0
            
            # 按照时间顺序排列，最新的在上面
            res.sort(key=lambda i:i['create_time'],reverse=True)

            for i in res:
                i['create_time']=i['create_time'][:10]

            for i in res:
                i['user']=(Account.objects.get(id=i['user'])).username
            return res
        else:
            return [] 


#
class RecUserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user','book','rating']








