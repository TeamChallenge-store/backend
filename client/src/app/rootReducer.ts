import { combineReducers } from '@reduxjs/toolkit';
import { subscribeFormSlice } from '~features/subscribe-form/model/slice';

import { baseApi } from '~shared/api/baseApi';

const rootReducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
  [subscribeFormSlice.name]: subscribeFormSlice.reducer,
});

export { rootReducer };
