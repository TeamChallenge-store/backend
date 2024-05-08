import React from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { RouterProvider } from 'react-router-dom';
import { PersistGate } from 'redux-persist/integration/react';
import { appRouter } from '~app/appRouter';
import { appStore, persistedStore } from '~app/appStore';

import '~shared/styles/base.scss';

const Root = () => (
  <React.StrictMode>
    <ReduxProvider store={appStore}>
      <PersistGate loading={null} persistor={persistedStore}>
        <RouterProvider router={appRouter()} />
      </PersistGate>
    </ReduxProvider>
  </React.StrictMode>
);

export { Root };
