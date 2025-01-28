# coding=utf-8
"""
Flash
-----
"""
# Workaround from fork https://github.com/oukiar/plyer/blob/master/plyer/platforms/android/flash.py
# The recent plyer 2.2.0 does not support android.hardware.camera2 and crashes when 
# running on SDK version 23 or later.

#from plyer.facades import Flash

ANDROID = False
try:
    from jnius import autoclass, cast
    from plyer.platforms.android import activity, SDK_INT
    ANDROID = True
except:
    pass


class Flash:
    _camera = None

    if ANDROID:
        if SDK_INT < 23: #use the deprecated api for Android V6 or earlier
            _Camera = autoclass("android.hardware.Camera")
            _CameraParameters = autoclass("android.hardware.Camera$Parameters")
            _SurfaceTexture = autoclass("android.graphics.SurfaceTexture")
        else:
            _Context = autoclass('android.content.Context')

        _PackageManager = autoclass('android.content.pm.PackageManager')
        activity.getPackageManager().hasSystemFeature(_PackageManager.FEATURE_CAMERA_FLASH)

    @staticmethod
    def on():
        if not ANDROID:
            return
        
        if Flash._camera is None:
            Flash._camera_open()
            if not Flash._camera:
                return
        
        if SDK_INT < 23:
            Flash._camera.setParameters(Flash._f_on)
        else:
            Flash._camera.setTorchMode(Flash._cameraid, True)

    @staticmethod
    def off():
        if not ANDROID or not Flash._camera:
            return
            
        if SDK_INT < 23:
            Flash._camera.setParameters(Flash._f_off)
        else:
            Flash._camera.setTorchMode(Flash._cameraid, False)

    @staticmethod
    def release():
        if SDK_INT < 23:
            if not Flash._camera:
                return
            Flash._camera.stopPreview()
            Flash._camera.release()
            Flash._camera = None

    @staticmethod
    def _camera_open():         
        if not ANDROID:
            return
        
        if SDK_INT < 23:   
            Flash.Flash._camera = Flash._Camera.open()
            Flash._f_on = Flash._camera.getParameters()
            Flash._f_off = Flash._camera.getParameters()
            Flash._f_on.setFlashMode(Flash._CameraParameters.FLASH_MODE_TORCH)
            Flash._f_off.setFlashMode(Flash._CameraParameters.FLASH_MODE_OFF)
            Flash._camera.startPreview()
            # Need this for Nexus 5
            Flash._camera.setPreviewTexture(Flash.SurfaceTexture(0))
        else:
            service = activity.getSystemService(Flash._Context.CAMERA_SERVICE)
            Flash._camera = cast('android.hardware.camera2.CameraManager', service)
            Flash._cameraid = Flash._camera.getCameraIdList()[0]

#def instance():
#    return Flash()
