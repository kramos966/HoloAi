cdef extern from *:
    ctypedef struct dc1394camera_t:
        pass

cdef extern from *:
    #ctypedef dc1394camera_t*           Camera_handle
    #ctypedef struct camwire_user_data* User_handle

    ctypedef struct Camwire_bus_handle:
        pass

    ctypedef Camwire_bus_handle* Camwire_handle

    #inline Camera_handle camwire_handle_get_camera(const Camwire_handle c_handle)

    #inline User_handle camwire_bus_get_userdata(const Camwire_handle c_handle)

    #int camwire_bus_set_userdata(const Camwire_handle c_handle, User_handle user_data)







cdef extern from "<camwire/camwirebus.h>":
    Camwire_handle* camwire_bus_create(int* num_handles)

    int camwire_bus_exists()

    void camwire_bus_destroy()

    void camwire_bus_reset()
