
s = 'a|aa|i|ii|u|uu|rq|ee|ei|o|ou|ax|a&mq|a&q|a&hq|aa&mq|aa&q|aa&hq|i&mq|ii&q|ii&hq|i&q|i&hq|ii&mq|u&mq|u&q|u&hq|uu&mq|uu&q|uu&hq|rq&mq|rq&q|rq&hq|ee&mq|ee&q|ee&hq|ei&mq|ei&q|ei&hq|o&mq|o&q|o&hq|ou&mq|ou&q|ou&hq'
s = s.split('|')
l = sorted(s, key = lambda x : (len(x),x), reverse = True)
print(len(l))
print('|'.join(l))