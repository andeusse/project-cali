import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ThemeType } from '../../types/theme';

interface ThemeState {
  value: ThemeType;
}

const initialState: ThemeState = {
  value: ThemeType.Light,
};

const themeSlice = createSlice({
  name: 'theme',
  initialState: initialState,
  reducers: {
    changeTheme(state) {
      state.value =
        state.value === ThemeType.Light ? ThemeType.Dark : ThemeType.Light;
    },
    setTheme(state, action: PayloadAction<ThemeType>) {
      state.value = action.payload;
    },
  },
});

export const { changeTheme, setTheme } = themeSlice.actions;

export default themeSlice.reducer;
