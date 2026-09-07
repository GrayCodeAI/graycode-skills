---
name: vue-composable-utilities
description: "Apply VueUse composables in Vue/Nuxt for state, browser APIs, sensors, reactivity, and animation concisely."
license: MIT
tags:
- vue
- composables
- reactivity
- nuxt
- state
---

# VueUse Functions

This skill is a decision-and-implementation guide for VueUse composables in Vue.js / Nuxt projects. It maps requirements to the most suitable VueUse function, applies the correct usage pattern, and prefers composable-based solutions over bespoke code to keep implementations concise, maintainable, and performant.

## When to Apply

- Apply this skill whenever assisting user development work in Vue.js / Nuxt.
- Always check first whether a VueUse function can implement the requirement.
- Prefer VueUse composables over custom code to improve readability, maintainability, and performance.
- Map requirements to the most appropriate VueUse function and follow the functionâ€™s invocation rule.
- Please refer to the `Invocation` field in the below functions table. For example:
  - `AUTO`: Use automatically when applicable.
  - `EXTERNAL`: Use only if the user already installed the required external dependency; otherwise reconsider, and ask to install only if truly needed.
  - `EXPLICIT_ONLY`: Use only when explicitly requested by the user.
  > *NOTE* User instructions in the prompt or `AGENTS.md` may override a functionâ€™s default `Invocation` rule.

## Functions

