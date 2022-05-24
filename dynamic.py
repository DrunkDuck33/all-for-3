import json

class Dynamic:
    '''
    REPOST:     1
    POST PIC:   2
    POST TXT:   4
    VIDEO:      8
    LONG POST:  64
    '''
    type = -1
    timestamp = -1
    # Summary is going to be posted at last
    summary = ""
    oid = -1

    def __init__(self, type):
        self.type = type

class RepostDynamic(Dynamic):
    def __init__(self, card):
        self.text = ""
        self.origin_type = 0
        self.urls = []

        super().__init__(1)
        self.text = card["item"]["content"]
        self.origin_type = card["item"]["orig_type"]
        if self.origin_type == 2:  # pic
            origin_dynamic = PicDynamic(json.loads(card["origin"])["item"])
            self.urls = origin_dynamic.pic_urls
        elif self.origin_type == 8:
            origin_dynamic = VideoDynamic(json.loads(card["origin"]))
            self.urls = [origin_dynamic.video_url]
        self.summary = self.text + "\n" + "\n".join(self.urls)

class PicDynamic(Dynamic):
    def __init__(self, item):
        self.pic_urls = []
        self.text = ""

        super().__init__(2)
        self.text = item["description"]
        
        for pic in item["pictures"]:
            self.pic_urls.append(pic["img_src"])
        self.summary = self.text

class TextDynamic(Dynamic):
    def __init__(self, item):
        self.text = ""

        super().__init__(4)
        self.text = item["content"]
        self.summary = self.text

class VideoDynamic(Dynamic):
    def __init__(self, card):

        self.title = ""
        self.text = ""
        self.video_url = ""

        super().__init__(8)
        self.title = card["title"]
        self.text = card["desc"]
        self.video_url = card["short_link"]

        self.summary = self.title + " " + self.text

class LongDynamic(Dynamic):
    title = ""
    text = ""
    def __init__(self, card):
        super().__init__(64)
        self.title = card["title"]
        self.text = card["summary"]
        
        self.summary = self.title