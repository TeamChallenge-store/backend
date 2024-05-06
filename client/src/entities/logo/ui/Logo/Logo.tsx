import { Link } from 'react-router-dom';

import css from './Logo.module.scss';

interface LogoProps {
  type: 'header' | 'footer';
  className?: string;
  onClick?: () => void;
}

const Logo: React.FC<LogoProps> = ({ type, className, onClick }) => {
  const logoClassName = type === 'header' ? css.headerLogo : css.footerLogo;

  return (
    <Link
      to="/"
      className={`${css.logo} ${logoClassName} ${className}`}
      onClick={onClick}
    >
      campfire
    </Link>
  );
};

export { Logo };
