# WinSparkle - Auto-update framework for Windows
# https://winsparkle.org/
# https://github.com/vslavik/winsparkle
#
# WinSparkle is distributed as pre-built binaries, so we just download and extract.

if(WIN32)
    set(WINSPARKLE_VERSION "0.8.3")

    # Determine architecture
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(WINSPARKLE_ARCH "x64")
    else()
        set(WINSPARKLE_ARCH "x86")
    endif()

    ExternalProject_Add(
        dep_WinSparkle
        EXCLUDE_FROM_ALL ON
        URL "https://github.com/vslavik/winsparkle/releases/download/v${WINSPARKLE_VERSION}/WinSparkle-${WINSPARKLE_VERSION}.zip"
        URL_HASH SHA256=5ff4a4604c78d57e01d83e22f79f5ffea0c4969defd48b45c69ccbd6b1a71e94
        DOWNLOAD_DIR ${DEP_DOWNLOAD_DIR}/WinSparkle
        # No build step needed - just install pre-built binaries
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ${CMAKE_COMMAND} -E copy_directory
            <SOURCE_DIR>/include ${DESTDIR}/include
        COMMAND ${CMAKE_COMMAND} -E copy
            <SOURCE_DIR>/${WINSPARKLE_ARCH}/Release/WinSparkle.dll ${DESTDIR}/bin/WinSparkle.dll
        COMMAND ${CMAKE_COMMAND} -E copy
            <SOURCE_DIR>/${WINSPARKLE_ARCH}/Release/WinSparkle.lib ${DESTDIR}/lib/WinSparkle.lib
    )
endif()
