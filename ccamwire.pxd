# camwire.pxd

# Declaratiopns from dc1394 and camwire_handle.h
cdef extern from *:
    ctypedef struct dc1394camera_t:
        pass

cdef extern from *:
    #ctypedef dc1394camera_t*           Camera_handle
    #ctypedef struct camwire_user_data* User_handle

    ctypedef struct Camwire_bus_handle:
        pass

    ctypedef Camwire_bus_handle* Camwire_handle

# camwire.h
cdef extern from "<camwire/camwire.h>":
    ctypedef struct Camwire_id:
        pass


    ctypedef enum Camwire_pixel:
        pass


    ctypedef enum Camwire_tiling:
        pass


    ctypedef struct Camwire_state:
        pass

    ctypedef struct Camwire_conf:
        pass

    int camwire_create(const Camwire_handle c_handle)

    int camwire_create_from_struct(const Camwire_handle c_handle,
			           const Camwire_state *set)

    void camwire_destroy(const Camwire_handle c_handle)

    int camwire_get_state(const Camwire_handle c_handle, Camwire_state *set)

    int camwire_set_state(const Camwire_handle c_handle, const Camwire_state *set)

    #int camwire_read_state_from_file(FILE *infile, Camwire_state *set)

    #int camwire_write_state_to_file(FILE *outfile, const Camwire_state *set)

    int camwire_get_config(const Camwire_handle c_handle, Camwire_conf *cfg)

    #int camwire_write_config_to_file(FILE *outfile, const Camwire_conf *cfg)

    int camwire_get_identifier(const Camwire_handle c_handle, Camwire_id *identifier)

    int camwire_get_stateshadow(const Camwire_handle c_handle, int *shadow)

    int camwire_set_stateshadow(const Camwire_handle c_handle, const int shadow)

    int camwire_get_num_framebuffers(const Camwire_handle c_handle,
				     int *num_frame_buffers)

    int camwire_set_num_framebuffers(const Camwire_handle c_handle,
				     const int num_frame_buffers)

    int camwire_get_framebuffer_lag(const Camwire_handle c_handle, int *buffer_lag)

    int camwire_flush_framebuffers(const Camwire_handle c_handle, const int num_to_flush,
			           int *num_flushed, int *buffer_lag)

    int camwire_get_frame_offset(const Camwire_handle c_handle, int *left, int *top)

    int camwire_set_frame_offset(const Camwire_handle c_handle, const int left,
			         const int top)

    int camwire_get_frame_size(const Camwire_handle c_handle, int *width, int *height)

    int camwire_set_frame_size(const Camwire_handle c_handle, const int width,
			       const int height)

    int camwire_get_pixel_coding(const Camwire_handle c_handle, Camwire_pixel *coding)

    int camwire_set_pixel_coding(const Camwire_handle c_handle,
			         const Camwire_pixel coding)

    int camwire_get_pixel_tiling(const Camwire_handle c_handle, Camwire_tiling *tiling)

    int camwire_pixel_depth(const Camwire_pixel coding, int *depth)

    int camwire_get_framerate(const Camwire_handle c_handle, double *framerate)

    int camwire_set_framerate(const Camwire_handle c_handle, const double framerate)

    int camwire_get_shutter(const Camwire_handle c_handle, double *shutter)

    int camwire_set_shutter(const Camwire_handle c_handle, const double shutter)

    int camwire_get_trigger_source(const Camwire_handle c_handle, int *external)

    int camwire_set_trigger_source(const Camwire_handle c_handle, const int external)

    int camwire_get_trigger_polarity(const Camwire_handle c_handle, int *rising);

    int camwire_set_trigger_polarity(const Camwire_handle c_handle, const int rising)

    int camwire_get_gain(const Camwire_handle c_handle, double *gain);

    int camwire_set_gain(const Camwire_handle c_handle, const double gain)

    int camwire_get_brightness(const Camwire_handle c_handle, double *brightness)

    int camwire_set_brightness(const Camwire_handle c_handle,
			       const double brightness)

    int camwire_get_white_balance(const Camwire_handle c_handle, double bal[2])

    int camwire_set_white_balance(const Camwire_handle c_handle, const double bal[2])

    int camwire_get_gamma(const Camwire_handle c_handle, int *gamma_on)

    int camwire_set_gamma(const Camwire_handle c_handle, const int gamma_on)

    int camwire_inv_gamma(const Camwire_handle c_handle, const void *cam_buf,
		          void *lin_buf, const unsigned long max_val)

    int camwire_get_colour_correction(const Camwire_handle c_handle, int *corr_on)

    int camwire_set_colour_correction(const Camwire_handle c_handle, const int corr_on)

    int camwire_get_colour_coefficients(const Camwire_handle c_handle, double coef[9])

    int camwire_set_colour_coefficients(const Camwire_handle c_handle,
				        const double coef[9])

    int camwire_get_single_shot(const Camwire_handle c_handle, int *single_shot_on)

    int camwire_set_single_shot(const Camwire_handle c_handle,
			        const int single_shot_on)

    int camwire_get_run_stop(const Camwire_handle c_handle, int *runsts)

    int camwire_set_run_stop(const Camwire_handle c_handle, const int runsts);

    int camwire_copy_next_frame(const Camwire_handle c_handle, void *buffer,
			        int *buffer_lag)

    int camwire_point_next_frame(const Camwire_handle c_handle, void **buf_ptr,
			         int *buffer_lag)

    int camwire_point_next_frame_poll(const Camwire_handle c_handle, void **buf_ptr,
				      int *buffer_lag)

    int camwire_unpoint_frame(const Camwire_handle c_handle)

    int camwire_get_framenumber(const Camwire_handle c_handle, long *framenumber)

    #int camwire_get_timestamp(const Camwire_handle c_handle, struct timespec *timestamp)

    int camwire_debug_print_status(const Camwire_handle c_handle)

    #int camwire_version(char const **version_str)

