---
name: std-ios-notifications
description: "Push notifications for iOS using UserNotifications framework and APNS. Use when integrating APNS push notifications in iOS applications."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# iOS Notifications

## **Priority: P2 (OPTIONAL)**


## Guidelines

- **Framework**: Use `UserNotifications` for all notification handling.
- **Delegate**: Implement `UNUserNotificationCenterDelegate` for foreground & tap handling.
- **Permissions**: Request `.alert`, `.badge`, `.sound` after priming user.
- **APNs**: Register for remote notifications in `AppDelegate`.
- **Badges**: Manage app icon badges manually (set to 0 to clear).

See APNs registration and permission examples

## Anti-Patterns

- **No Unconditional Requests**: Explain value proposition before system dialog.
- **No Missing Delegate**: Notifications won't trigger foreground callbacks without it.
- **No Forgotten Badge Clear**: User frustration increases if badges persist.

## References

- Implementation Details