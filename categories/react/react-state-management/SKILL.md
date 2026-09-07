---
name: react-state-management
description: "Use when implementing React state management with Zustand for lightweight state or Redux Toolkit for complex app-wide state."
license: MIT
tags:
- react
- state-management
- redux
- zustand
---

# State Management (Zustand & Redux Toolkit)

Use **Zustand** for lightweight, decentralized state, and **Redux Toolkit (RTK)** for complex, application-wide state with heavy business logic.

## Zustand Pattern
```typescript
import { create } from 'zustand';

interface UserState {
  user: string |" null;
  login: (user: string) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

## RTK Pattern
```typescript
import { createSlice, configureStore, PayloadAction } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null as string "| null },
  reducers: {
    login: (state, action: PayloadAction<string>) => { state.user = action.payload; },
  },
});

export const store = configureStore({ reducer: { auth: authSlice.reducer } });
```

## Architecture Flow
```mermaid
%%{init: {"theme": "default", "flowchart": {"useMaxWidth": true}}}%%
flowchart TD
    A[Component] -->|Dispatches Action| B(Store/Reducer)
    B -->|Updates State| C{State Tree}
    C -->|Re-renders| A
```
