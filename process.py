import cv2
import time
import os

from yolo import Yolo
from apparel import Apparel

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
            print(yolo.detect(frame))
            
            print(apparel.detect(filename, len(frame), len(frame[0])))
            print(apparel.detect_famous(filename, len(frame), len(frame[0])))
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