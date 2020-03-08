import cv2
import time
import os
import threading

from yolo import Yolo
from apparel import Apparel
from transcribe import Transcribe

import pyrebase
import json

config = json.loads(open('secret/config.json').read())

firebase = pyrebase.initialize_app(config)

# # build paths
db = firebase.database()
stg = firebase.storage()

lock = threading.Lock()

def add_fb(frames, ls, bb, out_dir, in_dir):
    for i, el in enumerate(ls):
        db.child(f'{out_dir}/{in_dir}/{el}/{frames}').push({
            "y_min": bb[i][0],
            "y_max": bb[i][1],
            "x_min": bb[i][2],
            "x_max": bb[i][3],
        })

def sep_list(lis, num_parts):
    avg = len(lis) / float(num_parts)
    out = []
    last = 0.0

    while last < len(lis):
        out.append(lis[int(last):int(last + avg)])
        last += avg

    return out


def get_frame_features_ls(ls, offset, output_loc, yolo, apparel):
    for block_no, frame_no in enumerate(ls):
        get_frame_features(output_loc, yolo, apparel, block_no + offset, frame_no)


def get_frame_features(output_loc, yolo, apparel, block_no, frame_no):
    filename = output_loc + "/" + str(frame_no + 1) + ".jpg"
    frame = cv2.imread(filename)

    stg.child(f'{output_loc}{frame_no+1}.jpg').put(f'{output_loc}{frame_no+1}.jpg')
    img_url = stg.child(f'{output_loc}{frame_no+1}.jpg').get_url(None)
    db.child(f'{output_loc}/frames/{block_no}/storage_loc').set(img_url)

    # FB - Labels
    label_data = dict({})
    
    lock.acquire()
    labels = yolo.detect(frame)
    lock.release()
    for label in labels:
        if label not in label_data:
            label_data[label] = {}
            label_data[label][str(block_no)] = 1
        else:
            label_data[label][str(block_no)] += 1 

    for key in label_data:
        db.child(f'{output_loc}/labels/{key}').update(label_data[key])

    # FB - Items
    items, items_box = apparel.detect(filename, len(frame), len(frame[0]))
    add_fb(block_no, items, items_box, output_loc, 'ebay')

    # FB - Famous
    celebs, celebs_box = apparel.detect_famous(filename, len(frame), len(frame[0]))
    add_fb(block_no, celebs, celebs_box, output_loc, 'celebrities')

    #os.remove(filename)


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
    
    # Get Transcription
    
    #tr_time_start = time.time()
    stg.child(f'videos/{input_loc}').put(input_loc)
    
    threads = []
    t1 = threading.Thread(
        target=transcribe.recognize_v2, 
        args=(f"gs://videosurfer-bad23.appspot.com/videos/{input_loc}", output_loc))

    #transcribe.recognize_v2(f"gs://videosurfer-bad23.appspot.com/videos/{input_loc}", output_loc)
    #tr_time_end = time.time()
    #print(f'Transcription Time: {tr_time_end-tr_time_start}\n')
    t1.start()
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
    print ("Converting video..\n")

    frame_ls = []
    frame_ls_el = critical_frame
    while(frame_ls_el < video_length):
        frame_ls.append(frame_ls_el)
        frame_ls_el += critical_frame
    
    
    
    for frame_no in frame_ls:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()

        # Write the results back to output location.
        cv2.imwrite(output_loc + "/" + str(frame_no + 1) + ".jpg", frame)
    
    sep_ls = sep_list(frame_ls, 8)
    sep_ls_len = []
    for i in range(len(sep_ls)):
        if i == 0:
            sep_ls_len.append(0)
        else:
            sep_ls_len.append(len(sep_ls[i-1]) + sep_ls_len[i-1])
    
    print(f'Time Before Thread: {time.time()-time_start}')

    for i, ls in enumerate(sep_ls):
        t = threading.Thread(target=get_frame_features_ls, args=(ls, sep_ls_len[i], output_loc, yolo, apparel))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('done')
    time_end = time.time()
    cap.release()
    print (f"Done extracting frames.\nIt took {time_end-time_start} seconds for conversion")
    print (f"Total Frames: {video_length}. Frames Extracted: {len(frame_ls)}")
    t1.join()
    print("Transcription done")
    #os.rmdir(output_loc)


if __name__=="__main__":

    input_loc = 'friends.mp4'
    output_loc = 'friends/'
    video_to_frames(input_loc, output_loc)