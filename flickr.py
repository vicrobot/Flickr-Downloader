import flickrapi
import flickr_api
import os

# Flickr api access key 
flickr=flickrapi.FlickrAPI('YOUR API KEY HERE', 'YOUR API SECRET HERE')
flickr_api.set_keys(api_key = "YOUR API KEY HERE", api_secret = "YOUR API SECRET HERE")
user_id_val = flickr_api.Person.findByUserName(input('Give user exact name as on profile of flickr:- \n').rstrip()).id


def url_list_maker(uiv):
    count = 0
    photos = flickr.walk_user(user_id = uiv, per_page = 100, extras = 'url_o')
    url_list = []
    for photo in photos:
        try:    
            url_list.append(photo.get('url_o')) # o ->original size; other vars instead will cause error for some due to unavailibility.
        except: pass
    return url_list

    
urls = url_list_maker(user_id_val)
for i in urls:
    os.system('wget {}'.format(i)) # wget command thus linux restriction
 
