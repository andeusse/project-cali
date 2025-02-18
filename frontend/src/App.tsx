import { useAppDispatch, useAppSelector } from './redux/reduxHooks';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import { setTheme } from './redux/slices/themeSlice';
import IsLoading from './components/IsLoading';
import { useEffect } from 'react';
import string2Theme from './utils/string2Theme';
import Router from './router/Router';
import './styles/table.scss';
import Config from './config/config';
import axios from 'axios';
import { setIsLoading } from './redux/slices/isLoadingSlice';
import ErrorDialog from './components/UI/ErrorDialog';
import { setError } from './redux/slices/errorSlice';
import Constants from './config/constants';

const LABEL_SIZE = '20px';
const TAB_SIZE = '18px';
const PRIMARY_COLOR = '#002D71';
const SECUNDARY_COLOR = '#f0f4fa';

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
              main: PRIMARY_COLOR,
            },
            background: {
              default: SECUNDARY_COLOR,
            },
            text: {
              primary: PRIMARY_COLOR,
            },
          },
          typography: {
            fontFamily: `"Lucida Sans Unicode","Roboto","Helvetica","Arial",sans-serif`,
            allVariants: {
              color: PRIMARY_COLOR,
            },
          },
          components: {
            MuiAccordion: {
              styleOverrides: {
                root: () => ({
                  backgroundColor: SECUNDARY_COLOR,
                  boxShadow:
                    '0px 5px 5px 0px rgba(0,45,113,0.2), 0px 2px 2px 0px rgba(0,45,113,0.15), 0px 1px 5px 0px rgba(0,45,113,0.15)',
                }),
              },
            },
            MuiInputLabel: {
              defaultProps: {
                sx: {
                  fontSize: LABEL_SIZE,
                },
              },
            },
            MuiOutlinedInput: {
              defaultProps: {
                sx: {
                  fontSize: LABEL_SIZE,
                },
              },
            },
            MuiTab: {
              defaultProps: {
                sx: {
                  fontSize: TAB_SIZE,
                  fontWeight: 1000,
                },
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
          components: {
            MuiInputLabel: {
              defaultProps: {
                sx: {
                  fontSize: LABEL_SIZE,
                },
              },
            },
            MuiOutlinedInput: {
              defaultProps: {
                sx: {
                  fontSize: LABEL_SIZE,
                },
              },
            },
            MuiTab: {
              defaultProps: {
                sx: {
                  fontSize: TAB_SIZE,
                  fontWeight: 1000,
                },
              },
            },
          },
        });

  useEffect(() => {
    dispatch(setIsLoading(true));
    axios
      .get(Config.getInstance().params.apiUrl, { timeout: 2000 })
      .then(() => {
        console.log(Config.getInstance().params.apiUrl);
        dispatch(setIsLoading(false));
      })
      .catch(() => {
        axios
          .get(process.env.REACT_APP_DEV_API_URL_PUBLIC!, { timeout: 2000 })
          .then(() => {
            Config.getInstance().params.apiUrl = process.env
              .REACT_APP_DEV_API_URL_PUBLIC
              ? process.env.REACT_APP_DEV_API_URL_PUBLIC
              : '';
            Config.getInstance().params.grafanaUrls = process.env
              .REACT_APP_DEV_GRAFANA_TABS_PUBLIC
              ? process.env.REACT_APP_DEV_GRAFANA_TABS_PUBLIC.split(' ')
              : [];
            Config.getInstance().params.electricalUrls = process.env
              .REACT_APP_DEV_ELECTRICAL_TABS_PUBLIC
              ? process.env.REACT_APP_DEV_ELECTRICAL_TABS_PUBLIC.split(' ')
              : [];
            console.log(Config.getInstance().params.apiUrl);
          })
          .catch(() => {
            console.log('Sin conexión con la API');
            dispatch(
              setError({
                isShown: true,
                message: Constants.NO_API_CONNECTION,
              })
            );
          })
          .finally(() => {
            dispatch(setIsLoading(false));
          });
      });
  }, [dispatch]);

  return (
    <ThemeProvider theme={themeMode}>
      <CssBaseline />
      <IsLoading isLoading={isLoading}></IsLoading>
      <ErrorDialog></ErrorDialog>
      <Router></Router>
    </ThemeProvider>
  );
}

export default App;
