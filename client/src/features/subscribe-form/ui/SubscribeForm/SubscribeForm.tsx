import { FC } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import css from './SubscribeForm.module.scss';
import emailIcon from '~shared/ui/Icon/icons/email.svg?url';
import { CustomButton } from '~shared/ui/CustomButton';
// eslint-disable-next-line max-len
import { SubscribeFormConfig } from '~features/subscribe-form/config/SubscribeFormConfig';
import {
  selectIsSubscribeSuccess,
  setSubscribeSuccess,
} from '~features/subscribe-form/model/slice';
import useDelay from '~shared/lib/useDelay';
import { InputErrorMessage } from '~shared/ui/InputErrorMessage';

const SubscribeForm: FC = () => {
  /* eslint-disable operator-linebreak */
  const { handleSubmit, handleChange, handleBlur, values, touched, errors } =
    SubscribeFormConfig();

  const dispatch = useDispatch();
  const isSubscribeSuccess = useSelector(selectIsSubscribeSuccess);

  useDelay({
    isShow: isSubscribeSuccess,
    hide: () => dispatch(setSubscribeSuccess(false)),
    delay: 5000,
  });

  return (
    <form className={css.subscribeInputForm} onSubmit={handleSubmit}>
      <div className={css.inputContainer}>
        <input
          className={css.subscribeInput}
          name="email"
          type="email"
          placeholder="Enter your email to get the best offers..."
          value={values.email}
          onChange={handleChange}
          onBlur={handleBlur}
          autoComplete="email"
        />
        <img className={css.emailIcon} src={emailIcon} alt="Email" />

        {touched.email && errors.email ? (
          <InputErrorMessage errorMessage={errors.email} />
        ) : null}
      </div>

      <CustomButton
        className={css.subscribeButton}
        buttonType="submit"
        bgColor="green"
      >
        SEND
      </CustomButton>
    </form>
  );
};

export { SubscribeForm };
