import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from BD_bot import *
from secret import token_bot, access_token
from main import VkTools


class BotInterface():

    def __init__(self, token_bot, access_token):
        self.interface = vk_api.VkApi(token=token_bot)
        self.api = VkTools(access_token)


    def message_send(self, user_id, message, attachment=None):
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
                    #event.user_id = user_id
                elif command == 'поиск':
                    user_info = self.api.get_profile_info(event.user_id)
                    users = self.api.serch_users(user_info)
                    user = users.pop()
                    #user_id = user['id']
                    photos_user = self.api.get_photos(user['id_vk'])
                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                        self.message_send(event.user_id,
                                        f'Встречайте {user["name"]}',
                                        attachment=attachment
                                          )
                    #add_user_viewed(user_id)

                    self.message_send(event.user_id, f'Продолжать поиск да/нет')

                elif command == "да":

                    user_info = self.api.get_profile_info(event.user_id)
                    users = self.api.serch_users(user_info)
                    photos_user = self.api.get_photos(user['id_vk'])
                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                        if num == 2:
                            break
                        self.message_send(event.user_id,
                                          f'Встречайте {user["name"]}',
                                          attachment=attachment
                                          )
                        self.message_send(event.user_id, f'Продолжать поиск да/нет')
                else:
                    self.message_send(event.user_id, 'пока')
                    break




if __name__ == '__main__':
    bot = BotInterface(token_bot, access_token)
    bot.event_handler()
