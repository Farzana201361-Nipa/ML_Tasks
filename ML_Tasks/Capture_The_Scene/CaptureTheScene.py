#Importing OpenCV library 
import cv2



#Function to extract overlapping frames with 30% overlap ratio
def extract_frames(video_path, overlap=0.3):
    cap= cv2.VideoCapture(video_path)
    
    #Condition to Checks if video is opened or not
    if not cap.isOpened():
        print("Error: Unable to open the video.")
        return []
    
    #Retrives the total framed and fps of the video
    total_frames= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps= cap.get(cv2.CAP_PROP_FPS)
    overlap_frames= int(fps * overlap) 
    
    #Creating list to store extracted frames
    frames = []
    frame_count = 0 
    print("*** video capture started...***")

    while True:
        #Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            break


        if frame_count % overlap_frames == 0:
            #Resizing to reduce memory usage
            frame = cv2.resize(frame, (640, 480))  
            #Adding the frames to list
            frames.append(frame)
        frame_count += 1
        
        #Condition to see the progress after 50 frames
        if frame_count% 50 == 0:
            print(f"{frame_count} frames  extracted and extraction goin on....")

    cap.release()
    print("Frame extraction done")
    return frames





#Function to stitch the frames into panaromic image
def stitch_frames(frames):
    stitcher = cv2.Stitcher_create() 
    # OpenCV stitcher class to stitch multiple frames
    status, result = stitcher.stitch(frames)

#Condition ot check the stitching status
    if status== cv2.Stitcher_OK:
        print("Stitching completed successfully.")
        return result
    else:
        print("Error", status)
        return None




# Main function
def main():
    # video_path= '/Users/farazanaakternipa/Desktop/video.mp4'
    video_path = 'video.mp4'
    
    # print("Extracting frames from the video...")
    #Call extract_frames() function
    frames= extract_frames(video_path, overlap=0.3)

    if not frames:
        print("No frames were extracted. (Exit)")
        return
    total_frames = len(frames)
    print(f"Total extracted frames: {total_frames}.")
    #Calling stitch_frames() function
    stitched_image= stitch_frames(frames)
 
    #Output
    if stitched_image is not None:
        output_path = "output.jpg"
        cv2.imwrite(output_path,stitched_image)
        print(f"Stitching completed. Image saved as '{output_path}'.")
    else:
        print("Stitching failed. So no output image generated.")


if __name__ == "__main__":
    main()
