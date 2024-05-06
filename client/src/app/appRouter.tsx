import { RouteObject, createHashRouter as Router } from 'react-router-dom';

import { baseLayout } from '~layout/baseLayout';

import { HomePage, ProductPage, ErrorPage } from '~lazyPages';

const routes: RouteObject[] = [
  {
    element: baseLayout,
    path: '/',
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'products/:category',
        element: <ProductPage />,
      },
      {
        path: 'about',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'contacts',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'payment',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'delivery',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'login',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'checkout',
        element: <h1>***in develop***</h1>,
      },
      {
        path: 'thank-you',
        element: <h1>***in develop***</h1>,
      },
      {
        path: '*',
        element: <ErrorPage />,
      },
    ],
  },
];

const appRouter = () => Router(routes);

export { appRouter };
