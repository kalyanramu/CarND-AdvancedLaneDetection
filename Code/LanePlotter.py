
import numpy as np
import cv2

class LanePlotter():
	def __init__(self,alpha=0.3,color=(0,255,0)):
		self.alpha = alpha
		self.poly_color = color

	def plot(self, undist_img, left_fit, right_fit, Minv):
		color_warp = np.zeros_like(undist_img).astype(np.uint8)

		fity = np.linspace(0, undist_img.shape[0] - 1, undist_img.shape[0])
		left_fitx = left_fit[0] * fity ** 2 + left_fit[1] * fity + left_fit[2]
		right_fitx = right_fit[0] * fity ** 2 + right_fit[1] * fity + right_fit[2]

		# Recast the x and y points into usable format for cv2.fillPoly()
		pts_left = np.array([np.transpose(np.vstack([left_fitx, fity]))])
		pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, fity])))])
		pts = np.hstack((pts_left, pts_right))
		pts = np.array(pts, dtype=np.int32)

		cv2.fillPoly(color_warp, pts, self.poly_color)

		# Warp the blank back to original image space using inverse perspective matrix (Minv)
		newwarp = cv2.warpPerspective(color_warp, Minv, (undist_img.shape[1], undist_img.shape[0]))
		# Combine the result with the original image
		result = cv2.addWeighted(undist_img, 1, newwarp, self.alpha, 0)

		return result