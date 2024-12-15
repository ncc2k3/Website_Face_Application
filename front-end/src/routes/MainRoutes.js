import { lazy } from 'react';

// project imports
import MainLayout from 'layout/MainLayout';
import Loadable from 'ui-component/Loadable';

// dashboard routing
const DashboardDefault = Loadable(lazy(() => import('views/dashboard/Default')));

// utilities routing
const UtilsTypography = Loadable(lazy(() => import('views/utilities/Typography')));
const UtilsColor = Loadable(lazy(() => import('views/utilities/Color')));
const UtilsShadow = Loadable(lazy(() => import('views/utilities/Shadow')));
const UtilsMaterialIcons = Loadable(lazy(() => import('views/utilities/MaterialIcons')));
const UtilsTablerIcons = Loadable(lazy(() => import('views/utilities/TablerIcons')));

// sample page routing
const SamplePage = Loadable(lazy(() => import('views/sample-page')));

// faces routing
const FacesDetection = Loadable(lazy(() => import('views/faces/face_detection')));
const FacesComparision = Loadable(lazy(() => import('views/faces/face_comparision')));
const LivenessDetection = Loadable(lazy(() => import('views/faces/face_liveness')));
const FacesSearch = Loadable(lazy(() => import('views/faces/face_search')));

import { Navigate } from 'react-router-dom';

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
  path: '/',
  element: <MainLayout />,
  children: [
    {
      path: '/', // Chuyển hướng từ root
      element: <Navigate to="/pages/login/login3" />
    },
    {
      path: 'dashboard',
      children: [
        {
          path: 'default',
          element: <DashboardDefault />
        }
      ]
    },

    // faces routing
    {
      path: 'faces',
      children: [
        {
          path: 'face-detection',
          element: <FacesDetection />
        }
      ]
    },

    {
      path: 'faces',
      children: [
        {
          path: 'face-comparision',
          element: <FacesComparision />
        }
      ]
    },

    {
      path: 'faces',
      children: [
        {
          path: 'face-search',
          element: <FacesSearch />
        }
      ]
    },

    {
      path: 'faces',
      children: [
        {
          path: 'liveness',
          element: <LivenessDetection />
        }
      ]
    },

    {
      path: 'utils',
      children: [
        {
          path: 'util-typography',
          element: <UtilsTypography />
        }
      ]
    },
    {
      path: 'utils',
      children: [
        {
          path: 'util-color',
          element: <UtilsColor />
        }
      ]
    },
    {
      path: 'utils',
      children: [
        {
          path: 'util-shadow',
          element: <UtilsShadow />
        }
      ]
    },
    {
      path: 'icons',
      children: [
        {
          path: 'tabler-icons',
          element: <UtilsTablerIcons />
        }
      ]
    },
    {
      path: 'icons',
      children: [
        {
          path: 'material-icons',
          element: <UtilsMaterialIcons />
        }
      ]
    },
    {
      path: 'sample-page',
      element: <SamplePage />
    }
  ]
};

export default MainRoutes;
