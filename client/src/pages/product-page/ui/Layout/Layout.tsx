import { FC, ReactNode } from 'react';
import cn from 'classnames';

import css from './Layout.module.scss';

type TLayoutProps = {
  sidebar?: ReactNode;
  sortBy?: ReactNode;
  filtersMob?: ReactNode;
  productList?: ReactNode;
  pagination?: ReactNode;
};

const Layout: FC<TLayoutProps> = props => {
  return (
    <section className={cn('container', css.productsSection)}>
      <div className={css.inner}>
        <aside className={css.filters}>{props.sidebar}</aside>

        <div className={css.listInner}>
          <div className={css.filtersMob}>{props.filtersMob}</div>
          <div className={css.select}>{props.sortBy}</div>
          <ul className={css.listGrid}>{props.productList}</ul>
          {props.pagination}
        </div>
      </div>
    </section>
  );
};

export { Layout };
