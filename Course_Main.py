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

    def get_all_photos(self, local_folder: str):
        data = self.get_photos()
        i = 0
        count = 50
        photos = []  # Список всех загруженных фото
        max_size_photo = {}  # Словарь вида {photo_name:photo_url}
        #local_folder = "E:\\colab_F\\Course\\"
 
        # Создаём папку на компьютере для скачивания фотографий
        if not os.path.exists(local_folder+'vk_images'):
            os.mkdir(local_folder+'vk_images')


        # Получаем все фотографии
        while i <= data['response']['count']:
            if i != 0:
                data = self.get_photos(offset=i, count=count)

                
            for photo in data['response']['items']:
                max_size = 0
                photos_info = {}
                # Сохраням информацию о самом большом фото в max_size_photo
                for size in photo['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
                        max_size_item = size
                if photo['likes']['count'] not in max_size_photo.keys():
                    max_size_photo[photo['likes']['count']] = max_size_item['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                else:
                    max_size_photo[f"{photo['likes']['count']} + {photo['date']}"] = max_size_item['url']
                    photos_info['file_name'] = f"{photo['likes']['count']}+{photo['date']}.jpg"

                # Сохраням список самых большых фотографий
                photos_info['size'] = max_size_item['type']
                photos.append(photos_info)
            #print(1,photos_info)
           # print(2,max_size_photo)
           # print(3,size)
          #  print(4,photo)
          #  print(5,photos)
            # Скачиваем фотографии
            for photo_name, photo_url in max_size_photo.items():
                with open(os.path.join(local_folder,'vk_images\%s' % f'{photo_name}.jpg'), 'wb') as file:
                    img = requests.get(photo_url)
                    #print(img.content)
                    file.write(img.content)

            print(f'Загружено {len(max_size_photo)} фото')
            i += count

        # Генерация json файла с фотографиями
        with open("photos.json", "w") as file:
            json.dump(photos, file, indent=4)




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

        def upload(self, file_path: str):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'OAuth {yandex_token}'}
            params = {'path': f'{folder_name}/{file_name}',
                      'overwrite': 'true'}

            # Получение ссылки
            response = requests.get(url=url, headers=headers, params=params)
            href = response.json().get('href')

            # Загрузка файла
            requests.put(href, data=open(files_path, 'rb'))


#Создание подключения к ВК
vk_access_token =str(input('Введите VK токен: ')) # токен ВК
user_id = '45432918' # идентификатор пользователя vk
vk = VK(vk_access_token, user_id)

# Получение фотографий
local_folder = "E:\\colab_F\\Course\\"
vk.get_all_photos(local_folder)

#Создание подключения к Я.Диску
yandex_token =  str(input('Введите токен на Яндекс диске: ')) # токен Я.Диска
uploader = YandexDisk(yandex_token) 

# Получение списка скаченных фотографий 
photos_list = os.listdir(local_folder+ "vk_images\\")
print(photos_list)
count = 0

folder_name = str(input('Введите имя папки на Яндекс диске: '))
uploader.folder_creation()

for photo in photos_list:
    file_name = photo
    files_path = local_folder + "vk_images\\"+photo
    result = uploader.upload(files_path)
    count += 1
    print(f'Загружено на Яндекс диск: {count} из {len(photos_list)}')
    print("["+count*"="+(len(photos_list)-count)*' '+"]",int(count/len(photos_list)*100),"%")