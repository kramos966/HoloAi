cimport ccamwirebus
cimport ccamwire
import numpy as np
cimport numpy as np

cdef int GAMMA_OFF = 0
cdef int CAM_STOP = 0
cdef int CAM_RUN = 1
cdef int CONT_SHOT = 0
cdef int SINGLE_SHOT = 1
cdef int CAMWIRE_SUCCESS = 0
cdef int CAMWIRE_FAILURE = 1

ctypedef np.uint16_t DTYPE_t

cdef class CamBus:
    # Type declaration of variables
    cdef ccamwirebus.Camwire_handle* handle_array
    cdef ccamwirebus.Camwire_handle c_handle
    cdef int ncam, current_cam
    cdef int success
    cdef int w, h   # Resolution of the images taken
    cdef void* capbuff  # Capture buffer

    def __cinit__(self):
        # TODO: Test success
        self.handle_array = NULL
        self.c_handle = NULL
        # Preparing camera
        self.handle_array = ccamwirebus.camwire_bus_create(&self.ncam)
        # Select camera. Only the first one found supported right now
        self.current_cam = 0
        self.c_handle = self.handle_array[self.current_cam]
        # Init
        self.success = ccamwire.camwire_create(self.c_handle)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot init camera")

        # Settings.
        # Stopping the camera
        self.success = ccamwire.camwire_set_run_stop(self.c_handle, CAM_STOP)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot stop camera")
        # Turning off gamma
        self.success = ccamwire.camwire_set_gamma(self.c_handle, GAMMA_OFF)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot turn off gamma")
        # Reducing to one the frame buffer
        self.success = ccamwire.camwire_set_num_framebuffers(self.c_handle, 1)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot set single buffer")

        # Setting single shot
        self.success = ccamwire.camwire_set_single_shot(self.c_handle,
                    SINGLE_SHOT)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot set single_shot")
        # Turing on camera again
        self.success = ccamwire.camwire_set_run_stop(self.c_handle, CAM_RUN)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot turn on camera")

        # Getting frame size
        self.success = ccamwire.camwire_get_frame_size(self.c_handle, &self.w,
                                                        &self.h)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot get frame size")

    cpdef capture_frame(self):
        # Defining array of the image
        cdef np.ndarray[np.uint16_t, ndim=2, mode="c"] image = np.empty(
                            (self.h, self.w), dtype=np.uint16)
        # Memoryview of the array
        cdef np.uint16_t[:, ::1] image_buff = image
        cdef np.npy_intp size = self.h * self.w

        # Copying the framebuffer into the direction pointed by the first
        # element of the memoryview
        # Turn on camera
        self.success = ccamwire.camwire_set_run_stop(self.c_handle, CAM_RUN)
        if self.success != CAMWIRE_SUCCESS:
            self.close()
            raise ValueError("Cannot turn on camera")
        # Capture
        self.success = ccamwire.camwire_copy_next_frame(self.c_handle,
                &image_buff[0, 0], NULL)
        if self.success != CAMWIRE_SUCCESS:
            raise ValueError("Cannot capture")

        return image.byteswap() #change endianness

    cpdef close(self):
        self.success = ccamwire.camwire_unpoint_frame(self.c_handle)
        ccamwire.camwire_destroy(self.c_handle)
        ccamwirebus.camwire_bus_destroy()
        print("Camera closed")
