import { FC } from 'react';
import { Link } from 'react-router-dom';

import css from './Catalog.module.scss';

const Catalog: FC = () => {
  return (
    <article className={css.catalog}>
      <h4 className={css.catalogTitle}>Catalog</h4>
      <ul className={css.catalogList}>
        <li>
          <Link to="/catalog/tents">Tents</Link>
        </li>
        <li>
          <Link to="/catalog/backpacks">Clothes</Link>
        </li>
        <li>
          <Link to="/catalog/clothing">Accessories</Link>
        </li>
        <li>
          <Link to="/catalog/shoes">Camping equipment</Link>
        </li>
        <li>
          <Link to="/catalog/shoes">Mountaineering</Link>
        </li>
      </ul>
    </article>
  );
};

export { Catalog };
