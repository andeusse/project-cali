import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import { RouterProvider } from 'react-router';

import NavigationBar from './NavigationBar';
import Error from '../views/Error';
import Home from '../views/Home';
import Monitoring from '../views/Monitoring';
import DigitalTwins from '../views/DigitalTwins';
import Scenarios from '../views/Scenarios';
import AboutUs from '../views/AboutUs';

type Props = {};

const Router = (props: Props) => {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <NavigationBar></NavigationBar>,
      errorElement: <Error></Error>,
      children: [
        {
          path: '/',
          element: <Home></Home>,
        },
        {
          path: '/monitoring',
          element: <Monitoring></Monitoring>,
        },
        {
          path: '/digitaltwins',
          element: <DigitalTwins></DigitalTwins>,
        },
        {
          path: '/scenarios',
          element: <Scenarios></Scenarios>,
        },
        {
          path: '/about',
          element: <AboutUs></AboutUs>,
        },
      ],
    },
  ]);
  return <RouterProvider router={router}></RouterProvider>;
};

export default Router;
