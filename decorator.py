


# def is_valid_token():
#     def decorator(func):
#         def wrap(request, *args, **kwargs):
#             token = None
#             token = request.META.get('HTTP_AUTHORIZATION', None)
#             if not token:
#                 return jsonify({'message' : 'Token is missing !!'}), 401
#             else:
#                 token = token.replace('Token ', '')
#                 try:
#                     data = jwt.decode(token, app.config['SECRET_KEY'])
#                     current_user = User.query\ 
#                     .filter_by(public_id = data['public_id'])\ 
#                     .first() 
#                     token_data = Token.objects.get(key=token)
#                     if not token_data.user.is_active:
#                         return HttpResponse("Unauthorized, Account Disabled", status=401)
#                 except Token.DoesNotExist:
#                     return HttpResponse("Unauthorized", status=401)
#             return func(request, *args, **kwargs)
#         return wraps(func)(wrap)
#     return decorator