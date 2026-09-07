---
name: video-dynamic-ad-insertion
description: "Integrate a dynamic ad insertion SDK to load HLS or DASH streams with ads into web, mobile, or TV apps. Use when a video player needs to load and play streams for livestream events or video on demand."
license: Apache-2.0
tags:
- video
- ads
- streaming
---

# IMA DAI SDK

Use the IMA DAI SDK to load HLS or DASH streams into the app for:

*   **Livestream events** configured in Google Ad Manager.
*   **Video on demand (VOD)** content ingested into Google Ad Manager.

## Prerequisites

Review the platform-specific integration guides for the target platforms:

*   **Web/HTML5/ReactJs/NodeJs/Angular:** Read
    StreamManager guide for loading
    stream URL from Google full-service DAI into `<video>` element.

*   **ChromeCast:** Read
    StreamManager guide for
    integrating the IMA DAI SDK into a ChromeCast Web Receiver.

*   **Android:** Read
    ImaServerSideAdInsertionMediaSource guide
    for integrating Media3 Exoplayer IMA extension.

*   **iOS/tvOS:** Read
    IMAStreamRequest guide for
    playing streams with `AVPlayer`.

*   **Roku:** Read StreamManager guide
    for implementing DAI on Roku SceneGraph.

## Quick start (general workflow)

1.  Import the SDK
2.  Initialize the SDK
3.  Add stream event listeners
4.  Set up timed metadata forwarding
5.  Make a stream request
6.  Clean up SDK resources when the stream fails or the user leaves the stream.
