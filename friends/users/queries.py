from django.db import connection


def get_user_friends(user_id):
    with connection.cursor() as cursor:
        cursor.execute("select username from users_user uu "
                       "join users_friendrequest uf on uu.id = uf.recipient_id or uu.id = uf.sender_id "
                       "WHERE uf.status = 2 and uu.id <> %s;", (user_id, ))
        row = cursor.fetchall()
    return row

