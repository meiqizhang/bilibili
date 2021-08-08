
records = [
    {"id": 1, "parent_id": 0, "text": "第一条留言"},
    {"id": 2, "parent_id": 1, "text": "第一条留言的第一条回复"},
    {"id": 3, "parent_id": 1, "text": "第一条留言的第二条回复"},
    {"id": 4, "parent_id": 2, "text": "第一条留言的第一条回复的回复"},

    {"id": 5, "parent_id": 0, "text": "第二条留言"},
    {"id": 6, "parent_id": 5, "text": "第二条留言的第一条回复"},
    {"id": 7, "parent_id": 5, "text": "第二条留言的第二条回复"},
    {"id": 8, "parent_id": 7, "text": "第二条留言的第二条回复的回复"},
]

'''
    - #1
        #2
            #4
        #3
    - #5
        #6
        #7
            #8
'''