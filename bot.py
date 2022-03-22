import argparse
import sys
import os
import re
import datetime
import time
from pytube import YouTube, exceptions
from moviepy.editor import *


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = ("{0:.1f}").format(bytes_downloaded / total_size * 100)
    progress = int(50 * (bytes_downloaded / total_size))
    status = "█" * progress + "-" * (50 - progress)
    sys.stdout.write(" ↳ |{bar}| {percent}%\r".format(bar=status, percent=percent))
    sys.stdout.flush()


def find_chapters(description):
    lines = description.split("\n")
    chapters = []
    for line in lines:
        time = re.search(r"(^|\s)(?:\d{1}|\d{2}):\d{2}:\d{2}", line)  # ($|\s)
        if time == None:
            time = re.search(r"(^|\s)(?:\d{1}|\d{2}):\d{2}", line)
        if time != None:
            rest = line[time.end() :].strip()
            time = time.group(0).strip()
            start_title_index = 0
            for curr in rest:
                if curr.isdigit() or curr.isalpha():
                    break
                else:
                    start_title_index += 1
            title = rest[start_title_index:]
            time_arr = time.split(":")
            time_in_seconds = 0
            for i in range(len(time_arr)):
                if i == 0:
                    time_in_seconds += int(time_arr[len(time_arr) - i - 1])
                else:
                    time_in_seconds += (60**i) * int(time_arr[len(time_arr) - i - 1])
            chapters.append([time_in_seconds, title])
    return chapters


def convert_video_to_clips(video_path, chapters, clips_path):
    video_object = VideoFileClip(video_path)
    for i in range(1, len(chapters)):
        curr_chapter = chapters[i]
        bef_chapter = chapters[i - 1]
        chapter_clip = video_object.subclip(bef_chapter[0], curr_chapter[0])
        clip_name = bef_chapter[1] + ".mp4"
        chapter_clip.write_videofile(clip_name)
        clips_path.append(clip_name)

    final_chapter = chapters[-1]
    final_chapter_clip = video_object.subclip(final_chapter[0])
    final_chapter_name = final_chapter[1] + ".mp4"
    final_chapter_clip.write_videofile(final_chapter_name)
    clips_path.append(final_chapter_name)


def main(args):
    video_link = args.video
    try:
        yt = YouTube(video_link, on_progress_callback=on_progress)
    except exceptions.RegexMatchError:
        print(f'"{video_link}" is invalid Youtube link!')
    except:
        print("Unable to create YouTube object!")
    else:
        print("Youtube object created...")
        try:
            # pass
            video_path = yt.streams.get_highest_resolution().download()
        except:
            print("Unable to download the video!")
        else:
            print(f"file_path is {video_path}")
            video_description = yt.description
            # video_length = yt.length - 1  # str(datetime.timedelta(seconds=yt.length))
            chapters = find_chapters(video_description)
            for chapter in chapters:
                print(chapter)

            if len(chapters) == 0:
                print("Couldn't find timestamps!")
                return

            clips_path = []
            convert_video_to_clips(video_path, chapters, clips_path)

            delete_clips = input("Do you want to delete the clips?(Y/N): ")
            if delete_clips == "Y":
                print(clips_path)
                for clip_path in clips_path:
                    os.remove(clip_path)
                os.remove(video_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Youtube videos.")
    parser.add_argument(
        "--video",
        required=True,
        help="Please provide a valid youtube video link.",
    )
    args = parser.parse_args()
    main(args)
