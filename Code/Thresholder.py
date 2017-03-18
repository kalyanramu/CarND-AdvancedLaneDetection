import cv2
import numpy as np


class Thresholder:
    def __init__(self):
        self.sobel_kernel = 3

        self.thresh_dir_min = 0.7
        self.thresh_dir_max = 1.3

        self.thresh_mag_min = 20
        self.thresh_mag_max = 100

    def dir_thresh(self, sobelx, sobely):
        abs_sobelx = np.abs(sobelx)
        abs_sobely = np.abs(sobely)
        scaled_sobel = np.arctan2(abs_sobely, abs_sobelx)
        sxbinary = np.zeros_like(scaled_sobel)
        sxbinary[(scaled_sobel >= self.thresh_dir_min) & (scaled_sobel <= self.thresh_dir_max)] = 1

        return sxbinary

    def mag_thresh(self, sobelx, sobely):
        gradmag = np.sqrt(sobelx ** 2 + sobely ** 2)
        scale_factor = np.max(gradmag) / 255
        gradmag = (gradmag / scale_factor).astype(np.uint8)
        binary_output = np.zeros_like(gradmag)
        binary_output[(gradmag >= self.thresh_mag_min) & (gradmag <= self.thresh_mag_max)] = 1

        return binary_output

    def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
        # Convert to grayscale
        #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Apply x or y gradient with the OpenCV Sobel() function
        # and take the absolute value
        if orient == 'x':
            abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
        if orient == 'y':
            abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
        # Rescale back to 8 bit integer
        scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))
        # Create a copy and apply the threshold
        binary_output = np.zeros_like(scaled_sobel)
        # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
        binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
        return binary_output

    def value_thresh(self, img,thresh):
        #expects a grey-scale value image, not color
        binary_output = np.zeros_like(img)
        binary_output[(img > thresh[0]) & (img < thresh[1])] = 1
        return binary_output

    def color_thresh(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        yellow_hsv_low = np.array([15, 100, 120], np.uint8)
        yellow_hsv_high = np.array([80, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(img, yellow_hsv_low, yellow_hsv_high)

        white_hsv_low = np.array([0, 0, 200], np.uint8)
        white_hsv_high = np.array([255, 30, 255], np.uint8)
        white_mask = cv2.inRange(img, white_hsv_low, white_hsv_high)

        binary_output = np.zeros_like(img[:, :, 0])
        binary_output[((yellow_mask != 0) | (white_mask != 0))] = 1
        return binary_output



    def threshold(self, img):
        # hls = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2HLS).astype(np.float)
        # s_channel = hls[:, :, 2]
        #value = self.value_thresh(s_channel,thresh=(100,255))

        sobelx = cv2.Sobel(img[:, :, 2], cv2.CV_64F, 1,0, ksize=self.sobel_kernel)
        sobely = cv2.Sobel(img[:, :, 2], cv2.CV_64F, 0,1, ksize=self.sobel_kernel)

        mag_img = self.mag_thresh(sobelx, sobely)
        dir_img = self.dir_thresh(sobelx, sobely)
        
        color_img = self.color_thresh(img)
        
        combined_img = np.zeros_like(mag_img)
        combined_img[((color_img == 1) & ((mag_img == 1) | (dir_img == 1)))] = 1
        #combined_img[(color_img == 1)&((mag_img == 1) | (dir_img == 1))] = 1
        return combined_img
