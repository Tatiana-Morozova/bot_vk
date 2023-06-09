import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from main import *


class BotInterface():

    def __init__(self, token_bot, access_token):
        self.interface = vk_api.VkApi(token=token_bot)
        self.api = VkTools(access_token)


    def message_send(self, user_id, message, attachment = None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, 'здравствуй, для поиска введите команду (поиск)'  )

                elif command == 'поиск':
                    add_users(event.user_id)
                    user_info = self.api.get_profile_info(event.user_id)
                    users = self.api.serch_users(user_info)
                    user = users.pop()

                    photos_user = self.api.get_photos(user['id_vk'])
                    self.message_send(event.user_id,
                                        f'Встречайте {user["name"]}  {user["screen_name"]}',
                                        photos_user
                                          )
                    add_user_viewed(user['id_vk'])

                    self.message_send(event.user_id, f'Продолжать поиск да/нет')

                elif command == "да":
                    user = users.pop()
                    photos_user = self.api.get_photos(user['id_vk'])
                    self.message_send(event.user_id,
                                        f'Встречайте {user["name"]}  {user["screen_name"]}',
                                      photos_user
                                          )
                    self.message_send(event.user_id, f'Продолжать поиск да/нет')
                elif command == 'нет':
                    self.message_send(event.user_id, 'пока')
                    drop_table()
                    break
                else:
                    self.message_send(event.user_id, 'не понимаю вашу команду, начните заново')
                    drop_table()
                    break







if __name__ == '__main__':
    bot = BotInterface(token_bot, access_token)
    bot.event_handler()
