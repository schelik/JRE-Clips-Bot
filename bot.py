import argparse
import sys
import os
import re
import datetime
import time

from Chapter import Chapter
from pytube import YouTube, exceptions
from moviepy.editor import *
from slugify import slugify
from PIL import Image, ImageDraw
from Youtube import upload_video


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = ("{0:.1f}").format(bytes_downloaded / total_size * 100)
    progress = int(50 * (bytes_downloaded / total_size))
    status = "█" * progress + "-" * (50 - progress)
    sys.stdout.write(" ↳ |{bar}| {percent}%\r".format(bar=status, percent=percent))
    sys.stdout.flush()


def create_chapters(description):
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
            file_name = slugify(title)
            video_file_name = file_name + ".mp4"
            thumbnail_file_name = file_name + ".png"
            chapters.append(
                Chapter(title, video_file_name, time_in_seconds, thumbnail_file_name)
            )
    return chapters


def convert_video_to_clips(video_path, chapters):
    video_object = VideoFileClip(video_path)
    for i in range(1, len(chapters)):
        curr_chapter = chapters[i]
        bef_chapter = chapters[i - 1]
        chapter_clip = video_object.subclip(
            bef_chapter.start_time, curr_chapter.start_time
        )
        chapter_clip.write_videofile(bef_chapter.video_file_name)
        chapter_clip.save_frame(bef_chapter.thumbnail_file_name)

    final_chapter = chapters[-1]
    final_chapter_clip = video_object.subclip(final_chapter.start_time)
    final_chapter_clip.write_videofile(final_chapter.video_file_name)
    final_chapter_clip.save_frame(final_chapter.thumbnail_file_name, t=10)
    video_object.close()


def add_square_and_image(chapters):
    for chapter in chapters:
        with Image.open(chapter.thumbnail_file_name).convert("RGBA") as base:
            draw = ImageDraw.Draw(base)
            draw.rectangle(((350, 90), (950, 630)), outline="green", width=10)
            base.save(chapter.thumbnail_file_name)


def upload_chapters(chapters):
    for chapter in chapters:
        upload_video(chapter)


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
            # print(yt.title)
            video_path = yt.streams.get_highest_resolution().download(
                filename=slugify(yt.title) + ".mp4"
            )
        except:
            print("Unable to download the video!")
        else:
            print(f"file_path is {video_path}")
            video_description = yt.description
            # video_length = yt.length - 1  # str(datetime.timedelta(seconds=yt.length))
            chapters = create_chapters(video_description)

            if len(chapters) == 0:
                print("Couldn't find timestamps!")
                return

            with open("log.txt", "w") as file:
                for chapter in chapters:
                    file.write(str(chapter.__dict__) + "\n")

            try:
                convert_video_to_clips(video_path, chapters)
            except:
                print("Unable to convert the video to clips!")
            else:
                # add_square_and_image(chapters)
                try:
                    upload_chapters(chapters)
                except:
                    print("Unable to upload chapters")

            delete_clips = input("Do you want to delete the clips(Y/N)?: ")
            if delete_clips == "Y":
                for chapter in chapters:
                    os.remove(chapter.video_file_name)
                    os.remove(chapter.thumbnail_file_name)
                # print(video_path)
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
