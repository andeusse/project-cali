import { useAppDispatch, useAppSelector } from './redux/reduxHooks';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import { setTheme } from './redux/slices/themeSlice';
import IsLoading from './components/IsLoading';
import { useEffect } from 'react';
import string2Theme from './utils/string2Theme';
import Router from './router/Router';
import './styles/table.scss';

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

  const themeMode =
    userTheme === 'light'
      ? createTheme({
          palette: {
            mode: userTheme,
            primary: {
              main: '#002D71',
            },
            background: {
              default: '#f0f4fa',
            },
            text: {
              primary: '#002D71',
            },
          },
          typography: {
            fontFamily: `"Lucida Sans Unicode","Roboto","Helvetica","Arial",sans-serif`,
            allVariants: {
              color: '#002D71',
            },
          },
          components: {
            MuiAccordion: {
              styleOverrides: {
                root: () => ({
                  backgroundColor: '#f0f4fa',
                  boxShadow:
                    '0px 5px 5px 0px rgba(0,45,113,0.2), 0px 2px 2px 0px rgba(0,45,113,0.15), 0px 1px 5px 0px rgba(0,45,113,0.15)',
                }),
              },
            },
          },
        })
      : createTheme({
          palette: {
            mode: userTheme,
          },
          typography: {
            fontFamily: `"Lucida Sans Unicode","Roboto","Helvetica","Arial",sans-serif`,
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
