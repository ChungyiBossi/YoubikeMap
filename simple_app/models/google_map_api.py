from googlemaps import Client

class GooogleMapClient():
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Client(key=api_key)
        self.fields =  [
            "name",
            "formatted_address",
            "business_status",
            "geometry/location",
            "place_id", 
            "opening_hours",
            "price_level",
            "rating",
            "user_ratings_total",
        ]

    def find_place(self, input_msg, latlng, fields=None):
        input_msg = input_msg.strip()
        if input_msg:
            return self.client.find_place(
                input=input_msg,
                input_type="phonenumber" if input_msg.isnumeric() else "textquery",
                fields=fields if fields else self.fields,
                location_bias=f'point:{latlng[0]},{latlng[1]}'
            )
        else:
            raise ValueError("Input is not provided for client.find_place ")

    def find_places_nearby(self, input_msg, latlng, search_range, open_now=True):
        input_msg = input_msg.strip()
        if input_msg:
            return self.client.places_nearby(
                radius=search_range,
                location=latlng,
                keyword=input_msg,
                open_now=open_now,
            )
        else:
            raise ValueError("Input is not provided for client.find_places_nearby ")


    ## TODO: get for detail from a place_id
    ## TODO: find path according to selection, desctibe it by either words or audio msg



