---
name: team-messaging
description: "Send and manage team chat messages through a suite CLI: post to chats, read threads, and manage conversations. Use when a user wants to communicate via instant messaging."
license: MIT
tags:
- messaging
- chat
- communication
---

# im (v1)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 `lark-shared/SKILL.md`，其中包含认证、权限处理**

## Core Concepts

- **Message**: A single message in a chat, identified by `message_id` (om_xxx). Supports types: text, post, image, file, audio, video, sticker, interactive (card), share_chat, share_user, merge_forward, etc.
- **Chat**: A group chat or P2P conversation, identified by `chat_id` (oc_xxx).
- **Thread**: A reply thread under a message, identified by `thread_id` (om_xxx or omt_xxx).
- **Reaction**: An emoji reaction on a message.
- **Flag**: A bookmark on a message or thread.
- **Feed Shortcut**: A chat pinned to the current user's feed sidebar, identified by `feed_card_id` (an `oc_xxx` open_chat_id for CHAT type).
- **Feed Group**: A tag that groups feed cards in the feed list, identified by `feed_group_id` (ofg_xxx). Members are feed cards, each identified by `feed_id` + `feed_type`. Two types: `normal` (members managed explicitly) and `rule` (members auto-derived from rules).

## Resource Relationships

```
Chat (oc_xxx)
├── Message (om_xxx)
│   ├── Thread (reply thread)
│   ├── Reaction (emoji)
│   └── Resource (image / file / video / audio)
└── Member (user / bot)
```

## Important Notes

### AppLink and Share Links

Prefer CLI-returned links: use `chat_app_link` to open joined conversations, `message_app_link` to open messages, and `share_link` to invite others to groups. If manually building a joined-conversation AppLink, use `https://<applink_host>/client/chat/open?openChatId=<oc_xxx>`, never `chatId=<oc_xxx>` or `lark://...chat_id=<oc_xxx>`.

### Identity and Token Mapping

- `--as user` means **user identity** and uses `user_access_token`. Calls run as the authorized end user, so permissions depend on both the app scopes and that user's own access to the target chat/message/resource.
- `--as bot` means **bot identity** and uses `tenant_access_token`. Calls run as the app bot, so behavior depends on the bot's membership, app visibility, availability range, and bot-specific scopes.
- If an IM API says it supports both `user` and `bot`, the token type changes who the operator is. The same API can succeed with one identity and fail with the other because owner/admin status, chat membership, tenant boundary, or app availability are checked against the current caller.

### Sender Name Resolution

When fetching messages (`+chat-messages-list`, `+threads-messages-list`, `+messages-mget`, `+messages-search`), the CLI shows a display name for both user and bot senders:

- **Server-provided name**: the read APIs return `sender_name` (plus the full-i18n `sender_i18n_names` map) on each message `sender`; the CLI surfaces it as the sender's `name` for users and bots alike. No name lookup and no extra permission are needed — **no contact scope** and no `application:bot.basic_info:read`.
- **Fallback to id**: when the server does not provide a name, the sender is shown by its id and the command still exits 0. There is no contact-directory fallback.

The raw `sender_name` is not duplicated in output (its value is in `name`); the full `sender_i18n_names` map (all locales) is preserved for consumers that need a specific language, alongside an optional `open_bot_id` (`ou_`) for bot senders aligned with the message-receive event channel. System messages (`msg_type: system`) have no sender name — that is normal, not an error.

### Default message enrichment (reactions / update_time)

The four message-pulling shortcuts (`+messages-mget`, `+chat-messages-list`, `+messages-search`, `+threads-messages-list`) automatically attach a `reactions` block and (for edited messages) `update_time` to each returned message — no separate `im.reactions.batch_query` call is needed. Pass `--no-reactions` to opt out. For the full contract (output shape, the `im:message.reactions:read` scope requirement, and the "missing field ≠ fetch failure" data rules), read `references/lark-im-message-enrichment.md`.

### Opt-in resource auto-download (`--download-resources`)

