## Old Item.get()
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item, 200  # no need for jsonify in flask RESTful
        return {"name": None, "price": None}, 404
# get_json() parameters
force will make this work even if header wasn't properly set
silent will return None instead of throwing an error
request_data = request.get_json(force=True, silent=True)