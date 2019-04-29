import flickrapi
import flickr_api
import urllib.request
import os
import sys

if __name__ != "__main__":
    print("File 'flickr.py' not meant for transcendings and imports, direct use only")
    sys.exit(0)

#functions
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
    name = str(name)
    new_n = name[:]
    while os.path.exists(new_n):
        num += 1
        new_n = name + str(num)
    return new_n
    

#reading logs
try:
    with open('logs', 'r') as  var:
        lines = [i.rstrip() for i in var.readlines() if len(i) ]
except FileNotFoundError:
    with open('logs', 'w+') as  var:
        lines = []
bool_contain = -1
bool_ask_old = 0
dict_ids = {}


#ids_handeling
for line in lines:
    if 'id1' in line: 
        bool_contain += 1
        dict_ids['id1'] = ''.join(line.split(' ')[1:])
    if 'id2' in line:
        bool_contain += 1
        dict_ids['id2'] = ''.join(line.split(' ')[1:])

if bool_contain == 1:
    inp_ask_old = input('Use previously saved keys?(Yes or No)').rstrip().lower()
    if inp_ask_old == 'yes':
        bool_ask_old = 1
        api_key_val = dict_ids['id1']
        secret_key_val = dict_ids['id2']
        #print(secret_key_val)
else:
    while 1:
        tjc = 1
        api_key_val = input('Give your API key  ').rstrip()
        secret_key_val = input('Give your API secret  ').rstrip()
    
        flickr_api.set_keys(api_key = api_key_val, api_secret = secret_key_val)
        try: flickr_api.Person.findByUserName('vicro_bot').id
        except flickr_api.flickrerrors.FlickrAPIError:
            print("Wrong Keys!!", "Try again")
            tjc = 0
        if tjc: break
    
    writable = ['id1 {}\n'.format(api_key_val), 'id2 {}\n'.format(secret_key_val)]
    with open('logs', 'w+') as var:
        var.writelines(writable)

#some globals' setup
flickr=flickrapi.FlickrAPI(api_key_val, secret_key_val)
flickr_api.set_keys(api_key = api_key_val, api_secret = secret_key_val)
user_name = input('Give user name:-  \n').rstrip()
user_id_val = flickr_api.Person.findByUserName(user_name).id

urls = url_list_maker(user_id_val)

#directory work
new_dir = mkname('Flickr_Imgs_{}'.format('_'.join(user_name.split(' '))))
os.mkdir(new_dir)
os.chdir(new_dir)

# terminal show
counter = 0
var = 100.0/(len(urls)*1.0)
print('Downloading ... {:05}%'.format(int(counter)), end = '', flush = True)
b, imagecount = 0, 1
for i in urls:
    try: urllib.request.urlretrieve( i, 'T{0}'.format(imagecount))
    except: pass
    counter += var
    print('\b'*6, end = '', flush = True)
    imagecount += 1
    print('{:05}'.format(counter)[:5]+'%', end = '', flush = True)
print('\nDone')
