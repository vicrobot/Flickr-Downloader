import flickrapi
import flickr_api
import urllib.request
import os
import sys


#######################
"""
#Pseudos

incomplete and complete status too.
urls' completion and incompletion too.
"""
#######################

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
            url_list.append(photo.get('url_o')) # o ->original size; other vars may not have all images.
        except: pass
    return url_list

def mkname(name):
    num = 0
    name = str(name)
    new_n = name[:]
    old_n = new_n
    while os.path.exists(new_n):
        old_n = new_n
        num += 1
        new_n = name + str(num)
    return(new_n, old_n)
    
def checkIds(akv, skv, print_M = 0):
    flickr_api.set_keys(api_key = akv, api_secret = skv)
    try: flickr_api.Person.findByUserName('vicro_bot').id
    except flickr_api.flickrerrors.FlickrAPIError:
        if print_M: print("Wrong Keys!!", "Try again")
        return 0
    return 1

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

if bool_contain == 1: bool_contain = checkIds(dict_ids['id1'],dict_ids['id2'])
if bool_contain == 1:
    inp_ask_old = input('Use previously saved keys?(Yes or No)').rstrip().lower()
    if inp_ask_old == 'yes':
        bool_ask_old = 1
        api_key_val = dict_ids['id1']
        secret_key_val = dict_ids['id2']
        #print(secret_key_val)
if not bool_ask_old:
    while 1:
        var1_ = 1
        api_key_val = input('Give your API key  ').rstrip()
        secret_key_val = input('Give your API secret  ').rstrip()
        var1_ = checkIds(api_key_val,secret_key_val, print_M = 1)
        if var1_: break
    writable = ['id1 {}\n'.format(api_key_val), 'id2 {}\n'.format(secret_key_val)]
    with open('logs', 'w+') as var:
        var.writelines(writable)

#some globals' setup
flickr=flickrapi.FlickrAPI(api_key_val, secret_key_val)
flickr_api.set_keys(api_key = api_key_val, api_secret = secret_key_val)
user_name = input('Give user name:-  \n').rstrip()
user_id_val = flickr_api.Person.findByUserName(user_name).id



#directory work
new_dir, old_dir = mkname('Flickr_Imgs_{}'.format('_'.join(user_name.split(' '))))
if not os.path.exists(old_dir):
    os.mkdir(new_dir)
    os.chdir(new_dir)
else: os.chdir(old_dir)

if not os.path.exists('.temp-logs'):
    imagecount = 0
    with open('.temp-logs', 'w+') as var:
        urls = url_list_maker(user_id_val)        ###### need to write something like yes! this has all urls and etc ##########
        var.write(str(urls))
        var.write('\n')
else:
    with open('.temp-logs', 'r+') as var:
        lines_urls_lgs = var.readlines()
    susp_int= lines_urls_lgs[1].rstrip()[5:]
    if susp_int: imagecount = int(susp_int) -1
    urls = eval(lines_urls_lgs[0].rstrip())[imagecount :]  #sometimes 1 image overridely get downloaded, toPreventLossOfUnperdictedIntruption


# terminal show
with open('.temp-logs', 'r+') as var: t_lines = var.readlines()
counter = 0
var = 100.0/(len(urls)*1.0)
print('Downloading ... {:05}%'.format(int(counter)), end = '', flush = True)
b = 0
for i in urls:
    try: urllib.request.urlretrieve( i, '{1}{0}'.format(imagecount, user_name[:1]))
    except KeyboardInterrupt:
        with open('.temp-logs', 'w+') as var:
            var.write(t_lines[0])
            var.write('imgC {}'.format(imagecount))
        print('\nAbort')
        sys.exit()
    except Exception: raise Exception
    counter += var
    print('\b'*6, end = '', flush = True)
    imagecount += 1
    print('{:05}'.format(counter)[:5]+'%', end = '', flush = True)

with open('.temp-logs', 'w+') as var:
    var.write(t_lines[0])
    var.write('imgC {}'.format(imagecount))    #Prob assumed that interuptn wil be at except block but 've2fix
print('\nDone')
