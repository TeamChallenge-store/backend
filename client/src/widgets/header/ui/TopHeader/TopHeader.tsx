import { Link } from 'react-router-dom';
import { Logo } from '~entities/logo';
import css from './TopHeader.module.scss';

const TopHeader = () => {
  return (
    <div className={css.top}>
      <div className="container">
        <div className={css.topInner}>
          <Logo type="header" className={css.logo} />
          <div className={css.info}>
            <Link className={css.link} to="/help">
              Help
            </Link>
            <Link className={css.link} to="/signIn">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export { TopHeader };
