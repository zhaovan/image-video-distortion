import os
from distort_image import distort_image_to_cone
import cv2
import numpy as np
import multiprocessing as mp
dir_name = "./video_frames"


results = []


def expect_result(result):
    results.append(result)


if __name__ == "__main__":
    pool = mp.Pool(mp.cpu_count())

    video_frames = os.listdir(dir_name)
    sorted_files = sorted(
        video_frames, key=lambda x: int(os.path.splitext(x)[0]))
    count = 0

    some_results = [pool.apply_async(distort_image_to_cone, args=(["./video_frames/" + file_name]), callback=expect_result)
                    for file_name in sorted_files[:2]]
    pool.close()
    print([result.get(timeout=120) for result in some_results])


# cv2.imwrite("./distorted_video_frames/%d.jpg" %
#             count, distorted_image)
# count += 1


# img_array = []
# new_dir = os.listdir("./distorted_video_frames")
# new_sorted_dir = sorted(l, key=lambda x: int(os.path.splitext(x)[0]))
# for filename in new_sorted_dir:
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     img_array.append(img)


# out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

# for i in range(len(img_array)):
#     out.write(img_array[i])

# out.release()
