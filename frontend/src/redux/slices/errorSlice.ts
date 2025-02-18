import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface errorState {
  isShown: boolean;
  message: string;
}

const initialState: errorState = {
  isShown: false,
  message: '',
};

const errorSlice = createSlice({
  name: 'Error',
  initialState: initialState,
  reducers: {
    setError(state, action: PayloadAction<errorState>) {
      state.isShown = action.payload.isShown;
      state.message = action.payload.message;
    },
  },
});

export const { setError } = errorSlice.actions;

export default errorSlice.reducer;
