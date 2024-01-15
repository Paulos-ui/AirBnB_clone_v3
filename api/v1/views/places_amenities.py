#!/usr/bin/python3
"""This handles all default API actions for the link between Place and
   Amenity objects
"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list all amenities of a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", id).to_dict for id
                     in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_del(place_id, amenity_id):
    """This deletes an amenity obj to a Place"""
    place = storage.get('Place', place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            amen_idx = place.amenity_ids.index(amenity_id)
            place.amenity_ids.pop(amen_idx)

        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_place_link(place_id, amenity_id):
    """Links an amenity with a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
