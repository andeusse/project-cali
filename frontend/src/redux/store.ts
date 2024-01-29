import { configureStore } from '@reduxjs/toolkit';

import themeReducer from './themeSlice';
import isLoadingReducer from './isLoadingSlice';

export const store = configureStore({
  reducer: {
    theme: themeReducer,
    isLoading: isLoadingReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
