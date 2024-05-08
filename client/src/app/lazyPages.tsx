import { lazy } from 'react';

const HomePage = lazy(() => import('~pages/home-page'));
const ProductPage = lazy(() => import('~pages/product-page'));
const ErrorPage = lazy(() => import('~pages/error-page'));

export { HomePage, ProductPage, ErrorPage };
