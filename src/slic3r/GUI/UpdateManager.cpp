#include "UpdateManager.hpp"
#include "libslic3r/libslic3r.h"

#include <boost/log/trivial.hpp>

// Windows implementation uses WinSparkle
#if defined(_WIN32) && defined(ORCA_HAS_WINSPARKLE)
#include <winsparkle.h>
#include <windows.h>
#endif

namespace Slic3r {
namespace GUI {

// Static member definitions (defined in UpdateManagerMac.mm for macOS)
#if !defined(__APPLE__)
bool UpdateManager::s_initialized = false;
std::string UpdateManager::s_appcast_url;
std::string UpdateManager::s_public_key;
#endif

#if defined(_WIN32) && defined(ORCA_HAS_WINSPARKLE)
// ============================================================================
// Windows Implementation (WinSparkle)
// ============================================================================

void UpdateManager::init(const std::string& appcast_url, const std::string& public_key)
{
    if (s_initialized) {
        BOOST_LOG_TRIVIAL(warning) << "UpdateManager::init called multiple times";
        return;
    }

    s_appcast_url = appcast_url;
    s_public_key = public_key;

    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Initializing WinSparkle with appcast URL: " << appcast_url;

    // Set application details for registry storage
    win_sparkle_set_app_details(L"SoftFever", L"OrcaSlicer", L"" SLIC3R_VERSION);

    // Set appcast URL
    win_sparkle_set_appcast_url(appcast_url.c_str());

    // Set EdDSA public key for signature verification
    if (!public_key.empty()) {
        win_sparkle_set_dsa_pub_pem(public_key.c_str());
        BOOST_LOG_TRIVIAL(info) << "UpdateManager: EdDSA public key configured";
    } else {
        BOOST_LOG_TRIVIAL(warning) << "UpdateManager: No public key provided, signature verification disabled";
    }

    // Initialize WinSparkle (starts background thread)
    win_sparkle_init();
    s_initialized = true;

    BOOST_LOG_TRIVIAL(info) << "UpdateManager: WinSparkle initialized successfully";
}

void UpdateManager::check_for_updates_interactive()
{
    if (!s_initialized) {
        BOOST_LOG_TRIVIAL(warning) << "UpdateManager::check_for_updates_interactive called before init";
        return;
    }

    BOOST_LOG_TRIVIAL(info) << "UpdateManager: User-triggered update check";
    win_sparkle_check_update_with_ui();
}

void UpdateManager::check_for_updates_background()
{
    if (!s_initialized) {
        BOOST_LOG_TRIVIAL(warning) << "UpdateManager::check_for_updates_background called before init";
        return;
    }

    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Background update check";
    win_sparkle_check_update_without_ui();
}

void UpdateManager::shutdown()
{
    if (!s_initialized) {
        return;
    }

    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Shutting down WinSparkle";
    win_sparkle_cleanup();
    s_initialized = false;
}

void UpdateManager::set_automatic_check_enabled(bool enabled)
{
    // WinSparkle manages automatic checks via registry settings
    // The user can configure this through WinSparkle's own preferences dialog
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Automatic check enabled: " << enabled;
}

#elif defined(__linux__)
// ============================================================================
// Linux Implementation (Stub - AppImageUpdate deferred)
// ============================================================================

void UpdateManager::init(const std::string& appcast_url, const std::string& public_key)
{
    s_appcast_url = appcast_url;
    s_public_key = public_key;
    s_initialized = true;
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Linux auto-update not yet implemented (stub)";
}

void UpdateManager::check_for_updates_interactive()
{
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Linux interactive update check not implemented";
    // TODO: Implement AppImageUpdate integration
    // For now, fall back to the old behavior (handled by caller)
}

void UpdateManager::check_for_updates_background()
{
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Linux background update check not implemented";
    // TODO: Implement AppImageUpdate integration
}

void UpdateManager::shutdown()
{
    s_initialized = false;
}

void UpdateManager::set_automatic_check_enabled(bool enabled)
{
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Linux automatic check not implemented";
}

#elif !defined(__APPLE__)
// ============================================================================
// Fallback Implementation (No auto-update support)
// ============================================================================

void UpdateManager::init(const std::string& appcast_url, const std::string& public_key)
{
    s_appcast_url = appcast_url;
    s_public_key = public_key;
    s_initialized = true;
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: No auto-update support on this platform";
}

void UpdateManager::check_for_updates_interactive()
{
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Interactive update check not available";
}

void UpdateManager::check_for_updates_background()
{
    BOOST_LOG_TRIVIAL(info) << "UpdateManager: Background update check not available";
}

void UpdateManager::shutdown()
{
    s_initialized = false;
}

void UpdateManager::set_automatic_check_enabled(bool enabled)
{
    // No-op
}

#endif

// Note: macOS implementation is in UpdateManagerMac.mm

} // namespace GUI
} // namespace Slic3r
