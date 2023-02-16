from PIL import Image
import imagehash
import cv2
import os


def is_similar(image0, image1, cutoff):
    '''перевіряє подібність двох зображень'''

    hash0 = imagehash.average_hash(Image.open(image0))
    hash1 = imagehash.average_hash(Image.open(image1))

    if hash0 - hash1 < cutoff:
        return True
    else:
        return False


def get_frames(file_name):
    '''розбиває гіфку на кадри, зберігає в папку і повертає список кадрів'''

    dir_name = 'downloads/data/' + file_name[:-4]

    cap = cv2.VideoCapture('downloads/' + file_name)

    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except OSError:
        print('Error: Creating directory of data')

    current_frame = 0
    list_frames = []

    while True:
        ret, frame = cap.read()

        if ret:
            if current_frame % 5 == 0:
                name_frame = dir_name + '/frame' + str(current_frame) + '.jpg'
                cv2.imwrite(name_frame, frame)

                if name_frame not in list_frames:
                    list_frames.append(name_frame)

                if current_frame == 0:
                    image0 = name_frame
                else:
                    image1 = name_frame
                    if is_similar(image0, image1, 20):
                        os.remove(image1)
                        list_frames.remove(image1)
                    else:
                        image0 = image1
            current_frame += 1
        else:
            break

    cap.release()

    if len(list_frames) > 3:
        list_frames = [list_frames[0], list_frames[1], list_frames[-1]]

    return list_frames