All functions listed below are part of the [VueUse](https://vueuse.org/) library, each section categorizes functions based on their functionality.

IMPORTANT: Each function entry includes a short `Description` and a detailed `Reference`. When using any function, always consult the corresponding document in `./references` for Usage details and Type Declarations.

### State

| Function | Description | Invocation |
|----------|-------------|------------|
| `createGlobalState` | Keep states in the global scope to be reusable across Vue instances | AUTO |
| `createInjectionState` | Create global state that can be injected into components | AUTO |
| `createSharedComposable` | Make a composable function usable with multiple Vue instances | AUTO |
| `injectLocal` | Extended `inject` with ability to call `provideLocal` to provide the value in the same component | AUTO |
| `provideLocal` | Extended `provide` with ability to call `injectLocal` to obtain the value in the same component | AUTO |
| `useAsyncState` | Reactive async state | AUTO |
| `useDebouncedRefHistory` | Shorthand for `useRefHistory` with debounced filter | AUTO |
| `useLastChanged` | Records the timestamp of the last change | AUTO |
| `useLocalStorage` | Reactive [LocalStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) | AUTO |
| `useManualRefHistory` | Manually track the change history of a ref when the user calls `commit()` | AUTO |
| `useRefHistory` | Track the change history of a ref | AUTO |
| `useSessionStorage` | Reactive [SessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) | AUTO |
| `useStorage` | Create a reactive ref that can be used to access & modify [LocalStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) or [SessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage) | AUTO |
| `useStorageAsync` | Reactive Storage with async support | AUTO |
| `useThrottledRefHistory` | Shorthand for `useRefHistory` with throttled filter | AUTO |

### Elements

| Function | Description | Invocation |
|----------|-------------|------------|
| `useActiveElement` | Reactive `document.activeElement` | AUTO |
| `useDocumentVisibility` | Reactively track [`document.visibilityState`](https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilityState) | AUTO |
| `useDraggable` | Make elements draggable | AUTO |
| `useDropZone` | Create a zone where files can be dropped | AUTO |
| `useElementBounding` | Reactive [bounding box](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) of an HTML element | AUTO |
| `useElementSize` | Reactive size of an HTML element | AUTO |
| `useElementVisibility` | Tracks the visibility of an element within the viewport | AUTO |
| `useIntersectionObserver` | Detects changes to a target element's visibility | AUTO |
| `useMouseInElement` | Reactive mouse position related to an element | AUTO |
| `useMutationObserver` | Watch for changes being made to the DOM tree | AUTO |
| `useParentElement` | Get parent element of the given element | AUTO |
| `useResizeObserver` | Reports changes to the dimensions of an Element's content or the border-box | AUTO |
| `useWindowFocus` | Reactively track window focus with `window.onfocus` and `window.onblur` events | AUTO |
| `useWindowScroll` | Reactive window scroll | AUTO |
| `useWindowSize` | Reactive window size | AUTO |

### Browser

| Function | Description | Invocation |
|----------|-------------|------------|
| `useBluetooth` | Reactive [Web Bluetooth API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API) | AUTO |
| `useBreakpoints` | Reactive viewport breakpoints | AUTO |
| `useBroadcastChannel` | Reactive [BroadcastChannel API](https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel) | AUTO |
| `useBrowserLocation` | Reactive browser location | AUTO |
| `useClipboard` | Reactive [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) | AUTO |
| `useClipboardItems` | Reactive [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) | AUTO |
| `useColorMode` | Reactive color mode (dark / light / customs) with auto data persistence | AUTO |
| `useCssSupports` | SSR compatible and reactive [`CSS.supports`](https://developer.mozilla.org/docs/Web/API/CSS/supports_static) | AUTO |
| `useCssVar` | Manipulate CSS variables | AUTO |
| `useDark` | Reactive dark mode with auto data persistence | AUTO |
| `useEventListener` | Use EventListener with ease | AUTO |
| `useEyeDropper` | Reactive [EyeDropper API](https://developer.mozilla.org/en-US/docs/Web/API/EyeDropper_API) | AUTO |
| `useFavicon` | Reactive favicon | AUTO |
| `useFileDialog` | Open file dialog with ease | AUTO |
| `useFileSystemAccess` | Create and read and write local files with [FileSystemAccessAPI](https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API) | AUTO |
| `useFullscreen` | Reactive [Fullscreen API](https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API) | AUTO |
| `useGamepad` | Provides reactive bindings for the [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) | AUTO |
| `useImage` | Reactive load an image in the browser | AUTO |
| `useMediaControls` | Reactive media controls for both `audio` and `video` elements | AUTO |
| `useMediaQuery` | Reactive [Media Query](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Testing_media_queries) | AUTO |
| `useMemory` | Reactive Memory Info | AUTO |
| `useObjectUrl` | Reactive URL representing an object | AUTO |
| `usePerformanceObserver` | Observe performance metrics | AUTO |
| `usePermission` | Reactive [Permissions API](https://developer.mozilla.org/en-US/docs/Web/API/Permissions_API) | AUTO |
| `usePreferredColorScheme` | Reactive [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) media query | AUTO |
| `usePreferredContrast` | Reactive [prefers-contrast](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast) media query | AUTO |
| `usePreferredDark` | Reactive dark theme preference | AUTO |
| `usePreferredLanguages` | Reactive [Navigator Languages](https://developer.mozilla.org/en-US/docs/Web/API/NavigatorLanguage/languages) | AUTO |
| `usePreferredReducedMotion` | Reactive [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) media query | AUTO |
| `usePreferredReducedTransparency` | Reactive [prefers-reduced-transparency](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency) media query | AUTO |
| `useScreenOrientation` | Reactive [Screen Orientation API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Orientation_API) | AUTO |
| `useScreenSafeArea` | Reactive `env(safe-area-inset-*)` | AUTO |
| `useScriptTag` | Creates a script tag | AUTO |
| `useShare` | Reactive [Web Share API](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share) | AUTO |
| `useSSRWidth` | Used to set a global viewport width which will be used when rendering SSR components that rely on the viewport width like `useMediaQuery` or `useBreakpoints` | AUTO |
| `useStyleTag` | Inject reactive `style` element in head | AUTO |
| `useTextareaAutosize` | Automatically update the height of a textarea depending on the content | AUTO |
| `useTextDirection` | Reactive [dir](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir) of the element's text | AUTO |
| `useTitle` | Reactive document title | AUTO |
| `useUrlSearchParams` | Reactive [URLSearchParams](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams) | AUTO |
| `useVibrate` | Reactive [Vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API) | AUTO |
| `useWakeLock` | Reactive [Screen Wake Lock API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API) | AUTO |
| `useWebNotification` | Reactive [Notification](https://developer.mozilla.org/en-US/docs/Web/API/notification) | AUTO |
| `useWebWorker` | Simple [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) registration and communication | AUTO |
| `useWebWorkerFn` | Run expensive functions without blocking the UI | AUTO |

### Sensors

| Function | Description | Invocation |
|----------|-------------|------------|
| `onClickOutside` | Listen for clicks outside of an element | AUTO |
| `onElementRemoval` | Fires when the element or any element containing it is removed from the DOM | AUTO |
| `onKeyStroke` | Listen for keyboard keystrokes | AUTO |
| `onLongPress` | Listen for a long press on an element | AUTO |
| `onStartTyping` | Fires when users start typing on non-editable elements | AUTO |
| `useBattery` | Reactive [Battery Status API](https://developer.mozilla.org/en-US/docs/Web/API/Battery_Status_API) | AUTO |
| `useDeviceMotion` | Reactive [DeviceMotionEvent](https://developer.mozilla.org/en-US/docs/Web/API/DeviceMotionEvent) | AUTO |
| `useDeviceOrientation` | Reactive [DeviceOrientationEvent](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent) | AUTO |
| `useDevicePixelRatio` | Reactively track [`window.devicePixelRatio`](https://developer.mozilla.org/docs/Web/API/Window/devicePixelRatio) | AUTO |
| `useDevicesList` | Reactive [enumerateDevices](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/enumerateDevices) listing available input/output devices | AUTO |
| `useDisplayMedia` | Reactive [`mediaDevices.getDisplayMedia`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia) streaming | AUTO |
| `useElementByPoint` | Reactive element by point | AUTO |
| `useElementHover` | Reactive element's hover state | AUTO |
| `useFocus` | Reactive utility to track or set the focus state of a DOM element | AUTO |
| `useFocusWithin` | Reactive utility to track if an element or one of its descendants has focus | AUTO |
| `useFps` | Reactive FPS (frames per second) | AUTO |
| `useGeolocation` | Reactive [Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API) | AUTO |
| `useIdle` | Tracks whether the user is being inactive | AUTO |
| `useInfiniteScroll` | Infinite scrolling of the element | AUTO |
| `useKeyModifier` | Reactive [Modifier State](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/getModifierState) | AUTO |
| `useMagicKeys` | Reactive keys pressed state | AUTO |
| `useMouse` | Reactive mouse position | AUTO |
| `useMousePressed` | Reactive mouse pressing state | AUTO |
| `useNavigatorLanguage` | Reactive [navigator.language](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/language) | AUTO |
| `useNetwork` | Reactive [Network status](https://developer.mozilla.org/en-US/docs/Web/API/Network_Information_API) | AUTO |
| `useOnline` | Reactive online state | AUTO |
| `usePageLeave` | Reactive state to show whether the mouse leaves the page | AUTO |
| `useParallax` | Create parallax effect easily | AUTO |
| `usePointer` | Reactive [pointer state](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events) | AUTO |
| `usePointerLock` | Reactive [pointer lock](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_Lock_API) | AUTO |
| `usePointerSwipe` | Reactive swipe detection based on [PointerEvents](https://developer.mozilla.org/en-US/docs/Web/API/PointerEvent) | AUTO |
| `useScroll` | Reactive scroll position and state | AUTO |
| `useScrollLock` | Lock scrolling of the element | AUTO |
| `useSpeechRecognition` | Reactive [SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition) | AUTO |
| `useSpeechSynthesis` | Reactive [SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) | AUTO |
| `useSwipe` | Reactive swipe detection based on [`TouchEvents`](https://developer.mozilla.org/en-US/docs/Web/API/TouchEvent) | AUTO |
| `useTextSelection` | Reactively track user text selection based on [`Window.getSelection`](https://developer.mozilla.org/en-US/docs/Web/API/Window/getSelection) | AUTO |
| `useUserMedia` | Reactive [`mediaDevices.getUserMedia`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) streaming | AUTO |

### Network

| Function | Description | Invocation |
|----------|-------------|------------|
| `useEventSource` | An [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) or [Server-Sent-Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) instance opens a persistent connection to an HTTP server | AUTO |
| `useFetch` | Reactive [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) provides the ability to abort requests | AUTO |
| `useWebSocket` | Reactive [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/WebSocket) client | AUTO |

### Animation

| Function | Description | Invocation |
|----------|-------------|------------|
| `useAnimate` | Reactive [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API) | AUTO |
| `useInterval` | Reactive counter that increases on every interval | AUTO |
| `useIntervalFn` | Wrapper for `setInterval` with controls | AUTO |
| `useNow` | Reactive current Date instance | AUTO |
| `useRafFn` | Call function on every `requestAnimationFrame` | AUTO |
| `useTimeout` | Reactive value that becomes `true` after a given time | AUTO |
| `useTimeoutFn` | Wrapper for `setTimeout` with controls | AUTO |
| `useTimestamp` | Reactive current timestamp | AUTO |
| `useTransition` | Transition between values | AUTO |

### Component

| Function | Description | Invocation |
|----------|-------------|------------|
| `computedInject` | Combine `computed` and `inject` | AUTO |
| `createReusableTemplate` | Define and reuse template inside the component scope | AUTO |
| `createTemplatePromise` | Template as Promise | AUTO |
| `templateRef` | Shorthand for binding ref to template element | AUTO |
| `tryOnBeforeMount` | Safe `onBeforeMount` | AUTO |
| `tryOnBeforeUnmount` | Safe `onBeforeUnmount` | AUTO |
| `tryOnMounted` | Safe `onMounted` | AUTO |
| `tryOnScopeDispose` | Safe `onScopeDispose` | AUTO |
| `tryOnUnmounted` | Safe `onUnmounted` | AUTO |
| `unrefElement` | Retrieves the underlying DOM element from a Vue ref or component instance | AUTO |
| `useCurrentElement` | Get the DOM element of current component as a ref | AUTO |
| `useMounted` | Mounted state in ref | AUTO |
| `useTemplateRefsList` | Shorthand for binding refs to template elements and components inside `v-for` | AUTO |
| `useVirtualList` | Create virtual lists with ease | AUTO |
| `useVModel` | Shorthand for v-model binding | AUTO |
| `useVModels` | Shorthand for props v-model binding | AUTO |

### Watch

| Function | Description | Invocation |
|----------|-------------|------------|
| `until` | Promised one-time watch for changes | AUTO |
| `watchArray` | Watch for an array with additions and removals | AUTO |
| `watchAtMost` | `watch` with the number of times triggered | AUTO |
| `watchDebounced` | Debounced watch | AUTO |
| `watchDeep` | Shorthand for watching value with `{deep: true}` | AUTO |
| `watchIgnorable` | Ignorable watch | AUTO |
| `watchImmediate` | Shorthand for watching value with `{immediate: true}` | AUTO |
| `watchOnce` | Shorthand for watching value with `{ once: true }` | AUTO |
| `watchPausable` | Pausable watch | AUTO |
| `watchThrottled` | Throttled watch | AUTO |
| `watchTriggerable` | Watch that can be triggered manually | AUTO |
| `watchWithFilter` | `watch` with additional EventFilter control | AUTO |
| `whenever` | Shorthand for watching value to be truthy | AUTO |

### Reactivity

| Function | Description | Invocation |
|----------|-------------|------------|
| `computedAsync` | Computed for async functions | AUTO |
| `computedEager` | Eager computed without lazy evaluation | AUTO |
| `computedWithControl` | Explicitly define the dependencies of computed | AUTO |
| `createRef` | Returns a `deepRef` or `shallowRef` depending on the `deep` param | AUTO |
| `extendRef` | Add extra attributes to Ref | AUTO |
| `reactify` | Converts plain functions into reactive functions | AUTO |
| `reactifyObject` | Apply `reactify` to an object | AUTO |
| `reactiveComputed` | Computed reactive object | AUTO |
| `reactiveOmit` | Reactively omit fields from a reactive object | AUTO |
| `reactivePick` | Reactively pick fields from a reactive object | AUTO |
| `refAutoReset` | A ref which will be reset to the default value after some time | AUTO |
| `refDebounced` | Debounce execution of a ref value | AUTO |
| `refDefault` | Apply default value to a ref | AUTO |
| `refManualReset` | Create a ref with manual reset functionality | AUTO |
| `refThrottled` | Throttle changing of a ref value | AUTO |
| `refWithControl` | Fine-grained controls over ref and its reactivity | AUTO |
| `syncRef` | Two-way refs synchronization | AUTO |
| `syncRefs` | Keep target refs in sync with a source ref | AUTO |
| `toReactive` | Converts ref to reactive | AUTO |
| `toRef` | Normalize value/ref/getter to `ref` or `computed` | EXPLICIT_ONLY |
| `toRefs` | Extended [`toRefs`](https://vuejs.org/api/reactivity-utilities.html#torefs) that also accepts refs of an object | AUTO |

### Array

| Function | Description | Invocation |
|----------|-------------|------------|
| `useArrayDifference` | Reactive get array difference of two arrays | AUTO |
| `useArrayEvery` | Reactive `Array.every` | AUTO |
| `useArrayFilter` | Reactive `Array.filter` | AUTO |
| `useArrayFind` | Reactive `Array.find` | AUTO |
| `useArrayFindIndex` | Reactive `Array.findIndex` | AUTO |
| `useArrayFindLast` | Reactive `Array.findLast` | AUTO |
| `useArrayIncludes` | Reactive `Array.includes` | AUTO |
| `useArrayJoin` | Reactive `Array.join` | AUTO |
| `useArrayMap` | Reactive `Array.map` | AUTO |
| `useArrayReduce` | Reactive `Array.reduce` | AUTO |
| `useArraySome` | Reactive `Array.some` | AUTO |
| `useArrayUnique` | Reactive unique array | AUTO |
| `useSorted` | Reactive sort array | AUTO |

### Time

| Function | Description | Invocation |
|----------|-------------|------------|
| `useCountdown` | Reactive countdown timer in seconds | AUTO |
| `useDateFormat` | Get the formatted date according to the string of tokens passed in | AUTO |
| `useTimeAgo` | Reactive time ago | AUTO |
| `useTimeAgoIntl` | Reactive time ago with i18n supported | AUTO |

### Utilities

| Function | Description | Invocation |
|----------|-------------|------------|
| `createDisposableDirective` | Utility for authoring disposable directives | AUTO |
| `createEventHook` | Utility for creating event hooks | AUTO |
| `createUnrefFn` | Make a plain function accepting ref and raw values as arguments | AUTO |
| `get` | Shorthand for accessing `ref.value` | EXPLICIT_ONLY |
| `isDefined` | Non-nullish checking type guard for Ref | AUTO |
| `makeDestructurable` | Make isomorphic destructurable for object and array at the same time | AUTO |
| `set` | Shorthand for `ref.value = x` | EXPLICIT_ONLY |
| `useAsyncQueue` | Executes each asynchronous task sequentially and passes the current task result to the next task | AUTO |
| `useBase64` | Reactive base64 transforming | AUTO |
| `useCached` | Cache a ref with a custom comparator | AUTO |
| `useCloned` | Reactive clone of a ref | AUTO |
| `useConfirmDialog` | Creates event hooks to support modals and confirmation dialog chains | AUTO |
| `useCounter` | Basic counter with utility functions | AUTO |
| `useCycleList` | Cycle through a list of items | AUTO |
| `useDebounceFn` | Debounce execution of a function | AUTO |
| `useEventBus` | A basic event bus | AUTO |
| `useMemoize` | Cache results of functions depending on arguments and keep it reactive | AUTO |
| `useOffsetPagination` | Reactive offset pagination | AUTO |
| `usePrevious` | Holds the previous value of a ref | AUTO |
| `useStepper` | Provides helpers for building a multi-step wizard interface | AUTO |
| `useSupported` | SSR compatibility `isSupported` | AUTO |
| `useThrottleFn` | Throttle execution of a function | AUTO |
| `useTimeoutPoll` | Use timeout to poll something | AUTO |
| `useToggle` | A boolean switcher with utility functions | AUTO |
| `useToNumber` | Reactively convert a string ref to number | AUTO |
| `useToString` | Reactively convert a ref to string | AUTO |

### @Electron

| Function | Description | Invocation |
|----------|-------------|------------|
| `useIpcRenderer` | Provides [ipcRenderer](https://www.electronjs.org/docs/api/ipc-renderer) and all of its APIs with Vue reactivity | EXTERNAL |
| `useIpcRendererInvoke` | Reactive [ipcRenderer.invoke API](https://www.electronjs.org/docs/api/ipc-renderer#ipcrendererinvokechannel-args) result | EXTERNAL |
| `useIpcRendererOn` | Use [ipcRenderer.on](https://www.electronjs.org/docs/api/ipc-renderer#ipcrendereronchannel-listener) with ease and [ipcRenderer.removeListener](https://www.electronjs.org/docs/api/ipc-renderer#ipcrendererremovelistenerchannel-listener) automatically on unmounted | EXTERNAL |
| `useZoomFactor` | Reactive [WebFrame](https://www.electronjs.org/docs/api/web-frame#webframe) zoom factor | EXTERNAL |
| `useZoomLevel` | Reactive [WebFrame](https://www.electronjs.org/docs/api/web-frame#webframe) zoom level | EXTERNAL |

### @Firebase

| Function | Description | Invocation |
|----------|-------------|------------|
| `useAuth` | Reactive [Firebase Auth](https://firebase.google.com/docs/auth) binding | EXTERNAL |
| `useFirestore` | Reactive [Firestore](https://firebase.google.com/docs/firestore) binding | EXTERNAL |
| `useRTDB` | Reactive [Firebase Realtime Database](https://firebase.google.com/docs/database) binding | EXTERNAL |

### @Head

| Function | Description | Invocation |
|----------|-------------|------------|
| [`createHead`](https://github.com/vueuse/head#api) | Create the head manager instance. | EXTERNAL |
| [`useHead`](https://github.com/vueuse/head#api) | Update head meta tags reactively. | EXTERNAL |

### @Integrations

| Function | Description | Invocation |
|----------|-------------|------------|
| `useAsyncValidator` | Wrapper for [`async-validator`](https://github.com/yiminghe/async-validator) | EXTERNAL |
| `useAxios` | Wrapper for [`axios`](https://github.com/axios/axios) | EXTERNAL |
| `useChangeCase` | Reactive wrapper for [`change-case`](https://github.com/blakeembrey/change-case) | EXTERNAL |
| `useCookies` | Wrapper for [`universal-cookie`](https://www.npmjs.com/package/universal-cookie) | EXTERNAL |
| `useDrauu` | Reactive instance for [drauu](https://github.com/antfu/drauu) | EXTERNAL |
| `useFocusTrap` | Reactive wrapper for [`focus-trap`](https://github.com/focus-trap/focus-trap) | EXTERNAL |
| `useFuse` | Easily implement fuzzy search using a composable with [Fuse.js](https://github.com/krisk/fuse) | EXTERNAL |
| `useIDBKeyval` | Wrapper for [`idb-keyval`](https://www.npmjs.com/package/idb-keyval) | EXTERNAL |
| `useJwt` | Wrapper for [`jwt-decode`](https://github.com/auth0/jwt-decode) | EXTERNAL |
| `useNProgress` | Reactive wrapper for [`nprogress`](https://github.com/rstacruz/nprogress) | EXTERNAL |
| `useQRCode` | Wrapper for [`qrcode`](https://github.com/soldair/node-qrcode) | EXTERNAL |
| `useSortable` | Wrapper for [`sortable`](https://github.com/SortableJS/Sortable) | EXTERNAL |

### @Math

| Function | Description | Invocation |
|----------|-------------|------------|
| `createGenericProjection` | Generic version of `createProjection` | EXTERNAL |
| `createProjection` | Reactive numeric projection from one domain to another | EXTERNAL |
| `logicAnd` | `AND` condition for refs | EXTERNAL |
| `logicNot` | `NOT` condition for ref | EXTERNAL |
| `logicOr` | `OR` conditions for refs | EXTERNAL |
| `useAbs` | Reactive `Math.abs` | EXTERNAL |
| `useAverage` | Get the average of an array reactively | EXTERNAL |
| `useCeil` | Reactive `Math.ceil` | EXTERNAL |
| `useClamp` | Reactively clamp a value between two other values | EXTERNAL |
| `useFloor` | Reactive `Math.floor` | EXTERNAL |
| `useMath` | Reactive `Math` methods | EXTERNAL |
| `useMax` | Reactive `Math.max` | EXTERNAL |
| `useMin` | Reactive `Math.min` | EXTERNAL |
| `usePrecision` | Reactively set the precision of a number | EXTERNAL |
| `useProjection` | Reactive numeric projection from one domain to another | EXTERNAL |
| `useRound` | Reactive `Math.round` | EXTERNAL |
| `useSum` | Get the sum of an array reactively | EXTERNAL |
| `useTrunc` | Reactive `Math.trunc` | EXTERNAL |

### @Motion

| Function | Description | Invocation |
|----------|-------------|------------|
| [`useElementStyle`](https://motion.vueuse.org/api/use-element-style) | Sync a reactive object to a target element CSS styling | EXTERNAL |
| [`useElementTransform`](https://motion.vueuse.org/api/use-element-transform) | Sync a reactive object to a target element CSS transform. | EXTERNAL |
| [`useMotion`](https://motion.vueuse.org/api/use-motion) | Putting your components in motion. | EXTERNAL |
| [`useMotionProperties`](https://motion.vueuse.org/api/use-motion-properties) | Access Motion Properties for a target element. | EXTERNAL |
| [`useMotionVariants`](https://motion.vueuse.org/api/use-motion-variants) | Handle the Variants state and selection. | EXTERNAL |
| [`useSpring`](https://motion.vueuse.org/api/use-spring) | Spring animations. | EXTERNAL |

### @Router

| Function | Description | Invocation |
|----------|-------------|------------|
| `useRouteHash` | Shorthand for a reactive `route.hash` | EXTERNAL |
| `useRouteParams` | Shorthand for a reactive `route.params` | EXTERNAL |
| `useRouteQuery` | Shorthand for a reactive `route.query` | EXTERNAL |

### @RxJS

| Function | Description | Invocation |
|----------|-------------|------------|
| `from` | Wrappers around RxJS's [`from()`](https://rxjs.dev/api/index/function/from) and [`fromEvent()`](https://rxjs.dev/api/index/function/fromEvent) to allow them to accept `ref`s | EXTERNAL |
| `toObserver` | Sugar function to convert a `ref` into an RxJS [Observer](https://rxjs.dev/guide/observer) | EXTERNAL |
| `useExtractedObservable` | Use an RxJS [`Observable`](https://rxjs.dev/guide/observable) as extracted from one or more composables | EXTERNAL |
| `useObservable` | Use an RxJS [`Observable`](https://rxjs.dev/guide/observable) | EXTERNAL |
| `useSubject` | Bind an RxJS [`Subject`](https://rxjs.dev/guide/subject) to a `ref` and propagate value changes both ways | EXTERNAL |
| `useSubscription` | Use an RxJS [`Subscription`](https://rxjs.dev/guide/subscription) without worrying about unsubscribing from it or creating memory leaks | EXTERNAL |
| `watchExtractedObservable` | Watch the values of an RxJS [`Observable`](https://rxjs.dev/guide/observable) as extracted from one or more composables | EXTERNAL |

### @SchemaOrg

| Function | Description | Invocation |
|----------|-------------|------------|
| [`createSchemaOrg`](https://vue-schema-org.netlify.app/api/core/create-schema-org.html) | Create the schema.org manager instance. | EXTERNAL |
| [`useSchemaOrg`](https://vue-schema-org.netlify.app/api/core/use-schema-org.html) | Update schema.org reactively. | EXTERNAL |

### @Sound

| Function | Description | Invocation |
|----------|-------------|------------|
| [`useSound`](https://github.com/vueuse/sound#examples) | Play sound effects reactively. | EXTERNAL |


