import requests
import os
import json

class VK:

    def __init__(self, vk_access_token, user_id, version='5.131'):
        self.token = vk_access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params,**params})
        return response.json()


    def get_photos(self, offset=0, count=50):

        url = 'https://api.vk.com/method/photos.get'
        params ={'owner_id': user_id,
                 'album_id': 'profile',
                 'access_token': vk_access_token,
                 'v': '5.131',
                 'extended': '1',
                 'photo_sizes': '1',
                 'count': count,
                 'offset': offset
                 }
        res = requests.get(url=url, params=params)
        return res.json()

    def get_all_photos(self):
        data = self.get_photos()
        all_photo_count = data['response']['count']  # Количество всех фотографий профиля
        i = 0
        count = 50
        photos = []  # Список всех загруженных фото
        max_size_photo = {}  # Словарь с парой название фото - URL фото максимального разрешения



        while i <= all_photo_count:
            if i != 0:
                data = self.get_photos(offset=i, count=count)

            # Проходимся по всем фотографиям



            for photo in data['response']['items']:
                max_size = 0
                photos_info = {}
                # Выбираем фото максимального разрешения и добавляем в словарь max_size_photo
                max_size_item=sorted(photo['sizes'],key=lambda x: x['height'] * x['width'],reverse=True )[0]

                if photo['likes']['count'] not in max_size_photo.keys():
                    max_size_photo[photo['likes']['count']] = max_size_item['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                    photos_info['url'] = max_size_item['url']
                else:
                    max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = max_size_item['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}+{photo['date']}.jpg"
                    photos_info['url'] = max_size_item['url']

                # Формируем список всех фотографий для дальнейшей упаковки в .json

                photos_info['size'] = max_size_item['type']
                photos.append(photos_info)
 

            i += count



        return photos


class YandexDisk:
        def __init__(self, token: str):
            self.token = token

        def folder_creation(self):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/'
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'OAuth {yandex_token}'}
            params = {'path': f'{folder_name}',
                      'overwrite': 'false'}
            # Cоздание папки
            requests.put(url=url, headers=headers, params=params)

        def upload(self, file, filename):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'OAuth {yandex_token}'}
            params = {'path': filename, 'overwrite': 'true'}

            # Получение ссылки
            response = requests.get(url=url, headers=headers, params=params)
            href = response.json().get('href')

            # Загрузка файла
            requests.put(href, data=file)


vk_access_token = str(input('Введите ВК токен: '))
user_id = '45432918' # идентификатор пользователя vk
vk = VK(vk_access_token, user_id)

# Получение фотографий
photos=vk.get_all_photos()

count = 0
yandex_token = str(input('Введите Яндекс токен: '))

uploader = YandexDisk(yandex_token)
folder_name = str(input('Введите имя папки на Яндекс диске: '))
uploader.folder_creation()
photos_json=[]

for photo in photos:
    file_name = f"{folder_name}/{photo['file_name']}"
    #files_path = folder_name+'\\' + photo
    response = requests.get(photo["url"])
    file = response.content
    result = uploader.upload(file,file_name)
    count += 1
    print(f'Загружено на Яндекс диск: {count} из {len(photos)}')
    print("["+count*"="+(len(photos)-count)*' '+"]",int(count/len(photos)*100),"%")
    photos_info={}
    photos_info['file_name'] = f"{photo['file_name']}.jpg"
    photos_info['url'] = photo['url']
    photos_json.append(photos_info)



with open("photos.json", "w") as file:
        json.dump(photos_json, file, indent=4)