from unittest import TestCase
import FaceRecognition.faceDetectAndTrack as fd
import numpy as np


class TestFacePos(TestCase):
    def test_update_on_same_face1(self):
        fd.maxFaceDistance = 30
        facePos = fd.FaceInfo(np.array((20, 20)), "A")
        self.assertTrue(facePos.update_on_same_face(np.array((20,20))))
        self.assertTrue(facePos.update_on_same_face(np.array((40,40))))

        self.assertFalse(facePos.update_on_same_face(np.array((100, 100))))

    def test_update_on_same_face2(self):
        fd.maxFaceDistance = 10
        facePos = fd.FaceInfo(np.array((20, 20)), "A")
        self.assertTrue(facePos.update_on_same_face(np.array((20,20))))
        self.assertFalse(facePos.update_on_same_face(np.array((40,40))))

        self.assertFalse(facePos.update_on_same_face(np.array((100, 100))))


    def test_calcCenter(self):
        center = fd.calc_center((0,0,10,10))

        self.assertEqual(center,(5,5))

        center = fd.calc_center((10,15,50,10))


        self.assertEqual((35,20),center)