`+chat-messages-list`, `+messages-mget`, and `+threads-messages-list` accept `--download-resources` to save eligible attachments into `./lark-im-resources/` and add a `resources` array to each message. It is off by default; stickers are not downloadable. A failed attachment is reported on that resource without aborting the message pull. Use `+messages-resources-download` for one attachment. See `references/lark-im-message-enrichment.md` for the output contract.

### Card Messages (Interactive)

**Before sending, replying with, or updating any `interactive` card (`+messages-send` / `+messages-reply` / `messages.patch`), you MUST read `references/card/lark-im-card-create.md` and follow its workflow.** The card JSON passed to `--msg-type interactive --content` (send/reply) or `messages.patch --data` (update) must be the output of that workflow — never hand-write or copy a card payload.

Card messages (`interactive` type) are not yet supported for compact conversion in event subscriptions. The raw event data will be returned instead, with a hint printed to stderr.

`interactive` cards support callback events (`card.action.trigger`) — see `references/lark-im-card-action-reply.md`.

### Audio Messages

`--audio` sends a voice message and supports only Opus audio files, for example `.opus` files or Ogg Opus (`.ogg`) files. For `mp3`, `wav`, or other non-Opus audio, either convert to `.opus` first and keep using `--audio`, or send the original file as an attachment with `--file`.

### Sending Doc Content as a Message

When sending content fetched from a Lark doc as a message, fetch the doc with --doc-format im-markdown, then send it as a message using the --markdown format. The fetched content is already in markdown; in any content-forwarding scenario, keep the fetched original text and send it in the --markdown format. Note: if the doc contains a cite tag with type="user", keep it as-is and do not strip the tag.

### Flag Types

Flags support two layers:

- **Message-layer flag**: `(ItemTypeDefault, FlagTypeMessage)` — regular message bookmark
- **Feed-layer flag**: `(ItemTypeThread/ItemTypeMsgThread, FlagTypeFeed)` — thread as feed-layer bookmark

Item types for feed-layer flags:
- **ItemTypeThread** (4) = thread in a topic-style chat
- **ItemTypeMsgThread** (11) = thread in a regular chat

### Feed Shortcut

Feed shortcuts add chats to the current user's feed sidebar. They are distinct from flags:

- **Flag** = bookmark on a message/thread, scoped to the user's bookmark list.
- **Feed shortcut** = entry in the user's feed sidebar (currently only chats).

