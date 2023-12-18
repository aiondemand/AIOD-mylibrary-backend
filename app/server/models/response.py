def ResponseModel(data, code = 200):
    return {
        "data": data,
        "code": code
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}