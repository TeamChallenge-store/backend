import {
  useSelector,
  type TypedUseSelectorHook,
  useDispatch,
} from 'react-redux';

import { AppDispatch, RootState } from '~app/appStore';

const useAppDispatch = useDispatch<AppDispatch>;
const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

export { useAppDispatch, useAppSelector };
