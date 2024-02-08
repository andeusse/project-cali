import { configureStore } from '@reduxjs/toolkit';

import themeReducer from './slices/themeSlice';
import isLoadingReducer from './slices/isLoadingSlice';

export const store = configureStore({
  reducer: {
    theme: themeReducer,
    isLoading: isLoadingReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