Key limits:
- Only **CHAT-type** (`feed_card_id` is `oc_xxx`) is exposed via OpenAPI; doc/app/subscription shortcuts exist internally but are not yet whitelisted.
- All three operations (create/remove/list) are **user-identity only** — they sign with `user_access_token`.
- Batch size is **10 per call** for create/remove; list is a one-page wrapper with opaque `page_token` pagination.

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`lark-cli im +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| `+chat-create` | Create a group chat or topic chat; user/bot; --chat-mode group|topic; private/public; invites users/bots; optionally sets bot manager |
| `+chat-list` | List chats the current user/bot is a member of; defaults to groups; pass --types=p2p,group to include p2p single chats (user-only); user/bot; supports sorting, auto-pagination, --exclude-muted (user-only) |
| `+chat-members-list` | List members of a chat; returns separate users[] / bots[] buckets; callable as user or bot; --member-types filters which kinds to return; --page-all pagination; surfaces truncations[] when the server caps a bucket |
| `+chat-messages-list` | List messages in a chat or P2P conversation; user/bot; accepts --chat-id or --user-id, resolves P2P chat_id, supports time range, --order asc/desc sorting, auto-pagination |
| `+chat-search` | Search visible group chats by --query keyword and/or --member-ids; user/bot; e.g. look up chat_id by group name; supports type filters, sorting, auto-pagination, and --exclude-muted (user identity only) |
| `+chat-update` | Update group chat name or description; user/bot; updates a chat's name or description |
| `+message-read-users` | List users who read one message; user/bot; identity-specific scopes; supports bounded auto-pagination |
| `+messages-edit` | Edit a message's content (text/post, including the attachment zone); bot-only (user identity is rejected by the server); PUT /open-apis/im/v1/messages/:message_id |
| `+messages-mget` | Batch get messages by IDs; user/bot; fetches up to 50 om_ message IDs, formats sender names, expands thread replies |
| `+messages-read-status` | Batch query whether the current user read 1–50 messages; user-only; returns readable items and invalid message IDs |
| `+messages-reply` | Reply to a message (supports thread replies); user/bot; supports text/markdown/post/media replies, reply-in-thread, idempotency key |
| `+messages-resources-download` | Download an image or file attached to a message; user/bot |
| `+messages-search` | Search messages across chats (supports keyword, sender, time range filters) with user or bot identity; filters by chat/sender/attachment/time, supports auto-pagination via `--page-all` / `--page-limit`, enriches results via batched mget and chats batch_query |
| `+messages-send` | Send a message to a chat or direct message; user/bot; sends to chat-id or user-id with text/markdown/post/media, supports idempotency key |
| `+threads-messages-list` | List messages in a thread; user/bot; accepts om_/omt_ input, resolves message IDs to thread_id, supports --order asc/desc sorting, auto-pagination |
| `+flag-create` | Create a bookmark on a message; user-only; defaults to message-layer flag; use --flag-type feed for feed-layer flag (item_type auto-detected from chat mode) |
| `+flag-cancel` | Cancel (remove) a bookmark. When no --flag-type is given, best-effort double-cancel: removes message layer and (when chat_type is determinable) feed layer |
| `+flag-list` | List bookmarks; user-only; auto-enriches feed-type thread entries with message content; `--page-all` is capped by `--page-limit` (default 20, max 1000), and `has_more=true` means the result is incomplete |
| `+feed-shortcut-create` | Add chats to the user's feed shortcuts; user-only; oc_xxx chat IDs only; batch up to 10 per call; `--head`/`--tail` controls insertion order; partial failures return an `ok:false` ledger |
| `+feed-shortcut-remove` | Remove chats from the user's feed shortcuts; user-only; batch up to 10 per call; removing an absent shortcut is idempotent success; real per-item failures return an `ok:false` ledger |
| `+feed-shortcut-list` | List one page of the user's feed shortcuts; user-only; omit `--page-token` for the first page; default output enriches CHAT entries under `detail`; pass `--no-detail` to skip the extra lookup and `im:chat:read` scope |
| `+feed-group-list` | List the caller's feed groups (tags); user-only; supports `--page-all` auto-pagination |
| `+feed-group-list-item` | List feed cards in a feed group (tag); user-only; enriches each item with chat_name resolved from feed_id; supports --page-all auto-pagination |
| `+feed-group-query-item` | Look up specific feed cards in a feed group (tag) by ID; user-only; enriches each item with chat_name resolved from feed_id |

## API Resources

```bash
lark-cli schema im.<resource>.<method>   # 调用 API 前必须先查看参数结构
lark-cli im <resource> <method> [flags] # 调用 API
```

> **重要**：使用原生 API 时，必须先运行 `schema` 查看 `--data` / `--params` 参数结构，不要猜测字段格式。

### chats

  - `create` — 创建群。Identity: `bot` only (`tenant_access_token`).
  - `get` — 获取群信息。Identity: supports `user` and `bot`; the caller must be in the target chat to get full details, and must belong to the same tenant for internal chats.
  - `link` — 获取群分享链接。Identity: supports `user` and `bot`; the caller must be in the target chat, must be an owner or admin when chat sharing is restricted to owners/admins, and must belong to the same tenant for internal chats.
  - `update` — 更新群信息。Identity: supports `user` and `bot`.

### chat.members

  - `create` — 将用户或机器人拉入群聊。Identity: supports `user` and `bot`; the caller must be in the target chat; for `bot` calls, added users must be within the app's availability; for internal chats the operator must belong to the same tenant; if only owners/admins can add members, the caller must be an owner/admin, or a chat-creator bot with `im:chat:operate_as_owner`.
  - `delete` — 将用户或机器人移出群聊。Identity: supports `user` and `bot`; only group owner, admin, or creator bot can remove others; max 50 users or 5 bots per request.

### chat.user_setting

  - `batch_query` — 批量查询当前用户在群内的个人偏好设置 (e.g. `is_muted` mutes normal messages, `is_mute_at_all` mutes @all messages); up to 10 chats per request. Identity: `user` only (`user_access_token`); the caller must be in each target chat.
  - `batch_update` — 批量更新当前用户在群内的个人偏好设置 (e.g. `is_muted` mutes normal messages, `is_mute_at_all` mutes @all messages); up to 10 chats per request. Identity: `user` only (`user_access_token`); the caller must be in each target chat.

### chat.nickname

  - `get` — 获取自己的群昵称。Get your own nickname in the chat (self-only). Identity: `user` only (`user_access_token`); returns an empty string when no nickname is set.
  - `update` — 设置自己的群昵称。Set or update your own nickname in the chat (self-only). Identity: `user` only (`user_access_token`); `nickname` must be a non-empty string (max 300 bytes). Use DELETE to clear it.
  - `delete` — 清空自己的群昵称。Clear your own nickname in the chat (self-only). Identity: `user` only (`user_access_token`).

### chat.join_requests

  - `list` — 列出群的待审批入群申请（仅群主/管理员，user_access_token）。List pending join requests for a chat. Identity: `user` only (`user_access_token`); the caller must be the chat owner or an admin. Paginated (`page_size` 1-100); stop on `has_more == false` — `page_token` is returned even on the last page, so paging while it is present never terminates.
  - `handle` — 批量审批入群申请（approve/reject，仅群主/管理员，user_access_token）。Approve or reject pending join requests in bulk (1-50 items, processed in order). Identity: `user` only (`user_access_token`); the caller must be the chat owner or an admin. `results[]` mirrors `items[]` in count and order — check each `result` (`success` / `failed` / `already_handled`); exit 0 does not mean every item succeeded.

### chat.managers

  - `add_managers` — 指定群管理员。Identity: supports `user` and `bot`; only the group owner can add managers; max 10 managers per chat (20 for super-large chats), and at most 5 bots per request.
  - `delete_managers` — 删除群管理员。Identity: supports `user` and `bot`; only the group owner can remove managers; max 50 users or 5 bots per request.

### chat.moderation

  - `get` — 获取群成员发言权限。Identity: supports `user` and `bot`; the caller must be in the target chat and belong to the same tenant.
  - `update` — 更新群发言权限。Identity: supports `user` and `bot`; only the group owner (or creator bot with `im:chat:operate_as_owner`) can update; the caller must be in the chat.

### messages

  - `read_status` — 批量查询当前用户对消息的已读状态。Identity: `user` only (`user_access_token`); accepts up to 50 message IDs and returns readable items plus invalid message IDs.Must-read
  - `delete` — 撤回消息。Identity: supports `user` and `bot`; for `bot` calls, the bot must be in the chat to revoke group messages; to revoke another user's group message, the bot must be the owner, an admin, or the creator; for user P2P recalls, the target user must be within the bot's availability.
  - `forward` — 转发消息。Identity: supports `user` and `bot`.
  - `merge_forward` — 合并转发消息。Identity: `bot` only (`tenant_access_token`).
  - `read_users` — 查询消息已读信息。Identity: supports `user` and `bot`; the caller must still be in the chat. A user can query messages they sent within the last 7 days, while a bot can query only messages sent by that bot within the last 7 days.Must-read
  - `patch` — 更新已发送的消息卡片。Update an interactive message card sent by the app. Identity: supports `user` and `bot`; the message must have been sent within the last 14 days, and `content` must be a JSON-serialized string no larger than 30 KB.Must-read
  - `urgent_app` — 发送应用内加急。Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.
  - `urgent_phone` — 发送电话加急。Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.
  - `urgent_sms` — 发送短信加急。Identity: `bot` only (`tenant_access_token`); the bot must be the message sender and must be in the conversation that contains the message.

### reactions

  - `batch_query` — 批量获取消息表情。Identity: supports `user` and `bot`.Must-read
  - `create` — 添加消息表情回复。Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message.Must-read
  - `delete` — 删除消息表情回复。Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message, and can only delete reactions added by itself.Must-read
  - `list` — 获取消息表情回复。Identity: supports `user` and `bot`; the caller must be in the conversation that contains the message.Must-read

### threads

  - `forward` — 转发话题。Identity: supports `user` and `bot`.

### images

  - `create` — 上传图片。Identity: supports `user` and `bot`; user identity requires `im:resource` scope on the UAT.

### files

  - `create` — 上传文件。Identity: supports `user` and `bot`; user identity requires `im:resource` scope on the UAT.

### pins

  - `create` — Pin 消息。Identity: supports `user` and `bot`.
  - `delete` — 移除 Pin 消息。Identity: supports `user` and `bot`.
  - `list` — 获取群内 Pin 消息。Identity: supports `user` and `bot`.

### feed.groups

  - `batch_add_item` — Batch add feed cards to a feed group. Identity: `user` only (`user_access_token`).Must-read
  - `batch_query` — Batch query feed groups. Identity: `user` only (`user_access_token`).Must-read
  - `batch_remove_item` — Batch remove feed cards from a feed group. Identity: `user` only (`user_access_token`).Must-read
  - `create` — Create a feed group. Identity: `user` only (`user_access_token`).Must-read
  - `delete` — Delete a feed group. Identity: `user` only (`user_access_token`).Must-read
  - `update` — Update a feed group. Identity: `user` only (`user_access_token`).Must-read

## 权限表

| 方法 | 所需 scope |
|------|-----------|
| `chats.create` | `im:chat:create` |
| `chats.get` | `im:chat:read` |
| `chats.link` | `im:chat:read` |
| `chats.update` | `im:chat:update` |
| `chat.members.create` | `im:chat.members:write_only` |
| `chat.members.delete` | `im:chat.members:write_only` |
| `chat.members.get` | `im:chat.members:read` |
| `+chat-members-list` | `im:chat.members:read` |
| `chat.user_setting.batch_query` | `im:chat.user_setting:read` |
| `chat.user_setting.batch_update` | `im:chat.user_setting:write` |
| `chat.managers.add_managers` | `im:chat.managers:write_only` |
| `chat.managers.delete_managers` | `im:chat.managers:write_only` |
| `chat.moderation.get` | `im:chat.moderation:read` |
| `chat.moderation.update` | `im:chat:moderation:write_only` |
| `chat.join_requests.list` | `im:chat.membership_application:read` |
| `chat.join_requests.handle` | `im:chat.membership_application:write` |
| `+messages-read-status` | user: `im:message:readonly` (recommended), `im:message`, or `im:message:get_as_user` |
| `+message-read-users` | user: `im:message:readonly` (recommended), `im:message`, `im:message:basic`, or `im:message:get_as_user`; bot: `im:message:readonly` |
| `messages.read_status` | `im:message:readonly` (recommended), `im:message`, or `im:message:get_as_user` |
| `messages.delete` | `im:message:recall` |
| `messages.forward` | `im:message` |
| `messages.merge_forward` | `im:message` |
| `messages.read_users` | user: `im:message:readonly` (recommended), `im:message`, `im:message:basic`, or `im:message:get_as_user`; bot: `im:message:readonly` |
| `messages.patch` | `im:message:update` |
| `messages.urgent_app` | `im:message.urgent` |
| `messages.urgent_phone` | `im:message.urgent:phone` |
| `messages.urgent_sms` | `im:message.urgent:sms` |
| `reactions.batch_query` | `im:message.reactions:read` |
| `reactions.create` | `im:message.reactions:write_only` |
| `reactions.delete` | `im:message.reactions:write_only` |
| `reactions.list` | `im:message.reactions:read` |
| `threads.forward` | `im:message` |
| `images.create` | `im:resource` |
| `files.create` | `im:resource` |
| `pins.create` | `im:message.pins:write_only` |
| `pins.delete` | `im:message.pins:write_only` |
| `pins.list` | `im:message.pins:read` |
| `feed.groups.batch_add_item` | `im:feed_group_v1:write` |
| `feed.groups.batch_query` | `im:feed_group_v1:read` |
| `feed.groups.batch_remove_item` | `im:feed_group_v1:write` |
| `feed.groups.create` | `im:feed_group_v1:write` |
| `feed.groups.delete` | `im:feed_group_v1:write` |
| `feed.groups.update` | `im:feed_group_v1:write` |
