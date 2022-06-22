from flask_login import login_required
from ..model import db, User, Manga, Likes
from flask import Blueprint, render_template, request, flash
from sqlalchemy import func
from .form import AboutMeForm

user = Blueprint('user', __name__)
SortTypeDict = {"1": "desc", "2": "desc", "3": "desc", "4": "desc"}


def SelfUrlContent(user_data, SortType=None):
    global SortTypeDict
    # 子查詢 先篩出所有mid的數量
    group_data = Likes.query.with_entities(Likes.mid, func.count(Likes.mid).label('total')).group_by(Likes.mid).subquery()

    # 此人上傳的
    # 把子查詢直接join 要用c去on https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.FromClause.c
    upload = Manga.query.with_entities(Manga.name, group_data.c.total, Manga.update_time).filter_by(insert_user=user_data.username).join(group_data, Manga.mid == group_data.c.mid, isouter=True)
    # print(upload)

    # 此人按讚的
    # 先查自己的like紀錄再關聯manga最後在連結子查詢
    liked = Likes.query.join(User, User.id == Likes.user_id, isouter=True).filter_by(account=user_data.account).with_entities(group_data.c.total, Manga.name, Manga.update_time) \
        .join(Manga, Likes.mid == Manga.mid, isouter=True).join(group_data, Manga.mid == group_data.c.mid, isouter=True)
    # print(liked)

    # 排序條件
    if SortType:
        if SortTypeDict[SortType] == "asc":
            SortTypeDict[SortType] = "desc"
            if SortType == "1":
                upload = upload.order_by(group_data.c.total.asc())
            elif SortType == "2":
                upload = upload.order_by(Manga.update_time.asc())
            elif SortType == "3":
                liked = liked.order_by(group_data.c.total.asc())
            else:
                liked = liked.order_by(Manga.update_time.asc())
        else:
            SortTypeDict[SortType] = "asc"
            if SortType == "1":
                upload = upload.order_by(group_data.c.total.desc())
            elif SortType == "2":
                upload = upload.order_by(Manga.update_time.desc())
            elif SortType == "3":
                liked = liked.order_by(group_data.c.total.desc())
            else:
                liked = liked.order_by(Manga.update_time.desc())
    # HomePage會進來這
    else:
        upload = upload.order_by(Manga.update_time.desc())
        liked = liked.order_by(Manga.update_time.desc())

    return upload, liked


@user.route("/user/<string:account>", methods=['GET', 'POST'])
@login_required
def HomePage(account):
    form = AboutMeForm()
    avatar_base64 = request.form.get('avatar_base64', '')
    if avatar_base64:
        now_user = User.query.filter_by(account=account).first()
        # now_user = User.query.filter_by(id=current_user.id).first()
        now_user.avatar_hash = avatar_base64
        db.session.commit()
        flash("Update Avatar Success")

    if form.validate_on_submit() and form.submit.data:
        now_user = User.query.filter_by(account=account).first()
        now_user.about_me = form.about_content.data
        db.session.commit()
        flash("Update ABOUT ME Success")

    user_data = User.query.filter_by(account=account).first_or_404()
    form.about_content.data = user_data.about_me

    upload, liked = SelfUrlContent(user_data)

    return render_template('user.html', user=user_data, upload=upload, liked=liked, form=form, account=account)


@user.route("/user/<string:account>/sort/<string:SortType>")
@login_required
def HomePageSort(account, SortType):
    user_data = User.query.filter_by(account=account).first_or_404()
    upload, liked = SelfUrlContent(user_data, SortType)

    if SortType in ['1', '2']:
        return render_template('your_upload.html', upload=upload)
    return render_template('liked_recently.html', liked=liked)
