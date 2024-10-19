import feed
#Rerun feed part 1


with open("all_video_ids.txt", "r") as file:
     content= file.read().splitlines() 

final_video_id = []
with open("all_video_ids_from_search.txt", "r") as file:
    content_small = file.read().splitlines() 

    for video_id in content_small:
        if video_id not in content:
            final_video_id.append(video_id)

for i in final_video_id:
    print(i)

#dictionary with search videos
videos =feed.videos

# Create a copy of the dictionary keys to avoid modifying the dictionary while iterating
video_keys = list(videos.keys())

# Iterate over the copied keys and remove from 'videos' if not in 'final_video_id'
for video_id in video_keys:
    if video_id not in final_video_id:
        videos.pop(video_id)

'''
print(videos)
print()
print(len(videos))
print()
print(len(final_video_id ))
'''

html_content = "<html><body><h1>YouTube Thumbnails</h1><div style='display: flex; flex-wrap: wrap;'>"

for video_id, title in videos.items():
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    link = f"https://www.youtube.com/watch?v={video_id}"  # Create link for each video
    html_content += f"<div style='margin: 10px; text-align: center;'>"
    html_content += f"<a href='{link}' target='_blank'>"  # Make the thumbnail clickable
    html_content += f"<img src='{thumbnail_url}' alt='{title}' style='width: 150px; height: auto;'></a>"
    html_content += f"<p>{title}</p></div>"

html_content += "</div></body></html>"

with open("thumbnails.html", "w", encoding='utf-8') as file:
    file.write(html_content)

print("HTML file 'thumbnails.html' created. Open it in your browser.")

































