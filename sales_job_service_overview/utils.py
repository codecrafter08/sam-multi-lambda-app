def api_response(success=False, data=None, message=None, error=None, pagination=None):
    response = {
        'success': success,
        'data': data if data is not None else {},
        'message': message if message is not None else 'something went wrong',
        'error': error if error is not None else None,
        'pagination': pagination if pagination is not None else None
    }
    return response 