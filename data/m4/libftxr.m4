dnl Functions for libftxr
dnl
dnl Version: 20170907

dnl Function to detect if libftxr is available
dnl ac_libftxr_dummy is used to prevent AC_CHECK_LIB adding unnecessary -l<library> arguments
AC_DEFUN([AX_LIBFTXR_CHECK_LIB],
  [dnl Check if parameters were provided
  AS_IF(
    [test "x$ac_cv_with_libftxr" != x && test "x$ac_cv_with_libftxr" != xno && test "x$ac_cv_with_libftxr" != xauto-detect],
    [AS_IF(
      [test -d "$ac_cv_with_libftxr"],
      [CFLAGS="$CFLAGS -I${ac_cv_with_libftxr}/include"
      LDFLAGS="$LDFLAGS -L${ac_cv_with_libftxr}/lib"],
      [AC_MSG_WARN([no such directory: $ac_cv_with_libftxr])
      ])
    ])

  AS_IF(
    [test "x$ac_cv_with_libftxr" = xno],
    [ac_cv_libftxr=no],
    [dnl Check for a pkg-config file
    AS_IF(
      [test "x$cross_compiling" != "xyes" && test "x$PKGCONFIG" != "x"],
      [PKG_CHECK_MODULES(
        [libftxr],
        [libftxr >= 20120527],
        [ac_cv_libftxr=yes],
        [ac_cv_libftxr=no])
      ])

    AS_IF(
      [test "x$ac_cv_libftxr" = xyes],
      [ac_cv_libftxr_CPPFLAGS="$pkg_cv_libftxr_CFLAGS"
      ac_cv_libftxr_LIBADD="$pkg_cv_libftxr_LIBS"],
      [dnl Check for headers
      AC_CHECK_HEADERS([libftxr.h])

    AS_IF(
        [test "x$ac_cv_header_libftxr_h" = xno],
        [ac_cv_libftxr=no],
        [dnl Check for the individual functions
        ac_cv_libftxr=yes

        AC_CHECK_LIB(
          ftxr,
          libftxr_get_version,
          [ac_cv_libftxr_dummy=yes],
          [ac_cv_libftxr=no])

        dnl TODO add functions

        ac_cv_libftxr_LIBADD="-lftxr"
        ])
      ])
    ])

  AS_IF(
    [test "x$ac_cv_libftxr" = xyes],
    [AC_DEFINE(
      [HAVE_LIBFTXR],
      [1],
      [Define to 1 if you have the `ftxr' library (-lftxr).])
    ])

  AS_IF(
    [test "x$ac_cv_libftxr" = xyes],
    [AC_SUBST(
      [HAVE_LIBFTXR],
      [1]) ],
    [AC_SUBST(
      [HAVE_LIBFTXR],
      [0])
    ])
  ])

dnl Function to detect if libftxr dependencies are available
AC_DEFUN([AX_LIBFTXR_CHECK_LOCAL],
  [dnl No additional checks.

  ac_cv_libftxr_CPPFLAGS="-I../libftxr";
  ac_cv_libftxr_LIBADD="../libftxr/libftxr.la";

  ac_cv_libftxr=local
  ])

dnl Function to detect how to enable libftxr
AC_DEFUN([AX_LIBFTXR_CHECK_ENABLE],
  [AX_COMMON_ARG_WITH(
    [libftxr],
    [libftxr],
    [search for libftxr in includedir and libdir or in the specified DIR, or no if to use local version],
    [auto-detect],
    [DIR])

  dnl Check for a shared library version
  AX_LIBFTXR_CHECK_LIB

  dnl Check if the dependencies for the local library version
  AS_IF(
    [test "x$ac_cv_libftxr" != xyes],
    [AX_LIBFTXR_CHECK_LOCAL

    AC_DEFINE(
      [HAVE_LOCAL_LIBFTXR],
      [1],
      [Define to 1 if the local version of libftxr is used.])
    AC_SUBST(
      [HAVE_LOCAL_LIBFTXR],
      [1])
    ])

  AM_CONDITIONAL(
    [HAVE_LOCAL_LIBFTXR],
    [test "x$ac_cv_libftxr" = xlocal])
  AS_IF(
    [test "x$ac_cv_libftxr_CPPFLAGS" != "x"],
    [AC_SUBST(
      [LIBFTXR_CPPFLAGS],
      [$ac_cv_libftxr_CPPFLAGS])
    ])
  AS_IF(
    [test "x$ac_cv_libftxr_LIBADD" != "x"],
    [AC_SUBST(
      [LIBFTXR_LIBADD],
      [$ac_cv_libftxr_LIBADD])
    ])

  AS_IF(
    [test "x$ac_cv_libftxr" = xyes],
    [AC_SUBST(
      [ax_libftxr_pc_libs_private],
      [-lftxr])
    ])

  AS_IF(
    [test "x$ac_cv_libftxr" = xyes],
    [AC_SUBST(
      [ax_libftxr_spec_requires],
      [libftxr])
    AC_SUBST(
      [ax_libftxr_spec_build_requires],
      [libftxr-devel])
    ])
  ])

