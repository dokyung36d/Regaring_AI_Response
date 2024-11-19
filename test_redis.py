import redis

r = redis.Redis(host='localhost', port=6379, db=0) # 로컬에 띄운 Redis 서버에 연결 
r.set('foo', 'bar')  # key: foo value: bar
print(r.get('foo'))  # foo 라는 키의 value를 가져옴

# import redis
# print(redis.__version__)