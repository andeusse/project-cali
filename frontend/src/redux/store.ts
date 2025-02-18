import { configureStore } from '@reduxjs/toolkit';

import themeReducer from './slices/themeSlice';
import isLoadingReducer from './slices/isLoadingSlice';
import errorReducer from './slices/errorSlice';

export const store = configureStore({
  reducer: {
    theme: themeReducer,
    isLoading: isLoadingReducer,
    error: errorReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
