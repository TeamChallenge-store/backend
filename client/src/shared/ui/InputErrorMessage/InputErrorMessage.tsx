import { FC } from 'react';
import css from './InputErrorMessage.module.scss';
import warningIcon from '../Icon/icons/warning.svg';

type TInputErrorMessageProps = {
  errorMessage: string;
  className?: string;
};

const InputErrorMessage: FC<TInputErrorMessageProps> = ({
  errorMessage,
  className,
}) => {
  return (
    <div className={`${className} ${css.errorMessage}`}>
      <img className={css.warningIcon} src={warningIcon} alt="error" />
      <span className={css.warning}>{errorMessage}</span>
    </div>
  );
};

export { InputErrorMessage };
