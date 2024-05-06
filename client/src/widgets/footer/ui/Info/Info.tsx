import { FC } from 'react';
import { Link } from 'react-router-dom';

import css from './Info.module.scss';

const Info: FC = () => {
  return (
    <article className={css.info}>
      <h4 className={css.infoTitle}>Company info</h4>
      <ul className={css.infoList}>
        <li>
          <Link to="info/about">About us</Link>
        </li>
        <li>
          <Link to="info/payment">Payment</Link>
        </li>
        <li>
          <Link to="info/delivery">Delivery</Link>
        </li>
        <li>
          <Link to="info/contacts">Contacts</Link>
        </li>
        <li>
          <Link to="info/exchange-and-return">Exchange and return</Link>
        </li>
      </ul>
    </article>
  );
};

export { Info };
