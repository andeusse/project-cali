import { ThemeType } from '../types/theme';

const string2Theme = (theme: string) => {
  if (theme.toLowerCase() === 'light') {
    return ThemeType.Light;
  }
  return ThemeType.Dark;
};

export default string2Theme;
