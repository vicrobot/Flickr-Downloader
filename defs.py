import flickrapi
import flickr_api
import urllib.request
import os, sys
import time


def url_list_maker(flickr_obj, uiv):
    """
    Returns a list of urls of all public photos a user has uploaded on flickr.
    User is identified through user id value(uiv) in argument.
    """
    count = 0
    photos = flickr_obj.walk_user(user_id = uiv, per_page = 100, extras = 'url_o')
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
    k1 = len(urls)
    if k1 == 0:
        return 0
    var = 100.0/(k1*1.0)
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
    return 1
