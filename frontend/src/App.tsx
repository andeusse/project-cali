import { useAppDispatch, useAppSelector } from './redux/reduxHooks';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import { setTheme } from './redux/slices/themeSlice';
import IsLoading from './components/IsLoading';
import { useEffect } from 'react';
import string2Theme from './utils/string2Theme';
import Router from './router/Router';

function App() {
  const userTheme = useAppSelector((state) => state.theme.value);
  const isLoading = useAppSelector((state) => state.isLoading.value);

  const dispatch = useAppDispatch();

  useEffect(() => {
    const storageTheme = localStorage.getItem('theme');
    if (storageTheme !== null) {
      dispatch(setTheme(string2Theme(storageTheme)));
    }
  }, [dispatch]);

  const themeMode = createTheme({
    palette: {
      mode: userTheme,
    },
  });

  return (
    <ThemeProvider theme={themeMode}>
      <CssBaseline />
      <IsLoading isLoading={isLoading}></IsLoading>
      <Router></Router>
    </ThemeProvider>
  );
}

export default App;
