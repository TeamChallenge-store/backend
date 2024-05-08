import { CustomButton } from '~shared/ui/CustomButton';

import css from './ErrorPage.module.scss';
import error from './icons/error.svg';

const ErrorPage = () => {
  return (
    <div className={css.errorContainer}>
      <img className={css.errorIcon} src={error} alt="error" />
      <h2 className={css.error}>404</h2>
      <h3 className={css.errorDesc}>
        We can’t find page that you’re looking for.
      </h3>
      <span className={css.errorSolution}>
        Maybe you can find what you need from our homepage.
      </span>
      <CustomButton to="/" bgColor="green" className={css.errorBtn}>
        Take me back to the home page
      </CustomButton>
      <CustomButton to="/" bgColor="green" className={css.errorBtnAdaptive}>
        to the home page
      </CustomButton>
    </div>
  );
};

export { ErrorPage };
