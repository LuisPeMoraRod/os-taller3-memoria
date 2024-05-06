import cv2
import numpy as np
from threading import Thread, Lock
import os
import time

INPUT_IMG = './input_img/image.jpg'
OUTPUT_DIR = './output_img'   
N_THREADS = 10
N_IMAGES = 100

class Image:
    """
    Abstracts CV2 image generation and filter process
    """
    def __init__(self, id: int, input_img: str, output_dir):
        self.id = id
        self.input_img = input_img
        self.output_dir = output_dir 
        self.img = cv2.imread(input_img)
    
    def blur(self):
        try:
            if self.img is not None:
                self.img = cv2.GaussianBlur(self.img, (5,5), 0)
                return
        except:
            print("An error occurred when trying to apply Gaussian blur")
    
    def write_out(self):
        image_name = f'{self.id}_{os.path.basename(self.input_img)}'
        output_filename = os.path.join(self.output_dir, image_name)
        cv2.imwrite(output_filename, self.img)
        print(f'Created {image_name}')

class ImageProcessor(Thread):
    """
    Handles thread that applies filter to a subset of images
    """
    def __init__(self, images, lock):
        Thread.__init__(self)
        self.images = images
        self.lock = lock
    
    def run(self):
        for image in self.images:
            with self.lock:
                image.blur()
                image.write_out()

def get_dataset(input_img: str, output_dir: str) -> list:
    """
    Return list with N image objects 
    """
    dataset = []
    for i in range(N_IMAGES):
        image = Image(id=i, input_img=input_img, output_dir=output_dir) 
        dataset.append(image)
    return dataset

def run_threads(images: list, n_threads: int):
    chunk_size = len(images) // n_threads
    threads = []
    lock = Lock()

    for i in range(n_threads):
        start = i * chunk_size
        end = None if i+1 == n_threads else (i+1) * chunk_size
        thread = ImageProcessor(images[start:end], lock)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def main(input_img: str, output_dir: str, n_threads: int):
    start_time = time.time()
    images = get_dataset(input_img, output_dir)
    run_threads(images, n_threads)
    end_time = time.time()
    print(f"Processing completed in {end_time - start_time} seconds.")

if __name__ == "__main__":
    main(INPUT_IMG, OUTPUT_DIR, N_THREADS)