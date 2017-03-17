import numpy as np
import cv2

class PerspectiveTransformer:
	def __init__(self):
		# from udacity
		src_pts = np.float32([[585, 460], [203, 720], [1127, 720], [695, 460]])
		dst_pts = np.float32([[320, 0], [320, 720], [960, 720], [960, 0]])

		# Get the perspective transformation matrix
		self.M = cv2.getPerspectiveTransform(src_pts, dst_pts)

		# Get the inverse perspective transformation matrix
		self.Minv = cv2.getPerspectiveTransform(dst_pts, src_pts)

    # Warp perspective example code
    # http://docs.opencv.org/3.1.0/da/d6e/tutorial_py_geometric_transformations.html
    # Compute and apply perpective transform
	def warp(self, img):
		img_size = (img.shape[1], img.shape[0])
		# keep same size as input image
		warped = cv2.warpPerspective(img, self.M, img_size, flags=cv2.INTER_LINEAR)
		return warped

	def unwarp(self, img):
		img_size =(img.shape[1],img.shape[0])
		unwarped = cv2.warpPerspective(img, self.Minv,flags=cv2.INTER_LINEAR)
		return unwarped
