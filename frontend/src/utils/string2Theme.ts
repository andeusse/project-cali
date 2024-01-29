import { themeType } from '../types/theme';

const string2Theme = (theme: string) => {
  if (theme.toLowerCase() === 'light') {
    return themeType.Light;
  }
  return themeType.Dark;
};

export default string2Theme;
