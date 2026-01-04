#pragma once

#include <string>

namespace Slic3r {
namespace GUI {

/// Cross-platform auto-update manager abstraction.
/// Uses WinSparkle on Windows, Sparkle 2 on macOS.
/// Linux support deferred (stub implementation).
class UpdateManager {
public:
    /// Initialize the platform-specific updater.
    /// Must be called once during application startup (GUI_App::on_init_inner).
    /// @param appcast_url URL to the appcast XML feed
    /// @param public_key Base64-encoded Ed25519 public key for signature verification
    static void init(const std::string& appcast_url, const std::string& public_key);

    /// Manual check triggered by user (Help -> Check for Updates).
    /// Shows UI regardless of whether an update is available.
    static void check_for_updates_interactive();

    /// Background check called on application startup.
    /// Only shows UI if an update is available.
    static void check_for_updates_background();

    /// Cleanup on application exit.
    static void shutdown();

    /// Enable or disable automatic update checks.
    /// @param enabled If true, automatically check for updates periodically
    static void set_automatic_check_enabled(bool enabled);

private:
    static bool s_initialized;
    static std::string s_appcast_url;
    static std::string s_public_key;
};

} // namespace GUI
} // namespace Slic3r
