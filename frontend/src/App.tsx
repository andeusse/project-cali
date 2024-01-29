import { useAppDispatch, useAppSelector } from './redux/reduxHooks';
import Button from '@mui/material/Button';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import { changeTheme, setTheme } from './redux/themeSlice';
import { setIsLoading } from './redux/isLoadingSlice';
import IsLoading from './components/IsLoading';
import { useEffect } from 'react';
import string2Theme from './utils/string2Theme';

function App() {
  const theme = useAppSelector((state) => state.theme.value);
  const isLoading = useAppSelector((state) => state.isLoading.value);
  const dispatch = useAppDispatch();

  useEffect(() => {
    const storageTheme = localStorage.getItem('theme');
    if (storageTheme !== null) {
      setTheme(string2Theme(storageTheme));
    }
  }, []);

  const themeMode = createTheme({
    palette: {
      mode: theme,
    },
  });

  return (
    <ThemeProvider theme={themeMode}>
      <CssBaseline />
      <Button
        variant="contained"
        color="success"
        onClick={() => dispatch(changeTheme())}
      >
        Theme
      </Button>
      <Button
        variant="contained"
        color="success"
        onClick={() => dispatch(setIsLoading(!isLoading))}
      >
        IsLoading
      </Button>
      <IsLoading isLoading={isLoading}></IsLoading>
    </ThemeProvider>
  );
}

export default App;
