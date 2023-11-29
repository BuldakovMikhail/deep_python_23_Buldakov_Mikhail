import cjson

# cjson.loads("ABOBA")
print(cjson.loads('{"aboba": "aaa"}'))
print(cjson.loads('{"aboba": "an", "abobs2a": 2}'))
print(cjson.loads('{"aboba": "an", "abobs2a": "an2"}'))
# cjson.loads('{"aboba": "an",}')
# cjson.loads('{"anopp"}')
print(cjson.loads('{}'))
print(cjson.loads('{"aboba": 22, "aboba": 22}'))
# cjson.loads('{"aboba": 22 "aboba": 22}')

ans = cjson.dumps({"an":2, "anona":"aboba"})
print(ans, type(ans))
