
from datetime import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from secret import access_token
from BD_bot import *



class VkTools():
    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)


    def get_profile_info(self, user_id):
        #global user_id, user_info
        info, = self.api.method('users.get',
                                {'user_id': user_id,
                                 'fields': 'city,bdate,sex,relation,home_town'
                                 }
                                )
        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'],
                     'sex': info['sex'],
                     'city': info['city']['id']
                     }

        return user_info

# if __name__ == '__main__':
#     bot = VkTools(access_token)
#     print(bot.get_profile_info(27031255))


    def serch_users(self,params):
        #global id_vk, users

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5



        users = self.api.method('users.search',
                                {'count': 10,
                                 'offset': 0,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
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
                            'name': user['first_name'] + ' ' + user['last_name']
                            }
                           )

        return res
# if __name__ == '__main__':
#      bot = VkTools(access_token)
#      params = bot.get_profile_info(27031255)
#      print(bot.serch_users(params))


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
                        'comments': photo['comments']['count'],
                        }
                       )

        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res


if __name__ == '__main__':
    bot = VkTools(access_token)
    params = bot.get_profile_info(27031255)
    users = bot.serch_users(params)
    print(bot.serch_users(params))
    print(bot.get_photos(users[5]['id_vk']))
