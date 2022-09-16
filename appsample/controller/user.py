from flask_login import login_required, current_user
from ..model import db, User, Manga, Likes, get_random
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import func
from .form import AboutMeForm, UploadDeleteForm, ModifyForm, ChangeSortForm

user = Blueprint('user', __name__)


def SelfUrlContent(user_data, PageType, SortType=None, page=None):
    # 子查詢 先篩出likes裡所有mid的各個數量
    group_data = Likes.query.with_entities(Likes.mid, func.coalesce(func.count(Likes.mid), 0).label('total')).group_by(Likes.mid).subquery()
    sel_data = Likes.query.with_entities(Likes.mid).filter_by(user_id=user_data.id).subquery()

    # 此人上傳的
    # 把子查詢直接join 要用c去on https://docs.sqlalchemy.org/en/14/core/selectable.html#sqlalchemy.sql.expression.FromClause.c
    upload = Manga.query.with_entities(Manga.mid, Manga.url, Manga.name, Manga.page, Manga.author, Manga.author_group, func.coalesce(group_data.c.total, 0).label('total'), Manga.update_time, Manga.insert_user, sel_data.c.mid.label('press'))\
                        .filter_by(insert_user=user_data.id).join(group_data, Manga.mid == group_data.c.mid, isouter=True).join(sel_data, Manga.mid == sel_data.c.mid, isouter=True)
    # print(upload)

    # 此人按讚的
    # 先查自己的like紀錄再關聯manga最後在連結子查詢
    liked = Likes.query.join(User, User.id == Likes.user_id, isouter=True).filter_by(account=user_data.account)\
        .add_columns(Manga.mid, Manga.url, Manga.name, Manga.page, Manga.author, Manga.author_group, func.coalesce(group_data.c.total, 0).label('total'), Manga.update_time, Manga.insert_user, Likes.user_id, Likes.mid.label('press'))\
        .join(Manga, Likes.mid == Manga.mid, isouter=True).join(group_data, Manga.mid == group_data.c.mid, isouter=True)
    # print(liked)
    # for i in liked:
    #     print(i)

    # 個人主頁
    if PageType == "main":
        # 個人主頁限制5筆
        upload = upload.paginate(0, 5, False)
        liked = liked.paginate(0, 5, False)
        # liked = liked.limit(5).all()
    # 單一頁面
    else:
        if SortType == 2:
            upload = upload.order_by(group_data.c.total.asc())
            liked = liked.order_by(group_data.c.total.asc())
        elif SortType == 3:
            upload = upload.order_by(Manga.update_time.desc())
            liked = liked.order_by(Manga.update_time.desc())
        elif SortType == 4:
            upload = upload.order_by(Manga.update_time.asc())
            liked = liked.order_by(Manga.update_time.asc())
        elif SortType == 5:
            upload = upload.order_by(Manga.insert_time.desc())
            liked = liked.order_by(Manga.insert_time.desc())
        elif SortType == 6:
            upload = upload.order_by(Manga.insert_time.asc())
            liked = liked.order_by(Manga.insert_time.asc())
        # type=1 或者超過6
        else:
            # TODO Postgre排序null會亂掉
            upload = upload.order_by(group_data.c.total.desc())
            liked = liked.order_by(group_data.c.total.desc())

        upload = upload.paginate(page, 10, False)
        liked = liked.paginate(page, 10, False)

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

    upload, liked = SelfUrlContent(user_data, "main")

    return render_template('user.html', user=user_data, chk="main", upload=upload, liked=liked, form=form, account=account)


@user.route("/user/<string:PageType>/<string:account>/<int:SortType>", methods=['GET', 'POST'])
@user.route("/user/<string:PageType>/<string:account>/<int:SortType>/<int:page>", methods=['GET', 'POST'])
@login_required
def UserContent(PageType, account, SortType, page=1):
    form = UploadDeleteForm()
    form1 = ModifyForm()
    form2 = ChangeSortForm()
    user_data = User.query.filter_by(account=account).first_or_404()

    if form.validate_on_submit() and form.delete.data:
        print(form.delete_mid.data)
        manga = Manga.query.filter_by(mid=form.delete_mid.data).first()
        if current_user.id == manga.insert_user or current_user.is_administrator():
            Likes.query.filter_by(mid=form.delete_mid.data).delete()
            Manga.query.filter_by(mid=form.delete_mid.data).delete()
            db.session.commit()
        return redirect(url_for('user.UserContent', PageType=PageType, account=account, SortType=SortType))

    if form1.validate_on_submit() and form1.submit.data:
        print(form1.mid.data)
        manga = Manga.query.filter_by(mid=form1.mid.data).first()
        if current_user.id == manga.insert_user or current_user.is_administrator():
            manga.name = form1.name.data
            manga.page = form1.pages.data
            manga.url = form1.url.data
            manga.author = form1.author.data
            manga.author_group = form1.group.data
            manga.update_user = current_user.id
            db.session.commit()
        return redirect(url_for('user.UserContent', PageType=PageType, account=account, SortType=SortType))

    if form2.validate_on_submit():
        print(form2.sort_choice.data)
        SortType = form2.sort_choice.data
        # return redirect(url_for('user.UserContent', PageType=PageType, account=account, SortType=form2.sort_choice.data))

    if request.form.get("mid") and current_user.id == user_data.id:
        return_data = Likes.query.filter(Likes.user_id == current_user.id, Likes.mid == request.form.get("mid")).first()
        print(return_data)
        if return_data:
            Likes.query.filter(Likes.user_id == current_user.id, Likes.mid == request.form.get("mid")).delete()
        else:
            like = Likes(user_id=current_user.id,
                         mid=request.form.get("mid"),
                         insert_user=current_user.id)
            db.session.add(like)
        db.session.commit()
        return redirect(url_for('user.UserContent', PageType=PageType, account=account, SortType=SortType))

    # 因應更改SortType時 可以selected選取的項目
    form2.sort_choice.default = SortType
    form2.process()
    upload, liked = SelfUrlContent(user_data, "single", SortType, page)
    # for i in upload.items:
    #     print(i)
    if PageType == "upload":
        return render_template('user_content.html', upload=upload, user=user_data, form=form, form1=form1, form2=form2, SortType=SortType, account=account, PageType=PageType, GR=get_random)
    elif PageType == "liked":
        return render_template('user_content.html', liked=liked, user=user_data, form=form, form1=form1, form2=form2, SortType=SortType, account=account, PageType=PageType, GR=get_random)
    # else:
    #     return render_template('index.html'), 404
