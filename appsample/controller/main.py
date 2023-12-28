from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func

from ..model import Likes, Manga, Permission, db, get_random
from .form import ModifyForm, UploadDeleteForm

main = Blueprint("main", __name__)


# index
@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# main page
# TODO 排序與模糊搜尋兩邊不相干 搜尋後按排序會以全部的做排序 希望做到兩邊能互相牽制
@main.route("/main", methods=["GET", "POST"])
def MainPage():
    form = ModifyForm()
    form1 = UploadDeleteForm()

    if form.validate_on_submit() and form.submit.data:
        if form.mid.data and current_user.can(Permission.MODIFY):
            # UpdateData = {"mid": form.mid.data, "url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data, "update_time": datetime.datetime.now()}
            # sqlOP("update manga set url = :url, name= :name, page= :page, author= :author, author_group= :author_group, update_time= :update_time where mid = :mid", UpdateData)
            manga = Manga.query.get_or_404(form.mid.data)
            manga.url = form.url.data
            manga.name = form.name.data
            manga.page = form.pages.data
            manga.author = form.author.data
            manga.author_group = form.group.data
            manga.update_user = current_user.id

            db.session.add(manga)
            db.session.commit()
            flash("Modify Success")
        elif current_user.can(Permission.MODIFY):
            manga = Manga(
                url=form.url.data,
                name=form.name.data,
                page=form.pages.data,
                author=form.author.data,
                author_group=form.group.data,
                status=False,
                update_user=current_user.id,
                insert_user=current_user.id,
            )
            db.session.add(manga)
            db.session.commit()
            flash("Insert Success")
        # clear the form
        return redirect(url_for("main.MainPage"))

    if form1.validate_on_submit() and form1.delete.data:
        print(form1.delete_mid.data)
        if current_user.is_administrator():
            Likes.query.filter_by(mid=form1.delete_mid.data).delete()
            Manga.query.filter_by(mid=form1.delete_mid.data).delete()
            db.session.commit()
        return redirect(url_for("main.MainPage"))

    if request.form.get("mid") and current_user.can(Permission.READ):
        return_data = Likes.query.filter(Likes.user_id == current_user.id, Likes.mid == request.form.get("mid")).first()
        print(return_data)
        if return_data:
            Likes.query.filter(Likes.user_id == current_user.id, Likes.mid == request.form.get("mid")).delete()
        else:
            like = Likes(user_id=current_user.id, mid=request.form.get("mid"), insert_user=current_user.id)
            db.session.add(like)
        db.session.commit()
        return redirect(url_for("main.MainPage"))
    elif request.form.get("mid"):
        flash("Login First")

    if current_user.can(Permission.READ):
        sel_data = Likes.query.with_entities(Likes.mid).filter_by(user_id=current_user.id).subquery()
        # Postgres的group by後只能秀group的欄位及相關的計數 所以先計算計數在join自己
        group_data = (
            Manga.query.with_entities(Manga.mid, func.count(Likes.mid).label("total"))
            .join(Likes, Manga.mid == Likes.mid, isouter=True)
            .group_by(Manga.mid)
            .subquery()
        )

        rows = (
            Manga.query.with_entities(
                Manga.mid,
                Manga.url,
                Manga.name,
                Manga.page,
                Manga.author,
                Manga.author_group,
                group_data.c.total,
                sel_data.c.mid.label("press"),
            )
            .join(group_data, Manga.mid == group_data.c.mid, isouter=True)
            .join(sel_data, Manga.mid == sel_data.c.mid, isouter=True)
        )
    else:
        rows = (
            Manga.query.with_entities(
                Manga.mid,
                Manga.url,
                Manga.name,
                Manga.page,
                Manga.author,
                Manga.author_group,
                func.count(Likes.mid).label("total"),
            )
            .join(Likes, Manga.mid == Likes.mid, isouter=True)
            .group_by(Manga.mid)
        )

    rand = Manga.query.order_by(func.random()).limit(5)

    return render_template(
        "main.html", rows=rows, rand=rand, form=form, form1=form1, Permission=Permission, GR=get_random
    )


# fuzzy search
@main.route("/fuzzy", methods=["POST"])
def FuzzySearch():
    PostDict = request.get_json()
    print(PostDict)
    if "input" in PostDict and PostDict["input"]:
        if current_user.can(Permission.READ):
            # 為符合Postgres和mysql更改
            return_data = db.session.execute(
                "SELECT m.*, total, ss.mid as press FROM manga m \
                            left join (select m.mid, count(l.mid) as total from manga m left join likes l on m.mid=l.mid group by m.mid) s on m.mid=s.mid\
                            left join (SELECT mid FROM likes where user_id=:uid) ss on m.mid=ss.mid where url like concat('%', :val, '%') or name like concat('%', :val, '%') or author like concat('%', :val, '%')\
                            or author_group like concat('%', :val, '%');",
                {"val": PostDict["input"], "uid": current_user.id},
            )
        else:
            return_data = db.session.execute(
                "SELECT m.*, total FROM manga m \
                            left join (select m.mid, count(l.mid) as total from manga m left join likes l on m.mid=l.mid group by m.mid) s on m.mid=s.mid\
                            where url like concat('%', :val, '%') or name like concat('%', :val, '%') or author like concat('%', :val, '%')\
                            or author_group like concat('%', :val, '%');",
                {"val": PostDict["input"]},
            )
        result = return_data.mappings().all()

        # for i, item in enumerate(return_data):
        #     return_data[i] = dict(item)
        #     return_data[i]['insert_time'] = return_data[i]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        #     return_data[i]['update_time'] = return_data[i]['update_time'].strftime('%Y-%m-%d %H:%M:%S')

        return render_template("url.html", rows=result, Permission=Permission, GR=get_random)
