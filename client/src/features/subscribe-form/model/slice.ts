import { PayloadAction, createSlice } from '@reduxjs/toolkit';

type TSubscribeFormSlice = {
  isSubscribeSuccess: boolean;
};

const initialState: TSubscribeFormSlice = {
  isSubscribeSuccess: true,
};

export const subscribeFormSlice = createSlice({
  name: 'subscribeForm',
  initialState,
  reducers: {
    setSubscribeSuccess: (state, action: PayloadAction<boolean>) => {
      /* eslint-disable no-param-reassign */
      state.isSubscribeSuccess = action.payload;
    },
  },
});

export const { setSubscribeSuccess } = subscribeFormSlice.actions;
export const selectIsSubscribeSuccess = (state: RootState) =>
  state.subscribeForm.isSubscribeSuccess;
export default subscribeFormSlice.reducer;
