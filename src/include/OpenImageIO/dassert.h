// Copyright Contributors to the OpenImageIO project.
// SPDX-License-Identifier: Apache-2.0
// https://github.com/AcademySoftwareFoundation/OpenImageIO


#pragma once

#include <cassert>
#include <cstdio>
#include <cstdlib>

#include <OpenImageIO/platform.h>


/// OIIO_ABORT_IF_DEBUG is a call to abort() for debug builds, but does
/// nothing for release builds.
#ifndef NDEBUG
#    define OIIO_ABORT_IF_DEBUG abort()
#else
#    define OIIO_ABORT_IF_DEBUG (void)0
#endif


/// OIIO_ASSERT(condition) checks if the condition is met, and if not,
/// prints an error message indicating the module and line where the error
/// occurred, and additionally aborts if in debug mode. When in release
/// mode, it prints the error message if the condition fails, but does not
/// abort.
///
/// OIIO_ASSERT_MSG(condition,msg,...) lets you add formatted output (a la
/// printf) to the failure message.
#define OIIO_ASSERT(x)                                                  \
    (OIIO_LIKELY(x)                                                     \
         ? ((void)0)                                                    \
         : (std::fprintf(stderr, "%s:%u: %s: Assertion '%s' failed.\n", \
                         __FILE__, __LINE__, OIIO_PRETTY_FUNCTION, #x), \
            OIIO_ABORT_IF_DEBUG))
#define OIIO_ASSERT_MSG(x, msg, ...)                                            \
    (OIIO_LIKELY(x)                                                             \
         ? ((void)0)                                                            \
         : (std::fprintf(stderr, "%s:%u: %s: Assertion '%s' failed: " msg "\n", \
                         __FILE__, __LINE__, OIIO_PRETTY_FUNCTION, #x,          \
                         __VA_ARGS__),                                          \
            OIIO_ABORT_IF_DEBUG))


/// OIIO_DASSERT and OIIO_DASSERT_MSG are the same as OIIO_ASSERT for debug
/// builds (test, print error, abort), but do nothing at all in release
/// builds (not even perform the test). This is similar to C/C++ assert(),
/// but gives us flexibility in improving our error messages. It is also ok
/// to use regular assert() for this purpose if you need to eliminate the
/// dependency on this header from a particular place (and don't mind that
/// assert won't format identically on all platforms).
#ifndef NDEBUG
#    define OIIO_DASSERT OIIO_ASSERT
#    define OIIO_DASSERT_MSG OIIO_ASSERT_MSG
#else
#    define OIIO_DASSERT(x) ((void)sizeof(x))          /*NOLINT*/
#    define OIIO_DASSERT_MSG(x, ...) ((void)sizeof(x)) /*NOLINT*/
#endif


/// Define OIIO_STATIC_ASSERT(cond) as a wrapper around static_assert(cond),
/// with appropriate fallbacks for older C++ standards.
#if (__cplusplus >= 201700L) /* FIXME - guess the token, fix when C++17 */
#    define OIIO_STATIC_ASSERT(cond) static_assert(cond)
#else
#    define OIIO_STATIC_ASSERT(cond) static_assert(cond, "")
#endif

/// Deprecated synonym:
#define OIIO_STATIC_ASSERT_MSG(cond, msg) static_assert(cond, msg)
