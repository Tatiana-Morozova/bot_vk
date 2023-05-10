from datetime import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from secret import access_token
from Interface import BotInterface

class VkTools():
    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)


    def get_profile_info(self, user_id):
        info, = self.api.method('users.get',
                                {'user_id': user_id,
                                 'fields': 'city,bdate,sex,relation,home_town,screen_name'
                                 }
                                )
        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'] if 'home_town' in info else None,
                     'sex': info['sex'] if 'sex' in info else None,
                     'city': info['city']['id'] if 'city[id]' in info else None,
                     'screen_name': info['screen_name']
                     }

        if user_info['bdate'] == None:
            message_send(user_id,'У вас в профиле не указан дата рождения, напиши его формате: например Y.YY.YYYY')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    user_info['bdate'] = event.text


        if user_info['home_town'] == None:
            message_send(user_id, 'В профиле не указан ваш город, напишите его например /Томск')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    user_info['home_town'] = event.text


        return user_info

    def serch_users(self,params):


        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5
        screen_name = 'screen_name'


        users = self.api.method('users.search',
                                {'count': 100,
                                 'offset': 0,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False,
                                 'fields': screen_name
                                 }
                                )

        try:
            users = users['items']
        except KeyError:
            return []

        res = []

        for user in users:
            if user['is_closed'] == False:
                res.append({'id_vk': user['id'],
                            'name': user['first_name'] + ' ' + user['last_name'],
                            'screen_name': user['screen_name']
                            }
                           )

        return res


    def get_photos(self,user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1
                                  }
                                 )
        try:
            photos = photos['items']
        except KeyError:
            return []

        res = []


        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count']
                        }
                       )


        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res



