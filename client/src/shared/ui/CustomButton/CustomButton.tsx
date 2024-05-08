import React, { FC } from 'react';
import { Link, Path } from 'react-router-dom';
import cn from 'classnames';

import css from './CustomButton.module.scss';

type TButtonColor = 'green' | 'white';

type TCustomButtonProps = {
  children: React.ReactNode;
  className?: string;
  to?: string | Partial<Path>;
  bgColor?: TButtonColor;
  onClick?: (e: React.MouseEvent) => void;
  buttonType?: 'button' | 'submit' | 'reset';
  id?: string;
  disabled?: boolean;
};

const CustomButton: FC<TCustomButtonProps> = ({
  children,
  className = '',
  to = '',
  bgColor = 'green',
  onClick = () => {},
  buttonType = 'button',
  id,
  disabled = false,
}) => {
  const hasIcon = React.Children.count(children) > 1;

  return to ? (
    <Link
      to={to}
      className={cn(
        css[bgColor],
        className,
        css.navigation,
        hasIcon && css.icon,
        { [css.disabled]: disabled },
      )}
      onClick={onClick}
      id={id}
      aria-disabled={disabled}
    >
      {children}
    </Link>
  ) : (
    <button
      onClick={onClick}
      className={cn(
        css[bgColor],
        { [css.disabled]: disabled },
        className,
        css.navigation,
      )}
      /* eslint-disable react/button-has-type */
      type={buttonType}
      id={id}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export { CustomButton };
