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

		#Get left lane and right lane curvature, car offset
		left_curverad,right_curverad = self.laneDetector.get_curvature(warp_img)
		car_offset = self.laneDetector.get_car_offset(warp_img)

		#Plot the detected lanes on image
		plotted_img = self.lanePlotter.plotPolygon(img,left_fit,right_fit,self.ptransformer.Minv)

		left_curve_str = "Left ROC: "+str(round(left_curverad,0))+"m"
		right_curve_str = "Right ROC: "+str(round(right_curverad,0))+"m"
		car_offset_str = "Car Offset:"+str(round(car_offset,3))+"m"

		#Overlay text
		text_img = self.lanePlotter.textOverLay(plotted_img,left_curve_str,pos=(100,100))
		text_img = self.lanePlotter.textOverLay(text_img,right_curve_str,pos=(100,150))
		text_img = self.lanePlotter.textOverLay(text_img,car_offset_str,pos=(100,200))
		return plotted_img


