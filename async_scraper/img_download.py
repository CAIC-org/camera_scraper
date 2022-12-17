# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:37:14 2022

@author: Ron Simenhois

This script download images. It run from a CLI or as a cron job.
It needs to have a json file with camera names and their url with the format:
    {"camera 1 name": "camera url 1",
     "camera 2 name": "camera url 2",
     "camera 3 name": "camera url 3"}
"""

import asyncio
import aiohttp
import os
import json
from datetime import datetime
import argparse
import platform

async def download_image(camera, url, session):
    """
    This function download an image and save it as: {camera name}/{date time}.jpg

    Parameters
    ----------
    camera : str
        The nane of the camera to use as directory name to save the image.
    url : str
        The camera url to download images from.
    session : async aiohttp.ClientSession class
        The http client session object to connect to the url and download the image.

    Returns
    -------
    None.

    """
    async with session.get(url) as response:
        img_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.jpg'
        filename = os.path.join(camera, img_name)
        with open(filename, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)


async def main(args):
    """
    This function gather download tasks from the list of cameras

    Parameters
    ----------
    args : argparse argument
        arguments with a json file name. This file contains a list of cameras
        names and their url. The fdefaultfile name is: camera_urls.json

    Returns
    -------
    None.

    """

    with open(args.camera_list) as f:
        cameras = json.load(f)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for camera, url in cameras.items():
            os.makedirs(camera, exist_ok=True)
            task = asyncio.create_task(download_image(camera, url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':

    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl', '--camera_list', default='camera_urls.json',
                        help='json file with camras urls')
    args = parser.parse_args()
    asyncio.run(main(args))
