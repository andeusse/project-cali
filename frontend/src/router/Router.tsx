import { createBrowserRouter } from 'react-router-dom';
import { Navigate, RouterProvider } from 'react-router';

import NavigationBar from '../components/NavigationBar';
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
          path: '/home',
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
        {
          path: '/',
          element: <Navigate to={'/home'}></Navigate>,
        },
      ],
    },
  ]);
  return <RouterProvider router={router}></RouterProvider>;
};

export default Router;
