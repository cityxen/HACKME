import pytchat
import os
chat = pytchat.create(video_id="46oKxQ3fy5E")
while chat.is_alive():
    for c in chat.get().sync_items():
        os.system("sam %s" % c.message)
        print(f"{c.datetime} [{c.author.name}] - {c.message}")

