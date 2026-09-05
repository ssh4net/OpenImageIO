# Copyright Contributors to the OpenImageIO project.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/AcademySoftwareFoundation/OpenImageIO

if (JXL_FOUND)
    set (_jxl_definitions USE_JXL)
    if (LINKSTATIC)
        list (APPEND _jxl_definitions JXL_STATIC_DEFINE=1)
    endif ()
    add_oiio_plugin (jxlinput.cpp jxloutput.cpp
                     INCLUDE_DIRS ${JXL_INCLUDES}
                     LINK_LIBRARIES ${JXL_LIBRARIES}
                     DEFINITIONS ${_jxl_definitions})
    unset (_jxl_definitions)
else()
    message (WARNING "JPEG XL plugin will not be built")
endif()
