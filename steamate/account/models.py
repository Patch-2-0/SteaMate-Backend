from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.

class Genre(models.Model):
    genre_name = models.CharField(max_length=50, unique=True)
    
class Game(models.Model):
    appid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

class User(AbstractUser):
    
    class GenderChoices(models.IntegerChoices):
        남 = 1, "남"
        여 = 2, "여"
        공개안함 = 3, "공개 안 함"
    
    nickname = models.CharField(max_length=50, unique=True)
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='필수. 20자 이하. 문자, 숫자 및 @/./+/-/_만 가능.', max_length=20, unique=True, validators=[UnicodeUsernameValidator(), MinLengthValidator(5)], verbose_name='username')
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to='user/profile_image/',
        default='user/profile_image/user_default_image.png')
    gender = models.IntegerField(choices = GenderChoices.choices, default=GenderChoices.공개안함)
    birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    steam_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    verification_expires_at = models.DateTimeField(default=now)
    # steam 관련 정보 추가
    steam_name = models.CharField(max_length=50, blank=True, null=True)
    steam_profile_url = models.URLField(blank=True, null=True)
    steam_avatar = models.URLField(blank=True, null=True)
    is_syncing = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """
        is_verified 값이 변경되면 is_active도 동기화
        처음 생성이 될 때, 이메일 인증 만료 시간을 10분 뒤로 설정
        """
        if not self.pk:
            self.verification_expires_at=now() + timedelta(minutes=10)
        self.is_active = self.is_verified
        super().save(*args, **kwargs)
    
    def is_verification_expired(self):
        """ 이메일 인증이 만료되었는지 확인하는 함수 """
        return not self.is_verified and now() > self.verification_expires_at


class UserLibraryGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    playtime = models.IntegerField(default=0, help_text="단위: 분")
    
    class Meta:
        unique_together = ('user', 'game')
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.playtime}분)"

class UserPreferredGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferred_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'game')

    def save(self, *args, **kwargs):
        if not UserLibraryGame.objects.filter(user=self.user, game=self.game).exists():
            raise ValueError("이 게임은 유저의 라이브러리에 없습니다.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

class UserPreferredGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferred_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} - {self.genre.genre_name}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GameTag(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('game', 'tag')
    
    def __str__(self):
        return f"{self.game.title} - {self.tag.name}"

class UserPreferredTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferred_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'tag')
    
    def __str__(self):
        return f"{self.user.username} - {self.tag.name}"
