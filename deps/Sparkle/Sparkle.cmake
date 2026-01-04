# Sparkle 2 - Auto-update framework for macOS
# https://sparkle-project.org/
# https://github.com/sparkle-project/Sparkle
#
# Sparkle is distributed as a pre-built framework, so we just download and extract.

if(APPLE)
    set(SPARKLE_VERSION "2.8.1")

    ExternalProject_Add(
        dep_Sparkle
        EXCLUDE_FROM_ALL ON
        URL "https://github.com/sparkle-project/Sparkle/releases/download/${SPARKLE_VERSION}/Sparkle-${SPARKLE_VERSION}.tar.xz"
        URL_HASH SHA256=5cddb7695674ef7704268f38eccaee80e3accbf19e61c1689efff5b6116d85be
        DOWNLOAD_DIR ${DEP_DOWNLOAD_DIR}/Sparkle
        # No build step needed - just install pre-built framework and tools
        CONFIGURE_COMMAND ""
        BUILD_COMMAND ""
        INSTALL_COMMAND ${CMAKE_COMMAND} -E make_directory ${DESTDIR}/Frameworks
        COMMAND ${CMAKE_COMMAND} -E copy_directory
            <SOURCE_DIR>/Sparkle.framework ${DESTDIR}/Frameworks/Sparkle.framework
        # Also install the Sparkle CLI tools (sign_update, generate_appcast) for CI/CD signing
        COMMAND ${CMAKE_COMMAND} -E make_directory ${DESTDIR}/bin
        COMMAND ${CMAKE_COMMAND} -E copy <SOURCE_DIR>/bin/sign_update ${DESTDIR}/bin/sign_update
        COMMAND ${CMAKE_COMMAND} -E copy <SOURCE_DIR>/bin/generate_appcast ${DESTDIR}/bin/generate_appcast
    )
endif()
