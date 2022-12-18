# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:47:40 2022

@author: Ron Simenhois
"""
import cv2
import os
from datetime import datetime

def save_video(images_path,
               fps,
               video_file_name,
               start_time='1970-01-01 00:00',
               end_time=None):
    """
    This function generate a video from images in a given folder

    Parameters
    ----------
    images_path : str
        A path to a folder with images.
    fps : int
        The video's frame per second.
    video_file_name : str
        The generated and saved video path.
    start_time : str, optional
        The date and time when the first frame of the video was taken.
        The default is '1970-01-01 00:00'.
    end_time : str, optional
        The date and time when the lasr frame of the video was taken.
        The default is None. If the value is None, the video will include
        all the images in the folder after the start_time

    Returns
    -------
    str
        The path to the saved video.

    """
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M').strftime('%Y_%m_%d_%H_%M_%S')
    if end_time is None:
        end_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    video_frames = []
    for im in os.listdir(images_path):
        if start_time <= os.path.splitext(im)[0] <= end_time:
            video_frames.append(cv2.imread(os.path.join(images_path, im)))
    if len(video_frames) > 0:
        if not video_file_name.endswith('.mp4'):
            video_file_name += '.mp4'

        heigth, width, ch = video_frames[0].shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename=video_file_name, fourcc=fourcc, fps=fps,
                              frameSize=(width, heigth),isColor=True)
        for frame in video_frames:
            out.write(frame)
        out.release()
        return f'Video saved to {video_file_name}'

