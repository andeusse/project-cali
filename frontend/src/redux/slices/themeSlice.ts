import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { themeType } from '../../types/theme';

interface ThemeState {
  value: themeType;
}

const initialState: ThemeState = {
  value: themeType.Light,
};

const themeSlice = createSlice({
  name: 'theme',
  initialState: initialState,
  reducers: {
    changeTheme(state) {
      state.value =
        state.value === themeType.Light ? themeType.Dark : themeType.Light;
    },
    setTheme(state, action: PayloadAction<themeType>) {
      state.value = action.payload;
    },
  },
});

export const { changeTheme, setTheme } = themeSlice.actions;

export default themeSlice.reducer;
