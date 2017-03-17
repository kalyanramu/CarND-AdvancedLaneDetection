from Undistorter import Undistorter
from Thresholder import Thresholder
from PerspectiveTransformer import PerspectiveTransformer
from LaneDetector import LaneDetector
from LanePlotter import LanePlotter

class LaneTracker():
	def __init__(self):
		self.undistorter = Undistorter()
		#print("Distortion Initiation Success")
		self.thresholder = Thresholder()
		#print("Thresholding Initiation Success")
		self.ptransformer = PerspectiveTransformer()
		#print("Perspective Transformer Initiation Success")
		self.laneDetector = LaneDetector()
		#print("Lane Detector Initiation Success") 
		self.lanePlotter = LanePlotter()
		#print("Lane Plotter Initiation Success") 

	def process(self,img):
		#Undistort the image to remove camera and lens distortion
		undist_img = self.undistorter.undistort(img)

		#Threshold the image to better identify lane lines
		thresh_img = self.thresholder.threshold(undist_img)

		#Perform perspective transformation so that converging lines become parallel without perspective error
		warp_img = self.ptransformer.warp(thresh_img)

		#Detect the lines through curve fit and curve-fit co-efficients
		left_fit,right_fit = self.laneDetector.detect(warp_img)

		#Get left lane and right lane curvature
		left_curverad,righr_curverad = self.laneDetector.get_curvature(warp_img)

		#Plot the detected lanes on image
		plotted_img = self.lanePlotter.plot(img,left_fit,right_fit,self.ptransformer.Minv)

		return plotted_img

