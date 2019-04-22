import flickrapi
import flickr_api
import urllib.request
import os

# Flickr api access key

api_key_val = input('Give your API key  ').rstrip()
secret_key_val = input('Give your API secret  ').rstrip()

flickr=flickrapi.FlickrAPI(api_key_val, secret_key_val)
flickr_api.set_keys(api_key = api_key_val, api_secret = secret_key_val)
user_id_val = flickr_api.Person.findByUserName(input('Give user name:-  \n').rstrip()).id


def url_list_maker(uiv):
    count = 0
    photos = flickr.walk_user(user_id = uiv, per_page = 100, extras = 'url_o')
    url_list = []
    for photo in photos:
        try:
            url_list.append(photo.get('url_o')) # o ->original size; other vars instead will cause error for some files due to unavailibility.
        except: pass
    return url_list

def mkname(name):
    num = 0
    woo = name
    while os.path.exists(woo):
        num += 0
        woo = woo + str(num)
    return woo

urls = url_list_maker(user_id_val)

new_dir = mkname('Flickr_Imgs')
os.mkdir(new_dir)
os.chdir(new_dir)

# terminal show
counter = 0
var = 100.0/(len(urls)*1.0)
deciP = int(str(var).split('.')[1][:4])
print('Downloading ... {:03}%'.format(int(counter)), end = '', flush = True)
b, imagecount = 0, 1
for i in urls:
    try: urllib.request.urlretrieve( i, 'T{0}'.format(imagecount))
    except: pass
    counter += var
    print('\b'*4, end = '', flush = True)
    imagecount += 1
    print('{:03}%'.format(int(counter)), end = '', flush = True)
print('\nDone')
