from logparser import LogParser

log_parser = LogParser()

log = '127.0.0.1-- 224 "CONNECT plugins.jetbrains.com:443 HTTP/1.1" 405[10/Jun/2024:12:26:37 +0300]'
log2 = '::1- - 46 "GET / HTTP/1.1" 200[10/Jun/2024:12:27:06 +0300]'

print(log_parser.parse_log(log))
print(log_parser.parse_log(log2))

