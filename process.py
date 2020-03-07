import cv2
import time
import os

from yolo import Yolo
from apparel import Apparel
<<<<<<< HEAD
from transcribe import Transcribe
=======
import pyrebase
import json

config = json.loads(open('secret/config.json').read())

firebase = pyrebase.initialize_app(config)

# # build paths
db = firebase.database()
stg = firebase.storage()

def add_fb(frames, ls, bb, out_dir, in_dir):
    for i, el in enumerate(ls):
        db.child(f'{out_dir}/{in_dir}/{el}/{frames}').push({
            "y_min": bb[i][0],
            "y_max": bb[i][1],
            "x_min": bb[i][2],
            "x_max": bb[i][3],
        })
>>>>>>> 39536c27454be01b0dd8ac61d6d155d63a24716c

def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
    except OSError:
        pass

    yolo = Yolo()
    apparel = Apparel()
    transcribe = Transcribe()

    print("Converting video to audio...")
    import moviepy.editor as mp
    #clip = mp.VideoFileClip("friends.mp4")
    #clip.audio.write_audiofile("friends.mp3")
    transcribe.recognize_v2("gs://videosurfer-bad23.appspot.com/friends.mp4")
    quit()

    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    framerate = cap.get(cv2.CAP_PROP_FPS)
    print ("Number of frames: ", video_length)
    print("Frame rate: ", framerate)
    # this is to get a frame for every 2 seconds
    critical_frame = int(framerate) * 2
    print("Critical frame: ", critical_frame)
    count = 0
    frames = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        count = count + 1
        if count % critical_frame == 0:
            # Write the results back to output location.
            filename = output_loc + "/" + str(count + 1) + ".jpg"
            cv2.imwrite(filename, frame)

            stg.child(f'{output_loc}{count+1}.jpg').put(f'{output_loc}{count+1}.jpg')
            img_url = stg.child(f'{output_loc}{count+1}.jpg').get_url(None)
            db.child(f'{output_loc}/frames/{frames}/storage_loc').set(img_url)

            print(yolo.detect(frame))
            # FB - Labels
            label_data = dict({})
            label_data[str(frames)] = dict({})
            for label in yolo.detect(frame):
                if label not in label_data[str(frames)]:
                    label_data[str(frames)][label] = 1
                else:
                    label_data[str(frames)][label] += 1 

            db.child(f'{output_loc}/labels').update(label_data)

            # FB - Items
            items, items_box = apparel.detect(filename, len(frame), len(frame[0]))
            add_fb(frames, items, items_box, output_loc, 'ebay')

            # FB - Famous
            celebs, celebs_box = apparel.detect(filename, len(frame), len(frame[0]))
            add_fb(frames, celebs, celebs_box, output_loc, 'celebrities')

            print(items)
            print(frames)
            
            frames = frames + 1

        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % frames)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break

if __name__=="__main__":

    input_loc = 'friends.mp4'
    output_loc = 'friends/'
    video_to_frames(input_loc, output_loc)