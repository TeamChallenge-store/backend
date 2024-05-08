import { FC } from 'react';
import { NavLink } from 'react-router-dom';
import classNames from 'classnames';
import css from './Navbar.module.scss';
import { navigationData } from './config/navigationData';

const active = ({ isActive }: { isActive: boolean }) =>
  classNames(css.link, {
    '': isActive,
  });

const Navbar: FC = () => {
  return (
    <nav className={css.nav}>
      <ul className={css.list}>
        {navigationData.map(item => (
          <li key={item.title} className={css.item}>
            <NavLink className={active} to={item.url}>
              {item.title}
            </NavLink>
            {item.submenu && (
              <ul className={css.submenu}>
                {item.submenu.map(subItem => (
                  <li key={subItem.title}>
                    <NavLink className={active} to={subItem.url}>
                      {subItem.title}
                    </NavLink>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};

export { Navbar };
