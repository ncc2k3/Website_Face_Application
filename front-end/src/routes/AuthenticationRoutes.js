import { lazy } from 'react';

// project imports
import Loadable from 'ui-component/Loadable';
import MinimalLayout from 'layout/MinimalLayout';

// login option 3 routing
const AuthLogin3 = Loadable(lazy(() => import('views/pages/authentication/authentication3/Login3')));
const AuthRegister3 = Loadable(lazy(() => import('views/pages/authentication/authentication3/Register3')));
const RegisterFaceID = Loadable(lazy(() => import('views/pages/authentication/auth-forms/RegisterFaceID')));
const LoginFaceID = Loadable(lazy(() => import('views/pages/authentication/auth-forms/LoginFaceID')));
const ResetPassword = Loadable(lazy(() => import('views/pages/authentication/auth-forms/ResetPassword')));

// ==============================|| AUTHENTICATION ROUTING ||============================== //

const AuthenticationRoutes = {
  path: '/',
  element: <MinimalLayout />,
  children: [
    {
      path: '/pages/login/login3',
      element: <AuthLogin3 />
    },
    {
      path: '/pages/register/register3',
      element: <AuthRegister3 />
    },
    {
      path: '/pages/register/register-face-id',
      element: <RegisterFaceID />
    },
    {
      path: '/pages/login/login-face-id',
      element: <LoginFaceID />
    },
    {
      path: '/pages/login/reset-password',
      element: <ResetPassword />
    }
  ]
};

export default AuthenticationRoutes;
