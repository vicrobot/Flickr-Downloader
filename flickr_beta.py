import flickrapi
import flickr_api
import urllib.request
import os, sys
import time


#######################
"""
#Pseudos

incomplete and complete status too.
urls' completion and incompletion too.

Its been a lot of if else, we need GUI.
All inputs should be from a particular class and their exception handeling.
Checking mimes of files downloaded and delete incomplete files.
Animated printings' alignment.
Files' extension appending
Aborting for connection reset; and retrying for failure.
"""
#######################

if __name__ != "__main__":
    anim_write("File 'flickr.py' not meant for transcendings and imports, direct use only")
    sys.exit(0)

#functions
def url_list_maker(uiv):
    """
    Returns a list of urls of all public photos a user has uploaded on flickr.
    User is identified through user id value(uiv) in argument.
    """
    count = 0
    photos = flickr.walk_user(user_id = uiv, per_page = 100, extras = 'url_o')
    url_list = []
    for photo in photos:
        try:
            url_list.append(photo.get('url_o')) # o ->original size; other vars may not have all images.
        except: pass
    return url_list

def mkname(name):
    """
    Returns a possible non-conflicting name able to be created in current directory.
    """
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
    """
    Checks whether the provided keys are correct or not.
    akv is access key, akv is secret key.
    print_M is used for showing a message if keys were wrong.
    """
    flickr_api.set_keys(api_key = akv, api_secret = skv)
    try: flickr_api.Person.findByUserName('vicro_bot').id
    except flickr_api.flickrerrors.FlickrAPIError:
        if print_M: anim_write("Wrong Keys!!", "Try again")
        return 0
    return 1

def anim_write(*string, t = 0.05):
    "AnimationWriter:- Prints iterable in fashion"
    for i in string:
        for j in i:
            print(j, end = '', flush = True)
            time.sleep(t)
        print('')
        time.sleep(0.02)

def input_anim(string, t=0.05):
    anim_write(string)
    return input()

def download(urls, filename, choice = 0, imagecount = 0):
    """
    Downloads files from url and uses filename as starting name for files.
    choice : it is the way of accessing photos(like through tags, user name etc).
    """
    if choice == 1:
        with open('.temp-logs', 'r+') as var: t_lines = var.readlines()
    counter, b = 0, 0
    var = 100.0/(len(urls)*1.0)
    print('Downloading ... {:05}%'.format(int(counter)), end = '', flush = True)
    for i in urls:
        try: urllib.request.urlretrieve( i, '{1}{0}.{2}'.format(imagecount, filename[0], i.split('.')[-1]))
        except KeyboardInterrupt:
            if choice == 1:
                #only for choice == 1 since no need to store urls for search results as they vary.
                with open('.temp-logs', 'w+') as var:
                    var.write(t_lines[0])
                    var.write('imgC {}'.format(imagecount))
                print('\nAbort')
                sys.exit()
            else: print('\nAbort'); sys.exit()
        counter += var
        print('\b'*6, end = '', flush = True)
        imagecount += 1
        print('{:05}'.format(counter)[:5]+'%', end = '', flush = True)
    print('\nDone')

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
    inp_ask_old = input_anim('Use previously saved keys?(Yes or No): ').rstrip().lower()
    if inp_ask_old == 'yes':
        bool_ask_old = 1
        api_key_val = dict_ids['id1']
        secret_key_val = dict_ids['id2']
        #print(secret_key_val)
if not bool_ask_old:
    while 1:
        var1_ = 1
        api_key_val = input_anim('Give your API key  ').rstrip()
        secret_key_val = input_anim('Give your API secret  ').rstrip()
        var1_ = checkIds(api_key_val,secret_key_val, print_M = 1)
        if var1_: break
    writable = ['id1 {}\n'.format(api_key_val), 'id2 {}\n'.format(secret_key_val)]
    with open('logs', 'w+') as var:
        var.writelines(writable)

