class RandomUserAgentMiddleware(UserAgentMiddleware):
	def __init__(self, settings, user_agent='Scrapy'):
		super(RandomUserAgentMiddleware, self).__init__()
		self.user_agent = user_agent
	def process_request(self, request, spider):
		ua = random.choice(self.user_agent_list)
		print "*********current user_agent %s*********"%ua
		request.heads.setdefault('User_Agent',ua)
		user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		]