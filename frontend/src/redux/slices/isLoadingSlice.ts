import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface isLoadingState {
  value: boolean;
}

const initialState: isLoadingState = {
  value: false,
};

const isLoadingSlice = createSlice({
  name: 'theme',
  initialState: initialState,
  reducers: {
    setIsLoading(state, action: PayloadAction<boolean>) {
      state.value = action.payload;
    },
  },
});

export const { setIsLoading } = isLoadingSlice.actions;

export default isLoadingSlice.reducer;
