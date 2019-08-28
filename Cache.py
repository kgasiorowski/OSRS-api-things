import json, time, os
from urllib import request, error

cache_path = './cache/'
image_cache_path = cache_path + 'icon/'
ids_file = 'ids'
ids_path = cache_path + ids_file

base_url = 'http://services.runescape.com/m=itemdb_oldschool'
item_info_url = base_url + '/api/catalogue/detail.json?item='
image_extension = '.gif'
cache_lifetime = 3600


def get_cached_item(item_no, force_refresh=False, force_refresh_icon=False):

    cached_item_path = cache_path + str(item_no)
    cached_data = None
    cached_data_age = None
    current_time = time.time()

    if os.path.exists(cached_item_path):
        with open(cached_item_path) as cached_json:
            try:
                cached_data = json.load(cached_json)
            except json.decoder.JSONDecodeError:
                print(F"Error: Cache was malformed ({item_no}). Refreshing...")
                cached_data = None

    # Calculate the cached data age
    if cached_data is not None:
        cached_data_age = current_time - cached_data['time']

    # If the cache is too old or doesn't exist, refresh
    if cached_data_age is None or cached_data_age > cache_lifetime or force_refresh:

        print(F'Invalid cache detected ({item_no}), refreshing...')

        # Request the data from the internets
        try:

            with request.urlopen(item_info_url + str(item_no)) as url:

                data = json.loads(url.read().decode())
                data['time'] = current_time

                # Overwrite the existing cache
                with open(cached_item_path, 'w') as file:
                    json.dump(data, file)

                # Refresh the icon if necessary
                __refresh_icon(data, force_refresh=force_refresh_icon)
                return data['item']

        except error.HTTPError:
            print(F"Error: Could not find item {item_no} (error 404)")
            return
        except json.decoder.JSONDecodeError:
            print('Error: The request seems to have failed. You may be requesting too quickly')
            raise RequestFailedError


    else:
        print(F'Valid cache detected ({item_no}), no refresh necessary')
        return cached_data['item']


def __refresh_icon(data, force_refresh=False):

    item_no = data['item']['id']
    image_path = image_cache_path + str(item_no) + image_extension
    os.makedirs(image_cache_path, exist_ok=True)

    if not os.path.exists(image_path) or force_refresh:
        request.urlretrieve(data['item']['icon'], image_path)


def get_cached_item_icon(item_no, force_refresh=False):

    if not os.path.exists(image_cache_path + str(item_no)):
        if get_cached_item(item_no, force_refresh=force_refresh) is None:
            return None

    return image_cache_path + str(item_no) + '.gif'


def get_item_ids():

    with open(ids_path, 'r') as ids:
        data = json.load(ids)

    return data


def search_ids(searchstring):

    ids = get_item_ids()
    return [item_id for item_id in ids if str.lower(searchstring) in str.lower(item_id['name'])]


class RequestFailedError(Exception):
    pass
