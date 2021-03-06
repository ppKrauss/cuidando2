import requests
import json

import geo

ENTRY_POINT = 'http://127.0.0.1:5000'
# ENTRY_POINT = "http://cuidando.org.br:5000"


def post_data():
    print("Loading data")

    # CACHE PORCA PARA AGILIZAR TESTES
    import pickle
    try:
        table = pickle.load(open("data/table.cache", 'rb'))
    except:
        table = geo.do_all()
        pickle.dump(table, open("data/table.cache", 'wb'))
    # -----------------------

    data = []
    for year in [2014, 2015]:
        print("Preparing data for post")
        for i, row in table.iterrows():
            lat, lon, reg = row['geoentity'].best_coords()
            if lat is None:
                lat, lon = 404, 404
            if lat == 404 or year != 2014:
                data.append({
                    "pk": row['pk'],
                    "lat": lat,
                    "lon": lon,
                    "reg": reg,
                    "year": year,
                    "descr": row['DS_PROJETO_ATIVIDADE'],
                })

    # print(data)
    print("Posting")
    r = perform_post('data', json.dumps(data))
    print("Posted", r.status_code)


# def post_people():
#     people = [
#         {
#             'firstname': 'John',
#             'lastname': 'Doe',
#             'role': ['author'],
#             'location': {'address': '422 South Gay Street', 'city': 'Auburn'},
#             'born': 'Thu, 27 Aug 1970 14:37:13 GMT'
#         },
#         {
#             'firstname': 'Serena',
#             'lastname': 'Love',
#             'role': ['author'],
#             'location': {'address': '363 Brannan St', 'city': 'San Francisco'},
#             'born': 'Wed, 25 Feb 1987 17:00:00 GMT'
#         },
#         {
#             'firstname': 'Mark',
#             'lastname': 'Green',
#             'role': ['copy', 'author'],
#             'location': {'address': '4925 Lacross Road', 'city': 'New York'},
#             'born': 'Sat, 23 Feb 1985 12:00:00 GMT'
#         },
#         {
#             'firstname': 'Julia',
#             'lastname': 'Red',
#             'role': ['copy'],
#             'location': {'address': '98 Yatch Road', 'city': 'San Francisco'},
#             'born': 'Sun, 20 Jul 1980 11:00:00 GMT'
#         },
#         {
#             'firstname': 'Anne',
#             'lastname': 'White',
#             'role': ['contributor', 'copy'],
#             'location': {'address': '32 Joseph Street', 'city': 'Ashfield'},
#             'born': 'Fri, 25 Sep 1970 10:00:00 GMT'
#         },
#     ]

#     r = perform_post('people', json.dumps(people))
#     print "'people' posted", r.status_code

#     valids = []
#     if r.status_code == 201:
#         response = r.json()
#         if response['_status'] == 'OK':
#             for person in response['_items']:
#                 if person['_status'] == "OK":
#                     valids.append(person['_id'])

#     return valids


# def post_works(ids):
#     works = []
#     for i in range(28):
#         works.append(
#             {
#                 'title': 'Book Title #%d' % i,
#                 'description': 'Description #%d' % i,
#                 'owner': random.choice(ids),
#             }
#         )

#     r = perform_post('works', json.dumps(works))
#     print "'works' posted", r.status_code


def perform_post(resource, data):
    headers = {'Content-Type': 'application/json'}
    return requests.post(endpoint(resource), data, headers=headers)


# def delete():
#     r = perform_delete('people')
#     print "'people' deleted", r.status_code
#     r = perform_delete('works')
#     print "'works' deleted", r.status_code


def delete():
    r = perform_delete('data')
    print("'data' deleted", r.status_code)


def perform_delete(resource):
    return requests.delete(endpoint(resource))


def endpoint(resource):
    return '%s/%s/' % (ENTRY_POINT, resource)


# def get():
#     r = requests.get(ENTRY_POINT)
#     print r.json

if __name__ == '__main__':
    delete()
    # ids = post_people()
    # post_works(ids)
    post_data()