#some globals' setup
flickr=flickrapi.FlickrAPI(api_key_val, secret_key_val)
flickr_api.set_keys(api_key = api_key_val, api_secret = secret_key_val)

types_uses = ['search through tags list', 'search through user name'] #more to be appended like a particular photoset &c
choice = int(input_anim('choose 0 for first element, 1 for second for\n{}'.format(types_uses)).rstrip())

if choice == 1:
    user_name = input_anim('Give user name:-  ').rstrip()
    user_id_val = flickr_api.Person.findByUserName(user_name).id

    #directory work
    new_dir, old_dir = mkname('Flickr_Imgs_{}'.format('_'.join(user_name.split(' '))))
    if not os.path.exists(old_dir):
        os.mkdir(new_dir)
        os.chdir(new_dir)
    else: os.chdir(old_dir)

    imagecount = 0
    if not os.path.exists('.temp-logs'):
        with open('.temp-logs', 'w+') as var:
            urls = url_list_maker(user_id_val)
            var.write(str(urls))
            var.write('\n')
    else:
        with open('.temp-logs', 'r+') as var:
            lines_urls_lgs = var.readlines()
        susp_int= lines_urls_lgs[1].rstrip()[5:]
        if susp_int: imagecount = int(susp_int) -1
        urls = eval(lines_urls_lgs[0].rstrip())[imagecount :]
    download(urls, user_name, choice = 1, imagecount = imagecount)
elif choice == 0:
    bool_broad = int(input_anim('You wanna search broad category or strict in tagging?\
    (1 for former/prior, 0 for later):').rstrip())
    text = input_anim("Give a general text for search: ").strip()
    if bool_broad == 1:
        t = flickr.tags.getRelated(api_key = api_key_val, tag = input_anim('give the tag name: ').rstrip())
        tags = [[j.text for j in i] for i in t][0]
        searched_elem = flickr.photos.search(api_key = api_key_val, tags = tags, 
        text = text, accuracy = 1, safe_search = 1, content_type = 1, extras = 'url_o',
        per_page = int(input_anim('how many images(max 500): ').rstrip())) 
        #there is media argument, per_page and page too. GUI handling needed.
    else:
        tags = [i.strip() for i in input_anim('give tags separated by comma: ').rstrip().split(',')]
        searched_elem = flickr.photos.search(api_key = api_key_val, tags = tags,
        text = text, accuracy = 1, safe_search = 1, content_type = 1, extras = 'url_o', 
        per_page = int(input_anim('how many images(max 500): ').rstrip()))
    photo_elems = [[j for j in i] for i in searched_elem][0]
    url_list = []
    counter_photo, printed, len_p = 1, False, 0
    print('No. of urls: ', end = '', flush = 1)
    for p in photo_elems:
        try:
            dict_ = p.attrib
            md = flickr.photos.getSizes(api_key = api_key_val, photo_id = dict_['id'])
            t1 = [[j.attrib['source'] for j in i][-1] for i in md][0]
            if printed: print('\b'*len_p, end = '', flush = 1)
            str_p = '{} '.format(counter_photo)
            len_p = len(str_p)
            print(str_p ,end = '', flush = 1)
            printed = 1
            counter_photo += 1
            url_list.append(t1)
        except KeyboardInterrupt: 
            print('\nAbort')
            sys.exit()
        except:
            printed = False
            anim_write('Error occured in retrieving url, Ignoring')
    #directory work
    new_dir, old_dir = mkname('Flickr_Imgs_{}'.format('_'.join(text.split(' '))))
    if not os.path.exists(old_dir):
        os.mkdir(new_dir)
        os.chdir(new_dir)
    else: os.chdir(old_dir)
    print('')
    download(url_list, text, choice = 0)


#flickr.photos.getSizes was helpful for retrieving urls from photo ids. 
# photo elems have attrib attribute having a dictionary of data about the photo's source etc.
#An album is called photoset in flickr
