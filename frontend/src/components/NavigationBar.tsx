import React, { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../redux/reduxHooks';
import {
  AppBar,
  Box,
  Container,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
} from '@mui/material';
import { Outlet, useLocation } from 'react-router-dom';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import MonitorIcon from '@mui/icons-material/Monitor';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import StackedLineChartIcon from '@mui/icons-material/StackedLineChart';
import InfoIcon from '@mui/icons-material/Info';

import { ThemeType } from '../types/theme';
import { changeTheme } from '../redux/slices/themeSlice';
import LinkButton from './UI/LinkButton';
import Logo from './UI/Logo';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import Config from '../config/config';

type Props = {};

type PageType = {
  text: string;
  to: string;
  icon: JSX.Element;
};

const pages: PageType[] = [
  {
    text: 'Home',
    to: '/home',
    icon: <HomeIcon></HomeIcon>,
  },
  {
    text: 'Monitoreo',
    to: '/monitoring',
    icon: <MonitorIcon></MonitorIcon>,
  },
  {
    text: 'Gemelos digitales',
    to: '/digitaltwins',
    icon: <ContentCopyIcon></ContentCopyIcon>,
  },
  {
    text: 'Escenarios',
    to: '/scenarios',
    icon: <StackedLineChartIcon></StackedLineChartIcon>,
  },
  {
    text: 'Acerca de',
    to: '/about',
    icon: <InfoIcon></InfoIcon>,
  },
];

const NavigationBar = (props: Props) => {
  const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
  const route = useLocation();

  const userTheme = useAppSelector((state) => state.theme.value);
  const dispatch = useAppDispatch();

  const handleChangeTheme = () => {
    localStorage.setItem(
      'theme',
      userTheme === ThemeType.Light ? ThemeType.Dark : ThemeType.Light
    );
    dispatch(changeTheme());
  };

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  return (
    <>
      <AppBar position="static">
        <HelmetProvider>
          <Helmet>
            <title>{`${route.pathname
              .split('/')[1]
              .toUpperCase()} | ${Config.getInstance().params.projectName.toUpperCase()}`}</title>
          </Helmet>
        </HelmetProvider>
        <Container maxWidth={false}>
          <Toolbar disableGutters>
            <Logo></Logo>
            <Box
              sx={{
                flexGrow: 1,
                display: { xs: 'flex', md: 'none' },
              }}
            >
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'left',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'left',
                }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{
                  display: { xs: 'block', md: 'none' },
                }}
              >
                {pages.map((page) => (
                  <MenuItem key={page.text} onClick={handleCloseNavMenu}>
                    <LinkButton
                      startIcon={page.icon}
                      sx={{
                        marginRight: 2,
                        color: 'inherit',
                      }}
                      to={`${page.to}`}
                    >
                      {page.text}
                    </LinkButton>
                  </MenuItem>
                ))}
              </Menu>
            </Box>

            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page) => (
                <LinkButton
                  key={page.text}
                  startIcon={page.icon}
                  sx={{ marginRight: 2, color: 'white' }}
                  to={`${page.to}`}
                >
                  {page.text}
                </LinkButton>
              ))}
            </Box>

            <Box sx={{ flexGrow: 0 }}>
              <IconButton onClick={handleChangeTheme}>
                {userTheme === ThemeType.Dark && (
                  <LightModeIcon></LightModeIcon>
                )}
                {userTheme === ThemeType.Light && <DarkModeIcon></DarkModeIcon>}
              </IconButton>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      <Outlet />
    </>
  );
};

export default NavigationBar;
