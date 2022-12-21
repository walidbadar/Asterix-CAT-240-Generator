

from cv2 import cv2
import numpy as np
import os
import utility as uti
import coordinates_convert as corcon

#following code is to test and view the raw radar data
fdata_obj = open(r'D:\Softwares\Waleed Docs\Books\Radar\Simulation\RadarDatasets_MKCF\5minutes_600x2048.double.data', 'rb')

while True:
        frame = np.fromfile(fdata_obj, 'float64', 600 * 2048)
        frame = frame.reshape([2048, 600])
        frame = frame.T
        # 通过计算均值mean
        # fmean = frame.mean(axis=1)
        # mfm   = np.tile(fmean,(600,1)).transpose()
        frame = frame - 4000  # frame.mean()
        # 归一化操作
        # dframe is for computing in double float
        dframe = uti.frame_normalize(frame)
        # #uframe is for displaying,optical flow computing and finding blob
        uframe = (dframe * 255).astype(np.uint8)
        canvas_polar = cv2.cvtColor(uframe, cv2.COLOR_GRAY2BGR)
        # cv2.putText(canvas_polar, obj_name+' frame ' + str(frame_id), org=(10, 50),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 255),
        #             thickness=2, lineType=cv2.LINE_AA)
        # cv2.imshow('polar', canvas_polar)

        # for cartesian-coordinates
        dispmat = corcon.polar2disp_njit(dframe, np.array([]))
        dispmat = uti.frame_normalize(dispmat)
        udispmat = (dispmat * 255).astype(np.uint8)
        canvas_disp = cv2.cvtColor(udispmat, cv2.COLOR_GRAY2BGR)
        # cv2.putText(canvas_disp, 'frame ' + str(frame_id), org=(10, 50),
        #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 255),
        #             thickness=2, lineType=cv2.LINE_AA)
        cv2.imshow('disp', canvas_disp)
        # cv2.moveWindow('polar',0,0)
        cv2.waitKey(1)