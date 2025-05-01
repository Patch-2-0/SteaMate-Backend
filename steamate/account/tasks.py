from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import UserPreferredGame, User, UserLibraryGame
from .utils import get_or_create_game, get_or_create_genre, fetch_steam_library
from django.db import transaction, IntegrityError
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email(subject, text_content, html_content, to_email):
    email = EmailMultiAlternatives(subject, text_content, None, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()


@shared_task
def fetch_and_save_user_games(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_syncing = True
        user.save()
    except User.DoesNotExist:
        logger.error(f"User does not exist (user_id: {user_id})")
        user.is_syncing = False
        user.save()
        return {"status": "error", "message": "사용자가 존재하지 않습니다."}

    logger.info(f"Steam 라이브러리 가져오기 요청 시작 (Steam id : {user.steam_id})")

    appids, titles, playtimes = fetch_steam_library(user.steam_id)

    if not appids:
        logger.warning(f"Steam 라이브러리 불러오기 실패 또는 빈 데이터 (steam_id: {user.steam_id})")
        user.is_syncing = False
        user.save(update_fields=["is_syncing"])
        return {"status": "error", "message": "Steam 라이브러리가 비어있거나, 프로필이 비공개 상태입니다."}

    try:
        with transaction.atomic():
            current_game_ids = []

            for i in range(len(appids)):
                game = get_or_create_game(appid=appids[i])
                if not game:
                    logger.warning(f"게임 정보를 가져오지 못함 (appid: {appids[i]})")
                    continue

                # 업데이트 또는 생성
                UserLibraryGame.objects.update_or_create(
                    user=user,
                    game=game,
                    defaults={"playtime": playtimes[i]}
                )

                # game이 None이 아닐 때만 추가
                current_game_ids.append(game.appid)

            if current_game_ids:
                UserLibraryGame.objects.filter(user=user).exclude(game_id__in=current_game_ids).delete()

    except IntegrityError as e:
        logger.error(f"UserLibraryGame 생성 오류: {str(e)}")
        user.is_syncing = False
        user.save()
        return {"status": "error", "message": "게임 데이터 저장 중 오류 발생"}

    user.is_syncing = False
    user.save()
    return {"status": "success", "message": "라이브러리 저장 완료"}


@shared_task
def delete_expired_unverified_users():
    expired_users = User.objects.filter(is_verified=False, verification_expires_at__lt=now())
    count, _ = expired_users.delete()
    return f"{count}명의 만료된 유저 삭제됨"

@shared_task
def send_token_mail(token, email):
    subject = "[SteaMate] 비밀번호 재설정 인증번호"
    text_content = f"""인증번호 : {token}
    
    3분 내에 입력해주세요."""
    html_content = f"""
    <html>
      <body>
        <p><strong>인증번호 : {token}</strong><br>
        3분 내에 입력해주세요.</p>
      </body>
    </html>
    """
    email_message = EmailMultiAlternatives(subject, 'text_content', None, [email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()